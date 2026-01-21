"""Validator for channel bindings references in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["ChannelBindingsRefValidator"]

from typing import TYPE_CHECKING

from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class ChannelBindingsRefValidator(ProcessorProtocol):
    """
    Validator for channel bindings references.

    This validator should be implemented to validate references to channel bindings
    in various objects.
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """Validate channel bindings references."""
        return spec
