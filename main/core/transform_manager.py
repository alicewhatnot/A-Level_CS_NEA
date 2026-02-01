from core.modify_function import ReflectFunction, ShiftFunction, StretchFunction
from core.queue import Queue
from core.function import Function 
from core.transformations_entry import enqueueTransformations
from core.ast import copyAST
import math

class TransformManager:
    """
    Manages a function and queue of transformations to be applied

    Responsible for executing the transformations in the correct order
    """
    def __init__(self, input_expression):
        self.transformations_queue = Queue(6)
        self.original_function = input_expression
        self.current_function = input_expression

    def addTransformations(self, x_stretch_box, y_stretch_box, x_shift_box, y_shift_box, x_reflect, y_reflect):
        """"
        Adds given transformations to the transformations queue
        """
        self.transformations_queue = enqueueTransformations(
            x_stretch_box, y_stretch_box, x_shift_box, y_shift_box, x_reflect, y_reflect
        )

    def applyTransformation(self, transformation, progress=1.0, base_function=None):
        """
        Applies a transformation at a given progress (0..1).
        If progress == 1, updates current_function.
        """
        if base_function is None:
            base_function = self.current_function

        temp_func = Function(
            copyAST(base_function.getFunction()),
            base_function.getFunctionVar(),
            base_function.getColour()
        )

        modifier = None

        if transformation.getType() == "shift":
            value = transformation.getVal() * progress
            modifier = ShiftFunction(temp_func, transformation.getAxis(), value)

        elif transformation.getType() == "stretch":
            scale = 1 + (transformation.getVal() - 1) * progress
            modifier = StretchFunction(temp_func, transformation.getAxis(), scale)

        elif transformation.getType() == "reflect":
            if progress == 1:
                modifier = ReflectFunction(temp_func, transformation.getAxis())
            else:
                nonlinear = math.sin(progress * math.pi / 2)
                scale = 1 - 2 * nonlinear
                axis = "y" if transformation.getAxis() == "x" else "x"
                modifier = StretchFunction(temp_func, axis, scale)

        if modifier is None:
            return temp_func

        result = modifier.ModifyFunction()

        if progress == 1:
            self.current_function = result

        return result


    def applyAllTransformations(self, graph_plotter):
        """
        Applies each transformation in the queue one after another
        """
        while not self.transformations_queue.isEmpty():
            transformation = self.transformations_queue.dequeue()
            new_func = self.applyTransformation(transformation)
            graph_plotter.plotSubsequent(new_func)

        # Resets the queue once the transformations have been applied
        self.transformations_queue = Queue(6)

    def getCurrentFunction(self):
        """
        Returns the current function
        """
        return self.current_function
            
    def nextTransformation(self):
        if self.transformations_queue.isEmpty():
            return None

        transformation = self.transformations_queue.dequeue()
        return self.applyTransformation(transformation, progress=1.0)

    def setBaseFunction(self, new_function):
        """
        Set a modified function as the new base function
        This is for implementation in repeated differentiation for further derivatives
        """
        self.current_function = new_function
        self.transformations_queue = Queue(1)

    def hasTransformations(self):
        return not self.transformations_queue.isEmpty()
        
