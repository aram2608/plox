from .core.scanner import Scanner
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


def run_file(path: Path):
    source = slurp_file(path)
    if source != None:
        scanner = Scanner(source=slurp_file(path))
        try:
            toks = scanner.scan_tokens()
        except Exception as e:
            print(e)
        else:
            for tok in toks:
                print(tok)
    else:
        print("Aborting execution.")
        sys.exit()


def run_scanner(source: str):
    scanner = Scanner(source)
    toks = scanner.scan_tokens()
    return toks


def repl():
    while True:
        source = input("> ")
        if source == "exit":
            break
        scanner = Scanner(source)
        toks = scanner.scan_tokens()


def main(file: Path) -> None:
    if file:
        run_file(file)
    else:
        repl()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, default=None, help="Path to Lox file.")
    args = parser.parse_args()
    main(args.file)
