from core.queue import Queue
from core.stack import Stack
import math

class ASTNode:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type
        self.value = value
        self.left = left
        self.right = right


def postfix(tokens):
    """
    Produces a postfix version of the token list
    """

    # Initialising variables and dictionaries
    postfix_queue = Queue(64)
    operator_stack = Stack(64)

    # BIDMAS order of operations
    precedence = {
        "+": 1, "-": 1, "*": 2, "/": 2, "**": 3
    }

    associativity = {
        "+": "L", "-": "L", "*": "L", "/": "L", "**": "R"
    }

    # Shunting yard algorithm for postfix production
    for index in range (len(tokens)):
        token = tokens[index][0]
        value = tokens[index][1]

        # Adds a number or variable straight to the queue
        if token == "NUMBER" or token == "NAME":
            postfix_queue.enqueue([token, value])

        # Adds function straight to the stack as it has highest precedence
        elif token == "FUNCTION":
            operator_stack.push([token, value])

        # Checking to see if the precedence of the item at the top of the stack is higher or lower than current
        elif token == "OP":
            while (not operator_stack.empty() and
                   operator_stack.top()[0] == "OP" and
                   (
                       (associativity[value] == "L" and precedence[value] <= precedence[operator_stack.top()[1]]) or
                       (associativity[value] == "R" and precedence[value] < precedence[operator_stack.top()[1]])
                   )):
                postfix_queue.enqueue(operator_stack.pop())
            operator_stack.push([token, value])

        # Add left parenthesis to the stack waiting for the other of the pair
        elif token == "LEFTPARENTHESIS":
            operator_stack.push([token, value])

        # Right parenthesis
        elif token == "RIGHTPARENTHESIS":
            while not operator_stack.empty() and operator_stack.top()[0] != "LEFTPARENTHESIS":
                postfix_queue.enqueue(operator_stack.pop())
            # Remove the left parenthesis
            if not operator_stack.empty() and operator_stack.top()[0] == "LEFTPARENTHESIS":
                operator_stack.pop()
            # If function is on top, pop it to queue
            if not operator_stack.empty() and operator_stack.top()[0] == "FUNCTION":
                postfix_queue.enqueue(operator_stack.pop())

    # Lastly pop any remaining operators and add to the queue
    while not operator_stack.empty():
        postfix_queue.enqueue(operator_stack.pop())

    print ("Converted To Postfix")
    return postfix_queue

def postfixToAST(postfix_queue):
    """
    Creates an AST from the postfix queue using the ASTNode class
    """
    node_stack = Stack(64)

    while not postfix_queue.isEmpty():
        token, value = postfix_queue.dequeue()

        # These will be leaves and so do not have children
        if token == "NUMBER" or token == "NAME":
            node = ASTNode(token, value, None, None)
            node_stack.push(node)

        # These will only have a left child as the parameter of the function
        elif token == "FUNCTION":
            operand = node_stack.pop()
            node = ASTNode(token, value, operand, None)
            node_stack.push(node)

        # These will use both children as are operators
        elif token == "OP":
            right = node_stack.pop()
            left = node_stack.pop()
            node = ASTNode(token, value, left, right)
            node_stack.push(node)

    # The remaining node is the root of the AST
    print ("AST Created")
    return node_stack.pop()

def evaluateAST(node, variable_value, variable, use_degrees=False, inside_trig=False ,needs_converting=True):
    """
    Recursively evaluates AST for a given value along the axis
    """
    if node is None:
        return None

    # Return the number 
    if node.type == "NUMBER":
        val = float(node.value)
        # Converts to radians if is degrees and is not mul / div by the variable
        if use_degrees and inside_trig and needs_converting:
            return math.radians(val)  
        return val

    # Return the value of the variable at that point along the axis
    if node.type == "NAME" and node.value == variable:
        return float(variable_value)

    # Operators
    if node.type == "OP":
        #Determine if children needs converting
        left_needs_converting = needs_converting
        right_needs_converting = needs_converting

        # Dont convert children if they're mul / div the variable
        if inside_trig and node.value in ("*", "/"):
            if node.left.type == "NUMBER" and node.right.type == "NAME":
                left_needs_converting = False
            elif node.left.type == "NAME" and node.right.type == "NUMBER":
                right_needs_converting = False

        # Fetch value of the left and right nodes
        left = evaluateAST(node.left, variable_value, variable, use_degrees, inside_trig, left_needs_converting)
        right = evaluateAST(node.right, variable_value, variable, use_degrees, inside_trig, right_needs_converting)

        if left is None or right is None:
            return None

        try:
            # Perform the operators
            if node.value == "+": 
                return left + right
            elif node.value == "-": 
                return left - right
            elif node.value == "*": 
                return left * right
            elif node.value == "/": 
                return left / right
            elif node.value == "**": 
                return left ** right
        except Exception:
            return None

    # Evaluate the functions
    if node.type == "FUNCTION":
        # When evaluating inside trig, set inside_trig=True
        argument = evaluateAST(node.left, variable_value, variable, use_degrees, inside_trig=True)
        if argument is None:
            return None
        if node.value == "sin": 
            return math.sin(argument)
        elif node.value == "cos": 
            return math.cos(argument)
        elif node.value == "tan": 
            return math.tan(argument)
        elif node.value == "ln":
            return math.log(argument)

    return None

def copyAST(node):
    """
    Produces a copy of the AST with the supplied root node
    """
    if node is None:
        return None
    return type(node)(
        node.type,
        node.value,
        copyAST(node.left),
        copyAST(node.right)
    )

def containsTrigFunction(node):
    """
    Returns True if AST contains sin, cos, or tan
    """
    if node is None:
        return False
    if node.type == "FUNCTION" and node.value in ("sin", "cos", "tan"):
        return True
    return containsTrigFunction(node.left) or containsTrigFunction(node.right)

def simplifyAST(node):
    """
    Recursively simplifies an AST.
    Designed to reduce excess nodes created from differentiation logic
    """

    if node is None:
        return None

    # Simplify children first (post-order traversal)
    node.left = simplifyAST(node.left)
    node.right = simplifyAST(node.right)

    # Leaf nodes cannot be simplified
    if node.type in ("NUMBER", "NAME"):
        return node

    # Simplifying logic for operators
    if node.type == "OP":
        op = node.value
        left = node.left
        right = node.right

        # If the operator is calculable, e.g. 5*3 then return a number node of 15
        # Reduces 3 nodes - OP, Left and Right to 1 node
        if left and right and left.type == "NUMBER" and right.type == "NUMBER":
            try:
                a = float(left.value)
                b = float(right.value)
                if op == "+": return ASTNode("NUMBER", str(a + b))
                if op == "-": return ASTNode("NUMBER", str(a - b))
                if op == "*": return ASTNode("NUMBER", str(a * b))
                if op == "/": return ASTNode("NUMBER", str(a / b))
                if op == "**": return ASTNode("NUMBER", str(a ** b))
            
            except Exception:
                pass

        # Algebraic simplification, e.g. x*1 = x
        # Reduces 3 nodes - OP, Left and Right to 1 node

        # x + 0
        if op == "+":
            if left.type == "NUMBER" and float(left.value) == 0:
                return right
            if right.type == "NUMBER" and float(right.value) == 0:
                return left

        # x - 0
        if op == "-":
            if right.type == "NUMBER" and float(right.value) == 0:
                return left

        if op == "*":
            # x * 0
            if (left.type == "NUMBER" and float(left.value) == 0) or (right.type == "NUMBER" and float(right.value) == 0):
                return ASTNode("NUMBER", "0")
            
            # x * 1
            if left.type == "NUMBER" and float(left.value) == 1:
                return right
            if right.type == "NUMBER" and float(right.value) == 1:
                return left

        if op == "/":
            # 0 / x
            if left.type == "NUMBER" and float(left.value) == 0:
                return ASTNode("NUMBER", "0")
            
            # x / 1
            if right.type == "NUMBER" and float(right.value) == 1:
                return left

        if op == "**":
            if right.type == "NUMBER":
                # x ** 1
                if float(right.value) == 1:
                    return left
                
                # x ** 0
                if float(right.value) == 0:
                    return ASTNode("NUMBER", "1")

        return node

    # Evaluate functions if possible
    if node.type == "FUNCTION":
        arg = node.left

        if arg and arg.type == "NUMBER":
            try:
                val = float(arg.value)
                if node.value == "sin":
                    return ASTNode("NUMBER", str(math.sin(val)))
                if node.value == "cos":
                    return ASTNode("NUMBER", str(math.cos(val)))
                if node.value == "tan":
                    return ASTNode("NUMBER", str(math.tan(val)))
            except Exception:
                pass

        # ln(1) = 0
        if node.value == "ln" and arg.type == "NUMBER" and float(arg.value) == 1:
            return ASTNode("NUMBER", "0")

        return node

    return node
