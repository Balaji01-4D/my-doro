"""Command-line entry point for the MyDoro application."""
from mydoro.main import parse_arguments, main

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
