from __future__ import annotations
from .token import Token, TokenType

from string import ascii_letters
from typing import Any, List, Dict


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


class Scanner:
    """
    The Lox Scanner Class, use for tokenizing source code/REPL input.
    """

    def __init__(self, source: str):
        """
        To initialize our class we only need to pass in a the 'source' code, ie
        a string of the Lox Script/REPL input
        """
        self.source: str = source
        # We store an integer value to represent the current tok position
        self.current: int = 0
        # An integer value to represent the point at which we start scanning toks
        self.start: int = None
        # We keep track of the line number of the Lox Script for error handling
        self.line: int = 0
        # To check if a token type is a number, we check if it can be found
        # in this member variable
        self.numbers: str = "0123456789"
        # We apply the same concept to strings and include '_' for identifiers/str
        self.alpha: str = ascii_letters + "_"
        # We need to save a list of tokens after scanning
        self.tokens: List[Token] = []
        # We store a map of predefined keywords that can not be identifiers/strings
        self.keywords: Dict[str, TokenType] = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }

    def scan_tokens(self) -> List[Token]:
        """
        Function use to create tokens out of source code/REPL input.
        It takes no arguments, and is simply a wrapper for the scan() method
        that runs until our source code is empty.
        """
        # We run until all source code is exhausted
        while not self.is_end():
            # We store our start position for error handling then proceed to scan
            self.start = self.current
            self.scan()

        # After the source code is depleted, we add an end of file toke and return
        # our generated tokens
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan(self) -> None:
        """
        This is the main logic for the creation of tokes. No arguments are passed
        in and no value is returned.
        We simply append any created tokens to the self.tokens member variable.
        """
        # We first advance forward, returning the character
        char: str = self.advance()
        # We then match the character against all our predefined token types
        # We could have used an if/elif/else statement but match is a bit cleaner
        # and more in line with Rob's jlox implementation
        match char:
            # We increment our line count on new lines
            case "\n":
                self.line += 1
            # We skip empty characters
            case " " | "\r" | "\t":
                pass
            # Single character tokens
            case "*":
                self.add_token(TokenType.STAR)
            case "%":
                self.add_token(TokenType.MOD)
            case "?":
                self.add_token(TokenType.QUESTION)
            case '"':
                self.make_string()
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case ":":
                self.add_token(TokenType.COLON)
            case ".":
                self.add_token(TokenType.DOT)
            # Double character tokens
            case "+":
                if self.match("+"):
                    self.add_token(TokenType.PLUS_PLUS)
                else:
                    self.add_token(TokenType.PLUS)
            case "-":
                if self.match("-"):
                    self.add_token(TokenType.MINUS_MINUS)
                else:
                    self.add_token(TokenType.MINUS)
            case "!":
                if self.match("="):
                    self.add_token(TokenType.BANG_EQUAL)
                else:
                    self.add_token(TokenType.BANG)
            case "=":
                if self.match("="):
                    self.add_token(TokenType.EQUAL_EQUAL)
                else:
                    self.add_token(TokenType.EQUAL)
            case "/":
                if self.match("/"):
                    self.make_comment()
                elif self.match("*"):
                    self.make_multiline_comment()
                else:
                    self.add_token(TokenType.SLASH)
            case ">":
                if self.match("="):
                    self.add_token(TokenType.GREATER_EQUAL)
                else:
                    self.add_token(TokenType.GREATER)
            case "<":
                if self.match("="):
                    self.add_token(TokenType.LESS_EQUAL)
                else:
                    self.add_token(TokenType.LESS)
            # Rob adds his identifiers and numbers as a default case
            # It's a little weird but it gets the job done
            case _:
                # We first check for numbers
                if self.is_digit(char):
                    self.make_number()
                # We can then check for identifiers/keywords
                elif self.is_alpha(char):
                    self.make_identifier()
                # Otherwise we kick out an error
                else:
                    raise ScanningError(
                        self.line,
                        "ScanningError: Unidentified token type.",
                    )

    def advance(self) -> str:
        """Method used to increment character count and return the next char."""
        char: str = self.source[self.current]
        self.current += 1
        return char

    def peek(self) -> str | None:
        """
        Method used to peek at the current character,
        Does not increment character count.
        """
        # We first make sure we have not reached the end of the file
        # If we have we return None
        if self.is_end():
            return None
        # We can then return our character if our check passes
        return self.source[self.current]

    def peek_next(self) -> str:
        """
        Method use to peek at the next character, does increment character count.
        """
        # We check if the next value is greater than the overall length of the source
        # If so we return a null terminator character
        if self.current + 1 >= len(self.source):
            return "\0"
        # If our check passes we return the next character
        return self.source[self.current + 1]

    def is_end(self) -> bool:
        """
        A simple helper method to test if we have reached the end of the file.
        """
        return self.current >= len(self.source)

    def add_token(self, _type: TokenType, literal: str | float | None = None) -> None:
        """
        This method creates our Token of interest and appends it to the self.tokens
        member variable.
        """
        # We first extract out the lexeme
        lex = self.source[self.start : self.current]
        # We can not create and add our token
        self.tokens.append(Token(_type, lex, literal, self.line))

    def make_string(self) -> None:
        """
        This method encapsulates the logic needed to create a string object in Lox.
        """
        # We continue to skip past characters as long as we have not reached
        # the end of the file or the closing ".
        while self.peek() != '"' and not self.is_end():
            # Lox allows multiline string
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        # If we reach the end of the file we throw and error
        if self.is_end():
            raise ScanningError(
                line=self.line, message="ScanningError: Unterminated string"
            )

        # We can now jump across the closing "
        self.advance()

        # We then substring out the lexeme of interest and create out token
        string: str = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, string)

    def make_number(self):
        """
        This method encapsulates the logic needed to create Lox numbers, ie floats.
        """
        # We continue so long as the current character is a number
        while self.is_digit(self.peek()):
            self.advance()

        # We leap over the decimal
        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

            # We then continue so long as the current character is a number
            while self.is_digit(self.peek()):
                self.advance()

        # We collect the stubstring of the source code and add it as our token
        lex = self.source[self.start : self.current]
        self.add_token(TokenType.NUMBER, float(lex))

    def make_identifier(self):
        """
        This method encapsulates the logic needed to create identifiers in Lox.
        """
        # We continue so long as the current character is alpha numeric
        while self.is_alpha_num(self.peek()):
            self.advance()

        # We substring out the lexeme
        text: str = self.source[self.start : self.current]

        # We now need to test if the lexeme is inside the dictionary containing
        # our reserved keywords
        if text in self.keywords:
            # If so we use the lexeme as a key and return the TokenType of interest
            self.add_token(self.keywords[text])
        # Otherwise we create a new identifier
        else:
            self.add_token(TokenType.IDENTIFIER)

    def make_comment(self):
        """Helper method to create comments."""
        # We simply skip past all characters until we reach a new line
        while self.peek() != "\n" and not self.is_end():
            self.advance()

    def make_multiline_comment(self):
        """Helper method to create multiline comments."""
        # We store the current position of the /* token
        mlc_line = self.line
        # We continue until we reach the end of the file
        while not self.is_end():
            # If we come across a new line we increment our line count
            if self.peek() == "\n":
                self.line += 1
                self.advance()
            # If we come across the closing */ token we can advance twice
            # to leap past these two characters and return out
            elif self.peek() == "*" and self.peek_next() == "/":
                self.advance()
                self.advance()
                return
            else:
                # We simply skip past all characters if none of our conditions our met
                self.advance()
        # If the mutline comment is unterminated we throw and error
        raise ScanningError(mlc_line, "Unterminated multiline comment")

    def is_alpha(self, char: str) -> bool:
        """A helper method to test if the current char is a letter."""
        # None can not be compared to a string so if we come across None for some
        # reason we need to make sure we don't throw and exception
        if char == None:
            return False
        # Otherwise we test if our character is in the self.alpha member
        # containing characters and "_"
        return char in self.alpha

    def is_digit(self, char: str) -> bool:
        """A simple helper to test if a character is a number."""
        # None can not be compared to a number so if we come across None for some
        # reason we need to make sure we don't throw and exception
        if char == None:
            return False
        # Otherwise we test if our character is in the self.numbers member
        return char in self.numbers

    def is_alpha_num(self, char: str) -> bool:
        """A helper method to wrap is_alpha() and is_digit()"""
        return self.is_alpha(char) or self.is_digit(char)

    def match(self, expected: str) -> bool:
        """
        This function is used during scanning to test if we have come across a
        two character token such as != or >=.
        Args:
            expected is a string of the expected character.
            If we wish to match a != token, we use match('=') to test
            if the bang is proceeded by the equals symbol.
        """
        # We first make sure we are not at the end of the file
        if self.is_end():
            return False

        # We peek at the current character and test if it the expected character
        if self.peek() != expected:
            return False

        # If our tests pass we need to increment past the second character and
        # return True
        self.current += 1
        return True
