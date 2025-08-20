from core.ast import ASTNode

def reflectXAxis(node):
    if node is None:
        return None
    negative_one = ASTNode("NUMBER", "-1", None, None)
    return ASTNode("OP", "*", negative_one, node)

def reflectYAxis(node):
    if node is None:
        return None
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
    if node is None:
        return None
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
    if node is None:
        return None
    shift_amount = ASTNode("NUMBER", str(shift), None, None)
    return ASTNode("OP", "+", node, shift_amount)

def stretchX(node, stretch):
    if node is None:
        return None
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
    if node is None:
        return None
    factor = ASTNode("NUMBER", str(stretch), None, None)
    return ASTNode("OP", "*", factor, node)