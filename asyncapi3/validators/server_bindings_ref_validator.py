"""Validator for server bindings references in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["ServerBindingsRefValidator"]

import logging

from typing import TYPE_CHECKING

from asyncapi3.models.base import Reference
from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class ServerBindingsRefValidator(ProcessorProtocol):
    """
    Validator for server bindings references.

    This validator should be implemented to validate references to server bindings
    in various objects.
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """
        Validate server binding references in the AsyncAPI specification.

        Args:
            spec: The AsyncAPI3 specification to validate

        Returns:
            The validated AsyncAPI3 specification

        Raises:
            ValueError: If server binding references are invalid
        """
        self._validate_root_servers_bindings_refs(spec)
        self._validate_components_servers_bindings_refs(spec)
        self._validate_components_server_bindings_refs(spec)

        return spec

    def _validate_root_servers_bindings_refs(self, spec: AsyncAPI3) -> None:
        """Validate server binding references in root servers."""
        if not spec.servers:
            return

        for server_name, server in spec.servers.root.items():
            if not hasattr(server, "bindings"):
                continue
            if not isinstance(server.bindings, Reference):
                continue
            self._validate_server_binding_ref(
                spec, server.bindings, f"server '{server_name}'"
            )

    def _validate_components_servers_bindings_refs(self, spec: AsyncAPI3) -> None:
        """Validate server binding references in components servers."""
        if not spec.components or not spec.components.servers:
            return

        for server_name, server in spec.components.servers.root.items():
            if not hasattr(server, "bindings"):
                continue
            if not isinstance(server.bindings, Reference):
                continue
            self._validate_server_binding_ref(
                spec, server.bindings, f"components server '{server_name}'"
            )

    def _validate_components_server_bindings_refs(self, spec: AsyncAPI3) -> None:
        """Validate server binding references within components server bindings."""
        if not spec.components or not spec.components.server_bindings:
            return

        for binding_name, binding in spec.components.server_bindings.root.items():
            if not isinstance(binding, Reference):
                continue
            self._validate_server_binding_ref(
                spec, binding, f"components server binding '{binding_name}'"
            )

    def _validate_server_binding_ref(
        self, spec: AsyncAPI3, binding_ref: Reference, context: str
    ) -> None:
        """
        Validate a single server binding reference.

        Args:
            spec: The AsyncAPI3 specification
            binding_ref: The server binding reference to validate
            context: Context string for error messages

        Raises:
            ValueError: If the server binding reference is invalid
        """
        ref_value = binding_ref.ref

        if not ref_value.startswith("#"):
            logging.warning(
                f"{context.capitalize()} binding reference '{ref_value}' is external. "
                "Cannot validate external references."
            )
            return

        if not ref_value.startswith("#/components/serverBindings/"):
            raise ValueError(
                f"{context.capitalize()} binding reference '{ref_value}' must point to "
                "#/components/serverBindings/ but points elsewhere."
            )

        binding_key = ref_value.replace("#/components/serverBindings/", "")
        if (
            not spec.components
            or not spec.components.server_bindings
            or binding_key not in spec.components.server_bindings.root
        ):
            raise ValueError(
                f"{context.capitalize()} references binding '{binding_key}' but "
                "binding does not exist in components/serverBindings."
            )
