"""Command-line entry point for the Doro application."""
from doro.main import parse_arguments, main

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
