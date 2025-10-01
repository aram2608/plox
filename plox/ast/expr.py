from __future__ import annotations
from abc import ABC, abstractmethod

from core.token import Token


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor) -> None:
        pass


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right


class ExprVisitor(ABC):
    @abstractmethod
    def visit_Unary(self, element: Unary) -> None:
        pass

    @abstractmethod
    def visit_Binary(self, element: Binary) -> None:
        pass
