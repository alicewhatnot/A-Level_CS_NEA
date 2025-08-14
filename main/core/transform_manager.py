from core.modify_function import (
    ReflectFunction, ShiftFunction, StretchFunction
)

class TransformManager:
    def __init__(self):
        self.transformations_queue = []
        self.current_function = None

    def add_transformations(self, transformations):
        # Add a list of transformation objects to the queue
        self.transformations_queue.extend(transformations)

    def apply_transformation(self, transformation):
        # Use the appropriate ModifyFunction subclass
        if transformation.type == "reflect":
            modifier = ReflectFunction(self.current_function, transformation.axis)
        elif transformation.type == "shift":
            modifier = ShiftFunction(self.current_function, transformation.axis, transformation.value)
        elif transformation.type == "stretch":
            modifier = StretchFunction(self.current_function, transformation.axis, transformation.value)
        else:
            modifier = None

        if modifier:
            self.current_function = modifier.modify_function()

    def apply_all_transformations(self):
        # Applies all transformations in the queue to the current function
        for transformation in self.transformations_queue:
            self.apply_transformation(transformation)

    def get_current_function(self):
        # Returns the current (possibly transformed) function AST
        return self.current_function