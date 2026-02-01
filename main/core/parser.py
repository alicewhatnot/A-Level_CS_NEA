import re
import math

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
        tok_type, tok_val = tokens[i]

        # Look for x followed by + or - then a NUMBER
        if tok_type == "NAME" and tok_val == x_variable:
            if i + 2 < len(tokens):
                next_tok_type, next_tok_val = tokens[i + 1]
                next2_tok_type, next2_tok_val = tokens[i + 2]

                if next_tok_type == "OP" and next_tok_val in ("+", "-") and next2_tok_type == "NUMBER":
                    # Keep x
                    new_tokens.append((tok_type, tok_val))
                    # Keep + or -
                    new_tokens.append((next_tok_type, next_tok_val))
                    # Convert number to radians
                    rad_val = str(float(next2_tok_val) * math.pi / 180)
                    new_tokens.append(("NUMBER", rad_val))
                    # Skip the next two tokens since we already processed them
                    i += 3
                    continue

        # Normal case, just copy the token
        new_tokens.append((tok_type, tok_val))
        i += 1

    return new_tokens

def parse(expression, convert):
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
    
    if convert: 
        tokens = convertXShiftsToRadians(tokens)

    print ("Returning Valid Tokens")
    
    for token in tokens:
        print (token)

    return tokens, variable
