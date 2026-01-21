"""Validator for parameter references in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["ParametersRefValidator"]

from typing import TYPE_CHECKING

from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class ParametersRefValidator(ProcessorProtocol):
    """
    Validator for parameter references.

    This validator should be implemented to validate references to parameters
    in various objects.
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """Validate parameter references."""
        return spec
