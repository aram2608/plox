from __future__ import annotations
from typing import List

from ..ast.expr import Unary, Binary, Literal, Expr
from .token import Token, TokenType


class ParserError(Exception):
    """A custom class for handling errors at parse time."""

    def __init__(self, token: TokenType, message: str):
        """
        To initialize our error class, we pass in the token of interest and an
        error message.
        """
        self.token = token
        self.message = message
        super().__init__(f"[Token {token}] Error: {message}")

    def __str__(self):
        RED = "\033[91m"
        RESET = "\033[0m"
        return f"{RED}[Token {self.token}] Error: {self.message}{RESET}"


class Parser:
    def __init__(self, tokens: List[Token]):
        """
        To initialize our parser class we only need to pass in a list of tokens.
        """
        self.tokens = tokens
        self.current = 0

    def parse(self) -> List[Expr]:
        """
        This function is the main logic for creating our abstract syntax tree.
        """
        # We initialize an empty list for our expressions
        exprs = []
        # While we have not reached the end of the list of tokens, we append
        # the parsed syntax tree to our list
        while not self.is_end():
            exprs.append(self.expression())

        # After parsing we return our list
        return exprs

    def expression(self) -> Expr:
        """Main method used to parse expressions."""
        return self.equality()

    def equality(self) -> Expr:
        """
        This function handles the parsing of equality operations.
        Example:
            1 == 1 or 1 != 4
        """
        # We first extract the left hand expression
        expr: Expr = self.comparison()

        # As long as we match a != or ==, we continuously extract the operator
        # Token and right hand expression before creating a binary expression
        # node, this ensures nested expressions are valid 1 == 1 == 4
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator: Token = self.previous()
            right: Expr = self.term()
            expr: Binary = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        """
        This function handles the parsing of comaprisons operators.
        Example:
            1 >= 4 or 1 > 4
        """
        # We extract the left hand expression
        expr: Expr = self.term()

        # While we match any comparison operators, we parse the operator Token
        # and right hand expression.
        while self.match(
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
        ):
            operator: Token = self.previous()
            right: Expr = self.term()
            expr: Binary = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        """
        Method to handle binary operations involding + and - operators.
        These operators have higher precedence than comparisons so this method is defined
        further beloew in our recursive descent parser.
        """
        # We create the left most expression from the factor
        expr: Expr = self.factor()

        # If we match any of the lower precedence arithmetic Tokens
        while self.match(TokenType.PLUS, TokenType.MINUS):
            # We continously add to the Binary node
            operator: Token = self.previous()
            right: Expr = self.unary()
            expr: Binary = Binary(expr, operator, right)

        # We then return the expression
        return expr

    def factor(self) -> Expr:
        """
        Method to handle binary operations involving *, /, and % operators.
        These operators have a higher precedence than simple addition and subtraction
        so we define this further down our recursive descent parser.
        """
        # We create the left most expression from the unary method
        expr: Expr = self.unary()

        # If we match any of the higher precedence arithmetic Tokens
        while self.match(TokenType.SLASH, TokenType.STAR, TokenType.MOD):
            # We continously add to the Binary node
            operator: Token = self.previous()
            right: Expr = self.unary()
            expr: Binary = Binary(expr, operator, right)

        # We then return the expression
        return expr

    def unary(self) -> Expr:
        """
        Method to handle parsing of unary operations involding !, -, and the increment
        and decrement operators.
        These operators have the highest precendence so we define this method at the
        bottom of our recursive descent parser, just ahead of the primitive types.
        """
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator: Token = self.previous()
            right: Unary = self.unary()
            return Unary(operator, right)
        # elif self.match(TokenType.MINUS_MINUS):
        #     # TODO: Add prefix decrement
        #     ...
        # elif self.match(TokenType.PLUS_PLUS):
        #     # TODO: Add prefix increment
        #     ...
        return self.primary()

    def primary(self) -> Literal:
        """
        Method to handle parsing of primitive types in Lox. These are the most basic components
        in any Lox script.
        """
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        # if self.match(TokenType.SUPER):
        #     keyword: Token = self.previous()
        #     self.consume(TokenType.DOT, "Expected '.' after super")
        #     method: Token = self.consume(
        #         TokenType.IDENTIFIER, "Expected superclass method name"
        #     )
        #     # TODO: Add super
        #     ...

        # if self.match(TokenType.THIS):
        #     # TODO: Add this
        #     ...

        # if self.match(TokenType.IDENTIFIER):
        #     # TODO: Add variables
        #     ...

        # if self.match(TokenType.LEFT_PAREN):
        #     # TODO: add groupings
        #     ...

        raise ParserError(self.peek(), "Expected expression")

    def advance(self) -> Token:
        """
        Helper method to advance forward and return the previous token. This method
        is similar to the scanner's advance method.
        """
        if not self.is_end():
            self.current += 1
        return self.previous()

    def check(self, _type: TokenType) -> bool:
        """
        Helper method to check a current tokens type.
        """
        if self.is_end():
            return False
        return self.peek()._type == _type

    def consume(self, _type: TokenType, message: str) -> Token:
        """
        Helper method to consume a Token and throw an error if the Token
        is not encountered.
        Args:
            _type is the token type of interest
            message is the error message we wish to display
        """
        if self.check(_type):
            return self.advance()
        raise ParserError(self.peek(), message)

    def match(self, *types: TokenType) -> bool:
        """
        Helper method to match an arbitary amount of types.
        Args:
            *args is an arbitrary amount of positional arguments stored as a tuple
            internally
        """
        # We iterate over each type in the tuple
        for _type in types:
            # If we match our type we advance and return True
            if self.check(_type):
                self.advance()
                return True
        # Otherwise we return false
        return False

    def is_end(self) -> bool:
        """Helper method to test if we are at the end of the tokens"""
        return self.peek()._type == TokenType.EOF

    def peek(self) -> Token:
        """Helper method to peek at the current token"""
        return self.tokens[self.current]

    def previous(self) -> Token:
        """Helper method to index the previous token and return it"""
        return self.tokens[self.current - 1]
