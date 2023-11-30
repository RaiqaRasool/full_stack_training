"""utils.py contains utils functions for main.py
"""


def year_boundary_check(year: int) -> bool:
    """
    Return true if year is between 2004 and 2016
    and false otherwise
    """
    if year and 2004 <= year <= 2016:
        return True
    return False


def int_(num: str) -> int:
    """Convert string to int while checking for null"""
    return int(num) if num else 0


def float_(num: str) -> float:
    """Convert string to float while checking for null"""
    return float(num) if num else 0.0
