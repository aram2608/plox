from plox.core.scanner import Scanner
from plox.core.token import Token, TokenType
from plox.core.parser import Parser
from plox.ast.expr import Unary, Binary, Literal

def run_parser(source: str):
    scanner = Scanner(source)
    toks = scanner.scan_tokens()
    parser = Parser(toks)
    ast = parser.parse()
    return ast

def test_addition():
    result = run_parser("1 + 1")
    assert result[0] == Binary(Literal(1.0), Token(TokenType.PLUS, "+"), Literal(1.0))

def test_subtraction():
    result = run_parser("1 - 1")
    assert result[0] == Binary(Literal(1.0), Token(TokenType.MINUS, "-"), Literal(1.0))

def test_division():
    result = run_parser("1 / 4")
    assert result[0] == Binary(Literal(1.0), Token(TokenType.SLASH, "/"), Literal(4.0))

def test_mult():
    result = run_parser("1 * 4")
    assert result[0] == Binary(Literal(1.0), Token(TokenType.STAR, "*"), Literal(4.0))

def test_nested_comment():
    # We ignore any nested comments inside of expressions
    result = run_parser("1 /* i should be ignored */ + 1")
    assert result[0] == Binary(Literal(1.0), Token(TokenType.PLUS, "+"), Literal(1.0))

def test_commented_out():
    # Nothing should be parsed
    result = run_parser("// TODO: Fix additon 1 + 1")
    assert not result