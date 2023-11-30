"""utils.py contains utils functions for main.py
"""


def value_error_decorator(func):
    """Wrap function in value error try-except block"""

    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except ValueError as e:
            print(f"Error: {e}")

    return wrapper


def int_(num: str) -> int:
    """Convert string to int while checking for null"""
    return int(num) if num else 0


def float_(num: str) -> float:
    """Convert string to float while checking for null"""
    return float(num) if num else 0.0
