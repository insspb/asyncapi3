"""Managers for handling reusable server objects in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["ServersManager"]


from typing import TYPE_CHECKING

from asyncapi3.managers.protocols import ProcessorProtocol
from asyncapi3.models.base import Reference
from asyncapi3.models.components import Components
from asyncapi3.models.server import Server, Servers

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class ServersManager(ProcessorProtocol):
    """
    Manager for handling Server objects in AsyncAPI specification.

    This manager ensures that all Server objects are stored in components/servers
    and replaced with Reference objects throughout the specification.
    Duplicate servers with the same name are not allowed.
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """
        Process servers in the AsyncAPI specification.

        Moves all servers from root to components/servers, replaces them with
        references, and ensures no duplicate server names exist.

        Args:
            spec: The AsyncAPI3 specification to process

        Returns:
            The modified AsyncAPI3 specification
        """
        self._ensure_components_servers_exist(spec)

        self._process_root_servers(spec)

        return spec

    def _ensure_components_servers_exist(self, spec: AsyncAPI3) -> None:
        """
        Ensure that components and servers section exist in the specification.

        Creates components with servers if components doesn't exist.
        Adds servers to existing components if servers section is missing.
        """
        if not spec.components:
            spec.components = Components(servers=Servers({}))
        elif not spec.components.servers:
            spec.components.servers = Servers({})

    def _process_root_servers(self, spec: AsyncAPI3) -> None:
        """Process servers in the root servers object."""
        if not spec.servers:
            return

        processed_servers: dict[str, Server | Reference] = {}

        for server_name, server in spec.servers.root.items():
            if isinstance(server, Reference):
                processed_servers[server_name] = server
                continue

            if isinstance(server, Server):
                self._ensure_is_unique_server(spec, server_name, server)
                self._add_server_to_components(spec, server_name, server)
                processed_servers[server_name] = Reference.to_component_server_name(
                    server_name
                )

        spec.servers.root = processed_servers

    def _ensure_is_unique_server(
        self,
        spec: AsyncAPI3,
        server_name: str,
        server: Server | Reference,
    ) -> None:
        """
        Ensure that a server with the given name doesn't already exist with different
        content.

        Args:
            spec: The AsyncAPI3 specification
            server_name: Name/key for the server to check
            server: Server object to validate for uniqueness

        Raises:
            ValueError: If a server with the same name but different content already
                exists
        """
        if not spec.components or not spec.components.servers:  # mypy types protection
            return

        if server_name in spec.components.servers.root:
            existing_server = spec.components.servers.root[server_name]
            if existing_server != server:
                raise ValueError(
                    f"Server name conflict detected: '{server_name}' already exists "
                    f"with different content. "
                    f"Existing: {existing_server.model_dump()}, "
                    f"New: {server.model_dump()}. Server names must be unique."
                )
            return

    def _add_server_to_components(
        self,
        spec: AsyncAPI3,
        server_name: str,
        server: Server,
    ) -> None:
        """
        Add a server to the components/servers section.

        Args:
            spec: The AsyncAPI3 specification
            server_name: Name/key for the server
            server: Server object to add
        """
        spec.components.servers.root[server_name] = server  # type: ignore[union-attr]
