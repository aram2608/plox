from .core.scanner import Scanner
from .core.parser import Parser
from .core.interpreter import Interpreter
from pathlib import Path
from typing_extensions import Annotated
import typer


def slurp_file(path: Path) -> str:
    """Helper function to slurp a file's contents."""
    # We cast to a path object just in case
    path = Path(path)
    # In a try block we attempt to open our file in read mode and extract the
    # contents
    # If any errors are caught we return an empty string so our scanner does not
    # get choked up
    try:
        with open(path, "r") as file:
            source = file.read()
    except Exception as e:
        print("File not found or could not be opened", e)
        return ""
    else:
        return source


def run_lox(source: str) -> None:
    """Helper function to wrap the basic Lox runtime components together."""
    # We initialize our scanner with the source code and attempt to create tokens
    scanner = Scanner(source)
    toks = scanner.scan_tokens()
    # We can then intialize our parser and attempt to make an ast
    parser = Parser(toks)
    ast = parser.parse()
    # We can then create an instance of our Interpreter and try to interpret the
    # provided ast if its not empty
    interpreter = Interpreter()
    if ast:
        interpreter.interpret(ast)


def run_file(path: Path) -> int:
    """Method to wrap the run_lox function so it works with a provided file"""
    # In a try block we attempt to interpret the provided source code
    try:
        run_lox(source=slurp_file(path))
    # If we catch an error we return a 1 exit code
    except Exception as e:
        print(e)
        return 1
    # Otherwise we return a 0 for successful exit
    return 0


def repl() -> int:
    """Method to wrap the run_lox function into REPL format."""
    # We initialize a list of exit code the user can use to gracefully leave the
    # progam
    QUIT_CODES = ["exit()", "exit", "quit", "quit()"]
    print("Welcome to the Lox REPL!")
    # We create an infinite loop to continuously parse Lox code
    while True:
        source = input(">>> ")
        if source in QUIT_CODES:
            break
        # We try to run the lox code and catch any exceptions
        # We don't exit since the REPL needs to run for as long as the user want
        try:
            run_lox(source=source)
        except Exception as e:
            print(e)
            continue
    # Once the REPL session is over we return a succes exit code
    return 0

app = typer.Typer()

@app.command()
def main(file: Annotated[Path, typer.Option()] = None) -> int:
    """
    Command line entry point for the Lox programming language.
    Options:
        --file: A command line option for providing a Lox Script
    Usage:
        lox: Fires up the Lox REPL
        lox --file my_example_script.lox: Load in a Lox file for interpretting
    """
    if file:
        return run_file(file)
    else:
        return repl()


if __name__ == "__main__":
    # We raise a system exit
    # This is a bit lower level of a concept but for every C/C++ program an int
    # is returned given the success of execution
    # Sucessful programs return 0, non-0 exit codes are usually errors of some kind
    raise SystemExit(app())
