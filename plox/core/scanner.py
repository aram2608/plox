from .token import Token, TokenType

from string import ascii_letters


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
        self.line = 0
        self.numbers = "0123456789"
        self.alpha = ascii_letters + "_"
        self.keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }

    def scan(self):
        while not self.is_end():
            self.start = self.current
            char = self.advance()
            match char:
                case "\n":
                    self.line += 1
                case " ":
                    pass
                case "+":
                    self.add_token(TokenType.PLUS)
                case "-":
                    self.add_token(TokenType.MINUS)
                case "/":
                    self.add_token(TokenType.SLASH)
                case "*":
                    self.add_token(TokenType.STAR)
                case '"':
                    self.make_string()
                case _:
                    if self.is_digit(char):
                        self.make_number()
                    elif self.is_alpha(char):
                        self.make_identifier()
                    else:
                        raise LexingError("Unidentified token type.")

    def advance(self):
        char = self.source[self.current]
        self.current += 1
        return char

    def peek(self):
        if self.is_end():
            return None
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def is_end(self) -> bool:
        return self.current >= len(self.source)

    def add_token(self, _type, value=None):
        self.tokens.append(Token(_type, value))

    def make_string(self):
        while self.peek() != '"' and not self.is_end():
            if self.peek() == "\n":
                self.line += 1
                self.advance()
        if self.is_end():
            raise LexingError("Unterminated string")

        self.advance()

        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def make_number(self):
        while self.is_digit(self.peek()):
            self.advance()

        # We leap over the decimal
        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        # We collect the stubstring of the source code and add it as our token
        self.tokens.append(
            Token(TokenType.NUMBER, value=float(self.source[self.start : self.current]))
        )

    def make_identifier(self):
        while self.is_alpha_num(self.peek()):
            self.advance()

        text = self.source[self.start : self.current]

        if text in self.keywords:
            self.add_token(Token(self.keywords[text]))

    def is_alpha(self, char):
        if char == None:
            return False
        return char in self.alpha

    def is_digit(self, char):
        if char == None:
            return False
        return char in self.numbers

    def is_alpha_num(self, char):
        return self.is_alpha(char) or self.is_digit(char)
