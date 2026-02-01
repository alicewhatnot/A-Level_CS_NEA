import math

class Transformation:
    """
    Transformation class, created at runtime for each transformation.
    Stores all information needed to apply the transformation.
    """
    def __init__(self, transform_type, transform_value=None, transform_axis=None, ):
        self.type = transform_type            # "shift", "stretch", "reflect", "differentiate", etc.
        self.value = transform_value          # numeric value (for shift/stretch)
        self.axis = transform_axis            # "x" or "y" (if applicable)
        self.converted = False

    def getVal(self):
        return self.value
    
    def convertToRad(self):
        # To convert the x shift to radians if the user has entered it in degrees
        if not self.converted: # Avoids converting more than once
            self.value = self.value * math.pi / 180
            self.converted = True
    
    def getType(self):
        return self.type

    def getAxis(self):
        return self.axis