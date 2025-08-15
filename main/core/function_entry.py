from core.parser import parse
from core.ast import postfix, postfixToAST

class FunctionEntry:
    def __init__(self, user_input: str):
        self.user_input = user_input
        self.tokens = []
        self.ast = None

    def parseFunction(self):
        '''Tokenise the user input string'''
        self.tokens = parse(self.user_input)
    
    def functionAST(self):
        '''Convert tokens to postfix then build the AST'''
        if not self.tokens:
            raise ValueError("Token list is empty - function must be parsed")
        self.tokens = postfix(self.tokens)
        self.ast = postfixToAST(self.tokens)
    
    def outputFunction(self):
        '''Return the AST'''
        if not self.ast:
            raise ValueError("AST must be created first")
        return self.ast
