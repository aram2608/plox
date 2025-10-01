from enum import Enum, auto


class TokenType(Enum):
    """
    A simple enum class to store the TokenTypes use in Lox.
    auto() is used to auto calculate the numeric value corresponding to the enum.
    """

    # Single-character tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()
    COLON = auto()
    QUESTION = auto()
    MOD = auto()

    # One or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    MINUS_MINUS = auto()
    PLUS_PLUS = auto()

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()
    EOF = auto()


class Token:
    """The Token class to present Lox Tokens."""

    def __init__(self, _type: TokenType, lexeme, literal=None, line=0):
        """
        We initalize each token with its given type, the lexeme/string representation
        a literal value (ie 1, 5, "hello world"), and the line number for error
        handling purposes.
        """
        self._type = _type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self) -> str:
        """A representation method to print out Tokens to the stream."""
        return f"Token: {self._type}, {self.lexeme} {self.literal}"
