"""NATS bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "NATSChannelBindings",
    "NATSMessageBindings",
    "NATSOperationBindings",
    "NATSServerBindings",
]

from pydantic import Field

from asyncapi3.models.base_models import NonExtendableBaseModel
from asyncapi3.models.helpers import is_null


class NATSServerBindings(NonExtendableBaseModel):
    """
    NATS Server Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class NATSChannelBindings(NonExtendableBaseModel):
    """
    NATS Channel Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class NATSOperationBindings(NonExtendableBaseModel):
    """
    NATS Operation Binding Object.

    This object contains information about the operation representation in NATS.
    """

    queue: str | None = Field(
        default=None,
        exclude_if=is_null,
        max_length=255,
        description=(
            "Defines the name of the queue to use. It MUST NOT exceed 255 characters."
        ),
    )
    binding_version: str = Field(
        default="0.1.0",
        alias="bindingVersion",
        description="The version of this binding. If omitted, 'latest' MUST be assumed",
    )


class NATSMessageBindings(NonExtendableBaseModel):
    """
    NATS Message Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """
