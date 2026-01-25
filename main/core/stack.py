class Stack:
    def __init__(self, max_size):
        # Create fixed-size array for stack items
        self.items = [None] * max_size

        # Index of the next free position (top of stack)
        self.top_index = 0

        # Maximum size of the stack
        self.max_size = max_size

    def push(self, value):
        # Adds a value to the top of the stack

        if self.top_index == self.max_size:
            print("Stack Overflow")
            return

        self.items[self.top_index] = value
        self.top_index += 1

    def pop(self):
        # Removes and returns the top value from the stack

        if self.top_index == 0:
            print("Stack Underflow")
            return None

        self.top_index -= 1
        value = self.items[self.top_index]
        self.items[self.top_index] = None

        return value

    def top(self):
        # Returns the top value without removing it

        if self.top_index == 0:
            return None

        return self.items[self.top_index - 1]

    def empty(self):
        # Returns True if the stack is empty
        return self.top_index == 0

    def size(self):
        # Returns the number of items in the stack
        return self.top_index
