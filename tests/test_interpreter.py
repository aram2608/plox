from plox.core.scanner import Scanner
from plox.core.parser import Parser
from plox.core.interpreter import Interpreter

def run_interpreter(source: str):
    scanner = Scanner(source)
    toks = scanner.scan_tokens()
    parser = Parser(toks)
    ast = parser.parse()
    interpreter = Interpreter()
    return interpreter.test_interpret(ast[0])

def test_plus_num():
    assert run_interpreter("1 + 1") == 2.0

def test_plus_string():
    assert run_interpreter('"hello" + "world"') == "helloworld"

def test_minus():
    assert run_interpreter("1 - 1") == 0.0

def test_star():
    assert run_interpreter("2 * 2") == 4.0

def test_slash():
    assert run_interpreter("4 / 2") == 2.0

def test_mod():
    assert run_interpreter("3 % 2") == 1.0

def test_bang():
    assert run_interpreter("!false") == True

def test_greater_equal():
    assert run_interpreter("3 >= 2") == True
    assert run_interpreter("3 >= 3") == True
    assert run_interpreter("3 >= 10") == False

def test_greater():
    assert run_interpreter("3 > 1") == True
    assert run_interpreter("3 > 10") == False

def test_lesser_equal():
    assert run_interpreter("3 <= 5") == True
    assert run_interpreter("3 <= 1") == False

def test_lesser():
    assert run_interpreter("3 < 5") == True
    assert run_interpreter("3 < 1") == False