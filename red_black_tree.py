# Red Black Tree stores nodes according to rideNumber

class RBTNode():
    def __init__(self, rideNumber, rideCost, tripDuration):
        self.rideNumber = rideNumber
        self.rideCost = rideCost
        self.tripDuration = tripDuration
        self.parent = None
        self.left = None
        self.right = None
        self.color = "red"
        self.minHeapNode = None


class RedBlackTree():
    def __init__(self):
        self.TNULL = RBTNode(0, 0, 0)
        self.TNULL.left = None
        self.TNULL.right = None
        self.TNULL.color = "black"
        self.TNULL.minHeapNode = None
        self.root = self.TNULL

    # Balancing the tree after deletion. Various cases considered depending on the color of parent, sibling and sibling's children.
    def balanceAfterDelete(self, currNode):
        # Keep looping till the currNode becomes red or we reach the root
        while currNode != self.root and currNode.color == "black":
            # If currNode is the left child of its parent, get the sibling and check its color.
            if currNode == currNode.parent.left:
                siblingNode = currNode.parent.right
                if siblingNode.color == "red":
                    siblingNode.color = "black"
                    currNode.parent.color = "red"
                    # Rotate left with currNode=black, parent=red, sibling=black
                    self.rotateLeft(currNode.parent)
                    siblingNode = currNode.parent.right

                # Check the color of sibling's children
                if siblingNode.left.color == "black" and siblingNode.right.color == "black":
                    # If both of sibling's children are black, color the sibling red and move the problem to the parent.
                    siblingNode.color = "red"
                    currNode = currNode.parent
                else:
                    if siblingNode.right.color == "black":
                        # If sibling's right child is black, color the sibling red and its left child black. Perform a rotateRight() on the sibling
                        siblingNode.left.color = "black"
                        siblingNode.color = "red"
                        self.rotateRight(siblingNode)
                        siblingNode = currNode.parent.right

                    siblingNode.color = currNode.parent.color
                    currNode.parent.color = "black"
                    siblingNode.right.color = "black"
                    self.rotateLeft(currNode.parent)
                    currNode = self.root
            else:
                siblingNode = currNode.parent.left
                if siblingNode.color == "red":
                    siblingNode.color = "black"
                    currNode.parent.color = "red"
                    self.rotateRight(currNode.parent)
                    siblingNode = currNode.parent.left

                if siblingNode.right.color == "black" and siblingNode.right.color == "black":
                    siblingNode.color = "red"
                    currNode = currNode.parent
                else:
                    if siblingNode.left.color == "black":
                        siblingNode.right.color = "black"
                        siblingNode.color = "red"
                        self.rotateLeft(siblingNode)
                        siblingNode = currNode.parent.left

                    siblingNode.color = currNode.parent.color
                    currNode.parent.color = "black"
                    siblingNode.left.color = "black"
                    self.rotateRight(currNode.parent)
                    currNode = self.root
        currNode.color = "red"

    # Performs a rotate operation to fix the red black tree
    def rbRotate(self, node1, node2):
        if node1.parent == None:
            self.root = node2
        elif node1 == node1.parent.left:    # If u is the left child of its parent
            node1.parent.left = node2
        else:
            node1.parent.right = node2
        node2.parent = node1.parent

    # Deletes a node from RBTree. Various cases depending on the color of node and the presence of child nodes.
    # Once the node is deleted, any red black tree rule violations are fixed by balanceAfterDelete().
    # Time complexity: O(logn)
    def deleteNode(self, node1):
        node2 = node1
        node2_original_color = node2.color
        if node1.left == self.TNULL:
            node3 = node1.right
            self.rbRotate(node1, node1.right)
        elif (node1.right == self.TNULL):
            node3 = node1.left
            self.rbRotate(node1, node1.left)
        else:
            # Replace node with its inorder successor
            node2 = self.getInorderSuccessor(node1.right)
            node2_original_color = node2.color
            node3 = node2.right
            if node2.parent == node1:
                node3.parent = node2
            else:
                self.rbRotate(node2, node2.right)
                node2.right = node1.right
                node2.right.parent = node2

            self.rbRotate(node1, node2)
            node2.left = node1.left
            node2.left.parent = node2
            node2.color = node1.color
        if node2_original_color == 0:
            self.balanceAfterDelete(node3)

        return True

    # Balance the tree after insertion. Various cases considered depending on the color of parent and uncle nodes.
    # Time complexity : O(height) = O(logn)
    def balanceAfterInsert(self, currNode):
        while currNode.parent.color == "red":
            # Check if parent is the right child of grandparent
            if currNode.parent == currNode.parent.parent.right:
                uncle = currNode.parent.parent.left
                if uncle.color == "red":
                    uncle.color = "black"
                    currNode.parent.color = "black"
                    currNode.parent.parent.color = "red"
                    currNode = currNode.parent.parent
                else:
                    if currNode == currNode.parent.left:
                        currNode = currNode.parent
                        self.rotateRight(currNode)
                    currNode.parent.color = "black"
                    currNode.parent.parent.color = "red"
                    self.rotateLeft(currNode.parent.parent)
            else:
                uncle = currNode.parent.parent.right

                if uncle.color == "red":
                    uncle.color = "black"
                    currNode.parent.color = "black"
                    currNode.parent.parent.color = "red"
                    currNode = currNode.parent.parent
                else:
                    if currNode == currNode.parent.right:
                        currNode = currNode.parent
                        self.rotateLeft(currNode)
                    currNode.parent.color = "black"
                    currNode.parent.parent.color = "red"
                    self.rotateRight(currNode.parent.parent)
            if currNode == self.root:
                break
        self.root.color = "black"

    # Gets the inorder successor
    # Time complexity: O(logn)
    def getInorderSuccessor(self, currNode):
        while currNode.left != self.TNULL:
            currNode = currNode.left
        return currNode

    # Left rotation to balance the tree
    # Time complexity: O(1)
    def rotateLeft(self, node1):
        node2 = node1.right
        node1.right = node2.left
        if node2.left != self.TNULL:
            node2.left.parent = node1

        node2.parent = node1.parent
        if node1.parent == None:
            self.root = node2
        elif node1 == node1.parent.left:
            node1.parent.left = node2
        else:
            node1.parent.right = node2
        node2.left = node1
        node1.parent = node2

    # Right rotation to balance the tree
    # Time complexity: O(1)
    def rotateRight(self, node1):
        node2 = node1.left
        node1.left = node2.right
        if node2.right != self.TNULL:
            node2.right.parent = node1

        node2.parent = node1.parent
        if node1.parent == None:
            self.root = node2
        elif node1 == node1.parent.right:
            node1.parent.right = node2
        else:
            node1.parent.left = node2
        node2.right = node1
        node1.parent = node2

    # Inserts a node in the red-black tree. New node is always inserted as a red node.
    # If red-red conflict occurs, it is resolved by balanceAfterInsert().
    # Time complexity : O(height) = O(logn)
    def insert(self, rideNumber, rideCost, tripDuration):
        node = RBTNode(rideNumber, rideCost, tripDuration)
        node.parent = None
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = "red"

        node1 = None
        node2 = self.root

        while node2 != self.TNULL:
            node1 = node2
            if node.rideNumber < node2.rideNumber:
                node2 = node2.left
            else:
                node2 = node2.right

        node.parent = node1
        if node1 == None:
            self.root = node
        elif node.rideNumber < node1.rideNumber:
            node1.left = node
        else:
            node1.right = node

        if node.parent == None:
            node.color = "black"
            return node

        if node.parent.parent == None:
            return node

        self.balanceAfterInsert(node)
        return node

    def getRoot(self):
        return self.root

    # Search for the node whose rideNumber = key. Search works recursively just like in a BST.
    # Time complexity : O(height) = O(logn)
    def search(self, key, node):
        if node == None:
            return node
        elif node.rideNumber == key:
            return node
        elif key < node.rideNumber:
            return self.search(key, node.left)
        else:
            return self.search(key, node.right)

    # Print all nodes whose rideNumber lies between lowerBound and upperBound. Searches for lowerBound and does inorder traversal till upperBound.
    # Time complexity : O(height+S) = O(logn+S) where S is the number of nodes in range
    def printRange(self, node, lowerBound, upperBound, res):

        if node == None:
            return res

        if node.rideNumber < lowerBound:
            res += self.printRange(node.right, lowerBound, upperBound, [])
        elif node.rideNumber > upperBound:
            res += self.printRange(node.left, lowerBound, upperBound, [])
        else:
            res += self.printRange(node.right, lowerBound,
                                   upperBound, [])
            res += [(node.rideNumber, node.rideCost, node.tripDuration)]
            res += self.printRange(node.left, lowerBound,
                                   upperBound, [])

        return res
