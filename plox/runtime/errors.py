from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.token import Token, TokenType


class InvalidAssignment(Exception):
    """A custom class to handle assignments."""

    def __init__(self, message: str, equals: Token):
        self.equals = equals
        self.message = message
        super().__init__(f"{message} at: {equals.lexeme}")

    def __str__(self):
        """Custom string method for the InvalidAssignment Exception"""
        # Some ASCII escape characters to pretty up the output
        RED = "\033[91m"
        RESET = "\033[0m"
        return f"{RED}[line: {self.equals.line}] {self.message} \n-> {self.equals.lexeme}{RESET}"


class ParserError(Exception):
    """A custom class for handling errors at parse time."""

    def __init__(self, token: TokenType, message: str):
        """
        To initialize our error class, we pass in the token of interest and an
        error message.
        """
        self.token = token
        self.message = message
        super().__init__(f"[line {token.line}] Error: {message}")

    def __str__(self):
        RED = "\033[91m"
        RESET = "\033[0m"
        return f"{RED}[line {self.token.line}]: Error: {self.message} \ngot -> {self.token.lexeme}{RESET}"


class ScanningError(Exception):
    def __init__(self, line: int, message: str, value=None):
        """
        A custom class to catch errors during scanning of Lox Scripts/REPL input.
        Args:
            line is is the line number in which the error occured
            message is the error message to be printed to the stream
            value is the literal value associated with any given token
        """
        self.line = line
        self.message = message
        self.value = value
        super().__init__(f"[line {line}] Error: {message}")

    def __str__(self):
        """
        A custom string representation method for the ScanningError class,
        If we have a value we return the string with value appended, otherwise
        we return the line and message only
        """
        # Some ASCII escape characters to pretty up the output
        RED = "\033[91m"
        RESET = "\033[0m"
        if self.value is not None:
            return (
                f"{RED}[line {self.line}] Error: {self.message} -> {self.value}{RESET}"
            )
        return f"{RED}[line {self.line}] Error: {self.message}{RESET}"


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


class UndefinedVariable(Exception):
    def __init__(self, token: Token, message: str):
        """
        A custom class to catch errors during retrieval of variables
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
        return f"{RED}Error: {self.message}\n-> {self.token.lexeme}{RESET}"
