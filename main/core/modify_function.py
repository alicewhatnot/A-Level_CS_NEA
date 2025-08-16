from main.core.transformations import (
    reflectXAxis, reflectYAxis, shiftX, shiftY, stretchX, stretchY
)
from core.differentiation import differentiate

class ModifyExpression:
    def __init__(self, altered_expression):
        self.altered_expression = altered_expression

    def modifyExpression(self):
        # Base method, should be overridden
        return self.altered_expression

class DifferentiateExpression(ModifyExpression):
    def modifyExpression(self):
        return differentiate(self.altered_expression)

class ShiftExpression(ModifyExpression):
    def __init__(self, altered_expression, axis, value):
        super().__init__(altered_expression)
        self.axis = axis
        self.value = value

    def modifyExpression(self):
        if self.axis == "x":
            return shiftX(self.altered_expression, self.value)
        elif self.axis == "y":
            return shiftY(self.altered_expression, self.value)
        return self.altered_expression

class StretchExpression(ModifyExpression):
    def __init__(self, altered_expression, axis, value):
        super().__init__(altered_expression)
        self.axis = axis
        self.value = value

    def modifyExpression(self):
        if self.axis == "x":
            return stretchX(self.altered_expression, self.value)
        elif self.axis == "y":
            return stretchY(self.altered_expression, self.value)
        return self.altered_expression

class ReflectExpression(ModifyExpression):
    def __init__(self, altered_expression, axis):
        super().__init__(altered_expression)
        self.axis = axis

    def modifyExpression(self):
        if self.axis == "x":
            return reflectXAxis(self.altered_expression)
        elif self.axis == "y":
            return reflectYAxis(self.altered_expression)
        return self.altered_expression
