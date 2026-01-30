from core.modify_function import ReflectFunction, ShiftFunction, StretchFunction, DifferentiateFunction
from core.queue import Queue
from core.function import Function 
from core.transformations_entry import enqueueTransformations
from core.ast import copyAST

class TransformManager:
    """
    Manages a function and queue of transformations to be applied

    Responsible for executing the transformations in the correct order
    """
    def __init__(self, input_expression):
        self.transformations_queue = Queue(6)
        self.current_function = input_expression

    def addTransformations(self, x_stretch_box, y_stretch_box, x_shift_box, y_shift_box, x_reflect, y_reflect):
        """"
        Adds given transformations to the transformations queue
        """
        self.transformations_queue = enqueueTransformations(
            x_stretch_box, y_stretch_box, x_shift_box, y_shift_box, x_reflect, y_reflect
        )

    def applyTransformation(self, transformation):
        """
        Applies a given transformation to the current function
        """
        new_func = None

        if transformation.type == "shift":
            new_func = ShiftFunction(self.current_function, transformation.axis, transformation.value)
        elif transformation.type == "stretch":
            new_func = StretchFunction(self.current_function, transformation.axis, transformation.value)
        elif transformation.type == "reflect":
            new_func = ReflectFunction(self.current_function, transformation.axis)
        elif transformation.type == "differentiate":
            new_func = DifferentiateFunction(self.current_function)

        if new_func:
            return new_func
        else:
            return None

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

    def setBaseFunction(self, new_function):
        """
        Sets the current function to the original function
        """
        self.current_function = new_function

    def getCurrentFunction(self):
        """
        Returns the current function
        """
        return self.current_function

    def hasTransformations(self):
        return not self.transformations_queue.isEmpty()
        
