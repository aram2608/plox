from abc import ABC, abstractmethod
from typing import Any, TypeVar, TYPE_CHECKING
from dataclasses import dataclass
from ..runtime.errors import InvalidAssignment

if TYPE_CHECKING:
    from ..core.token import Token

# Visitor method return type
R = TypeVar("R")


class Expr(ABC):
    """Abstract class for expressions."""

    @abstractmethod
    def accept(self, visitor: ExprVisitor[R]) -> R:  # type: ignore
        """
        Default accept method.
        Any derived classes must override this or an error will be thrown.
        """
        raise NotImplementedError

    def make_assignment(self, equals: Token, value: Expr) -> None:  # type: ignore
        """
        Default make assignment method. This is a bit of a hack but we are going
        to have the nodes themselves resolve assignments. Only Variable nodes
        are allowed to create them.
        """
        raise InvalidAssignment("Invalid Assignment Target", equals)


class ExprVisitor(ABC):
    """Abstract visitor class for expression."""

    @abstractmethod
    def visit_Variable(self, expr: Variable) -> R:  # type: ignore
        """
        Default visit Variable method.
        Any derived class must override this or an error will be throw
        """
        raise NotImplementedError

    @abstractmethod
    def visit_Assign(self, expr: Assign) -> R:  # type: ignore
        """
        Default visit Assign method.
        Any derived class must override this or an error will be throw
        """
        raise NotImplementedError

    @abstractmethod
    def visit_Conditional(self, expr: Conditional) -> R:  # type: ignore
        """
        Default visit Condtional method.
        Any derived class must override this or an error will be throw
        """
        raise NotImplementedError

    @abstractmethod
    def visit_Logical(self, expr: Logical) -> R:  # type: ignore
        """
        Default visit Logical method.
        Any derived class must override this or an error will be throw
        """
        raise NotImplementedError

    @abstractmethod
    def visit_Grouping(self, expr: Grouping) -> R:  # type: ignore
        """
        Default visit Grouping method.
        Any derived classes must override this or an error will be thrown.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_Binary(self, expr: Binary) -> R:  # type: ignore
        """
        Default visit Binary method.
        Any derived classes must override this or an error will be thrown.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_Unary(self, expr: Unary) -> R:  # type: ignore
        """
        Default visit Unary method.
        Any derived classes must override this or an error will be thrown.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_Literal(self, expr: Literal) -> R:  # type: ignore
        """
        Default visit Literal method.
        Any derived classes must override this or an error will be thrown.
        """
        raise NotImplementedError


@dataclass
class Variable(Expr):
    """
    Class used to represent Assign expressions. Construced as a dataclass
    Args:
        name is the token name of the variable
    """

    name: Token

    def accept(self, visitor):
        """Accept method override for the Variable node."""
        return visitor.visit_Variable(self)

    def make_assignment(self, equals: Token, value: Expr):
        """Make assignment override. We return a new Assign node."""
        return Assign(self.name, value)


@dataclass
class Assign(Expr):
    """
    Class used to represent Assign expressions. Construced as a dataclass
    Args:
        name is the token name of the variable
        value is an expression containing the variables value
    """

    name: Token
    value: Expr

    def accept(self, visitor):
        """Accept method override for the Assign node."""
        return visitor.visit_Assign(self)


@dataclass
class Conditional(Expr):
    """
    Class used to represent Condition expressions. Construced as a dataclass
    Args:
        condition is the expression to be evaluated and compared.
        left is the left expression
        operator is the ternary operator
        right is the right expression
    This class handles ternary expression which are one-liner if else statements
    For example:
        x = (1 < 4) ? 5 : 4
        x = 5
    """

    condition: Expr
    operator: Token
    left: Expr
    right: Expr

    def accept(self, visitor: ExprVisitor) -> R:
        """Accept method override for the Conditional node."""
        return visitor.visit_Conditional(self)


@dataclass
class Logical(Expr):
    """
    Class used to represent Logical expressions. Constructed as a dataclass
    Args:
        left is the left expression
        operator is the Token representation of the operator
        right is the right expression
    This class handles logical opertions such as 'True and True' or 'False or True'
    """

    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor) -> R:
        """Accept method override for the Logical node."""
        return visitor.visit_Logical(self)


@dataclass
class Grouping(Expr):
    """
    Class used to represent Groupings. Constructed as a dataclass
    Args:
        expr (ie expression) is the underlying expression contained in the
        parenthesis
    """

    expr: Expr

    def accept(self, visitor: ExprVisitor) -> R:
        """Accept method override for the Grouping node."""
        return visitor.visit_Grouping(self)


@dataclass
class Binary(Expr):
    """
    Class used to represent the Binary node. Constructed as a dataclass.
    Args:
        left is the left expression
        operator is the Token representation of the operator
        right is the right expression
    This class handles arithmetic operations such as 1 + 1, 1 / 2, etc...
    """

    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor) -> R:
        """Accept method override for the Binary node."""
        return visitor.visit_Binary(self)


@dataclass
class Unary(Expr):
    """
    Class representation of the Unary node. Constructed as a dataclass
    Args:
        operator is the Token representation of the operator
        right is the right expression
    This class handles arithmetic operations such as - 1, and logical operations
    such as !=
    """

    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor) -> R:
        """Accept method override for the Unary node."""
        return visitor.visit_Unary(self)


@dataclass
class Literal(Expr):
    """
    Class representation of the Literal node. Constructed as a dataclass.
    Args:
        value can be any assigned value (ie False, True, 1, "hello world", etc..)
    """

    value: Any

    def accept(self, visitor: ExprVisitor) -> R:
        """Accept method override for the Literal node."""
        return visitor.visit_Literal(self)
