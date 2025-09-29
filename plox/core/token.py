from enum import Enum, auto


class Token:
    def __init__(self, _type, value=None):
        self._type = _type
        self.value = value

    def __repr__(self):
        return f"Token: {self._type}, {self.value}"


class TokenType(Enum):
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    SLASH = auto()
    STAR = auto()
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FOR = auto()
    FUN = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()
    EOF = auto()
