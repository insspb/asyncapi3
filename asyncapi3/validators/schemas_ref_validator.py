"""Validator for schemas references in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["SchemasRefValidator"]

from typing import TYPE_CHECKING

from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class SchemasRefValidator(ProcessorProtocol):
    """
    Validator for schemas references.

    This validator should be implemented to validate references to schemas
    in various objects.
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """Validate schemas references."""
        return spec
