from abc import ABC, abstractmethod
from typing import List, TypeVar, TYPE_CHECKING
from dataclasses import dataclass

from .expr import Expr

if TYPE_CHECKING:
    from ..core.token import Token

# Visitor method return type
R = TypeVar("R")


class Stmt(ABC):
    """Abstract class for statements."""

    @abstractmethod
    def accept(self, visitor: StmtVisitor):  # type: ignore
        """
        Default accept method.
        Any derived classes must override this or an error will be thrown.
        """
        raise NotImplementedError


class StmtVisitor(ABC):
    """Abstract visitor class for statements."""

    @abstractmethod
    def visit_IfStmt(self, stmt: IfStmt) -> R:
        """
        Default visit IfStmt method.
        Any derived class must override this or an error wil be thrown.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_Block(self, stmt: Block) -> R:
        """
        Default visit Block method.
        Any derived class must override this or an error wil be thrown.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_Var(self, stmt: Var) -> R:
        """
        Default visit VarStmt method.
        Any derived class must override this or an error wil be thrown.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_ExpressionStmt(self, stmt: ExpressionStmt) -> R:
        """
        Default visit ExpressionStmt method.
        Any derived class must override this or an error will be thrown.
        """
        raise NotImplementedError

    @abstractmethod
    def visit_Print(self, stmt: Print) -> R:
        """
        Default visit Print method.
        Any derived class must override this or an error will be thrown.
        """
        raise NotImplementedError


@dataclass
class IfStmt(Stmt):
    """
    Class used to represent If statements. Constructed as a data class
    Args:
        condition is the underlying condition we test for
        then_branch is the branch executed if the condition is true
        else_branch is the branch executed if the conditon is false
    """

    condition: Expr
    then_branch: Stmt
    else_branch: Stmt | None

    def accept(self, visitor: StmtVisitor):
        """Accept method override for Ifstmts."""
        return visitor.visit_IfStmt(self)


@dataclass
class Block(Stmt):
    """
    Class used to represent Block statements. Constructed as a data class
    Args:
        stmts is a list of other statements
    """

    stmts: List[Stmt]

    def accept(self, visitor: StmtVisitor) -> R:
        """Accept method override for Block stmts."""
        return visitor.visit_Block(self)


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

    def accept(self, visitor: StmtVisitor) -> R:
        return visitor.visit_Print(self)
