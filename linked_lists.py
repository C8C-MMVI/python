"""
ALGORITHM:
1. Start Program
2. Create a Node class
3. Initialize the following methods for the Linked Lists:
    insert_at_beginning- Inserts data to the node
    delete_node- Deletes a specific node
    traverse- Travels through the given data until the program prints "None"
4. Insert the following integer data to the node: 5, 10, 15
5. Print the linked list
6. Delete the second data (10)
7. Print the updated linked list
8. Program ends
"""
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def insert_at_beginning(head, data):
    new_node = Node(data)
    new_node.next = head
    return new_node

def delete_node(node):
    if node is None or node.next is None:
        print("Error: The given node is None or the next node is None")
        return

    next_node = node.next
    node.next = next_node.next
    del next_node

def traverse(head):
    current = head
    while current:
        print(str(current.data) + " -> ", end=" ")
        current = current.next
    print("None")

head = None
head = insert_at_beginning(head, 15)
head = insert_at_beginning(head, 10)
head = insert_at_beginning(head, 5)
traverse(head)
delete_node(head)
traverse(head)