class Expression:
    def __init__(self, expression_tree, expression_colour=(201, 66, 119)):
        self.expression_tree = expression_tree  
        self.expression_colour = expression_colour

    def getExpression(self):
        return self.expression_tree

    def setExpression(self, new_expression_tree):
        self.expression_tree = new_expression_tree

    def getColour(self):
        return self.expression_colour

    def setColour(self, new_colour):
        self.expression_colour = new_colour
