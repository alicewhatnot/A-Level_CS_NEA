from core.queue import Queue
from core.stack import Stack

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

    return postfix_queue

def postfix_to_ast(postfix_queue):
    '''Creates an AST from the postfix queue using the ASTNode class'''
    node_stack = Stack(64)

    while not postfix_queue.is_empty():
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
    return node_stack.pop()