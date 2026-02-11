from core.ast import ASTNode, printAST

def reflectXAxis(node):
    """
    Reflects the function across the X-axis by multiplying the whole expression by -1
    """
    if node is None:
        return None
    # print("\nOriginal Node:")
    # printAST(node)
    negative_one = ASTNode("NUMBER", "-1", None, None)
    newNode = ASTNode("OP", "*", negative_one, node)
    # print("After reflection across X-axis:")
    # printAST(newNode)
    return newNode


def reflectYAxis(node):
    """
    Reflects the function across the Y-axis by multiplying variables by -1
    """
    if node is None:
        return None
    # print("\nOriginal Node:")
    # printAST(node)
    
    # Only reflect actual variables, not functions
    if node.type == "NAME":
        negative_one = ASTNode("NUMBER", "-1", None, None)
        newNode = ASTNode("OP", "*", negative_one, node)
        # print("Reflected variable across Y-axis:")
        # printAST(newNode)
        return newNode
    elif node.type == "FUNCTION":
        # Reflect inside the function argument
        node.left = reflectYAxis(node.left)
    else:
        # Recursively reflect left and right for operators
        if node.left:
            node.left = reflectYAxis(node.left)
        if node.right:
            node.right = reflectYAxis(node.right)
    # print("Node after reflection across Y-axis:")
    # printAST(node)
    return node


def shiftX(node, shift):
    """
    Shifts the function along the X-axis by subtracting the shift value 
    """
    if node is None:
        return None
    # print("\nOriginal Node:")
    # printAST(node)

    if node.type == "NAME":
        shift_amount = ASTNode("NUMBER", str(shift), None, None)
        newNode = ASTNode("OP", "-", node, shift_amount)
        # print("Shifted variable along X-axis:")
        # printAST(newNode)
        return newNode
    elif node.type == "FUNCTION":
        node.left = shiftX(node.left, shift)
    else:
        if node.left:
            node.left = shiftX(node.left, shift)
        if node.right:
            node.right = shiftX(node.right, shift)
    # print("Node after X-axis shift:")
    # printAST(node)
    return node


def shiftY(node, shift):
    """
    Shifts the function along the Y-axis by adding the shift value to the expression
    """
    if node is None:
        return None
    # print("\nOriginal Node:")
    # printAST(node)
    
    shift_amount = ASTNode("NUMBER", str(shift), None, None)
    newNode = ASTNode("OP", "+", node, shift_amount)
    # print("Node after Y-axis shift:")
    # printAST(newNode)
    return newNode


def stretchX(node, stretch):
    """
    Stretches the function along the X-axis by dividing variables by the stretch
    """
    if node is None:
        return None
    # print("\nOriginal Node:")
    # printAST(node)

    if node.type == "NAME":
        factor = ASTNode("NUMBER", str(stretch), None, None)
        newNode = ASTNode("OP", "/", node, factor)
        # print("Stretched variable along X-axis:")
        # printAST(newNode)
        return newNode
    elif node.type == "FUNCTION":
        node.left = stretchX(node.left, stretch)
    else:
        if node.left:
            node.left = stretchX(node.left, stretch)
        if node.right:
            node.right = stretchX(node.right, stretch)
    # print("Node after X-axis stretch:")
    # printAST(node)
    return node


def stretchY(node, stretch):
    """
    Stretches the function along the Y-axis by multiplying the whole expression by the stretch
    """
    if node is None:
        return None
    # print("\nOriginal Node:")
    # printAST(node)
    
    factor = ASTNode("NUMBER", str(stretch), None, None)
    newNode = ASTNode("OP", "*", factor, node)
    # print("Node after Y-axis stretch:")
    # printAST(newNode)
    return newNode
