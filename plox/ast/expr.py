from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, TypeVar, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from ..core.token import Token

# Visitor method return type
R = TypeVar("R")


class Expr(ABC):
    """Abstract class for expressions."""

    @abstractmethod
    def accept(self, visitor: ExprVisitor[R]) -> R:
        """
        Default accept method.
        Any derived classes must override this or an error will be thrown.
        """
        raise NotImplementedError


class ExprVisitor(ABC):
    """Abstract visitor class for expression"""

    @abstractmethod
    def visit_Grouping(self, expr: Grouping) -> R:
        """
        Default accept Grouping method.
        Any derived classes must override this or an error will be thrown.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_Unary(self, expr: Unary) -> R:
        """
        Default accept Unary method.
        Any derived classes must override this or an error will be thrown.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_Binary(self, expr: Binary) -> R:
        """
        Default accept Binary method.
        Any derived classes must override this or an error will be thrown.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_Literal(self, expr: Literal) -> R:
        """
        Default accept Literal method.
        Any derived classes must override this or an error will be thrown.
        """
        raise NotImplementedError


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
