from core.modify_function import (
    ReflectFunction, ShiftFunction, StretchFunction
)
from core.transformations_entry import enqueueTransformations
from core.queue import Queue
from core.function import Function 
from core.ast import copyAST


class TransformManager:
    def __init__(self, input_expression):
        self.transformations_queue = Queue(6)
        self.original_function = input_expression
        self.current_function = input_expression

    def addTransformations(self, x_stretch_box, y_stretch_box, x_shift_box, y_shift_box, x_reflect, y_reflect):
        self.transformations_queue = enqueueTransformations(
            x_stretch_box, y_stretch_box, x_shift_box, y_shift_box, x_reflect, y_reflect
        )

    def applyTransformation(self, transformation):
        ast_copy = copyAST(self.current_function.getFunction())
        new_function = Function(ast_copy)

        modifier = None
        if transformation.type == "shift":
            modifier = ShiftFunction(new_function, transformation.axis, transformation.value)
        elif transformation.type == "stretch":
            modifier = StretchFunction(new_function, transformation.axis, transformation.value)
        elif transformation.type == "reflect":
            modifier = ReflectFunction(new_function, transformation.axis)

        if modifier:
            transformed_function = modifier.ModifyFunction()
            self.current_function = transformed_function  # update for next transformation
            return transformed_function

        
    def applyAllTransformations(self, graph_plotter):
        while not self.transformations_queue.isEmpty():
            transformation = self.transformations_queue.dequeue()
            new_func = self.applyTransformation(transformation)
            graph_plotter.plotSubsequent(new_func)

        self.transformations_queue = Queue(6)

    def getCurrentFunction(self):
        return self.current_function
            
    def nextTransformation(self):
        """Apply the next transformation in the queue and return the new Function."""
        if self.transformations_queue.isEmpty():
            return None
        
        transformation = self.transformations_queue.dequeue()

        # Make a fresh copy of the original AST each time
        from core.function import Function
        from core.modify_function import ShiftFunction, StretchFunction, ReflectFunction

        ast_copy = self.current_function.getFunction()  # use copyAST if needed
        new_func = Function(ast_copy)

        modifier = None
        if transformation.type == "shift":
            modifier = ShiftFunction(new_func, transformation.axis, transformation.value)
        elif transformation.type == "stretch":
            modifier = StretchFunction(new_func, transformation.axis, transformation.value)
        elif transformation.type == "reflect":
            modifier = ReflectFunction(new_func, transformation.axis)

        if modifier:
            self.current_function = modifier.ModifyFunction()
            return self.current_function
        return None

    def hasTransformations(self):
        return not self.transformations_queue.isEmpty()