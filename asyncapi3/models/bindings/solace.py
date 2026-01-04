"""Solace bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "SolaceChannelBindings",
    "SolaceDestination",
    "SolaceMessageBindings",
    "SolaceOperationBindings",
    "SolaceQueue",
    "SolaceServerBindings",
    "SolaceTopic",
]


from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from asyncapi3.models.base import Reference
from asyncapi3.models.helpers import is_null
from asyncapi3.models.schema import Schema


class SolaceServerBindings(BaseModel):
    """
    Solace Server Binding Object.

    This object contains information about the server representation in Solace.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    binding_version: str = Field(
        default="0.4.0",
        alias="bindingVersion",
        description="The current version is 0.4.0.",
    )
    msg_vpn: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="msgVpn",
        description="The Virtual Private Network name on the Solace broker.",
    )
    client_name: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="clientName",
        max_length=160,
        description=(
            "A unique client name to use to register to the appliance. If specified, "
            "it must be a valid Topic name, and a maximum of 160 bytes in length when "
            "encoded as UTF-8."
        ),
    )


class SolaceChannelBindings(BaseModel):
    """
    Solace Channel Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(
        extra="forbid",
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )


class SolaceQueue(BaseModel):
    """
    Solace Queue.

    Queue configuration for Solace destination.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    name: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "The name of the queue, only applicable when destinationType is 'queue'."
        ),
    )
    topic_subscriptions: list[str] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="topicSubscriptions",
        description=(
            "A list of topics that the queue subscribes to, only applicable when "
            "destinationType is 'queue'. If none is given, the queue subscribes to "
            "the topic as represented by the channel name."
        ),
    )
    access_type: Literal["exclusive", "nonexclusive"] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="accessType",
        description=(
            "'exclusive' or 'nonexclusive'. Only applicable when destinationType is "
            "'queue'."
        ),
    )
    max_msg_spool_size: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="maxMsgSpoolSize",
        description=(
            "The maximum amount of message spool that the given queue may use. Only "
            "applicable when destinationType is 'queue'."
        ),
    )
    max_ttl: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="maxTtl",
        description=(
            "The maximum TTL to apply to messages to be spooled. Only applicable when "
            "destinationType is 'queue'."
        ),
    )


class SolaceTopic(BaseModel):
    """
    Solace Topic.

    Topic configuration for Solace destination.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    topic_subscriptions: list[str] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="topicSubscriptions",
        description=(
            "A list of topics that the client subscribes to, only applicable when "
            "destinationType is 'topic'. If none is given, the client subscribes to "
            "the topic as represented by the channel name."
        ),
    )


class SolaceDestination(BaseModel):
    """
    Solace Destination.

    Destination Objects are described here.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    binding_version: str = Field(
        default="0.4.0",
        alias="bindingVersion",
        description="The current version is 0.4.0.",
    )
    destination_type: Literal["queue", "topic"] = Field(
        alias="destinationType",
        description=(
            "'queue' or 'topic'. If the type is queue, then the subscriber can bind "
            "to the queue, which in turn will subscribe to the topic as represented "
            "by the channel name or to the provided topicSubscriptions."
        ),
    )
    # TODO: Make a default decision globally.
    delivery_mode: Literal["direct", "persistent"] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="deliveryMode",
        description=(
            "'direct' or 'persistent'. This determines the quality of service for "
            "publishing messages. Default is 'persistent'."
        ),
    )
    queue: SolaceQueue | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Queue configuration, only applicable when destinationType is 'queue'."
        ),
    )
    topic: SolaceTopic | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Topic configuration, only applicable when destinationType is 'topic'."
        ),
    )


class SolaceOperationBindings(BaseModel):
    """
    Solace Operation Binding Object.

    We need the ability to support several bindings for each operation.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    binding_version: str = Field(
        default="0.4.0",
        alias="bindingVersion",
        description="The current version is 0.4.0.",
    )
    destinations: list[SolaceDestination] | None = Field(
        default=None,
        exclude_if=is_null,
        description="Destination Objects are described next.",
    )
    time_to_live: int | Schema | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="timeToLive",
        description=(
            "Interval in milliseconds or a Schema Object containing the definition of "
            "the lifetime of the message."
        ),
    )
    priority: int | Schema | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "The valid priority value range is 0-255 with 0 as the lowest priority and "
            "255 as the highest or a Schema Object containing the definition of the "
            "priority."
        ),
    )
    dmq_eligible: bool | None = Field(
        default=None,
        exclude_if=is_null,
        alias="dmqEligible",
        description=(
            "Set the message to be eligible to be moved to a Dead Message Queue. The "
            "default value is false."
        ),
    )


class SolaceMessageBindings(BaseModel):
    """
    Solace Message Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(
        extra="forbid",
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )
