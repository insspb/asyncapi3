"""Managers for handling reusable objects in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["TagsManager"]

import logging

from typing import TYPE_CHECKING

from asyncapi3.managers.protocols import ProcessorProtocol
from asyncapi3.models.base import Reference, Tag
from asyncapi3.models.components import Components, Tags
from asyncapi3.models.operation import OperationTrait

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class TagsManager(ProcessorProtocol):
    """
    Manager for handling Tag objects in AsyncAPI specification.

    This manager ensures that all Tag objects are stored in components/tags
    and replaced with Reference objects throughout the specification.
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """
        Process tags in the AsyncAPI specification.

        Checks all objects that can contain tags (Info, root Servers, root Channels,
        root Operations, components Servers, components Channels, components Operations,
        components OperationTraits, components MessageTraits, components Messages,
        Messages within root Operations, and traits within root and components
        Operations)
        and ensures that duplicate tags are deduplicated, moved to components/tags,
        and replaced with references. Only unique tags are allowed.

        Args:
            spec: The AsyncAPI3 specification to process

        Returns:
            The modified AsyncAPI3 specification
        """
        self._ensure_components_tags_exist(spec)

        self._process_info_tags(spec)
        self._process_server_tags(spec)
        self._process_channel_tags(spec)
        self._process_operation_tags(spec)
        self._process_components_servers_tags(spec)
        self._process_components_channels_tags(spec)
        self._process_components_operations_tags(spec)
        self._process_components_operation_traits_tags(spec)
        self._process_components_message_traits_tags(spec)
        self._process_components_messages_tags(spec)
        self._process_operations_messages_tags(spec)
        return spec

    def _ensure_components_tags_exist(self, spec: AsyncAPI3) -> None:
        """
        Ensure that components and tags section exist in the specification.

        Creates components with tags if components doesn't exist.
        Adds tags to existing components if tags section is missing.
        """
        if not spec.components:
            spec.components = Components(tags=Tags({}))
        elif not spec.components.tags:
            spec.components.tags = Tags({})

    def _process_info_tags(self, spec: AsyncAPI3) -> None:
        """Process tags in the info object."""
        if not spec.info or not spec.info.tags:
            return

        spec.info.tags = self._process_tags_list(spec, spec.info.tags)

    def _process_server_tags(self, spec: AsyncAPI3) -> None:
        """Process tags in all servers."""
        if not spec.servers:
            return

        for server in spec.servers.root.values():
            # Only process if it's a Server object, not a Reference
            if hasattr(server, "tags") and server.tags:
                server.tags = self._process_tags_list(spec, server.tags)

    def _process_channel_tags(self, spec: AsyncAPI3) -> None:
        """Process tags in all channels."""
        if not spec.channels:
            return

        for channel in spec.channels.root.values():
            # Only process if it's a Channel object, not a Reference
            if hasattr(channel, "tags") and channel.tags:
                channel.tags = self._process_tags_list(spec, channel.tags)

    def _process_operation_tags(self, spec: AsyncAPI3) -> None:
        """Process tags in all operations."""
        if not spec.operations:
            return

        for operation in spec.operations.root.values():
            # Only process if it's an Operation object, not a Reference
            if hasattr(operation, "tags") and operation.tags:
                operation.tags = self._process_tags_list(spec, operation.tags)

            # Also process traits in operations
            if hasattr(operation, "traits") and operation.traits:
                operation.traits = self._process_operation_traits(
                    spec, operation.traits
                )

    def _process_components_messages_tags(self, spec: AsyncAPI3) -> None:
        """Process tags in messages stored directly in components."""
        if not spec.components or not spec.components.messages:
            return

        for message in spec.components.messages.root.values():
            # Only process if it's a Message object, not a Reference
            if hasattr(message, "tags") and message.tags:
                message.tags = self._process_tags_list(spec, message.tags)

    def _process_operations_messages_tags(self, spec: AsyncAPI3) -> None:
        """Process tags in messages within operations."""
        if not spec.operations:
            return

        for operation in spec.operations.root.values():
            # Only process if it's an Operation object, not a Reference
            if not hasattr(operation, "messages") or not operation.messages:
                continue
            for message in operation.messages:
                # Only process if it's a Message object, not a Reference
                # no cover as for now we do not deal with dereferenced references
                if hasattr(message, "tags") and message.tags:  # pragma: no cover
                    message.tags = self._process_tags_list(spec, message.tags)

    def _process_operation_traits(
        self, spec: AsyncAPI3, traits: list[OperationTrait | Reference]
    ) -> list[OperationTrait | Reference]:
        """
        Process traits in operations, extracting tags from OperationTrait objects.

        Args:
            spec: The AsyncAPI3 specification
            traits: List of traits to process

        Returns:
            List with OperationTrait objects processed for tags
        """
        processed_traits: list[OperationTrait | Reference] = []

        for trait in traits:
            if isinstance(trait, Reference):
                processed_traits.append(trait)
                continue
            if isinstance(trait, OperationTrait):
                # Process tags in the trait if it has them
                if hasattr(trait, "tags") and trait.tags:
                    trait.tags = self._process_tags_list(spec, trait.tags)
                processed_traits.append(trait)

        return processed_traits

    def _process_components_servers_tags(self, spec: AsyncAPI3) -> None:
        """Process tags in servers stored in components."""
        if not spec.components or not spec.components.servers:
            return

        for server in spec.components.servers.root.values():
            # Only process if it's a Server object, not a Reference
            if hasattr(server, "tags") and server.tags:
                server.tags = self._process_tags_list(spec, server.tags)

    def _process_components_channels_tags(self, spec: AsyncAPI3) -> None:
        """Process tags in channels stored in components."""
        if not spec.components or not spec.components.channels:
            return

        for channel in spec.components.channels.root.values():
            # Only process if it's a Channel object, not a Reference
            if hasattr(channel, "tags") and channel.tags:
                channel.tags = self._process_tags_list(spec, channel.tags)

    def _process_components_operations_tags(self, spec: AsyncAPI3) -> None:
        """Process tags in operations stored in components."""
        if not spec.components or not spec.components.operations:
            return

        for operation in spec.components.operations.root.values():
            # Only process if it's an Operation object, not a Reference
            if hasattr(operation, "tags") and operation.tags:
                operation.tags = self._process_tags_list(spec, operation.tags)

            # Also process traits in operations
            if hasattr(operation, "traits") and operation.traits:
                operation.traits = self._process_operation_traits(
                    spec, operation.traits
                )

    def _process_components_operation_traits_tags(self, spec: AsyncAPI3) -> None:
        """Process tags in operation traits stored in components."""
        if not spec.components or not spec.components.operation_traits:
            return

        for operation_trait in spec.components.operation_traits.root.values():
            # Only process if it's an OperationTrait object, not a Reference
            if hasattr(operation_trait, "tags") and operation_trait.tags:
                operation_trait.tags = self._process_tags_list(
                    spec, operation_trait.tags
                )

    def _process_components_message_traits_tags(self, spec: AsyncAPI3) -> None:
        """Process tags in message traits stored in components."""
        if not spec.components or not spec.components.message_traits:
            return

        for message_trait in spec.components.message_traits.root.values():
            # Only process if it's a MessageTrait object, not a Reference
            if hasattr(message_trait, "tags") and message_trait.tags:
                message_trait.tags = self._process_tags_list(spec, message_trait.tags)

    def _process_tags_list(
        self, spec: AsyncAPI3, tags: list[Tag | Reference]
    ) -> list[Tag | Reference]:
        """
        Process a list of tags, deduplicating them, moving to components and replacing
        with references. Only unique tags are preserved.

        Args:
            spec: The AsyncAPI3 specification
            tags: List of tags to process

        Returns:
            List with unique Tag objects replaced by Reference objects
        """
        processed_tags = set()

        for tag in tags:
            if isinstance(tag, Reference):
                processed_tags.add(tag)
                continue

            tag_name = self._get_tag_name(tag)
            existing_ref = self._find_existing_tag_ref(spec, tag)

            if existing_ref:
                processed_tags.add(existing_ref)
                continue

            # Add to components and create reference
            self._add_tag_to_components(spec, tag_name, tag)
            processed_tags.add(Reference.to_component_tag_name(tag_name))

        unique_tags: list[Tag | Reference] = list(processed_tags)
        return unique_tags

    def _get_tag_name(self, tag: Tag) -> str:
        """Generate a unique name for a tag based on its name field."""
        # Use the tag's name as the key, replace invalid characters
        return tag.name.replace(" ", "_").replace("-", "_")

    def _find_existing_tag_ref(self, spec: AsyncAPI3, tag: Tag) -> Reference | None:
        """
        Find if a tag already exists in components and return its reference.

        Args:
            spec: The AsyncAPI3 specification
            tag: Tag to find

        Returns:
            Reference to existing tag if found, None otherwise
        """
        if not spec.components or not spec.components.tags:  # mypy types protection
            return None

        tag_name = self._get_tag_name(tag)

        # Check if tag with same name exists
        if tag_name in spec.components.tags.root:
            existing_tag = spec.components.tags.root[tag_name]
            # Tag with same name but different content - log warning
            if existing_tag != tag:
                logging.warning(
                    f"Tag name conflict detected: '{tag_name}' already exists with "
                    f"different content. Existing: {existing_tag.model_dump()}, "
                    f"New: {tag.model_dump()}. Using existing tag."
                )

            return Reference.to_component_tag_name(tag_name)

        return None

    def _add_tag_to_components(self, spec: AsyncAPI3, tag_name: str, tag: Tag) -> None:
        """
        Add a tag to the components/tags section.

        Args:
            spec: The AsyncAPI3 specification
            tag_name: Name/key for the tag
            tag: Tag object to add
        """
        spec.components.tags.root[tag_name] = tag  # type: ignore[union-attr]
