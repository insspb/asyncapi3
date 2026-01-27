"""Utilities for reference validation in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = ["ReferenceResolutionResult", "resolve_reference"]

import logging

from typing import TYPE_CHECKING, Any, NamedTuple

from pydantic import BaseModel

from asyncapi3.models.base import Reference

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3

logger = logging.getLogger(__name__)


class ReferenceResolutionResult(NamedTuple):
    """Resolved object, its type, and the normalized access path."""

    resolved_object: Any
    resolved_type: type
    path: str


def resolve_reference(
    ref: str,
    spec: AsyncAPI3,
    visited_refs: set[str] | None = None,
) -> ReferenceResolutionResult | None:
    """
    Resolve a reference string to an object in the AsyncAPI specification.

    Args:
        ref: The reference string (e.g., "#/servers/MyServer",
            "#/components/schemas/MySchema")
        spec: The AsyncAPI3 specification instance
        visited_refs: Set of already visited references to detect cycles

    Returns:
        ReferenceResolutionResult if resolved successfully, None for external references

    Raises:
        ValueError: If reference format is unsupported, circular, or resolution fails
    """
    visited_refs = _initialize_visited_refs(ref=ref, visited_refs=visited_refs)

    if _is_external_reference(ref=ref):
        logger.warning("External reference '%s' cannot be validated locally", ref)
        return None

    path_parts = _parse_reference_path(ref=ref)

    try:
        resolved_object, resolved_type, full_path = _resolve_path_parts(
            spec=spec,
            path_parts=path_parts,
        )
    except AttributeError as exc:
        raise ValueError(f"Failed to resolve reference '{ref}': {exc}") from exc

    if isinstance(resolved_object, Reference):
        next_ref = resolved_object.ref
        return resolve_reference(
            ref=next_ref,
            spec=spec,
            visited_refs=visited_refs,
        )

    return ReferenceResolutionResult(
        resolved_object=resolved_object,
        resolved_type=resolved_type,
        path=full_path,
    )


def _initialize_visited_refs(
    ref: str,
    visited_refs: set[str] | None,
) -> set[str]:
    """Create or update the visited reference set and detect cycles."""
    if visited_refs is None:
        visited_refs = set()
    if ref in visited_refs:
        raise ValueError(f"Circular reference detected: {ref}")
    visited_refs.add(ref)
    return visited_refs


def _is_external_reference(ref: str) -> bool:
    """Return True when the reference points outside the current document."""
    return ref.startswith(("http://", "https://"))


def _parse_reference_path(ref: str) -> list[str]:
    """Split a reference string into path segments for navigation."""
    if not ref.startswith("#"):
        raise ValueError(f"Unsupported reference format: {ref}")
    path_parts = ref[1:].strip("/").split("/")
    if not path_parts or path_parts == [""]:
        raise ValueError(f"Invalid reference path: {ref}")
    return path_parts


def _resolve_path_parts(
    spec: AsyncAPI3,
    path_parts: list[str],
) -> tuple[Any, type, str]:
    """Resolve a sequence of reference path parts into a final object."""
    current_obj: Any = spec
    resolved_type: type = type(spec)
    full_path = "spec"

    for part in path_parts:
        if not part:
            continue
        full_path += f".{part}"
        current_obj, resolved_type = _resolve_path_part(
            current_obj=current_obj,
            part=part,
            full_path=full_path,
        )

    return current_obj, resolved_type, full_path


def _resolve_path_part(
    current_obj: Any,
    part: str,
    full_path: str,
) -> tuple[Any, type]:
    """Resolve a single path segment against the current object."""
    if _has_root_mapping(obj=current_obj):
        return _resolve_from_root(
            current_obj=current_obj,
            part=part,
            full_path=full_path,
        )
    if isinstance(current_obj, BaseModel):
        return _resolve_from_model(
            current_obj=current_obj,
            part=part,
            full_path=full_path,
        )
    if isinstance(current_obj, dict):
        return _resolve_from_dict(
            current_obj=current_obj,
            part=part,
            full_path=full_path,
        )
    raise ValueError(
        f"Cannot navigate to '{part}' in {full_path} (not a model or dict)"
    )


def _has_root_mapping(obj: Any) -> bool:
    """Return True when object has a root dict for navigation."""
    return hasattr(obj, "root") and isinstance(obj.root, dict)


def _resolve_from_root(
    current_obj: Any,
    part: str,
    full_path: str,
) -> tuple[Any, type]:
    """Resolve a path segment against a root mapping."""
    if part not in current_obj.root:
        raise ValueError(f"Reference key '{part}' not found in {full_path}")
    next_obj = current_obj.root[part]
    return next_obj, type(next_obj)


def _resolve_from_model(
    current_obj: Any,
    part: str,
    full_path: str,
) -> tuple[Any, type]:
    """Resolve a path segment against a Pydantic model instance."""
    field_name = _find_model_field_name(current_obj=current_obj, part=part)
    if field_name is None:
        raise ValueError(f"Field '{part}' not found in model at {full_path}")
    field_value = getattr(current_obj, field_name)
    if field_value is None:
        raise ValueError(f"Reference path '{full_path}' is None")
    return field_value, type(field_value)


def _find_model_field_name(current_obj: Any, part: str) -> str | None:
    """Find a field name on a model by name or alias."""
    for name, field_info in current_obj.__class__.model_fields.items():
        if name == part:
            return name
        if hasattr(field_info, "alias") and field_info.alias == part:
            return name
    return None


def _resolve_from_dict(
    current_obj: dict[str, Any],
    part: str,
    full_path: str,
) -> tuple[Any, type]:
    """Resolve a path segment against a dictionary."""
    if part not in current_obj:
        raise ValueError(f"Reference key '{part}' not found in {full_path}")
    next_obj = current_obj[part]
    return next_obj, type(next_obj)
