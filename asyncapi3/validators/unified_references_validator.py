"""Unified validator for all reference objects in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["UnifiedReferencesValidator"]

import fnmatch
import logging
import re

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, get_args

from asyncapi3.models.base import ExternalDocumentation, Reference, Tag
from asyncapi3.models.bindings import (
    ChannelBindingsObject,
    MessageBindingsObject,
    OperationBindingsObject,
    ServerBindingsObject,
)
from asyncapi3.models.channel import Channel, Parameter
from asyncapi3.models.message import Message, MessageTrait
from asyncapi3.models.operation import (
    Operation,
    OperationReply,
    OperationReplyAddress,
    OperationTrait,
)
from asyncapi3.models.schema import MultiFormatSchema, Schema
from asyncapi3.models.security import CorrelationID, SecurityScheme
from asyncapi3.models.server import Server, ServerVariable
from asyncapi3.protocols import ProcessorProtocol
from asyncapi3.validators.utils import resolve_reference

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3

logger = logging.getLogger(__name__)

# Single source of truth mapping of normalized reference paths to expected types.
# Keys are dot-separated paths in the normalized form produced by _normalize_path.
# Patterns support "*" for single segments and "**" for multi-segment matches. When
# multiple patterns match, the most specific pattern (more literal segments and
# fewer wildcards) wins. Update this mapping whenever a new referenceable path is
# introduced or when a ValueError indicates a missing path.
REFERENCE_TYPE_MAPPINGS = {
    "**.channel": Channel,
    "**.channels.*": Channel,
    "**.reply.channel": Channel,
    "**.channel_bindings.*": ChannelBindingsObject,
    "**.channels.*.bindings": ChannelBindingsObject,
    "**.correlation_id": CorrelationID,
    "**.correlation_ids.*": CorrelationID,
    "**.external_docs": ExternalDocumentation,
    "**.external_docs.*": ExternalDocumentation,
    "**.messages": Message,
    "**.messages.*": Message,
    "**.reply.messages": Message,
    "**.message_bindings.*": MessageBindingsObject,
    "**.message_traits.*.bindings": MessageBindingsObject,
    "**.messages.*.bindings": MessageBindingsObject,
    "**.messages.*.traits.*.bindings": MessageBindingsObject,
    "**.messages.*.traits.bindings": MessageBindingsObject,
    "**.message_traits.*": MessageTrait,
    "**.messages.*.traits": MessageTrait,
    "**.messages.*.traits.*": MessageTrait,
    "**.message_traits.*.headers": MultiFormatSchema | Schema,
    "**.messages.*.headers": MultiFormatSchema | Schema,
    "**.messages.*.payload": MultiFormatSchema | Schema,
    "**.messages.*.traits.*.headers": MultiFormatSchema | Schema,
    "**.messages.*.traits.headers": MultiFormatSchema | Schema,
    "**.schemas.*": MultiFormatSchema | Schema,
    "**.operations.*": Operation,
    "**.operation_bindings.*": OperationBindingsObject,
    "**.operation_traits.*.bindings": OperationBindingsObject,
    "**.operations.*.bindings": OperationBindingsObject,
    "**.operations.*.traits.*.bindings": OperationBindingsObject,
    "**.operations.*.traits.bindings": OperationBindingsObject,
    "**.replies.*": OperationReply,
    "**.reply": OperationReply,
    "**.replies.*.address": OperationReplyAddress,
    "**.reply.address": OperationReplyAddress,
    "**.reply_addresses.*": OperationReplyAddress,
    "**.operation_traits.*": OperationTrait,
    "**.operations.*.traits": OperationTrait,
    "**.operations.*.traits.*": OperationTrait,
    "**.parameters.*": Parameter,
    "**.*_bindings.*.*.client_id": Schema,
    "**.*_bindings.*.*.correlation_data": Schema,
    "**.*_bindings.*.*.group_id": Schema,
    "**.*_bindings.*.*.headers": Schema,
    "**.*_bindings.*.*.key": Schema,
    "**.*_bindings.*.*.maximum_packet_size": Schema,
    "**.*_bindings.*.*.message_expiry_interval": Schema,
    "**.*_bindings.*.*.priority": Schema,
    "**.*_bindings.*.*.query": Schema,
    "**.*_bindings.*.*.response_topic": Schema,
    "**.*_bindings.*.*.session_expiry_interval": Schema,
    "**.*_bindings.*.*.time_to_live": Schema,
    "**.bindings.*.client_id": Schema,
    "**.bindings.*.correlation_data": Schema,
    "**.bindings.*.group_id": Schema,
    "**.bindings.*.headers": Schema,
    "**.bindings.*.key": Schema,
    "**.bindings.*.maximum_packet_size": Schema,
    "**.bindings.*.message_expiry_interval": Schema,
    "**.bindings.*.priority": Schema,
    "**.bindings.*.query": Schema,
    "**.bindings.*.response_topic": Schema,
    "**.bindings.*.session_expiry_interval": Schema,
    "**.bindings.*.time_to_live": Schema,
    "**.operations.*.traits.*.security.*": SecurityScheme,
    "**.security": SecurityScheme,
    "**.security.*": SecurityScheme,
    "**.security_schemes.*": SecurityScheme,
    "**.servers": Server,
    "**.servers.*": Server,
    "**.server_bindings.*": ServerBindingsObject,
    "**.servers.*.bindings": ServerBindingsObject,
    "**.server_variables.*": ServerVariable,
    "**.servers.*.variables.*": ServerVariable,
    "**.tags": Tag,
    "**.tags.*": Tag,
}


class UnifiedReferencesValidator(ProcessorProtocol):
    """
    Unified validator for all reference objects in AsyncAPI 3.0 specification.

    This validator performs a comprehensive check of all Reference objects throughout
    the specification by recursively traversing all model fields and validating:

    - Reference objects exist and point to valid locations
    - Referenced objects have the correct expected types
    - No circular references exist in reference chains
    - External references are logged as warnings

    The validator uses Pydantic's model_fields to discover all fields that may contain
    references and checks them systematically.
    """

    def __call__(self, spec: AsyncAPI3) -> AsyncAPI3:
        """
        Validate all reference objects in the AsyncAPI specification.

        Args:
            spec: The AsyncAPI3 specification to validate

        Returns:
            The validated AsyncAPI3 specification

        Raises:
            ValueError: If any reference validation fails
        """
        logger.debug("Starting unified reference validation")

        self.validate_references(spec=spec)

        logger.debug("Unified reference validation completed successfully")
        return spec

    def validate_references(self, spec: AsyncAPI3) -> None:
        """
        Validate all references in the specification.

        Args:
            spec: The AsyncAPI3 specification to validate
        """
        validated_refs: set[str] = set()
        self.validate_references_recursive(
            spec=spec,
            obj=spec,
            current_path="spec",
            validated_refs=validated_refs,
        )

    def validate_references_recursive(
        self,
        spec: AsyncAPI3,
        obj: Any,
        current_path: str,
        validated_refs: set[str],
        visited_objects: set[int] | None = None,
    ) -> None:
        """
        Recursively validate references in an object and its nested fields.

        Args:
            spec: The AsyncAPI3 specification to validate
            obj: The object to validate (model instance, dict, list, etc.)
            current_path: Current path in the object hierarchy for error messages
            validated_refs: Set of already validated reference strings
            visited_objects: Set of object IDs to prevent infinite recursion

        Raises:
            ValueError: If reference validation fails
        """
        if visited_objects is None:
            visited_objects = set()

        obj_id = id(obj)
        if obj_id in visited_objects:
            return
        visited_objects.add(obj_id)

        try:
            if isinstance(obj, Reference):
                self.validate_reference(
                    spec=spec,
                    ref_obj=obj,
                    ref_path=current_path,
                    validated_refs=validated_refs,
                )
                return

            if isinstance(obj, list):
                self._validate_list_references(
                    spec=spec,
                    items=obj,
                    current_path=current_path,
                    validated_refs=validated_refs,
                    visited_objects=visited_objects,
                )
                return

            if isinstance(obj, Mapping):
                self._validate_mapping_references(
                    spec=spec,
                    mapping=obj,
                    current_path=current_path,
                    validated_refs=validated_refs,
                    visited_objects=visited_objects,
                )
                return

            if self._is_model_instance(obj=obj):
                self._validate_model_references(
                    spec=spec,
                    model=obj,
                    current_path=current_path,
                    validated_refs=validated_refs,
                    visited_objects=visited_objects,
                )
        finally:
            visited_objects.discard(obj_id)

    def validate_reference(
        self,
        spec: AsyncAPI3,
        ref_obj: Reference,
        ref_path: str,
        validated_refs: set[str],
    ) -> None:
        """
        Validate a single reference object.

        Args:
            ref_obj: The Reference object to validate
            ref_path: Path to this reference in the specification
            validated_refs: Set of already validated reference strings

        Raises:
            ValueError: If reference validation fails
        """
        ref_str = ref_obj.ref

        if ref_str not in validated_refs:
            validated_refs.add(ref_str)

        try:
            resolution_result = resolve_reference(ref=ref_str, spec=spec)
        except ValueError as exc:
            raise ValueError(f"Invalid reference at {ref_path}: {exc}") from exc

        if resolution_result is None:
            return

        _resolved_obj, resolved_type, resolved_path = resolution_result

        expected_type = self._get_expected_type_for_path(ref_path=ref_path)

        if not self._is_type_compatible(
            actual_type=resolved_type,
            expected_type=expected_type,
        ):
            expected_repr = self._format_type_name(expected_type=expected_type)
            resolved_repr = self._format_type_name(expected_type=resolved_type)
            raise ValueError(
                f"Reference at {ref_path} resolved to {resolved_path} with type "
                f"{resolved_repr}, expected {expected_repr}"
            )

        logger.debug("Reference '%s' validated successfully", ref_str)

    def _validate_list_references(
        self,
        spec: AsyncAPI3,
        items: list[Any],
        current_path: str,
        validated_refs: set[str],
        visited_objects: set[int],
    ) -> None:
        """Validate references inside a list."""
        for i, item in enumerate(items):
            self.validate_references_recursive(
                spec=spec,
                obj=item,
                current_path=f"{current_path}[{i}]",
                validated_refs=validated_refs,
                visited_objects=visited_objects,
            )

    def _validate_mapping_references(
        self,
        spec: AsyncAPI3,
        mapping: Mapping[str, Any],
        current_path: str,
        validated_refs: set[str],
        visited_objects: set[int],
    ) -> None:
        """Validate references inside a mapping."""
        for key, value in mapping.items():
            escaped_key = self._escape_path_segment(str(key))
            self.validate_references_recursive(
                spec=spec,
                obj=value,
                current_path=f"{current_path}.{escaped_key}",
                validated_refs=validated_refs,
                visited_objects=visited_objects,
            )

    def _validate_model_references(
        self,
        spec: AsyncAPI3,
        model: Any,
        current_path: str,
        validated_refs: set[str],
        visited_objects: set[int],
    ) -> None:
        """Validate references inside a Pydantic model instance."""
        for field_name, field_info in model.__class__.model_fields.items():
            field_value = getattr(model, field_name)

            if field_value is None or field_info.exclude:
                continue

            field_path = f"{current_path}.{field_name}"
            self.validate_references_recursive(
                spec=spec,
                obj=field_value,
                current_path=field_path,
                validated_refs=validated_refs,
                visited_objects=visited_objects,
            )

    def _is_model_instance(self, obj: Any) -> bool:
        """Return True when object looks like a Pydantic model instance."""
        return hasattr(obj, "__class__") and hasattr(obj.__class__, "model_fields")

    def _get_expected_type_for_path(self, ref_path: str) -> Any:
        """
        Determine the expected type for a reference based on its path.

        Args:
            ref_path: The path where the reference was found

        Returns:
            The expected type class.

        Raises:
            ValueError: If the reference path cannot be matched to any expected type
        """
        normalized_path = self._normalize_path(ref_path=ref_path)

        best_match = None
        best_score = None
        for pattern, expected_type in REFERENCE_TYPE_MAPPINGS.items():
            if not self._path_matches(pattern=pattern, path=normalized_path):
                continue
            score = self._pattern_specificity(pattern=pattern)
            if best_score is None or score > best_score:
                best_match = expected_type
                best_score = score

        if best_match is not None:
            return best_match

        raise ValueError(
            f"Unknown reference type for path: {normalized_path}, "
            f"you should extend `REFERENCE_TYPE_MAPPINGS`"
        )

    def _normalize_path(self, ref_path: str) -> str:
        """Normalize paths by removing root markers and list indices."""
        normalized_path = ref_path.replace(".root.", ".")
        if normalized_path.endswith(".root"):
            normalized_path = normalized_path[: -len(".root")]
        return re.sub(r"\[\d+\]", "", normalized_path)

    def _escape_path_segment(self, segment: str) -> str:
        """Escape dots in a path segment so they are not treated as delimiters."""
        return segment.replace("\\", "\\\\").replace(".", "\\.")

    def _split_path(self, path: str) -> list[str]:
        """Split a path by dots while honoring escaped dot segments."""
        parts: list[str] = []
        current: list[str] = []
        escaped = False
        for ch in path:
            if escaped:
                current.append(ch)
                escaped = False
                continue
            if ch == "\\":
                escaped = True
                continue
            if ch == ".":
                parts.append("".join(current))
                current = []
                continue
            current.append(ch)
        if escaped:
            current.append("\\")
        parts.append("".join(current))
        return parts

    def _path_matches(self, pattern: str, path: str) -> bool:
        """
        Match dot-delimited paths with wildcards.

        Rules:
        - "**" matches zero or more segments.
        - "*" matches exactly one segment.
        - Other segments may include "*" for a single-segment glob match.
        """
        pattern_parts = self._split_path(path=pattern)
        path_parts = self._split_path(path=path)
        return self._path_matches_recursive(
            pattern_parts=pattern_parts,
            path_parts=path_parts,
            pattern_index=0,
            path_index=0,
        )

    def _segment_matches(self, pattern_part: str, path_part: str) -> bool:
        """Match a single path segment against a pattern segment."""
        if pattern_part == "*":
            return True
        if "*" in pattern_part:
            return fnmatch.fnmatch(path_part, pattern_part)
        return pattern_part == path_part

    def _path_matches_recursive(
        self,
        pattern_parts: list[str],
        path_parts: list[str],
        pattern_index: int,
        path_index: int,
    ) -> bool:
        """Recursively match pattern segments against path segments."""
        if pattern_index == len(pattern_parts):
            return path_index == len(path_parts)

        pattern_part = pattern_parts[pattern_index]
        if pattern_part == "**":
            if pattern_index == len(pattern_parts) - 1:
                return True
            return any(
                self._path_matches_recursive(
                    pattern_parts=pattern_parts,
                    path_parts=path_parts,
                    pattern_index=pattern_index + 1,
                    path_index=next_index,
                )
                for next_index in range(path_index, len(path_parts) + 1)
            )

        if path_index >= len(path_parts):
            return False

        path_part = path_parts[path_index]
        if not self._segment_matches(
            pattern_part=pattern_part,
            path_part=path_part,
        ):
            return False

        return self._path_matches_recursive(
            pattern_parts=pattern_parts,
            path_parts=path_parts,
            pattern_index=pattern_index + 1,
            path_index=path_index + 1,
        )

    def _pattern_specificity(self, pattern: str) -> tuple[int, int, int, int]:
        """Rank patterns by how specific they are."""
        literal_segments = 0
        wildcard_segments = 0
        double_wildcards = 0
        pattern_parts = self._split_path(path=pattern)
        for part in pattern_parts:
            if part == "**":
                double_wildcards += 1
                wildcard_segments += 1
                continue
            if "*" in part:
                wildcard_segments += 1
                continue
            literal_segments += 1
        segment_count = len(pattern_parts)
        return (
            literal_segments,
            -double_wildcards,
            -wildcard_segments,
            segment_count,
        )

    def _is_type_compatible(self, actual_type: type, expected_type: Any) -> bool:
        """
        Check if an actual type is compatible with an expected type.

        Args:
            actual_type: The resolved type
            expected_type: The expected type (may be Union)

        Returns:
            True if types are compatible
        """
        union_types = get_args(expected_type)
        if union_types:
            return any(
                self._is_type_compatible(
                    actual_type=actual_type,
                    expected_type=union_type,
                )
                for union_type in union_types
            )

        if isinstance(expected_type, type):
            return actual_type == expected_type or issubclass(
                actual_type, expected_type
            )

        return actual_type == expected_type

    def _format_type_name(self, expected_type: Any) -> str:
        """Format a type name for error messages."""
        union_types = get_args(expected_type)
        if union_types:
            return " | ".join(
                self._format_type_name(expected_type=item) for item in union_types
            )

        if isinstance(expected_type, type):
            return expected_type.__name__

        return str(expected_type)
