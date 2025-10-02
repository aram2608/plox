from plox.core.scanner import Scanner
from plox.core.token import Token, TokenType
from plox.core.parser import Parser

def run_parser(source: str):
    scanner = Scanner(source)
    toks = scanner.scan_tokens()
    parser = Parser(toks)
    ast = parser.parse()
    return ast

def test_addition():
    result = run_parser("1 + 1")
    