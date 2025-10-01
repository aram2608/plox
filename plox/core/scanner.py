from __future__ import annotations
from .token import Token, TokenType

from string import ascii_letters
from typing import Any, List, Dict


class ScanningError(Exception):
    def __init__(self, line: int, message: str, value=None):
        self.line = line
        self.message = message
        self.value = value
        super().__init__(f"[line {line}] Error: {message}")

    def __str__(self):
        RED = "\033[91m"
        RESET = "\033[0m"
        if self.value is not None:
            return (
                f"{RED}[line {self.line}] Error: {self.message} -> {self.value}{RESET}"
            )
        return f"{RED}[line {self.line}] Error: {self.message}{RESET}"


class Scanner:
    def __init__(self, source: str):
        self.source: str = source
        self.current: int = 0
        self.start: int | None = None
        self.tokens: List[Token] = []
        self.line: int = 0
        self.numbers: str = "0123456789"
        self.alpha: str = ascii_letters + "_"
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
        while not self.is_end():
            self.start = self.current
            self.scan()

        self.add_token(TokenType.EOF)
        return self.tokens

    def scan(self) -> None:
        char: str = self.advance()
        match char:
            case "\n":
                self.line += 1
            case " " | "\r" | "\t":
                pass
            case "+":
                self.add_token(TokenType.PLUS)
            case "-":
                self.add_token(TokenType.MINUS)
            case "/":
                if self.match("/"):
                    self.make_comment()
                elif self.match("*"):
                    self.make_multiline_comment()
                else:
                    self.add_token(TokenType.SLASH)
            case "!":
                if self.match("="):
                    self.add_token(TokenType.BANG_EQUAL)
                else:
                    self.add_token(TokenType.BANG)
            case "*":
                self.add_token(TokenType.STAR)
            case "%":
                self.add_token(TokenType.MOD)
            case "=":
                if self.match("="):
                    self.add_token(TokenType.EQUAL_EQUAL)
                else:
                    self.add_token(TokenType.EQUAL)
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
            case _:
                if self.is_digit(char):
                    self.make_number()
                elif self.is_alpha(char):
                    self.make_identifier()
                else:
                    raise ScanningError(
                        line=self.line,
                        message="ScanningError: Unidentified token type.",
                    )

    def advance(self) -> str:
        char: str = self.source[self.current]
        self.current += 1
        return char

    def peek(self) -> str | None:
        if self.is_end():
            return None
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def is_end(self) -> bool:
        return self.current >= len(self.source)

    def add_token(self, _type: TokenType, literal: None | Any = None) -> None:
        text = self.source[self.start : self.current]
        print(text)
        self.tokens.append(
            Token(_type=_type, lexeme=text, literal=literal, line=self.line)
        )

    def make_string(self) -> None:
        while self.peek() != '"' and not self.is_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.is_end():
            raise ScanningError(
                line=self.line, message="ScanningError: Unterminated string"
            )

        self.advance()

        string: str = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, string)

    def make_number(self):
        while self.is_digit(self.peek()):
            self.advance()

        # We leap over the decimal
        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        # We collect the stubstring of the source code and add it as our token
        lex = self.source[self.start:self.current]
        self.tokens.append(
            Token(TokenType.NUMBER, float(lex))
        )

    def make_identifier(self):
        while self.is_alpha_num(self.peek()):
            self.advance()

        text: str = self.source[self.start : self.current]

        if text in self.keywords:
            self.add_token(self.keywords[text])
        else:
            self.add_token(TokenType.IDENTIFIER)

    def make_comment(self):
        while self.peek() != "\n" and not self.is_end():
            self.advance()

    def make_multiline_comment(self):
        mlc_line = self.line
        while not self.is_end():
            if self.peek() == "\n":
                self.line += 1
                self.advance()
            elif self.peek() == "*" and self.peek_next() == "/":
                self.advance()
                self.advance()
                return
            else:
                self.advance()
        raise ScanningError(line=mlc_line, message="Unterminated multiline comment")

    def is_alpha(self, char: str) -> bool:
        if char == None:
            return False
        return char in self.alpha

    def is_digit(self, char: str) -> bool:
        if char == None:
            return False
        return char in self.numbers

    def is_alpha_num(self, char: str) -> bool:
        return self.is_alpha(char) or self.is_digit(char)

    def match(self, expected: str) -> bool:
        if self.is_end():
            return False

        if self.peek() != expected:
            return False

        self.current += 1
        return True
