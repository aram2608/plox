from __future__ import annotations
from ..ast.expr import ExprVisitor, Expr, Binary, Unary, Literal, Grouping
from .token import Token, TokenType

from typing import TYPE_CHECKING, TypeVar, Any


class LoxRunTimeError(Exception):
    def __init__(self, token: Token, message: str):
        """
        A custom class to catch errors during interpretaton of Lox Scripts/REPL input.
        Args:
            token is the problematic token
            message is the error message to be printed to the stream
        """
        self.token = token
        self.message = message
        super().__init__(f"Error: {message} \n {token.lexeme}")

    def __str__(self):
        """
        A custom string representation method for the RunTimeError class.
        """
        # Some ASCII escape characters to pretty up the output
        RED = "\033[91m"
        RESET = "\033[0m"
        return f"{RED}Error: {self.message}\nOperator: {self.token.lexeme}{RESET}"


class Interpreter(ExprVisitor):
    def __init__(self):
        super().__init__()

    def interpret(self, expression: Expr) -> None:
        """
        An interactive form of the interpret method.
        This implementation prints the evaulated expression to the iostream.
        Args:
            expression is the expression we wish to evaluate
        """
        try:
            value = self.evaluate(expression)
            print(value)
        except LoxRunTimeError as e:
            print(e)

    def test_interpret(self, expression: Expr) -> Any:
        """
        A return form for the interpret method
        This implementation returns the evaluate value for ease of use with pytest
        Args:
            expression is the expression we wish to evaluate
        """
        return self.evaluate(expression)

    def evaluate(self, expression: Expr):
        """
        Main logic to evaluate expressions.
        Args:
            expression is the AST node we wish to evaluate
        """
        # We pass in a reference to self
        # and have it retrieve the correct vist method
        return expression.accept(self)

    def visit_Grouping(self, expr: Grouping) -> Any:
        """This functions provides the logice to interpret Groupind nodes."""
        # We simply evalaute the underlying expression and return it
        return self.evaluate(expr.expr)

    def visit_Binary(self, expr: Binary) -> Any:
        """
        This function provides the logic to interpret Binary nodes.
        """
        # We evaluate the left and right side expressions
        left: Any = self.evaluate(expr.left)
        right: Any = self.evaluate(expr.right)

        # We then match each operator type and perform the proper underlying
        # logic for both expressions
        match expr.operator._type:
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)
            case TokenType.GREATER:
                self.check_num_operands(expr.operator, left, right)
                return left > right
            case TokenType.GREATER_EQUAL:
                self.check_num_operands(expr.operator, left, right)
                return left >= right
            case TokenType.LESS:
                self.check_num_operands(expr.operator, left, right)
                return left < right
            case TokenType.LESS_EQUAL:
                self.check_num_operands(expr.operator, left, right)
                return left <= right
            case TokenType.MINUS:
                self.check_num_operands(expr.operator, left, right)
                return left - right
            # Since PLUS can be used for both strings and nums we add a special check
            case TokenType.PLUS:
                if type(left) == float and type(right) == float:
                    return left + right
                if type(left) == str and type(right) == str:
                    return left + right

                raise LoxRunTimeError(
                    expr.operator, "Operands must be two numbers or two strings."
                )
            # SLASH/MOD are also a bit special since if we divide by zero we create
            # a black hole which is not allowed
            case TokenType.SLASH:
                self.check_num_operands(expr.operator, left, right)
                if right == float(0):
                    raise LoxRunTimeError(expr.operator, "Division by zero.")
                return left / right
            case TokenType.MOD:
                self.check_num_operands(expr.operator, left, right)
                if right == float(0):
                    raise LoxRunTimeError(expr.operator, "Division by zero.")
                return left % right
            case TokenType.STAR:
                self.check_num_operands(expr.operator, left, right)
                return left * right

    def visit_Unary(self, expr: Unary) -> Any:
        """
        The override for visiting Binary nodes.
        We evaluate the underlying expression and return the result.
        """
        # We evaluate the right expression
        right: Any = self.evaluate(expr.right)

        # We then match the proper unary operator and apply the proper logic
        match expr.operator._type:
            case TokenType.BANG:
                return not self.is_truthy(right)
            case TokenType.MINUS:
                self.check_num_operand(expr.operator, right)
                return -right
        # Unreachable so we return nothing
        return

    def visit_Literal(self, expr: Literal) -> Any:
        """
        The override for visting Literal nodes.
        We simply return the elements underlying value
        expr->value
        """
        return expr.value

    def is_truthy(self, object: Any) -> bool:
        """A helper method to test if the underlying expression is truthy."""
        if type(object) == None:
            return False
        if type(object) == bool:
            return object
        return True

    def check_num_operand(self, operator: Token, operand: float) -> None:
        """Helper method to check the operand type to ensure it is a number."""
        if type(operand) == float:
            return
        raise LoxRunTimeError(operator, "Operand must be a number.")

    def check_num_operands(self, operator: Token, left: float, right: float):
        """Helper method to check two operand type to ensure they are numbers."""
        if type(left) == float and type(right) == float:
            return
        raise LoxRunTimeError(operator, "Operands must be numbers.")

    def is_equal(self, a: Any, b: Any) -> bool:
        """A helper method to test whether two objects are equal."""
        if type(a) == None and type(b) == None:
            return True
        if type(a) == None:
            return False
        if type(a) == str and type(b) == str:
            return a == b
        if type(a) == float and type(b) == float:
            return a == b
        if type(a) == bool and type(b) == bool:
            return a == b
        return False
