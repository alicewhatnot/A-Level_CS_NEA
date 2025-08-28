from core.modify_function import (
    ReflectFunction, ShiftFunction, StretchFunction, DifferentiateFunction
)
from core.transformations_entry import enqueueTransformations, enqueueDifferentiation
from core.queue import Queue
from core.function import Function 
from core.ast import copyAST
from core.transformation_class import Transformation


class TransformManager:
    def __init__(self, input_expression):
        self.transformations_queue = Queue(6)
        self.original_function = input_expression
        self.current_function = input_expression

    def addTransformations(self, x_stretch_box, y_stretch_box, x_shift_box, y_shift_box, x_reflect, y_reflect):
        self.transformations_queue = enqueueTransformations(
            x_stretch_box, y_stretch_box, x_shift_box, y_shift_box, x_reflect, y_reflect
        )

    def addDifferentiation(self):
        self.transformations_queue = enqueueDifferentiation(self.current_function)

    def applyTransformation(self, transformation, update_base=True):
        modifier = None

        if transformation.type == "shift":
            modifier = ShiftFunction(self.current_function, transformation.axis, transformation.value)
        elif transformation.type == "stretch":
            modifier = StretchFunction(self.current_function, transformation.axis, transformation.value)
        elif transformation.type == "reflect":
            modifier = ReflectFunction(self.current_function, transformation.axis)
        elif transformation.type == "differentiate":
            modifier = DifferentiateFunction(self.current_function)

        if modifier:
            new_func = modifier.ModifyFunction()
            if update_base:
                self.current_function = new_func
            return new_func

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

        # Always work on a fresh AST copy
        ast_copy = copyAST(self.current_function.getFunction())
        var_copy = self.current_function.getVariable()
        new_func = Function(ast_copy, var_copy)

        modifier = None
        if transformation.type == "shift":
            modifier = ShiftFunction(new_func, transformation.axis, transformation.value)
        elif transformation.type == "stretch":
            modifier = StretchFunction(new_func, transformation.axis, transformation.value)
        elif transformation.type == "reflect":
            modifier = ReflectFunction(new_func, transformation.axis)
        elif transformation.type == "differentiate":
            modifier = DifferentiateFunction(new_func)

        if modifier:
            self.current_function = modifier.ModifyFunction()
            return self.current_function
        return None

    def setBaseFunction(self, new_function):
        """
        Set a modified function (e.g., a derivative) as the new base function
        for future transformations.
        """
        self.current_function = new_function
        self.transformations_queue = Queue(1)

    def hasTransformations(self):
        return not self.transformations_queue.isEmpty()
        
