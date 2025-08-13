from core.parser import tokenize
from core.queue import Queue
import math

class TransformationsEntry:
    def __init__(self):
        self.user_inputs = []
        self.ordered_transformations = []

    def valid_transformation(self, value, type_):
        contains_name = False

        # Only parses value if not boolean
        if type_ != "reflect":
            tokens = tokenize(value)
            # If NAME pattern in value, will be rejected
            for token in tokens:
                if token[0] == "NAME":
                    contains_name = True
                    return False

        # Checking if the value is default, if so the transformation should be skipped
        if not contains_name:
            if type_ == "shift" and eval(value) == 0:
                return False
            elif type_ == "stretch" and eval(value) == 1:
                return False
            elif type_ == "reflect" and value is False:
                return False
            else:
                return True

        return False

    def enqueue_transformations(self, stretchX, stretchY, reflectX, reflectY, shiftX, shiftY, queue):
        # Get values from each entry box
        stretchX_value = stretchX.getText()
        stretchY_value = stretchY.getText()
        reflectX_bool = reflectX.is_selected()
        reflectY_bool = reflectY.is_selected()
        shiftX_value = shiftX.getText()
        shiftY_value = shiftY.getText()

        # Adds each transformation to the queue in the correct order if validTransformation returns true
        # Uses evaluate to convert an invalid entry such as 3 + 2 to 5
        # Needs to replace all ^ with ** as this is done in the parser which is unused here
        if self.valid_transformation(stretchX_value, "stretch"):
            queue.enqueue("stretch", eval(stretchX_value.replace("^", "**")), 'x')

        if self.valid_transformation(stretchY_value, "stretch"):
            queue.enqueue("stretch", eval(stretchY_value.replace("^", "**")), 'y')

        if self.valid_transformation(reflectX_bool, "reflect"):
            queue.enqueue("reflect", reflectX_bool, 'x')

        if self.valid_transformation(reflectY_bool, "reflect"):
            queue.enqueue("reflect", reflectY_bool, 'y')

        if self.valid_transformation(shiftX_value, "shift"):
            queue.enqueue("shift", eval(shiftX_value.replace("^", "**")), 'x')

        if self.valid_transformation(shiftY_value, "shift"):
            queue.enqueue("shift", eval(shiftY_value.replace("^", "**")), 'y')

