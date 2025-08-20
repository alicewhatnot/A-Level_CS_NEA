class Function:
    def __init__(self, function_tree, function_colour=(201, 66, 119)):
        self.function_tree = function_tree  
        self.function_colour = function_colour

    def getFunction(self):
        return self.function_tree

    def setFunction(self, new_function_tree):
        self.function_tree = new_function_tree

    def getColour(self):
        return self.function_colour

    def setColour(self, new_colour):
        self.function_colour = new_colour
