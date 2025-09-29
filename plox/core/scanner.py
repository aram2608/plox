from .token import Token, TokenType

class LexingError(Exception):
    def __init__(self, message, value=None):
        self.message = message
        self.value = value
        super().__init__(self.message)

class Scanner:
    def __init__(self, source):
        self.source = source
        self.current = 0
        self.start = None
        self.tokens = []
        self. line = 0
    
    def scan(self):
        while not self.is_end():
            self.start = self.current
            char = self.advance()
            if char == "+":
                self.add_token(TokenType.PLUS)
            elif char == "-":
                self.add_token(TokenType.MINUS)
            elif char in "0123456789":
                self.make_number()

    def advance(self):
        char = self.source[self.current]
        self.current += 1
        return char
    
    def peek(self):
        if self.is_end():
            return None
        return self.source[self.current]
    
    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def is_end(self):
        return self.current >= len(self.source)
    
    def add_token(self, _type, value=None):
        self.tokens.append(Token(_type, value))

    def make_number(self):
        while self.is_digit(self.peek()):
            self.advance()

        # We leap over the decimal
        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance();

        # We collect the stubstring of the source code and add it as our token
        self.tokens.append(Token(TokenType.NUMBER, value=float(self.source[self.start: self.current])))

    def is_digit(self, char):
        if char == None:
            return False
        return char in "0123456789"
