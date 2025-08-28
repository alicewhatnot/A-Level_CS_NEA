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
    '''Produces a postfix version of the token list'''

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
    '''Creates an AST from the postfix queue using the ASTNode class'''
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
    
def evaluateAST(node, x_value, variable, convert_degrees=False):
    """Recursively evaluates AST for a given x-value"""
    if node is None:
        return None

    if convert_degrees and node.type == "NAME" and node.value == variable:
        x_val = math.degrees(x_value)
    else:
        x_val = x_value

    if node.type == "NUMBER":
        return float(node.value)

    if node.type == "NAME" and node.value == variable:
        return x_val

    if node.type == "OP":
        left = evaluateAST(node.left, x_value, variable, convert_degrees)
        right = evaluateAST(node.right, x_value, variable, convert_degrees)

        if left is None or right is None:
            return None

        if node.value == "+":
            return left + right
        elif node.value == "-":
            return left - right
        elif node.value == "*":
            return left * right
        elif node.value == "/":
            try:
                return left / right  
            except: 
                return None
        elif node.value == "**":
            try:
                return left ** right
            except:
                return None

    if node.type == "FUNCTION":
        arg = evaluateAST(node.left, x_value, variable, convert_degrees = True)
        arg = math.radians(arg)
        if node.value == "sin":
            return math.sin(arg)
        elif node.value == "cos":
            return math.cos(arg)
        elif node.value == "tan":
            return math.tan(arg)

    return None


def copyAST(node):
    if node is None:
        return None
    return type(node)(
        node.type,
        node.value,
        copyAST(node.left),
        copyAST(node.right)
    )

def containsTrigFunction(node):
    """Returns True if AST contains sin, cos, or tan"""
    if node is None:
        return False
    if node.type == "FUNCTION" and node.value in ("sin", "cos", "tan"):
        return True
    return containsTrigFunction(node.left) or containsTrigFunction(node.right)
