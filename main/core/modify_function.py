from main.core.transformations import (
    reflectXAxis, reflectYAxis, shiftX, shiftY, stretchX, stretchY
)
from core.differentiation import differentiate

class ModifyFunction:
    def __init__(self, altered_function):
        self.altered_function = altered_function

    def modifyFunction(self):
        # Base method, should be overridden
        return self.altered_function

class DifferentiateFunction(ModifyFunction):
    def modifyFunction(self):
        return differentiate(self.altered_function)

class ShiftFunction(ModifyFunction):
    def __init__(self, altered_function, axis, value):
        super().__init__(altered_function)
        self.axis = axis
        self.value = value

    def modifyFunction(self):
        if self.axis == "x":
            return shiftX(self.altered_function, self.value)
        elif self.axis == "y":
            return shiftY(self.altered_function, self.value)
        return self.altered_function

class StretchFunction(ModifyFunction):
    def __init__(self, altered_function, axis, value):
        super().__init__(altered_function)
        self.axis = axis
        self.value = value

    def modifyFunction(self):
        if self.axis == "x":
            return stretchX(self.altered_function, self.value)
        elif self.axis == "y":
            return stretchY(self.altered_function, self.value)
        return self.altered_function

class ReflectFunction(ModifyFunction):
    def __init__(self, altered_function, axis):
        super().__init__(altered_function)
        self.axis = axis

    def modifyFunction(self):
        if self.axis == "x":
            return reflectXAxis(self.altered_function)
        elif self.axis == "y":
            return reflectYAxis(self.altered_function)
        return self.altered_function