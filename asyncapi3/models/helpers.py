__all__ = ["is_null"]

from typing import Any


def is_null(value: Any) -> bool:
    """
    Evaluates whether the provided input is equal to None, returning True if it is
    and False otherwise.
    """
    return value is None
