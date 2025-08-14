from core.ast import ASTNode

def reflectXAxis(node):
    # Performs a reflection in the x axis
    if node is None:
        return None
    # Create new nodes at root to multiply expression by -1
    negative_one = ASTNode("NUMBER", "-1", None, None)
    return ASTNode("OP", "*", negative_one, node)

def reflectYAxis(node):
    # Performs a reflection in the y axis
    if node is None:
        return None
    # Replaces every x with -1 * x in the AST
    elif node.type == "NAME" and node.value == "x":
        negative_one = ASTNode("NUMBER", "-1", None, None)
        return ASTNode("OP", "*", negative_one, node)
    else:
        if node.left:
            node.left = reflectYAxis(node.left)
        if node.right:
            node.right = reflectYAxis(node.right)
        return node

def shiftX(node, shift):
    # Performs a shift along the x axis
    if node is None:
        return None
    # Replace x with x - shift so a positive shift moves right
    elif node.type == "NAME" and node.value == "x":
        shift_amount = ASTNode("NUMBER", str(shift), None, None)
        return ASTNode("OP", "-", node, shift_amount)
    else:
        if node.left:
            node.left = shiftX(node.left, shift)
        if node.right:
            node.right = shiftX(node.right, shift)
        return node

def shiftY(node, shift):
    # Performs a shift along the y axis
    if node is None:
        return None
    # Adds the shift to the expression 
    shift_amount = ASTNode("NUMBER", str(shift), None, None)
    return ASTNode("OP", "+", node, shift_amount)

def stretchX(node, stretch):
    # Performs a stretch along the x axis
    if node is None:
        return None
    # Divide by stretch scale factor 
    elif node.type == "NAME" and node.value == "x":
        factor = ASTNode("NUMBER", str(stretch), None, None)
        return ASTNode("OP", "/", node, factor)
    else:
        if node.left:
            node.left = stretchX(node.left, stretch)
        if node.right:
            node.right = stretchX(node.right, stretch)
        return node

def stretchY(node, stretch):
    # Performs a stretch along the y axis
    if node is None:
        return None
    # Simply multiply the expression AST by stretch scale factor
    factor = ASTNode("NUMBER", str(stretch), None, None)
    return ASTNode("OP", "*", factor, node)