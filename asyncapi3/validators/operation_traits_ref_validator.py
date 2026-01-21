"""Validator for operation trait references in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["OperationTraitsRefValidator"]

from typing import TYPE_CHECKING

from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class OperationTraitsRefValidator(ProcessorProtocol):
    """
    Validator for operation trait references.

    This validator should be implemented to validate references to operation traits
    in various objects.
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """Validate operation trait references."""
        return spec
