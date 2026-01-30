__all__ = [
    "EmailStr",
    "is_null",
    "update_object_attributes",
    "validate_patterned_key",
]

import re

from types import EllipsisType
from typing import Any, TypeVar

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import CoreSchema, core_schema

UNSET = EllipsisType()
T = TypeVar("T")


def is_null(value: Any) -> bool:
    """
    Evaluates whether the provided input is equal to None, returning True if it is
    and False otherwise.
    """
    return value is None


def validate_patterned_key(key: str | Any, object_name: str = "object") -> None:
    """
    Validate that a key matches the AsyncAPI patterned key pattern.

    Args:
        key: The key to validate.
        object_name: Name of the object type for error message (e.g., "server",
            "channel").

    Raises:
        ValueError: If the key does not match the required pattern.
        TypeError: If the key is not a string.
    """
    pattern = re.compile(r"^[A-Za-z0-9_\-]+$")
    try:
        if not pattern.match(key):
            raise ValueError(
                f"Field '{key}' does not match patterned object key pattern. "
                "Keys must contain letters, digits, hyphens, and underscores."
            )
    except TypeError as error:
        raise TypeError(
            f"Key '{key}' must be a string, got {type(key).__name__}"
        ) from error


def update_object_attributes(obj: T, **kwargs: Any) -> T:
    """
    Update object attributes conditionally, skipping UNSET values.

    This utility function updates attributes of any Python object by setting
    only those attributes whose values are not equal to the UNSET sentinel value.
    This allows distinguishing between "not provided" and "explicitly set to None"
    in builder patterns and update operations.

    Args:
        obj: The object to update (any Python object).
        **kwargs: Attribute name-value pairs to update. Values equal to UNSET
            are ignored, while other values (including None) are set on the object.

    Returns:
        The same object with updated attributes.
    """
    for field_name, value in kwargs.items():
        if value is not UNSET:
            setattr(obj, field_name, value)
    return obj


class EmailStr(str):
    """
    Custom email string type with built-in validation.

    Validates email format and provides type safety for email addresses.
    """

    @staticmethod
    def _validate_email(value: str) -> str:
        """Validate email format and return EmailStr instance."""
        # Email regex pattern that rejects consecutive dots
        pattern = r"^(?!.*\.\.)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email format")
        return value

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """
        Define Pydantic core schema for EmailStr validation.

        Uses string schema as base with after validator for email format checking.
        """
        return core_schema.no_info_after_validator_function(
            lambda value: cls(cls._validate_email(value)), handler(str)
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        """
        Define JSON schema for EmailStr.

        Adds format field to specify that this is an email string.
        """
        json_schema = handler(core_schema)
        json_schema.update({"format": "email"})
        return json_schema
