from .core.scanner import Scanner


def main() -> None:
    scanner = Scanner("1.3458 + 1")
    scanner.scan()
    print(scanner.tokens)


if __name__ == "__main__":
    main()
