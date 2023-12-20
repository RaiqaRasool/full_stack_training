from slugify import slugify
from typing import Any

def validate_float(data: str) -> float:
    return float(data.replace(",",""))

def generate_slug(title: str) -> Any:
    return slugify(title)

