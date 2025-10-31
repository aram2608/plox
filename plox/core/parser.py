from typing import List

from ..ast.expr import (
    Expr,
    Variable,
    Logical,
    Conditional,
    Grouping,
    Binary,
    Unary,
    Literal,
)
from ..ast.stmt import Stmt, Var, ExpressionStmt, Print, Block
from .token import Token, TokenType
from ..runtime.errors import ParserError, InvalidAssignment


class Parser:
    def __init__(self, tokens: List[Token]):
        """
        To initialize our parser class we only need to pass in a list of tokens.
        """
        self.tokens = tokens
        self.current = 0

    def parse(self) -> List[Stmt]:
        """
        This function is the main logic for creating our abstract syntax tree.
        """
        # We initialize an empty list for our expressions
        smts = []
        # While we have not reached the end of the list of tokens, we append
        # the parsed syntax tree to our list
        while not self.is_end():
            smts.append(self.declaration())

        # After parsing we return our list
        return smts

    def declaration(self):
        """Method to handle parsing variable declarations."""
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()

            return self.statement()
        except ParserError:
            self.synchronize()
            return

    def var_declaration(self):
        """Main logic for creating variables."""
        # We first consume the identifer and throw an error if we do not encounter one
        name: Token = self.consume(TokenType.IDENTIFIER, "Expected variable name")

        # Lox allows unitialized variables so we start by giving it no value
        initializer: Expr = None
        # If we match an equal token we retrieve the underlying expression
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        # We make sure to close off the statement and return a new Var node
        self.consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")
        return Var(name, initializer)

    def statement(self):
        """Main method used to parse statements."""
        # We catch print statements
        if self.match(TokenType.PRINT):
            return self.print_stmt()

        # We catch any left braces '{'
        if self.match(TokenType.LEFT_BRACE):
            return self.block()

        # If nothing is matched skip into an expression statement
        return self.expression_stmt()

    def print_stmt(self):
        """Function to create print statements."""
        # We store the underlying expression
        value: Expr = self.expression()
        # We always end a statement with a semicolon
        self.consume(TokenType.SEMICOLON, "Expected ';' after value")
        # We then return the Print Stmt
        return Print(value)

    def expression_stmt(self) -> ExpressionStmt:
        """Function to create expression statements."""
        # We store the underlying expression
        value: Expr = self.expression()
        # We always end a statement with a semicolon
        self.consume(TokenType.SEMICOLON, "Expected ';' after value")
        # We then return the Expression Stmt
        return ExpressionStmt(value)

    def block(self) -> List[Stmt]:
        """Functon to parse block statements."""
        # We initialize a list to store statements
        statements: List[Stmt] = []

        # We add statements for as long as we don't reach the end of the file
        # and don't match a right brace '}'
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_end():
            statements.append(self.declaration())

        # Every block needs to be finished by a right brace
        self.consume(TokenType.RIGHT_BRACE, "Expected a '}' after a block")
        # We can now return the statements
        return Block(statements)

    def expression(self) -> Expr:
        """Main method used to parse expressions."""
        return self.assignment()

    def assignment(self):
        """Method to handle the parsing of assignments."""
        # We retrive the expression
        expr: Expr = self.conditional()

        # If we match the equal symbol
        if self.match(TokenType.EQUAL):
            # We extract the previous token and create a new value
            equals: Token = self.previous()
            value: Expr = self.assignment()

            # We then attempty to make an assignment and catch any errors
            try:
                return expr.make_assignment(equals, value)
            except InvalidAssignment as e:
                print(e)

        # If no assignment is made we simply return the expression
        return expr

    def conditional(self):
        expr: Expr = self.logical_or()

        while self.match(TokenType.QUESTION):
            operator: Token = self.previous()
            left: Expr = self.expression()
            self.consume(TokenType.COLON, "Expected ':'")
            right: Expr = self.conditional()
            expr: Conditional = Conditional(expr, operator, left, right)
        return expr

    def logical_or(self):
        """
        This function handles the parsing of logical and operations.
        Example:
            True or True
        """
        expr: Expr = self.logical_and()

        # While we math the or keyword
        while self.match(TokenType.OR):
            # We extract the token and right hand expression
            operator: Token = self.previous()
            right: Expr = self.logical_and()
            # We then create a Logical node
            expr: Binary = Logical(expr, operator, right)

        # We return the final expression
        return expr

    def logical_and(self):
        """
        This function handles the parsing of logical and operations.
        Example:
            True and True
        """
        # We first extract the left hand expression
        expr: Expr = self.equality()

        # While we match and Tokens
        while self.match(TokenType.AND):
            # We extract the token
            operator: Token = self.previous()
            # And right hand expression
            right: Expr = self.equality()
            # We then create a new Binary node
            expr: Binary = Logical(expr, operator, right)

        # We finally return our completed expression
        return expr

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
            right: Expr = self.factor()
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
        # The base primitives are quite simple, we match the TokenType and
        # return the appropriate Literal type
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

        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())

        # We first match the opening parenethesis '('
        if self.match(TokenType.LEFT_PAREN):
            # We then return the underlying the expression
            expr: Expr = self.expression()
            # We need to consume the closing ')' and throw and error if parens are
            # not closed
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            # We then return our grouping
            return Grouping(expr)

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

    def synchronize(self):
        """Method to synchronize parser after a parsing error."""
        # We advance once
        self.advance()
        # We define a set of TokenTypes to iterate over
        # These are common starters for statements
        starters = {
            TokenType.CLASS,
            TokenType.FUN,
            TokenType.VAR,
            TokenType.FOR,
            TokenType.IF,
            TokenType.WHILE,
            TokenType.PRINT,
            TokenType.RETURN,
        }
        # While we are not at the end
        while not self.is_end():
            # If the previous type is a semicolon we can return
            if self.previous()._type == TokenType.SEMICOLON:
                return
            # If the current type is in the set of token types we can return
            if self.peek()._type in starters:
                return
            # Otherwise we continue to advance
            self.advance()

    def is_end(self) -> bool:
        """Helper method to test if we are at the end of the tokens"""
        return self.peek()._type == TokenType.EOF

    def peek(self) -> Token:
        """Helper method to peek at the current token"""
        return self.tokens[self.current]

    def previous(self) -> Token:
        """Helper method to index the previous token and return it"""
        return self.tokens[self.current - 1]
