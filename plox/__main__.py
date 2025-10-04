from .core.scanner import Scanner
from .core.parser import Parser
from .core.interpreter import Interpreter
from pathlib import Path
import argparse
import sys


def slurp_file(path: Path) -> str | None:
    path = Path(path)
    try:
        with open(path, "r") as file:
            source = file.read()
    except Exception as e:
        print("File not found or could not be open", e)
        return None
    else:
        return source


def run_lox(source: str) -> None:
    scanner = Scanner(source)
    toks = scanner.scan_tokens()
    parser = Parser(toks)
    ast = parser.parse()
    interpreter = Interpreter()
    if ast:
        interpreter.interpret(ast)


def run_file(path: Path) -> int:
    try:
        run_lox(source=slurp_file(path))
    except Exception as e:
        print(e)
        return 1
    return 0


def repl() -> int:
    while True:
        source = input("> ")
        if source == "exit":
            break
        try:
            run_lox(source=source)
        except Exception as e:
            print(e)
            continue
    return 0


def main(argv=None) -> int | None:
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file", "-f", type=Path, default=None, help="Path to Lox file."
    )
    args = parser.parse_args(argv)

    if args.file:
        return run_file(args.file)
    else:
        return repl()


if __name__ == "__main__":
    raise SystemExit(main())
