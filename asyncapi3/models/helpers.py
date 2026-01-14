__all__ = ["EmailStr", "is_null", "validate_patterned_key"]

import re

from typing import Any

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import CoreSchema, core_schema


def is_null(value: Any) -> bool:
    """
    Evaluates whether the provided input is equal to None, returning True if it is
    and False otherwise.
    """
    return value is None


def validate_patterned_key(key: str, object_name: str = "object") -> None:
    """
    Validate that a key matches the AsyncAPI patterned key pattern.

    Args:
        key: The key to validate.
        object_name: Name of the object type for error message (e.g., "server",
            "channel").

    Raises:
        ValueError: If the key does not match the required pattern.
    """
    pattern = re.compile(r"^[A-Za-z0-9_\-]+$")
    if not pattern.match(key):
        raise ValueError(
            f"Field '{key}' does not match patterned object key pattern. "
            "Keys must contain letters, digits, hyphens, and underscores."
        )


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
