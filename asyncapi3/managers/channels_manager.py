"""Managers for handling reusable channel objects in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["ChannelsManager"]


from typing import TYPE_CHECKING

from asyncapi3.models.base import Reference
from asyncapi3.models.channel import Channel, Channels
from asyncapi3.models.components import Components
from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class ChannelsManager(ProcessorProtocol):
    """
    Manager for handling Channel objects in AsyncAPI specification.

    This manager ensures that all Channel objects are stored in components/channels
    and replaced with Reference objects throughout the specification.
    Duplicate channels with the same name are not allowed.
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """
        Process channels in the AsyncAPI specification.

        Moves all channels from root to components/channels, replaces them with
        references, and ensures no duplicate channel names exist.

        Args:
            spec: The AsyncAPI3 specification to process

        Returns:
            The modified AsyncAPI3 specification
        """
        self._ensure_components_channels_exist(spec)

        self._process_root_channels(spec)

        return spec

    def _ensure_components_channels_exist(self, spec: AsyncAPI3) -> None:
        """
        Ensure that components and channels section exist in the specification.

        Creates components with channels if components doesn't exist.
        Adds channels to existing components if channels section is missing.
        """
        if not spec.components:
            spec.components = Components(channels=Channels({}))
        elif not spec.components.channels:
            spec.components.channels = Channels({})

    def _process_root_channels(self, spec: AsyncAPI3) -> None:
        """Process channels in the root channels object."""
        if not spec.channels:
            return

        processed_channels: dict[str, Channel | Reference] = {}

        for channel_name, channel in spec.channels.root.items():
            if isinstance(channel, Reference):
                processed_channels[channel_name] = channel
                continue

            if isinstance(channel, Channel):
                self._ensure_is_unique_channel(spec, channel_name, channel)
                self._add_channel_to_components(spec, channel_name, channel)
                processed_channels[channel_name] = Reference.to_component_channel_name(
                    channel_name
                )

        spec.channels.root = processed_channels

    def _ensure_is_unique_channel(
        self,
        spec: AsyncAPI3,
        channel_name: str,
        channel: Channel | Reference,
    ) -> None:
        """
        Ensure that a channel with the given name doesn't already exist with different
        content.

        Args:
            spec: The AsyncAPI3 specification
            channel_name: Name/key for the channel to check
            channel: Channel object to validate for uniqueness

        Raises:
            ValueError: If a channel with the same name but different content already
                exists
        """
        if not spec.components or not spec.components.channels:  # mypy types protection
            return

        if channel_name in spec.components.channels.root:
            existing_channel = spec.components.channels.root[channel_name]
            if existing_channel != channel:
                raise ValueError(
                    f"Channel name conflict detected: '{channel_name}' already exists "
                    f"with different content. "
                    f"Existing: {existing_channel.model_dump()}, "
                    f"New: {channel.model_dump()}. Channel names must be unique."
                )
            return

    def _add_channel_to_components(
        self,
        spec: AsyncAPI3,
        channel_name: str,
        channel: Channel,
    ) -> None:
        """
        Add a channel to the components/channels section.

        Args:
            spec: The AsyncAPI3 specification
            channel_name: Name/key for the channel
            channel: Channel object to add
        """
        spec.components.channels.root[channel_name] = channel  # type: ignore[union-attr]
