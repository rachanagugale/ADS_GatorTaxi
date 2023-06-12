# Min Heap stores nodes according to their rideCost

class MinHeapNode:
    def __init__(self, rideNumber, rideCost, tripDuration, listIdx, RBTNode):
        self.rideNumber = rideNumber
        self.rideCost = rideCost
        self.tripDuration = tripDuration
        self.listIdx = listIdx
        self.RBTNode = RBTNode


class MinHeap:
    def __init__(self):
        node = MinHeapNode(0, 0, 0, 0, None)
        # Initializing heap with a dummy node for ease with finding parent and child indices.
        self.heapNodesList = [node]
        self.currentHeapSize = 0

    # Moves the value up in the tree to maintain the heap property.
    # Time complexity: O(height) = O(log n)
    def heapifyUpwards(self, i):
        # While the element is not the root and the child is smaller than the parent, keep looping
        while (i // 2 > 0):
            # If the element is less than its parent, swap the elements
            if (self.heapNodesList[i].rideCost < self.heapNodesList[i // 2].rideCost) or (self.heapNodesList[i].rideCost == self.heapNodesList[i // 2].rideCost and self.heapNodesList[i].tripDuration < self.heapNodesList[i // 2].tripDuration):
                self.heapNodesList[i], self.heapNodesList[i //
                                                          2] = self.heapNodesList[i // 2], self.heapNodesList[i]
                # Update the listIdx of the swapped nodes
                self.heapNodesList[i].listIdx = i
                self.heapNodesList[i//2].listIdx = i//2
                i = i // 2  # Parent's index
            else:
                break

    # Moves the value down in the tree to maintain the heap property.
    # Time complexity: O(height) = O(log n)
    def heapifyDownwards(self, i):
        # While the element is not a leaf and the child is smaller than the parent, keep looping
        while (i * 2) <= self.currentHeapSize:
            # Get the index of the min child of the current node
            minChildIdx = self.getMinChildIdx(i)
            # Swap the values of the current element is greater than its min child
            if (self.heapNodesList[i].rideCost > self.heapNodesList[minChildIdx].rideCost) or (self.heapNodesList[i].rideCost == self.heapNodesList[minChildIdx].rideCost and self.heapNodesList[i].tripDuration > self.heapNodesList[minChildIdx].tripDuration):
                self.heapNodesList[i], self.heapNodesList[minChildIdx] = self.heapNodesList[minChildIdx], self.heapNodesList[i]
                # Update the listIdx of the swapped nodes
                self.heapNodesList[i].listIdx = i
                self.heapNodesList[minChildIdx].listIdx = minChildIdx
            i = minChildIdx

    # Inserts a value into the heap by adding the new value at the end of the heap and heapifying it upwards
    # Time complexity : O(height) = O(logn)
    def insert(self, rideNumber, rideCost, tripDuration, RBTNode):
        self.currentHeapSize += 1
        newNode = MinHeapNode(rideNumber, rideCost,
                              tripDuration, self.currentHeapSize, RBTNode)
        self.heapNodesList.append(newNode)

        # Move the element to its position from bottom to the top
        self.heapifyUpwards(self.currentHeapSize)
        return newNode

    # Gets the index of the smaller child
    def getMinChildIdx(self, i):
        # Case where node has only 1 child. Return the index of that child
        if (i*2)+1 > self.currentHeapSize:
            return i * 2
        else:
            # Case where node has 2 children. Compare the children and return the index of the min child
            if (self.heapNodesList[i*2].rideCost < self.heapNodesList[(i*2)+1].rideCost) or (self.heapNodesList[i*2].rideCost == self.heapNodesList[(i*2)+1].rideCost and self.heapNodesList[i*2].tripDuration < self.heapNodesList[(i*2)+1].tripDuration):
                return i * 2
            else:
                return (i * 2) + 1

    # Deletes the root by swapping it with the last heap element. Then heapifies the last element
    # Time complexity : O(height) = O(logn)
    def deleteMin(self):
        # Equal to 1 since the heap list was initialized with a value
        if len(self.heapNodesList) == 1:
            return None

        root = self.heapNodesList[1]  # Get root

        # Swap the root with the last heap node
        self.heapNodesList[1], self.heapNodesList[self.currentHeapSize] = self.heapNodesList[self.currentHeapSize], self.heapNodesList[1]
        self.heapNodesList[1].listIdx = 1
        self.heapNodesList[self.currentHeapSize].listIdx = self.currentHeapSize

        # Pop the last heap element (This was set to the root node which we want to delete)
        self.heapNodesList.pop(-1)
        self.currentHeapSize -= 1

        # Heapify to satisfy the heap property
        self.heapifyDownwards(1)

        return root

    # Deletes an arbitrary heap node by index and heapifies to maintain the heap property
    # Time complexity : O(height) = O(logn)
    def deleteArbitraryByIdx(self, idx):
        oldNode = self.heapNodesList[idx]
        newNode = self.heapNodesList[self.currentHeapSize]

        # Swap the node at idx index with the last heap node
        self.heapNodesList[idx], self.heapNodesList[self.currentHeapSize] = self.heapNodesList[self.currentHeapSize], self.heapNodesList[idx]
        self.heapNodesList[idx].listIdx = idx
        self.heapNodesList[self.currentHeapSize].listIdx = self.currentHeapSize

        # Pop the last node and reduce the heapSize
        self.heapNodesList.pop(self.currentHeapSize)
        self.currentHeapSize -= 1

        if newNode.rideCost < oldNode.rideCost:
            # If the new rideCost is lesser, we only need to heapify upwards
            self.heapifyUpwards(idx)
        elif newNode.rideCost > oldNode.rideCost:
            # If the new rideCost is greater, we only need to heapify downwards
            self.heapifyDownwards(idx)
        else:  # If new rideCost = old rideCost, then check the tripDuration to decide the heapify direction
            if newNode.tripDuration < oldNode.tripDuration:
                self.heapifyUpwards(idx)
            elif newNode.tripDuration > oldNode.tripDuration:
                self.heapifyDownwards(idx)
