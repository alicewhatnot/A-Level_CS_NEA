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
    
def insert_implicit_multiplication(tokens):
    pass

def validate_tokens(tokens):
    pass

def parse_expression(expression):
    pass
