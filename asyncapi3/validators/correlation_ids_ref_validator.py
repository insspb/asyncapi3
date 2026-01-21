"""Validator for correlation ID references in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["CorrelationIdsRefValidator"]

from typing import TYPE_CHECKING

from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class CorrelationIdsRefValidator(ProcessorProtocol):
    """
    Validator for correlation ID references.

    This validator should be implemented to validate references to correlation IDs
    in various objects.
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """Validate correlation ID references."""
        return spec
