from plox.core.scanner import Scanner
from plox.core.token import Token, TokenType


def run_scanner(source: str):
    scanner = Scanner(source)
    toks = scanner.scan_tokens()
    return toks


def test_plus():
    result = run_scanner("+")
    assert result[0] == Token(TokenType.PLUS, "+")
    assert result[1] == Token(TokenType.EOF, "", None)


def test_minus():
    result = run_scanner("-")
    assert result[0] == Token(TokenType.MINUS, "-")
    assert result[1] == Token(TokenType.EOF, "", None)


def test_star():
    result = run_scanner("*")
    assert result[0] == Token(TokenType.STAR, "*")
    assert result[1] == Token(TokenType.EOF, "", None)


def test_slash():
    result = run_scanner("/")
    assert result[0] == Token(TokenType.SLASH, "/")
    assert result[1] == Token(TokenType.EOF, "", None)


def test_mod():
    result = run_scanner("%")
    assert result[0] == Token(TokenType.MOD, "%")
    assert result[1] == Token(TokenType.EOF, "", None)


def test_minus_minus():
    result = run_scanner("--")
    assert result[0] == Token(TokenType.MINUS_MINUS, "--")
    assert result[1] == Token(TokenType.EOF, "", None)


def test_plus_plus():
    result = run_scanner("++")
    assert result[0] == Token(TokenType.PLUS_PLUS, "++")


def test_keywords():
    keywords = {
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
    for kw, token_type in keywords.items():
        result = run_scanner(kw)
        assert result[0] == Token(token_type, kw)
        assert result[1] == Token(TokenType.EOF, "", None)

def test_string():
    result = run_scanner('"hello world"')
    assert result[0] == Token(TokenType.STRING, '"hello world"', 'hello world')
    assert result[1] == Token(TokenType.EOF, "", None)

def test_number():
    result = run_scanner("1")
    assert result[0] == Token(TokenType.NUMBER, float(1))

def test_simple_math():
    result = run_scanner("1 + 1")
    assert result[0] == Token(TokenType.NUMBER, float(1))
    assert result[1] == Token(TokenType.PLUS, "+")
    assert result[2] == Token(TokenType.NUMBER, float(1))
    assert result[3] == Token(TokenType.EOF, "", None)