class Stack:
    def __init__(self, max_size):
        self.__items = [None] * max_size
        self.__top_index = 0
        self.__max_size = max_size

    def push(self, value):
        if self.__top_index == self.__max_size:
            print("Stack Overflow")
            return
        self.__items[self.__top_index] = value
        self.__top_index += 1

    def pop(self):
        if self.__top_index == 0:
            print("Stack Underflow")
            return None
        self.__top_index -= 1
        value = self.__items[self.__top_index]
        self.__items[self.__top_index] = None  
        return value

    def top(self):
        if self.__top_index == 0:
            return None
        return self.__items[self.__top_index - 1]

    def empty(self):
        return self.__top_index == 0

    def size(self):
        return self.__top_index