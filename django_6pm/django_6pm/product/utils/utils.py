from typing import Any

from slugify import slugify


def validate_float(data: str) -> float:
    return float(data.replace(",", ""))


def generate_slug(title: str) -> str:
    return slugify(title)
