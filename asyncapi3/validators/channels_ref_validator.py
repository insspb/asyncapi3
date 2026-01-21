"""Validator for channels references in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["ChannelsRefValidator"]

from typing import TYPE_CHECKING

from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class ChannelsRefValidator(ProcessorProtocol):
    """
    Validator for channels references.

    This validator should be implemented to validate references to channels
    in various objects.
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """Validate channels references."""
        return spec
