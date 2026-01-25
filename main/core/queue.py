class Queue:
    def __init__(self, max_size):
        # Create fixed-size array for queue items
        self.items = [None] * max_size

        # Index of the front of the queue
        self.front = 0

        # Index of the rear of the queue
        self.rear = -1

        # Current number of items in the queue
        self.size = 0

        # Maximum size of the queue
        self.max_size = max_size

    def enqueue(self, value):
        # Adds an item to the rear of the queue

        if self.isFull():
            print("Queue Overflow")
            return

        self.rear = (self.rear + 1) % self.max_size
        self.items[self.rear] = value
        self.size += 1

    def dequeue(self):
        # Removes and returns the item at the front of the queue

        if self.isEmpty():
            return None

        item = self.items[self.front]
        self.items[self.front] = None

        self.front = (self.front + 1) % self.max_size
        self.size -= 1

        return item

    def isEmpty(self):
        # Returns True if the queue is empty
        return self.size == 0

    def isFull(self):
        # Returns True if the queue is full
        return self.size == self.max_size

    def clear(self):
        # Removes all items from the queue

        while not self.isEmpty():
            self.dequeue()
