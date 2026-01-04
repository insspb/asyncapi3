"""Anypoint MQ bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "AnypointMQChannelBindings",
    "AnypointMQMessageBindings",
    "AnypointMQOperationBindings",
    "AnypointMQServerBindings",
]

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from asyncapi3.models.base import Reference
from asyncapi3.models.helpers import is_null
from asyncapi3.models.schema import Schema


class AnypointMQServerBindings(BaseModel):
    """
    Anypoint MQ Server Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(extra="forbid")


class AnypointMQChannelBindings(BaseModel):
    """
    Anypoint MQ Channel Binding Object.

    The Anypoint MQ Channel Binding Object is defined by a JSON Schema, which defines
    these fields.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
    )

    destination: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "The destination (queue or exchange) name for this channel. SHOULD only be "
            "specified if the channel name differs from the actual destination name, "
            "such as when the channel name is not a valid destination name in Anypoint "
            "MQ. Optional, defaults to the channel name."
        ),
    )
    destination_type: Literal["exchange", "queue", "fifo-queue"] | None = Field(
        default="queue",
        exclude_if=is_null,
        alias="destinationType",
        description=(
            "The type of destination, which MUST be either exchange or queue or "
            "fifo-queue. SHOULD be specified to document the messaging model "
            "(publish/subscribe, point-to-point, strict message ordering) supported by "
            "this channel. Optional, defaults to queue."
        ),
    )
    binding_version: str | None = Field(
        default="0.1.0",
        exclude_if=is_null,
        alias="bindingVersion",
        description="The version of this binding. Optional, defaults to latest.",
    )


class AnypointMQOperationBindings(BaseModel):
    """
    Anypoint MQ Operation Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(extra="forbid")


class AnypointMQMessageBindings(BaseModel):
    """
    Anypoint MQ Message Binding Object.

    The Anypoint MQ Message Binding Object defines these fields.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
    )

    headers: Schema | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A Schema object containing the definitions for Anypoint MQ-specific "
            "headers (so-called protocol headers). This schema MUST be of type object "
            "and have a properties key. Examples of Anypoint MQ protocol headers are "
            "messageId and messageGroupId."
        ),
    )
    binding_version: str = Field(
        default="0.1.0",
        alias="bindingVersion",
        description="The version of this binding. Optional, defaults to latest.",
    )
