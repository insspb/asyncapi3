"""Validator for operation bindings references in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["OperationBindingsRefValidator"]

from typing import TYPE_CHECKING

from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class OperationBindingsRefValidator(ProcessorProtocol):
    """
    Validator for operation bindings references.

    This validator should be implemented to validate references to operation bindings
    in various objects.
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """Validate operation bindings references."""
        return spec
