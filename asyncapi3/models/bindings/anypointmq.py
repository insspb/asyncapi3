"""Anypoint MQ bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "AnypointMQChannelBindings",
    "AnypointMQMessageBindings",
    "AnypointMQOperationBindings",
    "AnypointMQServerBindings",
]

from typing import Literal

from pydantic import Field

from asyncapi3.models.base import Reference
from asyncapi3.models.base_models import NonExtendableBaseModel
from asyncapi3.models.helpers import is_null
from asyncapi3.models.schema import Schema


class AnypointMQServerBindings(NonExtendableBaseModel):
    """
    Anypoint MQ Server Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class AnypointMQChannelBindings(NonExtendableBaseModel):
    """
    Anypoint MQ Channel Binding Object.

    The Anypoint MQ Channel Binding Object is defined by a JSON Schema, which defines
    these fields.
    """

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
    binding_version: str = Field(
        default="0.1.0",
        alias="bindingVersion",
        description="The version of this binding. Optional, defaults to latest.",
    )


class AnypointMQOperationBindings(NonExtendableBaseModel):
    """
    Anypoint MQ Operation Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class AnypointMQMessageBindings(NonExtendableBaseModel):
    """
    Anypoint MQ Message Binding Object.

    The Anypoint MQ Message Binding Object defines these fields.
    """

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
