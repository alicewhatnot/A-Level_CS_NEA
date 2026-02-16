import re
import math
import time

def tokenize(expression):
    """
    Returns a two dimensional array of all characters in the expression and their associated token
    """
    #Initialise variables and clean the expression"""
    
    tokens = []
    index = 0
    valid_characters = True
    expression = expression.replace(" ", "")
    expression = expression.replace("^", "**")

    # Regex patterns to look for in the expression
    patterns = {
        "NUMBER": re.compile(r"(\d+(\.\d*)?|\.\d+)"),
        "FUNCTION": re.compile(r"(sin|cos|tan)"),
        "NAME": re.compile(r"[a-zA-Z]"),
        "OP": re.compile(r"\*\*|[+\-*/]"),
        "LEFTPARENTHESIS": re.compile(r"\("),
        "RIGHTPARENTHESIS": re.compile(r"\)")
    }
    
    # Checking every character in the expression while there are still no invalid found 
    while index < len(expression) and valid_characters:
        matched = False

        for item in patterns.items():
            token = item[0]
            pattern = item[1]

            # If a match is found then the relevant number of characters are added to tokens[]
            match = pattern.match(expression, index)
            if match:
                characters = match.group(0)

                # Special handling for single minus
                if token == "OP" and characters == "-":
                    # Unary minus if at start or after another operator or after '('
                    if len(tokens) == 0 or tokens[-1][0] in ("OP", "LEFTPARENTHESIS"):
                        # Look ahead for a number
                        num_match = patterns["NUMBER"].match(expression, index + 1)
                        if num_match:
                            num_str = num_match.group(0)
                            # Insert tokens for (0 - num)
                            tokens.append(("LEFTPARENTHESIS", "("))
                            tokens.append(("NUMBER", "0"))
                            tokens.append(("OP", "-"))
                            tokens.append(("NUMBER", num_str))
                            tokens.append(("RIGHTPARENTHESIS", ")"))

                            index += 1 + len(num_str)
                            matched = True
                            break
                        
                        # Look ahead for a variable
                        name_match = patterns["NAME"].match(expression, index + 1)
                        if name_match:
                            var_str = name_match.group(0)
                            # Insert tokens for (0 - var)
                            tokens.append(("LEFTPARENTHESIS", "("))
                            tokens.append(("NUMBER", "0"))
                            tokens.append(("OP", "-"))
                            tokens.append(("NAME", var_str))
                            tokens.append(("RIGHTPARENTHESIS", ")"))

                            index += 1 + len(var_str)
                            matched = True
                            break

                        # Look ahead for a function (like -sin(...))
                        func_match = patterns["FUNCTION"].match(expression, index + 1)
                        if func_match:
                            func_str = func_match.group(0)
                            tokens.append(("LEFTPARENTHESIS", "("))
                            tokens.append(("NUMBER", "0"))
                            tokens.append(("OP", "-"))
                            tokens.append(("FUNCTION", func_str))
                            index += 1 + len(func_str)
                            matched = True
                            break

                        # Look ahead for a parenthesis (like -(x+1))
                        paren_match = patterns["LEFTPARENTHESIS"].match(expression, index + 1)
                        if paren_match:
                            tokens.append(("LEFTPARENTHESIS", "("))
                            tokens.append(("NUMBER", "0"))
                            tokens.append(("OP", "-"))
                            index += 1
                            matched = True
                            break

                # Normal case
                tokens.append((token, characters))
                index += len(characters)
                matched = True
                break

        if not matched:
            valid_characters = False
    
    # Only returns token list if all characters are valid
    if valid_characters:
        return tokens
    else:
        return None
    
def insertImplicitMultiplication(tokens):
    """
    Adds multiplication where the user would consider it to be implicit
    """
    new_tokens = []
    length = len(tokens)

    for index in range(length - 1):
        current_token, current_value = tokens[index]
        next_token, next_value = tokens[index + 1]

        new_tokens.append((current_token, current_value))

        # Insert '*' if implicit multiplication detected
        if (current_token in ["NUMBER", "NAME", "RIGHTPARENTHESIS"] and
            next_token in ["NAME", "FUNCTION", "LEFTPARENTHESIS", "NUMBER"]):
            new_tokens.append(("OP", "*"))

    # Add last token
    new_tokens.append(tokens[-1])

    return new_tokens

def validateTokens(tokens):
    """
    Checks if the order of the tokens array is valid
    """
    parenthesis_balance = 0
    prev_token = None
    variable_found = False
    variable = None

    for index in range(len(tokens)):
        token = tokens[index][0]
        value = tokens[index][1]

        # Only sets prev_token if one exists
        if index > 0:
            prev_token = tokens[index - 1][0]
        else:
            prev_token = None

        # Only sets next_token if one exists
        if index < len(tokens) - 1:
            next_token = tokens[index + 1][0]
        else:
            next_token = None

        # Checking for parenthesis balance
        if token == "LEFTPARENTHESIS":
            parenthesis_balance += 1
        elif token == "RIGHTPARENTHESIS":
            parenthesis_balance -= 1
            if parenthesis_balance < 0:
                return False, variable

        # Checking for double operators, only allows if the second is a negative
        if prev_token == "OP" and token == "OP" and value != "-":
            return False, variable

        # Checking if a trigonometric function is followed by a parenthesis
        if token == "FUNCTION" and next_token != "LEFTPARENTHESIS":
            return False, variable

        # Checks to see if there is more than one variable attempting to be created
        if token == "NAME":
            if not variable_found:
                variable = value
                variable_found = True
            elif value != variable:
                return False, variable

        # ** must have a valid base
        if token == "OP" and value == "**":
            if prev_token not in ["NUMBER", "NAME", "RIGHTPARENTHESIS"]:
                return False, variable
            if next_token not in ["NUMBER", "NAME", "LEFTPARENTHESIS"]:
                return False, variable
            
             # NAME ** NAME
            prev_value = tokens[index - 1][1] if index > 0 else None
            next_value = tokens[index + 1][1] if index < len(tokens) - 1 else None
            if prev_token == "NAME" and next_token == "NAME" and prev_value == next_value:
                return False, variable
        
        # Checking for ()
        if token == "LEFTPARENTHESIS" and next_token == "RIGHTPARENTHESIS":
            return False, variable
        
    # Final check if the last token is an operator or if the parenthesis balance is incorrect
    if tokens[-1][0] == "OP" or parenthesis_balance != 0:
        return False, variable

    return True, variable

def convertXShiftsToRadians(tokens, x_variable="x"):
    """
    Converts any numeric constants added/subtracted to x into radians.
    """
    new_tokens = []
    i = 0
    while i < len(tokens):
        token_type, token_value = tokens[i]

        # Look for x followed by + or - then a NUMBER
        if token_type == "NAME" and token_value == x_variable:
            if i + 2 < len(tokens):
                next_token_type, next_token_value = tokens[i + 1]
                next2_token_type, next2_token_value = tokens[i + 2]

                if next_token_type == "OP" and next_token_value in ("+", "-") and next2_token_type == "NUMBER":
                    # Keep x
                    new_tokens.append((token_type, token_value))
                    # Keep + or -
                    new_tokens.append((next_token_type, next_token_value))
                    # Convert number to radians
                    rad_val = str(float(next2_token_value) * math.pi / 180)
                    new_tokens.append(("NUMBER", rad_val))
                    # Skip the next two tokens since we already processed them
                    i += 3
                    continue

        # Normal case, just copy the token
        new_tokens.append((token_type, token_value))
        i += 1

    return new_tokens

def parse(expression):
    """
    Brings together the three subroutines involved in parsing the expression
    """
    tokens = tokenize(expression)
    print ("Expression Tokenized")

    if not tokens:
        print ("Invalid Tokens")
        return [], None

    tokens = insertImplicitMultiplication(tokens)
    print ("Multiplication Inserted")

    valid, variable = validateTokens(tokens)
    if not valid:
        print ("Invalid Tokens")
        return [], None
    print ("Returning Valid Tokens")

    return tokens, variable

import math
import time

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

def evaluateAST(node, variable_value, variable):
    """
    Recursively evaluates an AST for a given variable value.
    """

    if node is None:
        return None

    # Numbers
    if node.type == "NUMBER":
        return float(node.value)

    # Variable
    if node.type == "NAME":
        if node.value == variable:
            return float(variable_value)
        return None  # unknown variable

    # Operators
    if node.type == "OP":
        # Recursively evaluate left and right
        left_val = evaluateAST(node.left, variable_value, variable)
        right_val = evaluateAST(node.right, variable_value, variable)

        if left_val is None or right_val is None:
            return None

        try:
            if node.value == "+":
                return left_val + right_val
            if node.value == "-":
                return left_val - right_val
            if node.value == "*":
                return left_val * right_val
            if node.value == "/":
                return left_val / right_val
            if node.value == "**":
                return left_val ** right_val
        except Exception:
            return None

    # Functions
    if node.type == "FUNCTION":
        arg_val = evaluateAST(node.left, variable_value, variable)
        if arg_val is None:
            return None

        try:
            if node.value == "sin":
                return math.sin(arg_val)
            if node.value == "cos":
                return math.cos(arg_val)
            if node.value == "tan":
                return math.tan(arg_val)
            if node.value == "ln":
                return math.log(arg_val)
        except Exception:
            return None

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

def isNumber(node, value=None):
    """
    Returns True if node is a number, and if value is supplied, checks if it matches
    Used in simplification logic to avoid fatal crashes when checking node values
    """
    if node is None:
        return False
    if node.type != "NUMBER":
        return False
    if value is not None:
        try:
            return float(node.value) == float(value)
        except:
            return False
    return True

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

        # Constant folding
        if isNumber(left) and isNumber(right):
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

        # x + 0
        if op == "+":
            if isNumber(left, 0):
                return right
            if isNumber(right, 0):
                return left

        # x - 0, 0 - x
        if op == "-":
            if isNumber(right, 0):
                return left
            if isNumber(left, 0):
                return ASTNode("OP", "*", ASTNode("NUMBER", "-1"), right)

        # Multiplication rules
        if op == "*":
            if isNumber(left, 0) or isNumber(right, 0):
                return ASTNode("NUMBER", "0")
            if isNumber(left, 1):
                return right
            if isNumber(right, 1):
                return left
            if isNumber(right, -1):
                return ASTNode("OP", "*", ASTNode("NUMBER", "-1"), left)

        # Division rules
        if op == "/":
            if isNumber(left, 0):
                return ASTNode("NUMBER", "0")
            if isNumber(right, 1):
                return left

        # Power rules
        if op == "**":
            if isNumber(right, 1):
                return left
            if isNumber(right, 0):
                return ASTNode("NUMBER", "1")

        # Rewrite 1 / u^n → u^-n
        if op == "/" and isNumber(left, 1):
            if right is not None and right.type == "OP" and right.value == "**":
                base = right.left
                exp = right.right
                if isNumber(exp):
                    return ASTNode("OP", "**", base, ASTNode("NUMBER", str(-float(exp.value))))

        # u^a * u^b = u^(a+b)
        if op == "*":
            if (
                left is not None and right is not None and
                left.type == "OP" and right.type == "OP" and
                left.value == "**" and right.value == "**" and
                left.left == right.left and
                isNumber(left.right) and isNumber(right.right)
            ):
                new_exp = float(left.right.value) + float(right.right.value)
                return ASTNode("OP", "**", left.left, ASTNode("NUMBER", str(new_exp)))

        # (u^a)^b = u^(a*b)
        if op == "**":
            if (
                left is not None and
                left.type == "OP" and left.value == "**" and
                isNumber(left.right) and isNumber(right)
            ):
                new_exp = float(left.right.value) * float(right.value)
                return ASTNode("OP", "**", left.left, ASTNode("NUMBER", str(new_exp)))

        return node

    # Function simplification
    if node.type == "FUNCTION":
        arg = node.left

        if isNumber(arg):
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

        if node.value == "ln" and isNumber(arg, 1):
            return ASTNode("NUMBER", "0")

        return node

    return node
    
def simplifyTrigPhase(node):
    """
    Simplifies sin((x ± c)/k) into sin(x/k ± c/k) form.
    """
    if node is None:
        return None

    # Recursively simplify children first
    node.left = simplifyTrigPhase(node.left)
    node.right = simplifyTrigPhase(node.right)

    # Only look inside trig functions
    if node.type == "FUNCTION" and node.value in ("sin", "cos", "tan"):
        arg = node.left

        # Check if argument is a division
        if arg.type == "OP" and arg.value == "/":
            numerator = arg.left
            denominator = arg.right

            # Only handle addition or subtraction in numerator
            if numerator.type == "OP" and numerator.value in ("+", "-") and denominator.type == "NUMBER":
                left = numerator.left
                right = numerator.right

                # Determine which is variable and which is number
                if left.type == "NAME" and right.type == "NUMBER":
                    new_left = ASTNode("OP", "/", left, copyAST(denominator))
                    new_right = ASTNode("NUMBER", str(float(right.value)/float(denominator.value)))
                    new_arg = ASTNode("OP", numerator.value, new_left, new_right)
                    node.left = new_arg
                    return node

                if left.type == "NUMBER" and right.type == "NAME":
                    new_left = ASTNode("OP", "/", right, copyAST(denominator))
                    new_right = ASTNode("NUMBER", str(float(left.value)/float(denominator.value)))
                    # Flip operator if number is on the left
                    op = "+" if numerator.value == "+" else "-"
                    new_arg = ASTNode("OP", op, new_left, new_right)
                    node.left = new_arg
                    return node

    return node

# Debug subroutine used to output the entire tree
def printAST(node, depth=0):
    if node is None:
        return
    print("  " * depth + f"{node.type}: {node.value}")
    printAST(node.left, depth + 1)
    printAST(node.right, depth + 1)

class Queue:
    def __init__(self, max_size):
        # Create fixed-size array for queue items
        self.items = [None] * max_size

        # Index of the front of the queue
        self.front = 0

        # Index of the rear of the queue
        self.rear = -1

        # Current number of items in the queue
        self.size = 0

        # Maximum size of the queue
        self.max_size = max_size

    def enqueue(self, value):
        # Adds an item to the rear of the queue

        if self.isFull():
            print("Queue Overflow")
            return

        self.rear = (self.rear + 1) % self.max_size
        self.items[self.rear] = value
        self.size += 1

    def dequeue(self):
        # Removes and returns the item at the front of the queue

        if self.isEmpty():
            return None

        item = self.items[self.front]
        self.items[self.front] = None

        self.front = (self.front + 1) % self.max_size
        self.size -= 1

        return item

    def isEmpty(self):
        # Returns True if the queue is empty
        return self.size == 0

    def isFull(self):
        # Returns True if the queue is full
        return self.size == self.max_size

    def clear(self):
        # Removes all items from the queue

        while not self.isEmpty():
            self.dequeue()

class Stack:
    def __init__(self, max_size):
        # Create fixed-size array for stack items
        self.items = [None] * max_size

        # Index of the next free position (top of stack)
        self.top_index = 0

        # Maximum size of the stack
        self.max_size = max_size

    def push(self, value):
        # Adds a value to the top of the stack

        if self.top_index == self.max_size:
            print("Stack Overflow")
            return

        self.items[self.top_index] = value
        self.top_index += 1

    def pop(self):
        # Removes and returns the top value from the stack

        if self.top_index == 0:
            print("Stack Underflow")
            return None

        self.top_index -= 1
        value = self.items[self.top_index]
        self.items[self.top_index] = None

        return value

    def top(self):
        # Returns the top value without removing it

        if self.top_index == 0:
            return None

        return self.items[self.top_index - 1]

    def empty(self):
        # Returns True if the stack is empty
        return self.top_index == 0

    def size(self):
        # Returns the number of items in the stack
        return self.top_index

expression = "a+3b"
tokens, variable = parse(expression)
postfix_queue = postfix(tokens)
ast = postfixToAST(postfix_queue)
printAST(ast)