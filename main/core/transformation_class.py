from core.ast import ASTNode

class Transformation:
    '''Transformation class, created at runtime for each transformation'''
    def __init__(self, transform_type, transform_value, transform_axis):
        self.type = transform_type
        self.value = transform_value
        self.axis = transform_axis

