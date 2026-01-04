"""IBM MQ bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "IBMMQChannelBindings",
    "IBMMQMessageBindings",
    "IBMMQOperationBindings",
    "IBMMQQueue",
    "IBMMQServerBindings",
    "IBMMQTopic",
]

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from asyncapi3.models.helpers import is_null


class IBMMQServerBindings(BaseModel):
    """
    IBM MQ Server Binding Object.

    This object contains server connection information about the IBM MQ server, referred
    to as an IBM MQ queue manager. This object contains additional connectivity
    information not possible to represent within the core AsyncAPI specification.

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

    group_id: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="groupId",
        description=(
            "Defines a logical group of IBM MQ server objects. This is necessary to "
            "specify multi-endpoint configurations used in high availability "
            "deployments. If omitted, the server object is not part of a group. MUST "
            "NOT be specified for URI Scheme http:// or file://."
        ),
    )
    ccdt_queue_manager_name: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="ccdtQueueManagerName",
        description=(
            "The name of the IBM MQ queue manager to bind to in the CCDT file. "
            "Optional, defaults to *. MUST NOT be specified for URI Scheme ibmmq://."
        ),
    )
    cipher_spec: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="cipherSpec",
        description=(
            "The recommended cipher specification used to establish a TLS connection "
            "between the client and the IBM MQ queue manager. More information on "
            "SSL/TLS cipher specifications supported by IBM MQ can be found in the "
            "IBM MQ Knowledge Center. Optional, defaults to ANY. MUST NOT be specified "
            "for protocol ibmmq or URI Scheme file:// or http://."
        ),
    )
    multi_endpoint_server: bool | None = Field(
        default=None,
        exclude_if=is_null,
        alias="multiEndpointServer",
        description=(
            "If multiEndpointServer is true then multiple connections can be workload "
            "balanced and applications should not make assumptions as to where "
            "messages are processed. Where message ordering, or affinity to specific "
            "message resources is necessary, a single endpoint "
            "(multiEndpointServer = false) may be required. Optional, defaults to "
            "false. MUST NOT be specified for URI Scheme file:// or http://."
        ),
    )
    heart_beat_interval: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="heartBeatInterval",
        description=(
            "The recommended value (in seconds) for the heartbeat sent to the queue "
            "manager during periods of inactivity. A value of zero means that no heart "
            "beats are sent. A value of 1 means that the client will use the value "
            "defined by the queue manager. More information on heart beat interval can "
            "be found in the IBM MQ Knowledge Center. Optional, defaults to 300. MUST "
            "be 0-999999."
        ),
    )
    binding_version: str = Field(
        default="0.1.0",
        alias="bindingVersion",
        description="The version of this binding. Optional, defaults to latest.",
    )


class IBMMQQueue(BaseModel):
    """
    IBM MQ Queue.

    Defines the properties of a queue.
    """

    model_config = ConfigDict(
        extra="forbid",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    object_name: str = Field(
        max_length=48,
        alias="objectName",
        description=(
            "Defines the name of the IBM MQ queue associated with the channel. "
            "A value MUST be specified. MUST NOT exceed 48 characters in length. "
            "MUST be a valid IBM MQ queue name."
        ),
    )
    is_partitioned: bool = Field(
        default=False,
        alias="isPartitioned",
        description=(
            "Defines if the queue is a cluster queue and therefore partitioned. If "
            "true, a binding option MAY be specified when accessing the queue. More "
            "information on binding options can be found in the IBM MQ Knowledge "
            "Center. Optional, defaults to false. If false, binding options SHOULD "
            "NOT be specified when accessing the queue."
        ),
    )
    exclusive: bool = Field(
        default=False,
        description=(
            "Specifies if it is recommended to open the queue exclusively. Optional, "
            "defaults to false."
        ),
    )


class IBMMQTopic(BaseModel):
    """
    IBM MQ Topic.

    Defines the properties of a topic.
    """

    model_config = ConfigDict(
        extra="forbid",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    string: str | None = Field(
        default=None,
        exclude_if=is_null,
        max_length=10240,
        description=(
            "The value of the IBM MQ topic string to be used. Optional. Note: if "
            "specified, SHALL override AsyncAPI channel name. MUST NOT exceed 10240 "
            "characters in length. MAY coexist with topic.objectName."
        ),
    )
    object_name: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="objectName",
        max_length=48,
        description=(
            "The name of the IBM MQ topic object. Optional. Note: if specified, SHALL "
            "override AsyncAPI channel name. MUST NOT exceed 48 characters in length. "
            "MAY coexist with topic.string."
        ),
    )
    durable_permitted: bool = Field(
        default=True,
        alias="durablePermitted",
        description=(
            "Defines if the subscription may be durable. Optional, defaults to true."
        ),
    )
    last_msg_retained: bool = Field(
        default=False,
        alias="lastMsgRetained",
        description=(
            "Defines if the last message published will be made available to new "
            "subscriptions. Optional, defaults to false."
        ),
    )


# TODO: Has cross-fields constraints
class IBMMQChannelBindings(BaseModel):
    """
    IBM MQ Channel Binding Object.

    This object contains information about the channel representation in IBM MQ. Each
    channel corresponds to a Queue or Topic within IBM MQ.

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

    destination_type: Literal["topic", "queue"] = Field(
        default="topic",
        alias="destinationType",
        description=(
            "Defines the type of AsyncAPI channel. Optional, defaults to topic. MUST "
            "be either topic or queue. For type topic, the AsyncAPI channel name "
            "MUST be assumed for the IBM MQ topic string unless overridden."
        ),
    )
    queue: IBMMQQueue | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Defines the properties of a queue. REQUIRED if destinationType = queue. "
            "queue and topic fields MUST NOT coexist within a channel binding."
        ),
    )
    topic: IBMMQTopic | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Defines the properties of a topic. OPTIONAL if destinationType = topic. "
            "queue and topic fields MUST NOT coexist within a channel binding."
        ),
    )
    max_msg_length: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="maxMsgLength",
        description=(
            "The maximum length of the physical message (in bytes) accepted by the "
            "Topic or Queue. Messages produced that are greater in size than this "
            "value may fail to be delivered. More information on the maximum message "
            "length can be found in the IBM MQ Knowledge Center. Optional, defaults to "
            "negotiated on IBM MQ channel. MUST be 0-104,857,600 bytes (100 MB)."
        ),
    )
    binding_version: str = Field(
        default="0.1.0",
        alias="bindingVersion",
        description="The version of this binding. Optional, defaults to latest.",
    )


class IBMMQOperationBindings(BaseModel):
    """
    IBM MQ Operation Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(
        extra="forbid",
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )


# TODO: Has cross-fields constraints
class IBMMQMessageBindings(BaseModel):
    """
    IBM MQ Message Binding Object.

    This object contains information about the message representation in IBM MQ.

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

    type: Literal["string", "jms", "binary"] = Field(
        default="string",
        description="The type of the message.",
    )
    headers: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Defines the IBM MQ message headers to include with this message. More "
            "than one header can be specified as a comma separated list. Supporting "
            "information on IBM MQ message formats can be found in the IBM MQ "
            "Knowledge Center. Optional if type = binary. headers MUST NOT be "
            "specified if type = string or jms."
        ),
    )
    description: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Provides additional information for application developers: describes "
            "the message type or format."
        ),
    )
    expiry: int | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "The recommended setting the client should use for the TTL (Time-To-Live) "
            "of the message. This is a period of time expressed in milliseconds and "
            "set by the application that puts the message. expiry values are API "
            "dependant e.g., MQI and JMS use different units of time and default "
            "values for unlimited. General information on IBM MQ message expiry can "
            "be found in the IBM MQ Knowledge Center. Optional, defaults to "
            "unlimited. expiry value MUST be either zero (unlimited) or greater than "
            "zero."
        ),
    )
    binding_version: str = Field(
        default="0.1.0",
        alias="bindingVersion",
        description="The version of this binding. Optional, defaults to latest.",
    )
