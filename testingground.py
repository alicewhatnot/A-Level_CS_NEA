def validTransformation(value, type):
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


def enqueueTransformations(x_stretch_box, y_stretch_box, x_shift_box, y_shift_box, x_reflect, y_reflect):
    # X-axis
    if validTransformation(stretchX_value, "stretch"):
        transformations_queue.enqueue(Transformation("stretch", eval(stretchX_value.replace("^", "**")), 'x'))
    if validTransformation(reflectX_bool, "reflect"):
        transformations_queue.enqueue(Transformation("reflect", reflectX_bool, 'x'))
    if validTransformation(shiftX_value, "shift"):
        transformations_queue.enqueue(Transformation("shift", eval(shiftX_value.replace("^", "**")), 'x'))


    # Y-axis
    if validTransformation(stretchY_value, "stretch"):
        transformations_queue.enqueue(Transformation("stretch", eval(stretchY_value.replace("^", "**")), 'y'))
    if validTransformation(reflectY_bool, "reflect"):
        transformations_queue.enqueue(Transformation("reflect", reflectY_bool, 'y'))
    if validTransformation(shiftY_value, "shift"):
        transformations_queue.enqueue(Transformation("shift", eval(shiftY_value.replace("^", "**")), 'y'))

    try:
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
    except:
        return False