# Structure of a Binary Tree Node
class Node:
    def __init__(self, v):
        self.data = v
        self.left = None
        self.right = None


# Function to print preorder traversal
def printPreorder(node):
    if node is None:
        return

    # Deal with the node
    print(node.data, end=' ')

    # Recur on left subtree
    printPreorder(node.left)

    # Recur on right subtree
    printPreorder(node.right)


if __name__ == '__main__':
    root = Node(15)
    root.left = Node(25)
    root.right = Node(35)
    root.left.left = Node(45)
    root.left.right = Node(55)
    root.right.right = Node(65)

    printPreorder(root)