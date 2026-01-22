"""Validator for external documentation references in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["ExternalDocsRefValidator"]

import logging

from typing import TYPE_CHECKING, Any

from asyncapi3.models.base import Reference
from asyncapi3.protocols import ProcessorProtocol

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


class ExternalDocsRefValidator(ProcessorProtocol):
    """
    Validator for external documentation references in AsyncAPI specification.

    Allowed reference values:
    - External references (not starting with "#"): logged as warning only
    - Internal references: must point to "#/components/externalDocs/{key}"
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """
        Validate external documentation references in the AsyncAPI specification.

        Args:
            spec: The AsyncAPI3 specification to validate

        Returns:
            The validated AsyncAPI3 specification

        Raises:
            ValueError: If external documentation references are invalid
        """
        # Validate root level objects
        self.validate_info_external_docs_ref(spec)
        self.validate_info_tags_external_docs_refs(spec)
        self.validate_servers_external_docs_refs(spec)
        self.validate_channels_external_docs_refs(spec)
        self.validate_channels_messages_external_docs_refs(spec)
        self.validate_operations_external_docs_refs(spec)

        # Validate externalDocs in all component collections
        self.validate_components_channels_external_docs_refs(spec)
        self.validate_components_external_docs_external_docs_refs(spec)  # self
        self.validate_components_message_traits_external_docs_refs(spec)
        self.validate_components_messages_external_docs_refs(spec)
        self.validate_components_operations_external_docs_refs(spec)
        self.validate_components_operation_traits_external_docs_refs(spec)
        self.validate_components_servers_external_docs_refs(spec)
        self.validate_components_tags_external_docs_refs(spec)

        # Validate schemas (separate as they have special handling)
        self.validate_components_schemas_external_docs_refs(spec)

        return spec

    def validate_info_external_docs_ref(self, spec: AsyncAPI3) -> None:
        """Validate externalDocs in info."""
        if not spec.info:
            return
        self._validate_ref_field(spec, spec.info, "info")

    def validate_info_tags_external_docs_refs(self, spec: AsyncAPI3) -> None:
        """Validate externalDocs in info.tags."""
        # Check tags in info
        if not spec.info or not spec.info.tags:
            return

        for i, tag in enumerate(spec.info.tags):
            if isinstance(tag, Reference):
                continue
            self._validate_ref_field(spec, tag, f"tag at info.tags[{i}]")

    def validate_servers_external_docs_refs(self, spec: AsyncAPI3) -> None:
        """Validate externalDocs in servers."""
        if not spec.servers:
            return
        self._validate_external_docs_collection(spec.servers.root, spec, "server")

    def validate_channels_external_docs_refs(self, spec: AsyncAPI3) -> None:
        """Validate externalDocs in channels."""
        if not spec.channels:
            return
        self._validate_external_docs_collection(spec.channels.root, spec, "channel")

    def validate_channels_messages_external_docs_refs(self, spec: AsyncAPI3) -> None:
        """Validate externalDocs in messages within channels."""
        if not spec.channels:
            return
        for channel_name, channel in spec.channels.root.items():
            if isinstance(channel, Reference) or not channel.messages:
                continue
            for msg_name, msg in channel.messages.root.items():
                if isinstance(msg, Reference):
                    continue
                self._validate_ref_field(
                    spec, msg, f"message '{msg_name}' in channel '{channel_name}'"
                )

    def validate_operations_external_docs_refs(self, spec: AsyncAPI3) -> None:
        """Validate externalDocs in operations."""
        if not spec.operations:
            return
        self._validate_external_docs_collection(spec.operations.root, spec, "operation")

    def validate_components_channels_external_docs_refs(self, spec: AsyncAPI3) -> None:
        """Validate externalDocs in components channels."""
        if not spec.components or not spec.components.channels:
            return
        self._validate_external_docs_collection(
            collection=spec.components.channels.root,
            spec=spec,
            item_type="channel",
            context_prefix="components",
        )

    def validate_components_external_docs_external_docs_refs(
        self, spec: AsyncAPI3
    ) -> None:
        """Validate externalDocs references within externalDocs themselves."""
        if not spec.components or not spec.components.external_docs:
            return

        for name, doc in spec.components.external_docs.root.items():
            if isinstance(doc, Reference):
                self.validate_external_doc_ref(
                    spec=spec,
                    ref=doc,
                    context=f"components.externalDocs['{name}']",
                )

    def validate_components_messages_external_docs_refs(self, spec: AsyncAPI3) -> None:
        """Validate externalDocs in components messages."""
        if not spec.components or not spec.components.messages:
            return
        self._validate_external_docs_collection(
            collection=spec.components.messages.root,
            spec=spec,
            item_type="message",
            context_prefix="components",
        )

    def validate_components_message_traits_external_docs_refs(
        self, spec: AsyncAPI3
    ) -> None:
        """Validate externalDocs in components message traits."""
        if not spec.components or not spec.components.message_traits:
            return
        self._validate_external_docs_collection(
            collection=spec.components.message_traits.root,
            spec=spec,
            item_type="message trait",
            context_prefix="components",
        )

    def validate_components_operations_external_docs_refs(
        self, spec: AsyncAPI3
    ) -> None:
        """Validate externalDocs in components operations."""
        if not spec.components or not spec.components.operations:
            return
        self._validate_external_docs_collection(
            collection=spec.components.operations.root,
            spec=spec,
            item_type="operation",
            context_prefix="components",
        )

    def validate_components_operation_traits_external_docs_refs(
        self, spec: AsyncAPI3
    ) -> None:
        """Validate externalDocs in components operation traits."""
        if not spec.components or not spec.components.operation_traits:
            return
        self._validate_external_docs_collection(
            collection=spec.components.operation_traits.root,
            spec=spec,
            item_type="operation trait",
            context_prefix="components",
        )

    def validate_components_servers_external_docs_refs(self, spec: AsyncAPI3) -> None:
        """Validate externalDocs in components servers."""
        if not spec.components or not spec.components.servers:
            return
        self._validate_external_docs_collection(
            collection=spec.components.servers.root,
            spec=spec,
            item_type="server",
            context_prefix="components",
        )

    def validate_components_tags_external_docs_refs(self, spec: AsyncAPI3) -> None:
        """Validate externalDocs in components.tags."""
        # Tags can be in root.info.tags, or in various objects
        # But we also need to check root.components.tags
        if spec.components and spec.components.tags:
            for name, tag in spec.components.tags.root.items():
                if isinstance(tag, Reference):
                    continue
                self._validate_ref_field(spec, tag, f"tag '{name}'")

    def validate_components_schemas_external_docs_refs(self, spec: AsyncAPI3) -> None:
        """Validate externalDocs in schemas."""
        if not spec.components or not spec.components.schemas:
            return
        for name, schema in spec.components.schemas.root.items():
            # MultiFormatSchema doesn't have external_docs in our model,
            # but Schema does.
            if hasattr(schema, "external_docs"):
                self._validate_ref_field(spec, schema, f"schema '{name}'")

    def _validate_ref_field(
        self,
        spec: AsyncAPI3,
        obj: Any,
        context: str,
    ) -> None:
        """Validate externalDocs field in an object."""
        if not hasattr(obj, "external_docs") or not obj.external_docs:
            return

        external_docs = obj.external_docs
        if isinstance(external_docs, Reference):
            self.validate_external_doc_ref(spec, external_docs, context)

    def validate_external_doc_ref(
        self,
        spec: AsyncAPI3,
        ref: Reference,
        context: str,
    ) -> None:
        """
        Validate a single external documentation reference.

        Args:
            spec: The AsyncAPI3 specification
            ref: The external documentation reference to validate
            context: Context string for error messages

        Raises:
            ValueError: If the reference is invalid
        """
        ref_value = ref.ref

        if ref_value.startswith("#"):
            self.validate_internal_external_doc_ref(spec, ref, context)
            return

        self.validate_external_external_doc_ref(spec, ref, context)

    def validate_external_external_doc_ref(
        self,
        spec: AsyncAPI3,
        ref: Reference,
        context: str,
    ) -> None:
        """
        Validate an external external documentation reference.

        This method can be overridden to provide custom validation
        for external references.

        Args:
            spec: The AsyncAPI3 specification
            ref: The external reference to validate
            context: Context string for error messages
        """
        logging.warning(
            "%s external documentation reference '%s' "
            "is external. Cannot validate external references.",
            context.capitalize(),
            ref.ref,
        )

    def validate_internal_external_doc_ref(
        self,
        spec: AsyncAPI3,
        ref: Reference,
        context: str,
    ) -> None:
        """
        Validate an internal external documentation reference.

        This method can be overridden to provide custom validation logic
        for internal references.

        Args:
            spec: The AsyncAPI3 specification
            ref: The internal reference to validate
            context: Context string for error messages

        Raises:
            ValueError: If the reference is invalid
        """
        ref_value = ref.ref

        if not ref_value.startswith("#/components/externalDocs/"):
            raise ValueError(
                f"{context.capitalize()} external documentation reference "
                f"'{ref_value}' must point to #/components/externalDocs/ "
                "but points elsewhere."
            )

        doc_key = ref_value.replace("#/components/externalDocs/", "")
        if (
            not spec.components
            or not spec.components.external_docs
            or doc_key not in spec.components.external_docs.root
        ):
            raise ValueError(
                f"{context.capitalize()} references external documentation '{doc_key}' "
                "but it does not exist in components/externalDocs."
            )

    def _validate_external_docs_collection(
        self,
        collection: dict[str, Any] | None,
        spec: AsyncAPI3,
        item_type: str,
        context_prefix: str = "",
    ) -> None:
        """Validate externalDocs in a collection of objects."""
        if not collection:
            return
        prefix = f"{context_prefix} " if context_prefix else ""
        for name, item in collection.items():
            if isinstance(item, Reference):
                continue
            self._validate_ref_field(spec, item, f"{prefix}{item_type} '{name}'")
