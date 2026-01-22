"""Common functions for reference validation in AsyncAPI 3.0 specification."""

from __future__ import annotations

__all__ = [
    "is_external_ref",
    "validate_component_exists",
    "validate_root_channel_ref",
    "validate_root_operation_ref",
]
import logging

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asyncapi3.models.asyncapi import AsyncAPI3


def is_external_ref(ref_value: str, context: str) -> bool:
    """
    Check if reference is external and log warning if it is.

    Args:
        ref_value: The reference value to check
        context: Context description for logging

    Returns:
        True if reference is external (validation skipped), False otherwise
    """
    if not ref_value.startswith("#"):
        logging.warning(
            f"{context} contains external reference '{ref_value}'. "
            "Cannot validate external references."
        )
        return True
    return False


def validate_component_exists(
    spec: AsyncAPI3,
    ref_value: str,
    component_path: str,
    context: str,
) -> None:
    """
    Validate that a component reference points to an existing component.

    Args:
        spec: The AsyncAPI3 specification
        ref_value: The reference value (e.g., "#/components/schemas/MySchema")
        component_path: The component path (e.g., "schemas")
        context: Context description for error messages

    Raises:
        ValueError: If the referenced component does not exist
    """
    expected_prefix = f"#/components/{component_path}/"
    if not ref_value.startswith(expected_prefix):
        raise ValueError(
            f"{context} reference '{ref_value}' must point to "
            f"{expected_prefix} but points elsewhere."
        )

    component_key = ref_value.replace(expected_prefix, "")
    if (
        not spec.components
        or not getattr(spec.components, component_path, None)
        or component_key not in getattr(spec.components, component_path).root
    ):
        raise ValueError(
            f"{context} references '{ref_value}' but component "
            f"'{component_key}' does not exist in #/components/{component_path}."
        )


def validate_root_channel_ref(
    spec: AsyncAPI3,
    ref_value: str,
    context: str,
) -> None:
    """
    Validate that a reference points to a channel in the root channels object.

    Args:
        spec: The AsyncAPI3 specification
        ref_value: The reference value
        context: Context description for error messages

    Raises:
        ValueError: If the reference is invalid
    """
    if not ref_value.startswith("#/channels/"):
        raise ValueError(
            f"{context} reference '{ref_value}' must point to "
            "#/channels/ but points elsewhere."
        )

    channel_key = ref_value.replace("#/channels/", "")
    if not spec.channels or channel_key not in spec.channels.root:
        raise ValueError(
            f"{context} references '{ref_value}' but channel "
            f"'{channel_key}' does not exist in root channels."
        )


def validate_root_operation_ref(spec: AsyncAPI3, ref_value: str, context: str) -> None:
    """
    Validate that a reference points to an operation in the root operations object.

    Args:
        spec: The AsyncAPI3 specification
        ref_value: The reference value
        context: Context description for error messages

    Raises:
        ValueError: If the reference is invalid
    """
    if not ref_value.startswith("#/operations/"):
        raise ValueError(
            f"{context} reference '{ref_value}' must point to "
            "#/operations/ but points elsewhere."
        )

    operation_key = ref_value.replace("#/operations/", "")
    if not spec.operations or operation_key not in spec.operations.root:
        raise ValueError(
            f"{context} references '{ref_value}' but operation "
            f"'{operation_key}' does not exist in root operations."
        )
