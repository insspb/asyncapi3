"""NATS bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "NATSChannelBindings",
    "NATSMessageBindings",
    "NATSOperationBindings",
    "NATSServerBindings",
]

from pydantic import BaseModel, ConfigDict, Field

from asyncapi3.models.helpers import is_null


class NATSServerBindings(BaseModel):
    """
    NATS Server Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(
        extra="forbid",
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )


class NATSChannelBindings(BaseModel):
    """
    NATS Channel Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(
        extra="forbid",
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )


class NATSOperationBindings(BaseModel):
    """
    NATS Operation Binding Object.

    This object contains information about the operation representation in NATS.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

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


class NATSMessageBindings(BaseModel):
    """
    NATS Message Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(
        extra="forbid",
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )
