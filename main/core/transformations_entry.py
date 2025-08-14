from core.transformation_class import Transformation

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
        transformation = Transformation("stretch", eval(stretchX_value.replace("^", "**")), 'x')
        queue.enqueue(transformation)

    if self.valid_transformation(stretchY_value, "stretch"):
        transformation = Transformation("stretch", eval(stretchY_value.replace("^", "**")), 'y')
        queue.enqueue(transformation)

    if self.valid_transformation(reflectX_bool, "reflect"):
        transformation = Transformation("reflect", reflectX_bool, 'x')
        queue.enqueue(transformation)

    if self.valid_transformation(reflectY_bool, "reflect"):
        transformation = Transformation("reflect", reflectY_bool, 'y')
        queue.enqueue(transformation)

    if self.valid_transformation(shiftX_value, "shift"):
        transformation = Transformation("shift", eval(shiftX_value.replace("^", "**")), 'x')
        queue.enqueue(transformation)

    if self.valid_transformation(shiftY_value, "shift"):
        transformation = Transformation("shift", eval(shiftY_value.replace("^", "**")), 'y')
        queue.enqueue(transformation)

        