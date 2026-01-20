"""Managers for handling reusable channel parameter objects."""

from __future__ import annotations

__all__ = ["ChannelParametersManager"]


from typing import TYPE_CHECKING

from asyncapi3.models.base import Reference
from asyncapi3.models.channel import Parameter, Parameters
from asyncapi3.models.components import Components
from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class ChannelParametersManager(ProcessorProtocol):
    """
    Manager for handling Parameter objects in channel parameters.

    This manager ensures that all Parameter objects in channels are stored in
    components/parameters and replaced with Reference objects throughout
    the specification. Duplicate parameters with the same name are not allowed.
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """
        Process channel parameters in the AsyncAPI specification.

        Moves all parameters from channels to components/parameters, replaces them with
        references, and ensures no duplicate parameter names exist.

        Args:
            spec: The AsyncAPI3 specification to process

        Returns:
            The modified AsyncAPI3 specification
        """
        self._ensure_components_parameters_exist(spec)

        self._process_root_channels_parameters(spec)
        self._process_components_channels_parameters(spec)

        return spec

    def _ensure_components_parameters_exist(self, spec: AsyncAPI3) -> None:
        """
        Ensure that components and parameters section exist in the specification.

        Creates components with parameters if components doesn't exist.
        Adds parameters to existing components if parameters section is missing.
        """
        if not spec.components:
            spec.components = Components(parameters=Parameters({}))
        elif not spec.components.parameters:
            spec.components.parameters = Parameters({})

    def _process_root_channels_parameters(self, spec: AsyncAPI3) -> None:
        """Process parameters in channels in the root channels object."""
        if not spec.channels:
            return

        for channel in spec.channels.root.values():
            # Only process if it's a Channel object, not a Reference
            if hasattr(channel, "parameters") and channel.parameters:
                channel.parameters.root = self._process_parameters_map(
                    spec, channel.parameters.root
                )

    def _process_components_channels_parameters(self, spec: AsyncAPI3) -> None:
        """Process parameters in channels stored in components."""
        if not spec.components or not spec.components.channels:
            return

        for channel in spec.components.channels.root.values():
            # Only process if it's a Channel object, not a Reference
            if hasattr(channel, "parameters") and channel.parameters:
                channel.parameters.root = self._process_parameters_map(
                    spec, channel.parameters.root
                )

    def _process_parameters_map(
        self,
        spec: AsyncAPI3,
        parameters: dict[str, Parameter | Reference],
    ) -> dict[str, Parameter | Reference]:
        """
        Process a map of parameters, moving them to components and creating references.

        Args:
            spec: The AsyncAPI3 specification
            parameters: Map of parameters to process

        Returns:
            Map with Parameter objects replaced by Reference objects
        """
        processed_parameters: dict[str, Parameter | Reference] = {}

        for parameter_name, parameter in parameters.items():
            if isinstance(parameter, Reference):
                processed_parameters[parameter_name] = parameter
                continue

            if isinstance(parameter, Parameter):
                existing_ref = self._check_existing_parameter_ref(
                    spec, parameter_name, parameter
                )

                if existing_ref is None:
                    self._add_parameter_to_components(spec, parameter_name, parameter)

                processed_parameters[parameter_name] = (
                    Reference.to_component_parameter_name(parameter_name)
                )

        return processed_parameters

    def _check_existing_parameter_ref(
        self, spec: AsyncAPI3, parameter_name: str, parameter: Parameter
    ) -> Reference | None:
        """
        Check if a parameter with the given name already exists in components.

        Args:
            spec: The AsyncAPI3 specification
            parameter_name: Name/key for the parameter to check
            parameter: Parameter object to validate for uniqueness

        Returns:
            Reference to existing parameter if found, None if not found

        Raises:
            ValueError: If a parameter with the same name but different content already
                exists
        """
        if not spec.components or not spec.components.parameters:  # mypy protection
            return None

        if parameter_name in spec.components.parameters.root:
            existing_obj = spec.components.parameters.root[parameter_name]
            if existing_obj != parameter:
                raise ValueError(
                    f"Parameter name conflict: '{parameter_name}' already exists "
                    "with different content. "
                    f"Existing: {existing_obj.model_dump()}, "
                    f"New: {parameter.model_dump()}. Parameter names must be unique."
                )
            return Reference.to_component_parameter_name(parameter_name)

        return None

    def _add_parameter_to_components(
        self, spec: AsyncAPI3, parameter_name: str, parameter: Parameter
    ) -> None:
        """
        Add a parameter to the components/parameters section.

        Args:
            spec: The AsyncAPI3 specification
            parameter_name: Name/key for the parameter
            parameter: Parameter object to add
        """
        spec.components.parameters.root[parameter_name] = parameter  # type: ignore[union-attr]
