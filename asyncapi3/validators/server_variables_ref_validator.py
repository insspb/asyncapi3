"""Validators for server variable references in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["ServerVariablesRefValidator"]

import logging

from typing import TYPE_CHECKING

from asyncapi3.models.base import Reference
from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class ServerVariablesRefValidator(ProcessorProtocol):
    """
    Validator for server variable references in AsyncAPI specification.

    This validator checks that all server variable references are valid:
    - Server variable references in servers and components must point to
      existing server variables in root servers or components/serverVariables
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """
        Validate server variable references in the AsyncAPI specification.

        Args:
            spec: The AsyncAPI3 specification to validate

        Returns:
            The validated AsyncAPI3 specification

        Raises:
            ValueError: If server variable references are invalid
        """
        self._validate_root_servers_variables_refs(spec)
        self._validate_components_servers_variables_refs(spec)
        self._validate_components_server_variables_refs(spec)

        return spec

    def _validate_root_servers_variables_refs(self, spec: AsyncAPI3) -> None:
        """Validate server variable references in root servers."""
        if not spec.servers:
            return

        for server_name, server in spec.servers.root.items():
            if not hasattr(server, "variables") or not server.variables:
                continue

            for var_name, var in server.variables.items():
                if not isinstance(var, Reference):
                    continue
                self._validate_server_variable_ref(
                    spec,
                    var,
                    f"server '{server_name}' variable '{var_name}'",
                )

    def _validate_components_servers_variables_refs(self, spec: AsyncAPI3) -> None:
        """Validate server variable references in components servers."""
        if not spec.components or not spec.components.servers:
            return

        for server_name, server in spec.components.servers.root.items():
            if not hasattr(server, "variables") or not server.variables:
                continue

            for var_name, var in server.variables.items():
                if not isinstance(var, Reference):
                    continue
                self._validate_server_variable_ref(
                    spec,
                    var,
                    f"components server '{server_name}' variable '{var_name}'",
                )

    def _validate_components_server_variables_refs(self, spec: AsyncAPI3) -> None:
        """Validate server variable references within components server variables."""
        if not spec.components or not spec.components.server_variables:
            return

        for var_name, var in spec.components.server_variables.root.items():
            if not isinstance(var, Reference):
                continue
            self._validate_server_variable_ref(
                spec, var, f"components server variable '{var_name}'"
            )

    def _validate_server_variable_ref(
        self, spec: AsyncAPI3, var_ref: Reference, context: str
    ) -> None:
        """
        Validate a single server variable reference.

        Args:
            spec: The AsyncAPI3 specification
            var_ref: The server variable reference to validate
            context: Context string for error messages

        Raises:
            ValueError: If the server variable reference is invalid
        """
        ref_value = var_ref.ref

        if not ref_value.startswith("#"):
            logging.warning(
                f"{context.capitalize()} reference '{ref_value}' is external. "
                "Cannot validate external references."
            )
            return

        if ref_value.startswith("#/servers/"):
            self._validate_root_server_variable_ref(spec, ref_value, context)
        elif ref_value.startswith("#/components/servers/"):
            self._validate_components_server_variable_ref(spec, ref_value, context)
        elif ref_value.startswith("#/components/serverVariables/"):
            var_key = ref_value.replace("#/components/serverVariables/", "")
            if (
                not spec.components
                or not spec.components.server_variables
                or var_key not in spec.components.server_variables.root
            ):
                raise ValueError(
                    f"{context.capitalize()} references '{ref_value}' but server "
                    f"variable '{var_key}' does not exist in "
                    "#/components/serverVariables."
                )
        else:
            raise ValueError(
                f"{context.capitalize()} reference '{ref_value}' must point to "
                "#/servers/{server}/variables/{var}, "
                "#/components/servers/{server}/variables/{var} or "
                "#/components/serverVariables/{var} but points elsewhere."
            )

    def _validate_root_server_variable_ref(
        self, spec: AsyncAPI3, ref_value: str, context: str
    ) -> None:
        """
        Validate reference to a root server variable.

        Args:
            spec: The AsyncAPI3 specification
            ref_value: The reference value (e.g., "#/servers/prod/variables/port")
            context: Context string for error messages

        Raises:
            ValueError: If the reference is invalid
        """
        # Expected format: #/servers/{server_name}/variables/{var_name}
        parts = ref_value.split("/")
        if len(parts) != 5 or parts[1] != "servers" or parts[3] != "variables":
            raise ValueError(
                f"{context.capitalize()} reference '{ref_value}' must follow the "
                "format #/servers/{server}/variables/{var}."
            )

        server_name = parts[2]
        var_name = parts[4]

        if not spec.servers or server_name not in spec.servers.root:
            raise ValueError(
                f"{context.capitalize()} references server '{server_name}' but server "
                f"does not exist in root servers."
            )

        server = spec.servers.root[server_name]
        if not hasattr(server, "variables") or not server.variables:
            raise ValueError(
                f"{context.capitalize()} references server '{server_name}' variable "
                f"'{var_name}' but server has no variables."
            )

        if var_name not in server.variables:
            raise ValueError(
                f"{context.capitalize()} references server '{server_name}' variable "
                f"'{var_name}' but variable does not exist."
            )

    def _validate_components_server_variable_ref(
        self, spec: AsyncAPI3, ref_value: str, context: str
    ) -> None:
        """
        Validate reference to a components server variable.

        Args:
            spec: The AsyncAPI3 specification
            ref_value: The reference value
                (e.g., "#/components/servers/prod/variables/port")
            context: Context string for error messages

        Raises:
            ValueError: If the reference is invalid
        """
        # Expected format: #/components/servers/{server_name}/variables/{var_name}
        parts = ref_value.split("/")
        if (
            len(parts) != 6
            or parts[1] != "components"
            or parts[2] != "servers"
            or parts[4] != "variables"
        ):
            raise ValueError(
                f"{context.capitalize()} reference '{ref_value}' must follow the "
                "format #/components/servers/{server}/variables/{var}."
            )

        server_name = parts[3]
        var_name = parts[5]

        if not spec.components or not spec.components.servers:
            raise ValueError(
                f"{context.capitalize()} references components server '{server_name}' "
                f"but components servers do not exist."
            )

        if server_name not in spec.components.servers.root:
            raise ValueError(
                f"{context.capitalize()} references components server '{server_name}' "
                f"but server does not exist in components/servers."
            )

        server = spec.components.servers.root[server_name]
        if not hasattr(server, "variables") or not server.variables:
            raise ValueError(
                f"{context.capitalize()} references components server '{server_name}' "
                f"variable '{var_name}' but server has no variables."
            )

        if var_name not in server.variables:
            raise ValueError(
                f"{context.capitalize()} references components server '{server_name}' "
                f"variable '{var_name}' but variable does not exist."
            )
