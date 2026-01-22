"""Validators for tag references in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["TagsRefValidator"]

import logging

from typing import TYPE_CHECKING, Any

from asyncapi3.models.base import Reference
from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class TagsRefValidator(ProcessorProtocol):
    """
    Validator for tag references in AsyncAPI specification.

    This validator checks that all tag references are valid:
    - Tag references in info, channels, operations, servers, and messages
      must point to existing tags in components/tags

    Allowed reference values:
    - External references (not starting with "#"): logged as warning only
    - Internal references: must point to "#/components/tags/{key}"

    The validator can be customized by overriding these methods:
    - _validate_external_tag_ref(): customize handling of external references
    - _validate_internal_tag_ref(): customize validation logic for internal references
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """
        Validate tag references in the AsyncAPI specification.

        Args:
            spec: The AsyncAPI3 specification to validate

        Returns:
            The validated AsyncAPI3 specification

        Raises:
            ValueError: If tag references are invalid
        """
        self.validate_info_tags_refs(spec)
        self.validate_servers_tags_refs(spec)
        self.validate_channels_tags_refs(spec)
        self.validate_channels_messages_tags_refs(spec)
        self.validate_operations_tags_refs(spec)
        self.validate_components_messages_tags_refs(spec)
        self.validate_components_channels_tags_refs(spec)
        self.validate_components_operations_tags_refs(spec)
        self.validate_components_servers_tags_refs(spec)
        self.validate_components_operation_traits_tags_refs(spec)
        self.validate_components_message_traits_tags_refs(spec)
        self.validate_components_channels_messages_tags_refs(spec)
        self.validate_components_tags_refs(spec)

        return spec

    def _validate_tags_list(
        self,
        spec: AsyncAPI3,
        tags: list,
        context: str,
    ) -> None:
        """Validate a list of tags that may contain references."""
        for tag in tags:
            if not isinstance(tag, Reference):
                continue
            self.validate_tag_ref(spec, tag, context)

    def _validate_tags_in_collection(
        self,
        spec: AsyncAPI3,
        objects: dict[str, Any],
        context_template: str,
    ) -> None:
        """Validate tags in a collection of objects."""
        for object_name, obj in objects.items():
            if not hasattr(obj, "tags") or not obj.tags:
                continue
            self._validate_tags_list(
                spec, obj.tags, context_template.format(name=object_name)
            )

    def validate_info_tags_refs(self, spec: AsyncAPI3) -> None:
        """Validate tag references in info object."""
        if not spec.info or not spec.info.tags:
            return
        self._validate_tags_list(spec, spec.info.tags, "info")

    def validate_channels_tags_refs(self, spec: AsyncAPI3) -> None:
        """Validate tag references in root channels."""
        if not spec.channels:
            return
        self._validate_tags_in_collection(spec, spec.channels.root, "channel '{name}'")

    def validate_operations_tags_refs(self, spec: AsyncAPI3) -> None:
        """Validate tag references in root operations."""
        if not spec.operations:
            return
        self._validate_tags_in_collection(
            spec, spec.operations.root, "operation '{name}'"
        )

    def validate_servers_tags_refs(self, spec: AsyncAPI3) -> None:
        """Validate tag references in root servers."""
        if not spec.servers:
            return
        self._validate_tags_in_collection(spec, spec.servers.root, "server '{name}'")

    def validate_components_messages_tags_refs(self, spec: AsyncAPI3) -> None:
        """Validate tag references in components messages."""
        if not spec.components or not spec.components.messages:
            return
        self._validate_tags_in_collection(
            spec, spec.components.messages.root, "components message '{name}'"
        )

    def validate_components_channels_tags_refs(self, spec: AsyncAPI3) -> None:
        """Validate tag references in components channels."""
        if not spec.components or not spec.components.channels:
            return
        self._validate_tags_in_collection(
            spec, spec.components.channels.root, "components channel '{name}'"
        )

    def validate_components_operations_tags_refs(self, spec: AsyncAPI3) -> None:
        """Validate tag references in components operations."""
        if not spec.components or not spec.components.operations:
            return
        self._validate_tags_in_collection(
            spec, spec.components.operations.root, "components operation '{name}'"
        )

    def validate_components_servers_tags_refs(self, spec: AsyncAPI3) -> None:
        """Validate tag references in components servers."""
        if not spec.components or not spec.components.servers:
            return
        self._validate_tags_in_collection(
            spec, spec.components.servers.root, "components server '{name}'"
        )

    def validate_components_operation_traits_tags_refs(self, spec: AsyncAPI3) -> None:
        """Validate tag references in components operation traits."""
        if not spec.components or not spec.components.operation_traits:
            return
        self._validate_tags_in_collection(
            spec,
            spec.components.operation_traits.root,
            "components operation trait '{name}'",
        )

    def validate_components_message_traits_tags_refs(self, spec: AsyncAPI3) -> None:
        """Validate tag references in components message traits."""
        if not spec.components or not spec.components.message_traits:
            return
        self._validate_tags_in_collection(
            spec,
            spec.components.message_traits.root,
            "components message trait '{name}'",
        )

    def validate_channels_messages_tags_refs(self, spec: AsyncAPI3) -> None:
        """Validate tag references in messages of root channels."""
        if not spec.channels:
            return
        for channel_name, channel in spec.channels.root.items():
            if isinstance(channel, Reference) or not channel.messages:
                continue
            for message_name, message in channel.messages.root.items():
                if isinstance(message, Reference) or not message.tags:
                    continue
                self._validate_tags_list(
                    spec,
                    message.tags,
                    f"message '{message_name}' in channel '{channel_name}'",
                )

    def validate_components_channels_messages_tags_refs(self, spec: AsyncAPI3) -> None:
        """Validate tag references in messages of components channels."""
        if not spec.components or not spec.components.channels:
            return
        for channel_name, channel in spec.components.channels.root.items():
            if isinstance(channel, Reference) or not channel.messages:
                continue
            for message_name, message in channel.messages.root.items():
                if isinstance(message, Reference) or not message.tags:
                    continue
                self._validate_tags_list(
                    spec,
                    message.tags,
                    f"message '{message_name}' in components channel '{channel_name}'",
                )

    def validate_components_tags_refs(self, spec: AsyncAPI3) -> None:
        """Validate tag references in components tags."""
        if not spec.components or not spec.components.tags:
            return
        for tag_name, tag in spec.components.tags.root.items():
            if isinstance(tag, Reference):
                self.validate_tag_ref(spec, tag, f"components tag '{tag_name}'")

    def validate_tag_ref(
        self,
        spec: AsyncAPI3,
        tag_ref: Reference,
        context: str,
    ) -> None:
        """
        Validate a single tag reference.

        Args:
            spec: The AsyncAPI3 specification
            tag_ref: The tag reference to validate
            context: Context string for error messages
                (e.g., "info", "channel 'my_channel'")

        Raises:
            ValueError: If the tag reference is invalid
        """
        ref_value = tag_ref.ref

        if ref_value.startswith("#"):
            self.validate_internal_tag_ref(spec, tag_ref, context)
            return

        self.validate_external_tag_ref(spec, tag_ref, context)

    def validate_external_tag_ref(
        self,
        spec: AsyncAPI3,
        tag_ref: Reference,
        context: str,
    ) -> None:
        """
        Validate an external tag reference.

        This method can be overridden to provide custom validation
        for external references.

        Args:
            spec: The AsyncAPI3 specification
            tag_ref: The external tag reference to validate
            context: Context string for error messages
        """
        logging.warning(
            f"{context.capitalize()} tag reference '{tag_ref.ref}' is external. "
            "Cannot validate external references."
        )

    def validate_internal_tag_ref(
        self,
        spec: AsyncAPI3,
        tag_ref: Reference,
        context: str,
    ) -> None:
        """
        Validate an internal tag reference.

        This method can be overridden to provide custom validation logic
        for internal references.

        Args:
            spec: The AsyncAPI3 specification
            tag_ref: The internal tag reference to validate
            context: Context string for error messages

        Raises:
            ValueError: If the tag reference is invalid
        """
        ref_value = tag_ref.ref

        if not ref_value.startswith("#/components/tags/"):
            raise ValueError(
                f"{context.capitalize()} tag reference '{ref_value}' must point to "
                "#/components/tags/ but points elsewhere."
            )

        tag_key = ref_value.replace("#/components/tags/", "")
        if (
            not spec.components
            or not spec.components.tags
            or tag_key not in spec.components.tags.root
        ):
            raise ValueError(
                f"{context.capitalize()} references tag '{tag_key}' but tag "
                f"does not exist in components/tags."
            )
