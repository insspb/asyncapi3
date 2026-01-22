"""Managers for handling reusable channel message objects."""

from __future__ import annotations

__all__ = ["ChannelMessagesManager"]


from typing import TYPE_CHECKING

from asyncapi3.models.base import Reference
from asyncapi3.models.components import Components
from asyncapi3.models.message import Message, Messages
from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class ChannelMessagesManager(ProcessorProtocol):
    """
    Manager for handling Message objects in channel messages in AsyncAPI specification.

    This manager ensures that all Message objects in channels are stored in
    components/messages and replaced with Reference objects throughout
    the specification. Duplicate messages with the same name are not allowed.
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """
        Process channel messages in the AsyncAPI specification.

        Moves all messages from channels to components/messages, replaces them with
        references, and ensures no duplicate message names exist.

        Args:
            spec: The AsyncAPI3 specification to process

        Returns:
            The modified AsyncAPI3 specification
        """
        self._ensure_components_messages_exist(spec)

        self._process_root_channels_messages(spec)
        self._process_components_channels_messages(spec)

        return spec

    def _ensure_components_messages_exist(self, spec: AsyncAPI3) -> None:
        """
        Ensure that components and messages section exist in the specification.

        Creates components with messages if components doesn't exist.
        Adds messages to existing components if messages section is missing.
        """
        if not spec.components:
            spec.components = Components(messages=Messages({}))
        elif not spec.components.messages:
            spec.components.messages = Messages({})

    def _process_root_channels_messages(self, spec: AsyncAPI3) -> None:
        """Process messages in channels in the root channels object."""
        if not spec.channels:
            return

        for channel in spec.channels.root.values():
            # Only process if it's a Channel object, not a Reference
            if hasattr(channel, "messages") and channel.messages:
                channel.messages.root = self._process_messages_map(
                    spec, channel.messages.root
                )

    def _process_components_channels_messages(self, spec: AsyncAPI3) -> None:
        """Process messages in channels stored in components."""
        if not spec.components or not spec.components.channels:
            return

        for channel in spec.components.channels.root.values():
            # Only process if it's a Channel object, not a Reference
            if hasattr(channel, "messages") and channel.messages:
                channel.messages.root = self._process_messages_map(
                    spec, channel.messages.root
                )

    def _process_messages_map(
        self,
        spec: AsyncAPI3,
        messages: dict[str, Message | Reference],
    ) -> dict[str, Message | Reference]:
        """
        Process a map of messages, moving them to components and creating references.

        Args:
            spec: The AsyncAPI3 specification
            messages: Map of messages to process

        Returns:
            Map with Message objects replaced by Reference objects
        """
        processed_messages: dict[str, Message | Reference] = {}

        for message_name, message in messages.items():
            if isinstance(message, Reference):
                processed_messages[message_name] = message
                continue

            if isinstance(message, Message):
                existing_ref = self._check_existing_message_ref(
                    spec, message_name, message
                )

                if existing_ref is None:
                    self._add_message_to_components(spec, message_name, message)

                processed_messages[message_name] = Reference.to_component_message_name(
                    message_name
                )

        return processed_messages

    def _check_existing_message_ref(
        self, spec: AsyncAPI3, message_name: str, message: Message
    ) -> Reference | None:
        """
        Check if a message with the given name already exists in components.

        Args:
            spec: The AsyncAPI3 specification
            message_name: Name/key for the message to check
            message: Message object to validate for uniqueness

        Returns:
            Reference to existing message if found, None if not found

        Raises:
            ValueError: If a message with the same name but different content already
                exists
        """
        if not spec.components or not spec.components.messages:  # mypy types protection
            return None

        if message_name in spec.components.messages.root:
            existing_obj = spec.components.messages.root[message_name]
            if existing_obj != message:
                raise ValueError(
                    f"Message name conflict detected: '{message_name}' already exists "
                    "with different content. "
                    f"Existing: {existing_obj.model_dump()}, "
                    f"New: {message.model_dump()}. Message names must be unique."
                )
            return Reference.to_component_message_name(message_name)

        return None

    def _add_message_to_components(
        self, spec: AsyncAPI3, message_name: str, message: Message
    ) -> None:
        """
        Add a message to the components/messages section.

        Args:
            spec: The AsyncAPI3 specification
            message_name: Name/key for the message
            message: Message object to add
        """
        spec.components.messages.root[message_name] = message  # type: ignore[union-attr]
