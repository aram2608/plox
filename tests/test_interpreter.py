from plox.core.scanner import Scanner
from plox.core.parser import Parser
from plox.core.interpreter import Interpreter, LoxRunTimeError

from contextlib import redirect_stdout
from io import StringIO

def run_test(source: str):
    scanner = Scanner(source)
    toks = scanner.scan_tokens()
    parser = Parser(toks)
    ast = parser.parse()
    interpreter = Interpreter()
    interpreter.interpret(ast)

    # We need to capture print output so we use the StringIO to capture the
    # iostream buffer
    buffer = StringIO()
    with redirect_stdout(buffer):
        interpreter.interpret(ast)
    # We then return the buffer
    return buffer.getvalue()

def test_plus_num():
    # A bit hacky but we need to test against strings with new line characters
    assert run_test("print 1 + 1;") == '2.0\n'

def test_plus_string():
    assert run_test('print "hello" + "world";') == "helloworld\n"

def test_minus():
    assert run_test("print 1 - 1;") == '0.0\n'

def test_star():
    assert run_test("print 2 * 2;") == '4.0\n'

def test_slash():
    assert run_test("print 4 / 2;") == '2.0\n'

def test_mod():
    assert run_test("print 3 % 2;") == '1.0\n'

def test_bang():
    assert run_test("print !false;") == 'True\n'

def test_greater_equal():
    assert run_test("print 3 >= 2;") == 'True\n'
    assert run_test("print 3 >= 3;") == 'True\n'
    assert run_test("print 3 >= 10;") == 'False\n'

def test_greater():
    assert run_test("print 3 > 1;") == 'True\n'
    assert run_test("print 3 > 10;") == 'False\n'

def test_lesser_equal():
    assert run_test("print 3 <= 5;") == 'True\n'
    assert run_test("print 3 <= 1;") == 'False\n'

def test_lesser():
    assert run_test("print 3 < 5;") == 'True\n'
    assert run_test("print 3 < 1;") == 'False\n'

def test_grouped_math():
    assert run_test("print ( 1 + 1 ) + ( 4 * 4 );") == '18.0\n'

def test_complex_math():
    assert run_test("print (1 / 5 + 4 / 1 + ( 4 + 4)) * 2;") == '24.4\n'

def test_logical_basic():
    assert run_test("print true and true;") == 'True\n'
    assert run_test("print true and false;") == 'False\n'
    assert run_test("print true or false;") == 'True\n'
    assert run_test("print false or false;") == 'False\n'

def test_logical_returns_operand():
    assert run_test('print "hello" and "world";') == "world\n"
    assert run_test("print nil and nil;") == 'None\n'
    assert run_test("print nil or false;") == 'False\n'
    assert run_test('print false or "x";') == "x\n"
    assert run_test("print false and 42;") == 'False\n'
    assert run_test("print 0 and 1;") == '1.0\n'
    assert run_test("print 0 or nil;") == '0.0\n'

def test_conditional():
    assert run_test('print (1 < 4) ? 5 : 4;') == '5.0\n'
    assert run_test('print (false) ? 5 : 4;') == '4.0\n'
    assert run_test('print (1 == 1) ? 10 : 4;') == '10.0\n'
    assert run_test('print (110 >= 110) ? "hello" : "world";') == "hello\n"

def test_if():
    assert run_test('if (1 > 0) print 5;') == '5.0\n'
    assert run_test('if (1 < 0) print 5; else print 3;') == '3.0\n'