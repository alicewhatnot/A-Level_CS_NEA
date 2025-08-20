from core.modify_function import (
    ReflectFunction, ShiftFunction, StretchFunction
)
from core.transformations_entry import enqueueTransformations
from core.queue import Queue


class TransformManager:
    def __init__(self, input_expression):
        self.transformations_queue = Queue(6)
        self.current_function = input_expression

    def addTransformations(self, x_stretch_box, y_stretch_box, x_shift_box, y_shift_box, x_reflect, y_reflect):
        self.transformations_queue = enqueueTransformations(
            x_stretch_box, y_stretch_box, x_shift_box, y_shift_box, x_reflect, y_reflect
        )

    def applyTransformation(self, transformation):
        modifier = None
        if transformation.type == "shift":
            modifier = ShiftFunction(self.current_function, transformation.axis, transformation.value)
        elif transformation.type == "stretch":
            modifier = StretchFunction(self.current_function, transformation.axis, transformation.value)
        elif transformation.type == "reflect":
            modifier = ReflectFunction(self.current_function, transformation.axis)

        if modifier:
            self.current_function = modifier.ModifyFunction()

    def applyAllTransformations(self, graph_plotter, screen):
            # Apply every transformation in the queue
            while not self.transformations_queue.isEmpty():
                transformation = self.transformations_queue.dequeue()
                self.applyTransformation(transformation)
            # Update the graph with the transformed function
            graph_plotter.plotSubsequent(screen, self.current_function)

    def getCurrentFunction(self):
        return self.current_function
            
