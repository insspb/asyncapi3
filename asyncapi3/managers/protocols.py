"""Protocols definitions for AsyncAPI specification processors."""

from __future__ import annotations

__all__ = ["ProcessorProtocol"]


from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


@runtime_checkable
class ProcessorProtocol(Protocol):
    """Protocol for processors that handle AsyncAPI specification processing."""

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """
        Process and optimize the given AsyncAPI specification.

        This method should check all relevant objects in the specification,
        move duplicate objects to components, and replace them with references.

        Args:
            spec: The AsyncAPI3 specification to process
        """
        ...
