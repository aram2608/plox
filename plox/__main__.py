from .core.scanner import Scanner
from pathlib import Path
import argparse


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
        raise SystemExit(1)


def main(file: Path) -> None:
    if file:
        run_file(file)
    else:
        print("No file provided.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    main(args.path)
