"""MQTT bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "MQTTChannelBindings",
    "MQTTLastWill",
    "MQTTMessageBindings",
    "MQTTOperationBindings",
    "MQTTServerBindings",
]

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from asyncapi3.models.base import Reference
from asyncapi3.models.helpers import is_null
from asyncapi3.models.schema import Schema


class MQTTLastWill(BaseModel):
    """
    MQTT Last Will and Testament configuration.

    Last Will and Testament configuration. topic, qos, message and retain are
    properties of this object.
    """

    model_config = ConfigDict(
        extra="forbid",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    topic: str = Field(
        description="The topic where the Last Will and Testament message will be sent.",
    )
    qos: Literal[0, 1, 2] = Field(
        description=(
            "Defines how hard the broker/client will try to ensure that the Last Will "
            "and Testament message is received. Its value MUST be either 0, 1 or 2."
        ),
    )
    message: str = Field(
        description="Last Will message.",
    )
    retain: bool = Field(
        description=(
            "Whether the broker should retain the Last Will and Testament message or "
            "not."
        ),
    )


class MQTTServerBindings(BaseModel):
    """
    MQTT Server Binding Object.

    This object contains information about the server representation in MQTT.

    This object MUST contain only the properties defined below.
    """

    model_config = ConfigDict(
        extra="forbid",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    client_id: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="clientId",
        description="The client identifier.",
    )
    clean_session: bool | None = Field(
        default=None,
        exclude_if=is_null,
        alias="cleanSession",
        description=(
            "Whether to create a persistent connection or not. When false, the "
            "connection will be persistent. This is called clean start in MQTTv5."
        ),
    )
    last_will: MQTTLastWill | None = Field(
        default=None,
        exclude_if=is_null,
        alias="lastWill",
        description="Last Will and Testament configuration.",
    )
    keep_alive: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="keepAlive",
        description=(
            "Interval in seconds of the longest period of time the broker and the "
            "client can endure without sending a message."
        ),
    )
    session_expiry_interval: int | Schema | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="sessionExpiryInterval",
        description=(
            "Interval in seconds or a Schema Object containing the definition of the "
            "interval. The broker maintains a session for a disconnected client until "
            "this interval expires."
        ),
    )
    maximum_packet_size: int | Schema | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="maximumPacketSize",
        description=(
            "Number of bytes or a Schema Object representing the maximum packet size "
            "the client is willing to accept."
        ),
    )
    binding_version: str = Field(
        default="0.2.0",
        alias="bindingVersion",
        description="The version of this binding. If omitted, 'latest' MUST be assumed",
    )


class MQTTChannelBindings(BaseModel):
    """
    MQTT Channel Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(
        extra="forbid",
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )


class MQTTOperationBindings(BaseModel):
    """
    MQTT Operation Binding Object.

    This object contains information about the operation representation in MQTT.

    This object MUST contain only the properties defined below.
    """

    model_config = ConfigDict(
        extra="forbid",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    qos: Literal[0, 1, 2] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Defines the Quality of Service (QoS) levels for the message flow between "
            "client and server. Its value MUST be either 0 (At most once delivery), 1 "
            "(At least once delivery), or 2 (Exactly once delivery)."
        ),
    )
    retain: bool | None = Field(
        default=None,
        exclude_if=is_null,
        description="Whether the broker should retain the message or not.",
    )
    message_expiry_interval: int | Schema | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="messageExpiryInterval",
        description=(
            "Interval in seconds or a Schema Object containing the definition of the "
            "lifetime of the message."
        ),
    )
    binding_version: str = Field(
        default="0.2.0",
        alias="bindingVersion",
        description="The version of this binding. If omitted, 'latest' MUST be assumed",
    )


class MQTTMessageBindings(BaseModel):
    """
    MQTT Message Binding Object.

    This object contains information about the message representation in MQTT.

    This object MUST contain only the properties defined below.
    """

    model_config = ConfigDict(
        extra="forbid",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    payload_format_indicator: Literal[0, 1] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="payloadFormatIndicator",
        description=(
            "Either: 0 (zero): Indicates that the payload is unspecified bytes, or 1: "
            "Indicates that the payload is UTF-8 encoded character data."
        ),
    )
    correlation_data: Schema | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="correlationData",
        description=(
            "Correlation Data is used by the sender of the request message to identify "
            "which request the response message is for when it is received."
        ),
    )
    content_type: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="contentType",
        description=(
            "String describing the content type of the message payload. This should "
            "not conflict with the contentType field of the associated AsyncAPI "
            "Message object."
        ),
    )
    response_topic: str | Schema | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="responseTopic",
        description="The topic (channel URI) for a response message.",
    )
    binding_version: str = Field(
        default="0.2.0",
        alias="bindingVersion",
        description="The version of this binding. If omitted, 'latest' MUST be assumed",
    )
