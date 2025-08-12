from main.core.transformation import Transformation

class Queue:
    def __init__(self, max_size):
        self.__items = [None] * max_size
        self.__front = 0
        self.__rear = -1
        self.__size = 0
        self.__max_size = max_size

    def enqueue_object(self, type_, value, axis):
        '''Adds transformations to the queue'''
        '''If overflow occurs, a problem has occurred '''
        if self.is_full():
            print("Queue Overflow")
            return
        self.__rear = (self.__rear + 1) % self.__max_size
        transformation = Transformation(type_, value, axis)
        self.__items[self.__rear] = transformation
        self.__size += 1

    def enqueue(self, value):
        if self.is_full():
            print("Queue Overflow")
            return
        self.__rear = (self.__rear + 1) % self.__max_size
        self.__items[self.__rear] = value
        self.__size += 1

    def dequeue(self):
        '''If transformation then returns the transformation at the front of the queue for graphing'''
        if self.is_empty():
            return None
        item = self.__items[self.__front]
        self.__items[self.__front] = None 
        self.__front = (self.__front + 1) % self.__max_size
        self.__size -= 1
        return item

    def is_empty(self):
        return self.__size == 0

    def is_full(self):
        return self.__size == self.__max_size