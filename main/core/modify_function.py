from core.transformations import (
    reflectXAxis, reflectYAxis, shiftX, shiftY, stretchX, stretchY
)
from core.differentiation import differentiate

class ModifyFunction:
    def __init__(self, altered_function):
        self.altered_function = altered_function  # This is a Function object

    def ModifyFunction(self):
        return self.altered_function

class DifferentiateFunction(ModifyFunction):
    def ModifyFunction(self):
        new_tree = differentiate(self.altered_function.getFunction())
        self.altered_function.setFunction(new_tree)
        return self.altered_function

class ShiftFunction(ModifyFunction):
    def __init__(self, altered_function, axis, value):
        super().__init__(altered_function)
        self.axis = axis
        self.value = value

    def ModifyFunction(self):
        tree = self.altered_function.getFunction()
        if self.axis == "x":
            tree = shiftX(tree, self.value)
        elif self.axis == "y":
            tree = shiftY(tree, self.value)
        self.altered_function.setFunction(tree)
        return self.altered_function

class StretchFunction(ModifyFunction):
    def __init__(self, altered_function, axis, value):
        super().__init__(altered_function)
        self.axis = axis
        self.value = value

    def ModifyFunction(self):
        tree = self.altered_function.getFunction()
        if self.axis == "x":
            tree = stretchX(tree, self.value)
        elif self.axis == "y":
            tree = stretchY(tree, self.value)
        self.altered_function.setFunction(tree)
        return self.altered_function

class ReflectFunction(ModifyFunction):
    def __init__(self, altered_function, axis):
        super().__init__(altered_function)
        self.axis = axis

    def ModifyFunction(self):
        tree = self.altered_function.getFunction()
        if self.axis == "x":
            tree = reflectXAxis(tree)
        elif self.axis == "y":
            tree = reflectYAxis(tree)
        self.altered_function.setFunction(tree)
        return self.altered_function
