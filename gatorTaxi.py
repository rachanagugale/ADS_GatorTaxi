# This is the main driver program

import min_heap
import red_black_tree
import sys


class CabService:
    def __init__(self):
        self.minHeap = min_heap.MinHeap()
        self.redBlack = red_black_tree.RedBlackTree()

    # Searches for the ride with given rideNumber in RBTree and prints its details. If such a ride is not found, prints (0,0,0)
    # Time complexity = O(logn) as search in RBTree is O(logn)
    def print(self, rideNumber):
        result = self.redBlack.search(rideNumber, self.redBlack.getRoot())
        if result != None:
            print("(" + str(result.rideNumber) + "," +
                  str(result.rideCost) + "," + str(result.tripDuration) + ")", end="\n")
        else:
            print("(0,0,0)")

    # Searches for all the rides with ride numbers lying between rideNumber1 and rideNumber2 in RBTree.
    # Prints the details of all the rides found in ascending order of rideNums.
    # Time complexity = O(logn+S) where S is the number of rides in range.
    def printRange(self, rideNumber1, rideNumber2):
        res = self.redBlack.printRange(
            self.redBlack.getRoot(), rideNumber1, rideNumber2, [])
        if len(res) == 0:
            print("(0,0,0)")
        else:
            res.sort()
            resStr = str(res)
            resStr = resStr.replace('[', '')
            resStr = resStr.replace(']', '')
            resStr = resStr.replace(' ', '')
            print(resStr)

    # Inserts node in both RBTree and minHeap. Connects the inserted nodes by pointers.
    # If node with same rideNum already present, the program is terminated.
    # Time complexity = O(logn) as insert in RBTree and MinHeap take O(logn)
    def insert(self, rideNumber, rideCost, tripDuration):
        res = self.redBlack.search(rideNumber, self.redBlack.getRoot())
        if res:
            print("Duplicate RideNumber", end="")
            return False
        else:
            rbtNode = self.redBlack.insert(rideNumber, rideCost, tripDuration)
            minHeapNode = self.minHeap.insert(
                rideNumber, rideCost, tripDuration, rbtNode)
            rbtNode.minHeapNode = minHeapNode
            return True

    # Gets the next ride with the minimum rideCost from the minHeap and prints it.
    # Deletes this node from the minHeap and also deletes the corresponding RBTree node by using the pointer available to it in the minHeap node.
    # If the heap is empty, prints an error message
    # Time complexity = O(logn) as deleting from a minHeap takes O(logn) and deletion from a RBTree also takes O(logn)
    def getNextRide(self):
        minHeapNode = self.minHeap.deleteMin()

        if minHeapNode != None:
            print("(" + str(minHeapNode.rideNumber) + "," +
                  str(minHeapNode.rideCost) + "," + str(minHeapNode.tripDuration) + ")", end="\n")
            self.redBlack.deleteNode(minHeapNode.RBTNode)
        else:
            print("No active ride requests")

    # Retrieves the ride with the rideNumber from RBTree and deletes it.
    # Also deletes the corresponding heap node by using the pointer to it from the RBTree node.
    # Time complexity = O(logn). Deletion from RBTree takes O(logn) and heapify in minHeap takes O(logn)
    def cancelRide(self, rideNumber):
        # If the node doesn't exist, delete_node returns False
        rbtNode = self.redBlack.search(rideNumber, self.redBlack.getRoot())
        if rbtNode:
            self.redBlack.deleteNode(rbtNode)
            self.minHeap.deleteArbitraryByIdx(rbtNode.minHeapNode.listIdx)

    # Updates the ride with rideNumber with a new tripDuration.
    # For this operation, the current ride is retrived and deleted from the RBTree and
    # MinHeap and a new ride with the same rideNumber but new tripDuration is inserted in the RBTree and MinHeap.
    # Time Complexity = O(logn). TC of cancelRide + insertRide
    def updateTrip(self, rideNumber, newTripDuration):
        currNode = self.redBlack.search(rideNumber, self.redBlack.getRoot())

        if currNode == None:
            return

        rideCost = currNode.rideCost
        if newTripDuration > 2*currNode.tripDuration:
            # If new tripDuration more than twice old duration, delete ride
            rbtNode = self.redBlack.search(rideNumber, self.redBlack.getRoot())
            self.redBlack.deleteNode(rbtNode)
            self.minHeap.deleteArbitraryByIdx(rbtNode.minHeapNode.listIdx)
        elif newTripDuration > currNode.tripDuration:
            # If new tripDuration more than oldDuration, add 10 to tripCost
            oldRBTnode = self.redBlack.search(
                rideNumber, self.redBlack.getRoot())
            self.redBlack.deleteNode(oldRBTnode)
            self.minHeap.deleteArbitraryByIdx(oldRBTnode.minHeapNode.listIdx)
            newRBTNode = self.redBlack.insert(
                rideNumber, rideCost+10, newTripDuration)
            newMinHeapNode = self.minHeap.insert(rideNumber, rideCost+10,
                                                 newTripDuration, newRBTNode)
            newRBTNode.minHeapNode = newMinHeapNode
        elif newTripDuration <= currNode.tripDuration:
            # If new tripDuration less than oldDuration, delete the old nodes and add new nodes with new trip durations
            oldRBTnode = self.redBlack.search(
                rideNumber, self.redBlack.getRoot())
            self.redBlack.deleteNode(oldRBTnode)
            self.minHeap.deleteArbitraryByIdx(oldRBTnode.minHeapNode.listIdx)
            newRBTNode = self.redBlack.insert(
                rideNumber, rideCost, newTripDuration)
            newMinHeapNode = self.minHeap.insert(rideNumber, rideCost,
                                                 newTripDuration, newRBTNode)
            newRBTNode.minHeapNode = newMinHeapNode


orig_stdout = sys.stdout
output_file = open('output_file.txt', 'w')
sys.stdout = output_file

obj = CabService()
# Parsing input from the input file and calling the appropriate functions
with open(sys.argv[1], "r") as input_file:
    for inputStr in input_file:
        if "Insert" in inputStr:
            idx1 = inputStr.find("(")
            idx2 = inputStr.find(")")
            tmpList = inputStr[idx1+1: idx2]
            listToStr = ''.join([str(i) for i in tmpList])
            listAfterSplit = listToStr.split(",")
            rideNumber = int(listAfterSplit[0].strip())
            rideCost = int(listAfterSplit[1].strip())
            tripDuration = int(listAfterSplit[2].strip())
            flag = obj.insert(rideNumber, rideCost, tripDuration)
            if flag == False:
                break
        elif "GetNextRide" in inputStr:
            obj.getNextRide()
        elif "Cancel" in inputStr:
            idx1 = inputStr.find("(")
            idx2 = inputStr.find(")")
            tmpList = inputStr[idx1+1: idx2]
            listToStr = ''.join([str(i) for i in tmpList])
            rideNumber = int(listToStr.strip())
            obj.cancelRide(rideNumber)
        elif "UpdateTrip" in inputStr:
            idx1 = inputStr.find("(")
            idx2 = inputStr.find(")")
            tmpList = inputStr[idx1+1: idx2]
            listToStr = ''.join([str(i) for i in tmpList])
            listAfterSplit = listToStr.split(",")
            rideNumber = int(listAfterSplit[0].strip())
            newTripDuration = int(listAfterSplit[1].strip())
            obj.updateTrip(rideNumber, newTripDuration)
        elif "Print(" in inputStr:
            idx1 = inputStr.find("(")
            idx2 = inputStr.find(")")
            tmpList = inputStr[idx1+1: idx2]
            listToStr = ''.join([str(i) for i in tmpList])
            listAfterSplit = listToStr.split(",")
            if len(listAfterSplit) == 1:
                rideNumber = int(listAfterSplit[0].strip())
                obj.print(rideNumber)
            else:
                lowIdx = int(listAfterSplit[0].strip())
                highIdx = int(listAfterSplit[1].strip())
                obj.printRange(lowIdx, highIdx)

sys.stdout = orig_stdout
output_file.close()
