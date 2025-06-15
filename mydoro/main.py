"""Main entry point for the MyDoro application."""
import argparse
from mydoro.app import main
from mydoro import __version__


def parse_arguments():
    """Parse command line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="MyDoro - A modern Pomodoro timer for your terminal"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version=f"MyDoro {__version__}",
        help="Show version information and exit"
    )
    parser.add_argument(
        "--pomodoro", 
        type=int, 
        help="Set pomodoro duration in minutes"
    )
    parser.add_argument(
        "--short-break", 
        type=int, 
        help="Set short break duration in minutes"
    )
    parser.add_argument(
        "--long-break", 
        type=int, 
        help="Set long break duration in minutes"
    )
    parser.add_argument(
        "--cycles", 
        type=int, 
        help="Set number of cycles before a long break"
    )
    parser.add_argument(
        "--theme", 
        type=str, 
        choices=["dracula", "monokai", "github_dark", "github_light"],
        help="Set the application theme"
    )
    
    return parser.parse_args()


def main_cli():
    """Entry point for the CLI script."""
    args = parse_arguments()
    main(args)


if __name__ == "__main__":
    main_cli()
