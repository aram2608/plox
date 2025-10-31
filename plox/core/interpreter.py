from ..ast.expr import (
    ExprVisitor,
    Expr,
    Assign,
    Variable,
    Binary,
    Unary,
    Literal,
    Grouping,
)
from ..ast.stmt import StmtVisitor, Stmt, Var, ExpressionStmt, Print
from .token import Token, TokenType
from ..runtime.errors import LoxRunTimeError
from ..runtime.environment import Environment

from typing import Any


class Interpreter(ExprVisitor, StmtVisitor):
    """Interpreter class for interpreting Lox programs."""

    def __init__(self):
        """
        We initialize the Interpreter with a base environment for storing Lox
        objects.
        """
        self.environment = Environment()
        super().__init__()

    def interpret(self, stmts: list[Stmt]) -> None:
        """
        Method to interpret Lox statements
        Args:
            stmts is the list of statements we wish to evaluate
        """
        try:
            for stmt in stmts:
                if stmt is not None:
                    self.execute(stmt)
        except LoxRunTimeError as e:
            print(e)

    def execute(self, stmt: Stmt) -> None:
        """
        Main logic to execute statements.
        Args:
            stmt is the AST node we wish to execute
        """
        # We pass in a reference to self
        # and have it retrieve the correct statement visitor method
        stmt.accept(self)

    def evaluate(self, expr: Expr):
        """
        Main logic to evaluate expressions.
        Args:
            expression is the AST node we wish to evaluate
        """
        # We pass in a reference to self
        # and have it retrieve the correct expression vist method
        return expr.accept(self)

    def visit_Assign(self, expr: Assign):
        """Method to visit Assign node."""
        # We evalute the underlying value
        value: Any = self.evaluate(expr.value)
        # We then assign it to the environment
        # Error catching is handled by the environment itself
        self.environment.assign(expr.name, expr.value)
        return value

    def visit_Variable(self, expr: Variable):
        """Method to return variables from the environment."""
        return self.environment.get(expr.name)

    def visit_Var(self, stmt: Var) -> None:
        """Method to visit variables."""
        # We first initialize an empty value
        value: Any = None

        # If our object is initialized we evaluate the underlying expression
        # and store it in a variable
        if stmt.initializer != None:
            value = self.evaluate(stmt.initializer)

        # We can then define it in our environment
        self.environment.define(stmt.name.lexeme, value)

    def visit_ExpressionStmt(self, stmt: ExpressionStmt) -> None:
        """Method to visit expression statements."""
        # We simply evaluate the expression and return None
        self.evaluate(stmt.expr)

    def visit_Print(self, stmt: Print) -> None:
        """Method to visit print statements."""
        # Quite simply we evalute the underlying expression and print to iostream
        value: Any = self.evaluate(stmt.expr)
        print(value)

    def visit_Conditional(self, expr) -> Any:
        """This method provides the logic to interpret Conditional nodes."""
        # We evaluate the expression we wish to test
        condtion: Any = self.evaluate(expr.condition)

        # We test if the condition is true
        if self.is_truthy(condtion):
            # If so, we return the left expression
            return self.evaluate(expr.left)
        else:
            # Otherwise we return the left expression
            return self.evaluate(expr.right)

    def visit_Logical(self, expr) -> Any:
        """This method provides the logic to interpret Logical nodes."""
        # We first evaluate the leftmost expression
        left: Any = self.evaluate(expr.left)

        # This method allows us to short circuit the Logical expression
        # We test if the TokenType is and OR keyword
        if expr.operator._type == TokenType.OR:
            # OR short-circuits when left is truthy
            if self.is_truthy(left):
                return left
        else:
            # AND short-circuits when left is falsy
            if not self.is_truthy(left):
                return left

        # If no short-circuit, evaluate right
        return self.evaluate(expr.right)

    def visit_Grouping(self, expr: Grouping) -> Any:
        """This functions provides the logic to interpret Grouping nodes."""
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
        if object is None:
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
