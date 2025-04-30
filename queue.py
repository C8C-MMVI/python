class FixedStringQueue():

    def __init__(self, size): # Initial method
        self.size = size
        self.queue = []

    def isEmpty(self):
        return len(self.queue) == 0

    def isFull(self):
        return len(self.queue) == self.size

    def enqueue(self, item):
        if not isinstance(item, str):  # Ensures only strings are allowed
            print("Only string elements are allowed.")
            return

        if self.isFull():
            print("Queue is full! Cannot enqueue")
        else:
            self.queue.append(item)
            # print(f'Enqueued: {item}')

    def dequeue(self):
        if self.isEmpty():
            print("Queue is empty. Cannot dequeue.")
            return None
        return self.queue.pop(0)

    def peek(self):
        if self.isEmpty():
            print("Queue is empty. No front element.")
            return None
        return self.queue[0]

# Queue implementation
queue = FixedStringQueue(4)

queue.enqueue("Grace")
queue.enqueue("Vienna")
queue.enqueue("Charlie")
queue.enqueue("David")
queue.enqueue("Eve") # Data exceeded the maximum queue size

print("Front element:", queue.peek())
print("Removed:", queue.dequeue())
# Whether the expected output should have the same peek twice or it's a document error is unknown
print("Front element:", queue.peek())
print("Front element:", queue.peek())
