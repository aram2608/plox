from typing import Dict, Any, TYPE_CHECKING
from .errors import UndefinedVariable

if TYPE_CHECKING:
    from ..core.token import Token


class Environment:
    """Environment class to store Lox objects."""

    def __init__(self, enclosing: Environment | None = None):
        """
        We initialize every environment with a dictionary to contain our Lox
        objects.
        Python does not allow different constructor so we default to have no
        enclosing scope and only assign if provided at the point of intializations.
        Example
            env = Environment() -> No enclosing scope
            env = Environment(outer: Environment) -> Enclosing scope provided
        """
        self.enclosing = enclosing
        self.values: Dict[str, Any] = {}

    def define(self, name: str, value: Any) -> None:
        """Method to define variables into the environment."""
        # We simply store the value by the name
        self.values[name] = value

    def get(self, name: Token) -> Any:
        """Method to retrieve variables from the environment."""
        # We do a lookup for the value by name
        if name.lexeme in self.values:
            # If found we simply return
            return self.values[name.lexeme]

        # If we have an enclosing environment we need to check for the variable
        if self.enclosing is not None:
            return self.enclosing.get(name)

        # Otherwise we throw an error
        raise UndefinedVariable(name, "Undefined variable")

    def assign(self, name: Token, value: Any) -> None:
        """Method to change a variables stored value."""
        # We do a lookup for the value by name
        if name.lexeme in self.values:
            # If found we simply override the previous value with the new one
            self.values[name.lexeme] = value
            # We make sure to return out or else we fall into the exception
            return

        # We do a lookup for the value in the enclosing scope if it exists
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            # We need to return out so we don't fall into the exception
            return

        # If the variable is not defined we throw an error
        raise UndefinedVariable(name, "Undefined variable")
