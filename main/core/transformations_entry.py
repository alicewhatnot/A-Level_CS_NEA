from core.transformation_class import Transformation
from core.parser import tokenize
from core.queue import Queue

def validTransformation(value, type):
    contains_name = False
    
    # Only parses value if not boolean
    if type != "reflect":
        tokens = tokenize(value) 
        
        # If NAME pattern in value, will be rejected
        for token in tokens:
            if token[0] == "NAME":
                contains_name = True
                return False

   # Checking if the value is none
    if value == "":
        return False
    
    # Checking if the value is default, if so the transformation should be skipped
    if not contains_name:
        if type == "shift" and eval(value) == 0:
            return False
        elif type == "stretch" and eval(value) == 1:
            return False
        elif type == "reflect" and value is False:
            return False
        
        # Checking if stretching by scale factor 0
        elif type == "stretch" and eval(value) == 0:
            return False
        else:
            return True

    return False

def enqueueTransformations(x_stretch_box, y_stretch_box, x_shift_box, y_shift_box, x_reflect, y_reflect):
    transformations_queue = Queue(6)

    # Read values from input boxes
    stretchX_value = x_stretch_box.getText()
    stretchY_value = y_stretch_box.getText()
    shiftX_value = x_shift_box.getText()
    shiftY_value = y_shift_box.getText()
    reflectX_bool = x_reflect.getValue()
    reflectY_bool = y_reflect.getValue()

    if validTransformation(stretchX_value, "stretch"):
        transformations_queue.enqueue(Transformation("stretch", eval(stretchX_value.replace("^", "**")), 'x'))
    if validTransformation(stretchY_value, "stretch"):
        transformations_queue.enqueue(Transformation("stretch", eval(stretchY_value.replace("^", "**")), 'y'))
    if validTransformation(reflectX_bool, "reflect"):
        transformations_queue.enqueue(Transformation("reflect", reflectX_bool, 'x'))
    if validTransformation(reflectY_bool, "reflect"):
        transformations_queue.enqueue(Transformation("reflect", reflectY_bool, 'y'))
    if validTransformation(shiftX_value, "shift"):
        transformations_queue.enqueue(Transformation("shift", eval(shiftX_value.replace("^", "**")), 'x'))
    if validTransformation(shiftY_value, "shift"):
        transformations_queue.enqueue(Transformation("shift", eval(shiftY_value.replace("^", "**")), 'y'))

    return transformations_queue
        
def enqueueDifferentiation():
    transformations_queue = Queue(1)
    transformations_queue.enqueue(Transformation("differentiate"))
    return transformations_queue