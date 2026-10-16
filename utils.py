"""
utils.py - Helper functions for safe user input (exception handling)
Project  : Student Management System
Author   : Dipeeka Patidar
"""
import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


def get_text(prompt, allow_empty=False):
    """Keep asking until the user types some text."""
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        print("  [!] Input cannot be empty. Please try again.")


def get_name(prompt, allow_empty=False):
    """Name must contain only letters and spaces."""
    while True:
        value = input(prompt).strip()
        if not value and allow_empty:
            return value
        if value and all(ch.isalpha() or ch.isspace() for ch in value):
            return " ".join(value.split()).title()
        print("  [!] Name should contain only letters and spaces.")


def get_int(prompt, min_value=None, max_value=None, allow_empty=False):
    """Keep asking until a valid whole number (within range) is typed."""
    while True:
        raw = input(prompt).strip()
        if raw == "" and allow_empty:
            return None
        try:
            number = int(raw)
        except ValueError:
            print("  [!] Invalid input. Please enter a whole number.")
            continue
        if min_value is not None and number < min_value:
            print(f"  [!] Value must be at least {min_value}.")
            continue
        if max_value is not None and number > max_value:
            print(f"  [!] Value must be at most {max_value}.")
            continue
        return number


def get_float(prompt, min_value=None, max_value=None, allow_empty=False):
    """Keep asking until a valid number (within range) is typed."""
    while True:
        raw = input(prompt).strip()
        if raw == "" and allow_empty:
            return None
        try:
            number = float(raw)
        except ValueError:
            print("  [!] Invalid input. Please enter a number.")
            continue
        if min_value is not None and number < min_value:
            print(f"  [!] Value must be at least {min_value}.")
            continue
        if max_value is not None and number > max_value:
            print(f"  [!] Value must be at most {max_value}.")
            continue
        return number


def get_password(prompt):
    """Password input (visible on screen so it is easy to type)."""
    return input(prompt)


def confirm(prompt):
    answer = input(f"{prompt} (y/n): ").strip().lower()
    return answer in ("y", "yes")
