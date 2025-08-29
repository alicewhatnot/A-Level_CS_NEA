class Queue:
    def __init__(self, max_size):
        self.__items = [None] * max_size
        self.__front = 0
        self.__rear = -1
        self.__size = 0
        self.__max_size = max_size

    def enqueue(self, value):
        if self.isFull():
            print("Queue Overflow")
            return
        self.__rear = (self.__rear + 1) % self.__max_size
        self.__items[self.__rear] = value
        self.__size += 1

    def dequeue(self):
        if self.isEmpty():
            return None
        item = self.__items[self.__front]
        self.__items[self.__front] = None 
        self.__front = (self.__front + 1) % self.__max_size
        self.__size -= 1
        return item

    def isEmpty(self):
        return self.__size == 0

    def isFull(self):
        return self.__size == self.__max_size
    
    def clear(self):
        while not self.isEmpty:
            self.dequeue()
    
    