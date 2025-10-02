from enum import Enum, auto
from typing import Any


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

    def __init__(
        self,
        _type: TokenType,
        lexeme: str,
        literal: float | str | None = None,
        line: int | None = None,
    ):
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
        if not self.lexeme:
            return f"Token: {self._type}, {self.literal}"
        return f"Token: {self._type}, {self.lexeme}, {self.literal}"

    def __eq__(self, other):
        """
        This method is the == operator overload for the Token class.
        It is important that we define an overloaded equality operator as it
        will make our life a lot easier when writing unit tests or any kind of
        logical code where we have to compared two Tokens.
        """
        # We first check if the other object is a Token
        if isinstance(other, Token):
            # If our check passes we compare all member variables for equality
            return (
                self._type == other._type
                and self.lexeme == other.lexeme
                and self.literal == self.literal
            )
        # If our check fails then there is no way the other object could be equal
        return False

    def __ne__(self, other):
        """
        This method is the != operator overload for the Token class.
        It is important that we define an overloaded inequality operator as it
        will make our life a lot easier when writing unit tests or any kind of
        logical code where we have to compared two Tokens.
        """
        # We first check if the other value is a token
        if isinstance(other, Token):
            # If so we make sure that all the underlying member variables are not
            # equal
            return (
                self._type != self.lexeme
                and self.lexeme != other.lexeme
                and self.literal != other.literal
            )
        # If our check fails then the two objects are obviously unequal
        return True
