"""Base model classes for AsyncAPI 3.0 specification."""

__all__ = ["ExtendableBaseModel", "NonExtendableBaseModel"]

import re

from pydantic import BaseModel, ConfigDict, model_validator


class ExtendableBaseModel(BaseModel):
    """
    Base model that allows specification extensions.

    Extensions are fields prefixed with "x-" that follow the pattern
    ^x-[\\w\\d\\.\\x2d_]+$. This model allows extra fields and validates that any
    additional fields match the extension pattern.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    @model_validator(mode="after")
    def validate_extensions(self) -> "ExtendableBaseModel":
        """
        Validate that any extra fields match the specification extension pattern.

        Extensions must start with "x-" and follow the regex pattern
        ^x-[\\w\\d\\.\\x2d_]+$.
        """
        if not self.model_extra:
            return self

        extension_pattern = re.compile(r"^x-[\w\d\.\x2d_]+$")
        for key in self.model_extra:
            if not extension_pattern.match(key):
                raise ValueError(
                    f"Field '{key}' does not match specification extension pattern. "
                    f"Extensions must start with 'x-' and contain only word "
                    f"characters, digits, dots, hyphens, and underscores."
                )
        return self


class NonExtendableBaseModel(BaseModel):
    """
    Base model that does not allow specification extensions or extra fields.

    This model forbids any extra fields beyond those explicitly defined.
    """

    model_config = ConfigDict(
        extra="forbid",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )
