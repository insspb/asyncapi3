"""Validators for server references in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["ServersRefValidator"]

import logging

from typing import TYPE_CHECKING

from asyncapi3.models.base import Reference
from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class ServersRefValidator(ProcessorProtocol):
    """
    Validator for server references in AsyncAPI specification.

    This validator checks that all server references are valid:
    - Root servers references must be local and point to components/servers
    - Root channels servers references must point to root servers
    - Components channels may reference servers from any location
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """
        Validate server references in the AsyncAPI specification.

        Args:
            spec: The AsyncAPI3 specification to validate

        Returns:
            The validated AsyncAPI3 specification

        Raises:
            ValueError: If server references are invalid
        """
        self._validate_root_servers_refs(spec)
        self._validate_channels_servers_refs(spec)
        self._validate_components_channels_servers_refs(spec)

        return spec

    def _validate_root_servers_refs(self, spec: AsyncAPI3) -> None:
        """Validate references in root servers object."""
        if not spec.servers:
            return

        for server_name, server in spec.servers.root.items():
            if isinstance(server, Reference):
                ref_value = server.ref
            else:
                continue

            if not ref_value.startswith("#"):
                logging.warning(
                    f"Server '{server_name}' contains external reference '{ref_value}'."
                    " Cannot validate external references."
                )
                continue

            if not ref_value.startswith("#/components/servers/"):
                raise ValueError(
                    f"Server '{server_name}' reference '{ref_value}' must point to "
                    "#/components/servers/ but points elsewhere."
                )

            server_key = ref_value.replace("#/components/servers/", "")
            if (
                not spec.components
                or not spec.components.servers
                or server_key not in spec.components.servers.root
            ):
                raise ValueError(
                    f"Server '{server_name}' references '{ref_value}' but server "
                    f"'{server_key}' does not exist in components/servers."
                )

    def _validate_channels_servers_refs(self, spec: AsyncAPI3) -> None:
        """Validate server references in root channels."""
        if not spec.channels:
            return

        for channel_name, channel in spec.channels.root.items():
            if not hasattr(channel, "servers") or not channel.servers:
                continue

            for server_ref in channel.servers:
                ref_value = server_ref.ref

                if not ref_value.startswith("#"):
                    logging.warning(
                        f"Channel '{channel_name}' server reference '{ref_value}' "
                        f"is external. Cannot validate external references."
                    )
                    continue

                if not ref_value.startswith("#/servers/"):
                    raise ValueError(
                        f"Channel '{channel_name}' server reference '{ref_value}' "
                        f"must point to #/servers/ but points to '{ref_value}'."
                    )

                server_key = ref_value.replace("#/servers/", "")
                if not spec.servers or server_key not in spec.servers.root:
                    raise ValueError(
                        f"Channel '{channel_name}' references server '{server_key}' "
                        f"but server does not exist in root servers."
                    )

    def _validate_components_channels_servers_refs(self, spec: AsyncAPI3) -> None:
        """Validate server references in components channels."""
        if not spec.components or not spec.components.channels:
            return

        for channel_name, channel in spec.components.channels.root.items():
            if not hasattr(channel, "servers") or not channel.servers:
                continue

            for server_ref in channel.servers:
                ref_value = server_ref.ref

                if not ref_value.startswith("#"):
                    logging.warning(
                        f"Components channel '{channel_name}' server reference "
                        f"'{ref_value}' is external. "
                        "Cannot validate external references."
                    )
                    continue

                if ref_value.startswith("#/servers/"):
                    server_key = ref_value.replace("#/servers/", "")
                    if not spec.servers or server_key not in spec.servers.root:
                        raise ValueError(
                            f"Components channel '{channel_name}' references root "
                            f"server '{server_key}' but server does not exist in root "
                            f"servers."
                        )
                elif ref_value.startswith("#/components/servers/"):
                    server_key = ref_value.replace("#/components/servers/", "")
                    if (
                        not spec.components.servers
                        or server_key not in spec.components.servers.root
                    ):
                        raise ValueError(
                            f"Components channel '{channel_name}' references components"
                            f" server '{server_key}' but server does not exist in "
                            f"components/servers."
                        )
                else:
                    raise ValueError(
                        f"Components channel '{channel_name}' server reference "
                        f"'{ref_value}' must point to #/servers/ or "
                        f"#/components/servers/ but points elsewhere."
                    )
