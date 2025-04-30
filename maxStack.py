"""
Algorithm:
     1 Start Program
     2 Initialize the value 6 to variable MAXSIZE, indicating the maximum size of the stack
     3 Initialize variable stack containing the formula [0] * MAXSIZE
     4 Initialize variable top with -1
     5 Declare the following methods needed for stacks:
        - isEmpty()
        - isFull()
        - pop()
         -push()
         -peek()
     6 Using push(), add the following numerical data to stack: 10, 20, 30
     7 Display the current stack using a for loop
     8 Using isFull(), check whether the stack length is equal to MAXSIZE and display "The stack is full!" if isFull() returns True;
       display "The stack is not full or empty" if isFull() returns False
     9 Check the current stack using peek() and display the top stack
    10 Pop all available data on stack using pop() and display the popped elements using a while loop
    11 Using isEmpty(), check whether the stack length is equivalent to top and display "The stack is empty!" if isEmpty()
       returns True; display "The stack still has contents" if isEmpty() returns False
    12 Program ends

"""

MAXSIZE = 6
stack = [0] * MAXSIZE
top = -1
def isEmpty():
    if top == -1:
        return True
    else:
        return False
def isFull():
    if top == MAXSIZE:
        return True
    else:
        return False
def pop():
    global top # global variable can be used in any area
    data = 0
    if isEmpty() != 1:
        data = stack[top]
        top = top - 1
        return data
    else:
        print("Could not retrieve data, Stack is empty.")
    return data
def push(data):
    global top
    if isFull() !=1:
        top = top + 1
        stack[top] = data
    else:
        print("\nCould not insert data, Stack is full.")
        return data
def peek():
    if not isEmpty():
        return stack[top]
    else:
        print("Stack is empty.")
        return None

# Stack implementation
push(10)
push(20)
push(30)
print("Stack Elements: ")
for i in range (MAXSIZE):
    print("Push:", stack[i], end = " \n")
print("Is stack full?")
if isFull():
    print("The stack is full!")
else:
    print("The stack is not full or empty")
print("Peek:", peek())
print("Elements popped: ")
while isEmpty() != 1:
    data = pop()
    print("Pop:", data, end = " \n")
print("Is stack empty?")
if isEmpty():
    print("The stack is empty!")
else:
    print("The stack still has contents")