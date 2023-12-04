"""utils.py contains utils functions for main.py
"""
from datetime import datetime


def validate_int(num: str) -> int:
    """Convert string to int while checking for null"""
    return int(num) if num else 0


def validate_float(num: str) -> float:
    """Convert string to float while checking for null"""
    return float(num) if num else 0.0


def validate_date(value: str, date_format: str = "%Y/%m") -> datetime:
    """Validate date with its format while converting it into datetime object"""
    return datetime.strptime(value, date_format)

