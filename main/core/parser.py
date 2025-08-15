import re

def tokenize(expression):
    '''Returns a two dimensional array of all characters in the expression and their associated token'''
    #Initialise variables and clean the expression'''
    tokens = []
    index = 0
    valid_characters = True
    expression = expression.replace(" ", "")
    expression = expression.replace("^", "**")

    # Regex patterns to look for in the expression
    patterns = {
        "NUMBER": re.compile(r"\d+(\.\d+)?"),
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
    '''Adds multiplication where the user would consider it to be implicit'''
    #Initialise variables
    new_tokens = []
    length = len(tokens)

    for index in range(length - 1):
        current_token = tokens[index][0]
        current_value = tokens[index][1]
        next_token = tokens[index + 1][0]

        new_tokens.append([current_token, current_value])

        # If two relevant tokens are next to each other, insert a new '*' operator token
        if (current_token in ["NUMBER", "NAME", "RIGHTPARENTHESIS"] and
            next_token in ["NAME", "FUNCTION", "LEFTPARENTHESIS"]):
            new_tokens.append(["OP", "*"])

    # Add the last token
    new_tokens.append(tokens[-1])

    return new_tokens

def validateTokens(tokens):
    '''Checks if the order of the tokens array is valid'''
    parenthesis_balance = 0
    prev_token = None
    prev_value = None
    variable_found = False
    variable = None

    for index in range(len(tokens)):
        token = tokens[index][0]
        value = tokens[index][1]

        # Only sets prev_token if one exists
        if index > 0:
            prev_token = tokens[index - 1][0]
            prev_value = tokens[index - 1][1]
        else:
            prev_token = None
            prev_value = None

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
                return False

        # Checking for double operators, only allows if the second is a negative
        if prev_token == "OP" and token == "OP" and value != "-":
            return False

        # Checking if a trigonometric function is followed by a parenthesis
        if token == "FUNCTION" and next_token != "LEFTPARENTHESIS":
            return False

        # Checks to see if there is more than one variable attempting to be created
        if token == "NAME":
            if not variable_found:
                variable = value
                variable_found = True
            elif value != variable:
                return False

    # Final check if the last token is an operator or if the parenthesis balance is incorrect
    if tokens[-1][0] == "OP" or parenthesis_balance != 0:
        return False

    return True

def parse(expression):
    '''Brings together the three subroutines involved in parsing the expression'''
    tokens = tokenize(expression)
    if tokens is None:
        return None

    tokens = insertImplicitMultiplication(tokens)
    if not validateTokens(tokens):
        return None

    return tokens
