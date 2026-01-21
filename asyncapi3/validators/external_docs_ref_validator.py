"""Validator for external documentation references in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["ExternalDocsRefValidator"]

from typing import TYPE_CHECKING

from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class ExternalDocsRefValidator(ProcessorProtocol):
    """
    Validator for external documentation references.

    This validator should be implemented to validate references to external
    documentation in various objects.
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """Validate external documentation references."""
        return spec
