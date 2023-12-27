from typing import Any

from slugify import slugify

from product.constants import Color


def validate_float(data: str) -> float:
    return float(data.replace(",", ""))


def generate_slug(title: str) -> str:
    return slugify(title)


def print_status_msg(msg: str, status: str = "success") -> None:
    if status == "error":
        print(Color.RED.value + msg + Color.RESET.value)
    else:
        print(Color.GREEN.value + msg + Color.RESET.value)


def generate_mapping(data, key):
    data_mapping = {}
    for item in data:
        data_mapping[getattr(item, key)] = item
    return data_mapping
