from core.ast import ASTNode, printAST

def reflectXAxis(node):
    """
    Reflects the function across the X-axis by multiplying the whole expression by -1
    """
    if node is None:
        return None
    print("")
    printAST(node)
    negative_one = ASTNode("NUMBER", "-1", None, None)
    newNode = ASTNode("OP", "*", negative_one, node)
    printAST(newNode)
    return newNode


def reflectYAxis(node):
    """
    Reflects the function across the Y-axis by multiplying variables by -1
    """
    if node is None:
        return None
    print("")
    printAST(node)
    if node.type == "NAME":
        negative_one = ASTNode("NUMBER", "-1", None, None)
        newNode = ASTNode("OP", "*", negative_one, node)
        printAST(newNode)
        return newNode
    else:
        # Recursively reflect left and right subtrees
        if node.left:
            node.left = reflectYAxis(node.left)
        if node.right:
            node.right = reflectYAxis(node.right)
        printAST(node)
        return node


def shiftX(node, shift):
    """
    Shifts the function along the X-axis by subtracting the shift value 
    """
    if node is None:
        return None
    print("")
    printAST(node)
    if node.type == "NAME":
        shift_amount = ASTNode("NUMBER", str(shift), None, None)
        newNode = ASTNode("OP", "-", node, shift_amount)
        printAST(newNode)
        return newNode
    else:
        if node.left:
            node.left = shiftX(node.left, shift)
        if node.right:
            node.right = shiftX(node.right, shift)
        printAST(node)
        return node


def shiftY(node, shift):
    """
    Shifts the function along the Y-axis by adding the shift value to the expression
    """
    if node is None:
        return None
    print("")
    printAST(node)
    shift_amount = ASTNode("NUMBER", str(shift), None, None)
    newNode = ASTNode("OP", "+", node, shift_amount)
    printAST(newNode)
    return newNode


def stretchX(node, stretch):
    """
    Stretches the function along the X-axis by dividing by the stretch
    """
    if node is None:
        return None
    print("")
    printAST(node)
    if node.type == "NAME":
        factor = ASTNode("NUMBER", str(stretch), None, None)
        newNode = ASTNode("OP", "/", node, factor)
        printAST(newNode)
        return newNode
    else:
        if node.left:
            node.left = stretchX(node.left, stretch)
        if node.right:
            node.right = stretchX(node.right, stretch)
        printAST(node)
        return node


def stretchY(node, stretch):
    """
    Stretches the function along the Y-axis by multiplying by the stretch
    """
    if node is None:
        return None
    print("")
    printAST(node)
    factor = ASTNode("NUMBER", str(stretch), None, None)
    newNode = ASTNode("OP", "*", factor, node)
    printAST(newNode)
    return newNode
