"""Validator for server variable references in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["ServerVariablesRefValidator"]

from typing import TYPE_CHECKING

from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class ServerVariablesRefValidator(ProcessorProtocol):
    """
    Validator for server variable references.

    This validator should be implemented to validate references to server variables
    in various objects.
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """Validate server variable references."""
        return spec
