"""Base model classes for AsyncAPI 3.0 specification."""

__all__ = ["ExtendableBaseModel", "NonExtendableBaseModel", "PatternedRootModel"]

import re

from collections.abc import Iterator
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, RootModel, model_validator

from asyncapi3.models.helpers import validate_patterned_key

T = TypeVar("T")


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


class PatternedRootModel(RootModel[dict[str, T]], Generic[T]):
    """
    Base class for AsyncAPI patterned objects that validate key patterns.

    This model validates that all keys match the AsyncAPI patterned object key pattern
    ^[A-Za-z0-9_\\-]+$.
    """

    model_config = ConfigDict(
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    def __iter__(self) -> Iterator[str]:  # type: ignore[override]
        return iter(self.root)

    def __getitem__(self, item: str) -> T:
        return self.root[item]

    def __setitem__(self, key: str, value: T) -> None:
        self.root[key] = value

    def __delitem__(self, key: str) -> None:
        del self.root[key]

    def __contains__(self, key: str) -> bool:
        return key in self.root

    def __len__(self) -> int:
        return len(self.root)

    @model_validator(mode="after")
    def validate_patterned_keys(self) -> "PatternedRootModel[T]":
        """
        Validate that all keys in the input data match the AsyncAPI patterned
        object key pattern.

        Keys must match the regex pattern ^[A-Za-z0-9_\\-]+$
        """
        if not self.root:
            return self

        for field_name in self.root:
            validate_patterned_key(field_name, "object")
        return self
