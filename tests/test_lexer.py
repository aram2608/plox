from plox.core.scanner import Scanner
from plox.core.token import Token, TokenType

def run_scanner(source: str):
    scanner = Scanner(source)
    toks = scanner.scan_tokens()
    return toks

def test_plus():
    result = run_scanner("+")
    assert result == []