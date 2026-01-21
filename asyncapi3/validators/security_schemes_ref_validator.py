"""Validator for security scheme references in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["SecuritySchemesRefValidator"]

from typing import TYPE_CHECKING

from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class SecuritySchemesRefValidator(ProcessorProtocol):
    """
    Validator for security scheme references.

    This validator should be implemented to validate references to security schemes
    in various objects.
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """Validate security scheme references."""
        return spec
