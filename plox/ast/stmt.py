from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, TypeVar, TYPE_CHECKING
from dataclasses import dataclass

from .expr import Expr

if TYPE_CHECKING:
    from ..core.token import Token

# Visitor method return type
R = TypeVar("R")


class Stmt(ABC):
    """Abstract class for statements."""

    @abstractmethod
    def accept(self, visitor: StmtVisitor):
        """
        Default accept method.
        Any derived classes must override this or an error will be thrown.
        """
        raise NotImplementedError


class StmtVisitor(ABC):
    """Abstract visitor class for statements."""

    @abstractmethod
    def visit_Var(self, stmt: Stmt) -> R:
        raise NotImplementedError

    @abstractmethod
    def visit_ExpressionStmt(self, stmt: Stmt) -> R:
        """
        Default visit ExpressionStmt method.
        Any derived class must override this or an error will be throw
        """
        raise NotImplementedError

    @abstractmethod
    def visit_Print(self, stmt: Stmt) -> R:
        """
        Default visit Print method.
        Any derived class must override this or an error will be throw
        """
        raise NotImplementedError


@dataclass
class Var(Stmt):
    """
    Class used to represent Var statements. Constructed as a data class
    Args:
        name is the token for the variable name
        initializer is the expression used to initialize the variable
    """

    name: Token
    initializer: Expr

    def accept(self, visitor: StmtVisitor) -> R:
        """Accept method override for Var statements."""
        return visitor.visit_Var(self)


@dataclass
class ExpressionStmt(Stmt):
    """
    Class used to represent Expression Statments. Constructed as a data class
    Args:
        expr is the underlying expression to be evaluate
    """

    expr: Expr

    def accept(self, visitor: StmtVisitor) -> R:
        return visitor.visit_ExpressionStmt(self)


@dataclass
class Print(Stmt):
    """
    Class used to represent Print Statments. Constructed as a data class
    Args:
        expr is the underlying expression to be printed
    """

    expr: Expr

    def accept(self, visitor):
        return visitor.visit_Print(self)
