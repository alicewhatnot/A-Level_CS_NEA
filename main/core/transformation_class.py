
class Transformation:
    '''Transformation class, created at runtime for each transformation'''
    def __init__(self, transform_type, transform_value = None, transform_axis = None):
        self.type = transform_type
        self.value = transform_value
        self.axis = transform_axis

