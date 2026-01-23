from core.ast import ASTNode

def differentiate(node):
    """
    Recursivly differentiates a node and its relevant children
    """
    if node is None:
        return None

    # Returns the derivative of a number which is 0
    elif node.type == "NUMBER":
        return ASTNode("NUMBER", "0", None, None)

    # Returns the derivative of a single variable which is 1
    elif node.type == "NAME":
        return ASTNode("NUMBER", "1", None, None)

    elif node.type == "OP":
        operator = node.value

        # Differentiates left and right of the operator, using the rule d/dx[f ± g] = f' ± g'
        if operator == "+" or operator == "-":
            left_differentiated = differentiate(node.left)
            right_differentiated = differentiate(node.right)
            return ASTNode("OP", operator, left_differentiated, right_differentiated)

        elif operator == "*":
            # Implements the product rule (d/dx[fg] = f'g + fg') to differentiate left * right
            left = node.left
            right = node.right
            left_differentiated = differentiate(left)
            right_differentiated = differentiate(right)
            term1 = ASTNode("OP", "*", left_differentiated, right)
            term2 = ASTNode("OP", "*", right_differentiated, left)
            return ASTNode("OP", "+", term1, term2)

        elif operator == "**":
            # Implements the power rule (d/dx[u^n] = n * u^(n-1) * u') to differentiate a base to a numerical exponent
            base = node.left
            exponent = node.right
            if exponent.type == "NUMBER":
                try:
                    new_exponent_value = str(int(exponent.value) - 1)
                except ValueError:
                    return None
                new_exponent = ASTNode("NUMBER", new_exponent_value, None, None)
                base_differentiated = differentiate(base)
                value_to_power = ASTNode("OP", "**", base, new_exponent)
                coefficient = ASTNode("NUMBER", exponent.value, None, None)
                product = ASTNode("OP", "*", coefficient, value_to_power)
                return ASTNode("OP", "*", product, base_differentiated)
            
            elif exponent.type == "NAME" and base.type == "NUMBER":
                # Implements the rule d/dx[a^x] = a^x * ln(a) to differentiate a numerical base to a variable exponent
                # logarithms are not implemented in the parser as they are out of the scope of the project however implementation for this rule alone is simple as is not user facing
                ln_base = ASTNode("FUNCTION", "ln", ASTNode("NUMBER", base.value, None, None), None)
                value_to_power = ASTNode("OP", "**", ASTNode("NUMBER", base.value, None, None), exponent)
                return ASTNode("OP", "*", value_to_power, ln_base)
            
            else:
                return None

    # Differentiates a function using the chain rule (d/dx[f(g)] = f'g')
    elif node.type == "FUNCTION":
        # if argument is a constant number, derivative is 0
        # implemented for further derivatives of exponential functions
        if node.left.type == "NUMBER":
            return ASTNode("NUMBER", "0", None, None)
    
        function = node.value
        argument = node.left
        argument_differentiated = differentiate(argument)

        # Uses the chain rule for the cases of sin and cos 
        if function == "sin":
            cos_node = ASTNode("FUNCTION", "cos", argument, None)
            return ASTNode("OP", "*", cos_node, argument_differentiated)
        elif function == "cos":
            sin_node = ASTNode("FUNCTION", "sin", argument, None)
            negative = ASTNode("NUMBER", "-1", None, None)
            negative_sin = ASTNode("OP", "*", sin_node, negative)
            return ASTNode("OP", "*", negative_sin, argument_differentiated)
        
        # Splits tan into sin/cos to differentiate
        elif function == "tan":
            cos_node = ASTNode("FUNCTION", "cos", argument, None)
            cos_squared = ASTNode("OP", "**", cos_node, ASTNode("NUMBER", "2", None, None))
            reciprocal = ASTNode("OP", "/", ASTNode("NUMBER", "1", None, None), cos_squared)
            return ASTNode("OP", "*", reciprocal, argument_differentiated)

    # Safety catch if the node cannot be differentiated
    return None