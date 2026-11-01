"""Small helper functions for the command-line application."""

from datetime import date


def today_iso() -> str:
    """Return today's date in ISO format."""
    return date.today().isoformat()


def prompt_non_empty(prompt: str) -> str:
    """Prompt until the user enters a non-empty value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")
