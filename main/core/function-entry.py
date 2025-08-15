from core.parser import parseExpression
from core.ast import postfix, postfixToAST

class FunctionEntry:
    def __init__(self, user_input: str):
        self.user_input = user_input
        self.tokens = parseExpression(user_input)
        self.postfix_tokens = postfix(self.tokens)
        self.ast = postfixToAST(self.postfix_tokens)

    def output_function(self):
        return self.ast
