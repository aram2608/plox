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


def run(source: str):
    scanner = Scanner(source)
    toks = scanner.scan_tokens()
    parser = Parser(toks)
    ast = parser.parse()
    interpreter = Interpreter()
    interpreter.interpret(ast[0])


def run_file(path: Path):
    try:
        run(source=slurp_file(path))
    except Exception as e:
        print(e)


# def repl():
#     while True:
#         source = input("> ")
#         if source == "exit":
#             break
#         scanner = Scanner(source)
#         toks = scanner.scan_tokens()
#         parser = Parser(toks)
#         ast = parser.parse()


def main(file: Path) -> None:
    if file:
        run_file(file)
    else:
        print("REPL not implemented")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, default=None, help="Path to Lox file.")
    args = parser.parse_args()
    main(args.file)
