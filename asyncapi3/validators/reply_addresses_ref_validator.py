"""Validator for reply address references in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["ReplyAddressesRefValidator"]

from typing import TYPE_CHECKING

from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class ReplyAddressesRefValidator(ProcessorProtocol):
    """
    Validator for reply address references.

    This validator should be implemented to validate references to reply addresses
    in various objects.
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """Validate reply address references."""
        return spec
