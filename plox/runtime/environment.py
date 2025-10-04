from __future__ import annotations
from typing import Dict, Any, TYPE_CHECKING
from .errors import UndefinedVariable

if TYPE_CHECKING:
    from ..core.token import Token


class Environment:
    def __init__(self):
        self.values: Dict[str, Any] = {}

    def define(self, name: str, value: Any) -> None:
        """Method to define variables into the environment."""
        self.values[name] = value

    def get(self, name: Token) -> Any:
        """Method to retrieve variables from the environment."""
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        raise UndefinedVariable(name, "Undefined variable")
    
    def assign(self, name: Token, value: Any) -> None:
        """Method to change a variables stored value."""
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        raise UndefinedVariable(name, "Undefined variable")