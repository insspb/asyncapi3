"""AMQP 0-9-1 bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "AMQPChannelBindings",
    "AMQPExchange",
    "AMQPMessageBindings",
    "AMQPOperationBindings",
    "AMQPQueue",
    "AMQPServerBindings",
]


from typing import Literal

from pydantic import Field, field_validator, model_validator

from asyncapi3.models.base_models import NonExtendableBaseModel
from asyncapi3.models.helpers import is_null


class AMQPServerBindings(NonExtendableBaseModel):
    """
    AMQP Server Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class AMQPExchange(NonExtendableBaseModel):
    """
    AMQP Exchange.

    When is=routingKey, this object defines the exchange properties.
    """

    name: str = Field(
        max_length=255,
        description="The name of the exchange. It MUST NOT exceed 255 characters long.",
    )
    type: Literal["topic", "direct", "fanout", "default", "headers"] = Field(
        description=(
            "The type of the exchange. Can be either topic, direct, fanout, default or "
            "headers."
        ),
    )
    durable: bool | None = Field(
        default=None,
        exclude_if=is_null,
        description="Whether the exchange should survive broker restarts or not.",
    )
    auto_delete: bool | None = Field(
        default=None,
        exclude_if=is_null,
        alias="autoDelete",
        description=(
            "Whether the exchange should be deleted when the last queue is unbound "
            "from it."
        ),
    )
    vhost: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="The virtual host of the exchange. Defaults to /.",
    )


class AMQPQueue(NonExtendableBaseModel):
    """
    AMQP Queue.

    When is=queue, this object defines the queue properties.
    """

    name: str | None = Field(
        default=None,
        exclude_if=is_null,
        max_length=255,
        description="The name of the queue. It MUST NOT exceed 255 characters long.",
    )
    durable: bool | None = Field(
        default=None,
        exclude_if=is_null,
        description="Whether the queue should survive broker restarts or not.",
    )
    exclusive: bool | None = Field(
        default=None,
        exclude_if=is_null,
        description="Whether the queue should be used only by one connection or not.",
    )
    auto_delete: bool | None = Field(
        default=None,
        exclude_if=is_null,
        alias="autoDelete",
        description=(
            "Whether the queue should be deleted when the last consumer unsubscribes."
        ),
    )
    vhost: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="The virtual host of the queue. Defaults to /.",
    )


class AMQPChannelBindings(NonExtendableBaseModel):
    """
    AMQP Channel Binding Object.

    This object contains information about the channel representation in AMQP.

    This object MUST contain only the properties defined below.
    """

    is_: Literal["queue", "routingKey"] = Field(
        alias="is",
        description=(
            "Defines what type of channel is it. Can be either queue or routingKey "
            "(default)."
        ),
    )
    exchange: AMQPExchange | None = Field(
        default=None,
        exclude_if=is_null,
        description="When is=routingKey, this object defines the exchange properties.",
    )
    queue: AMQPQueue | None = Field(
        default=None,
        exclude_if=is_null,
        description="When is=queue, this object defines the queue properties.",
    )
    binding_version: str = Field(
        default="0.3.0",
        alias="bindingVersion",
        description="The version of this binding. If omitted, 'latest' MUST be assumed",
    )

    @model_validator(mode="after")
    def validate_exchange_queue_depending_on_is(self) -> "AMQPChannelBindings":
        """
        Validate that exchange and queue fields are set according to the 'is' field.

        When is='routingKey', exchange must be provided and queue must not be provided.
        When is='queue', queue must be provided and exchange must not be provided.
        """
        if self.is_ == "routingKey":
            if self.exchange is None:
                raise ValueError("exchange must be provided when is='routingKey'")
            if self.queue is not None:
                raise ValueError("queue must not be provided when is='routingKey'")
        elif self.is_ == "queue":
            if self.queue is None:
                raise ValueError("queue must be provided when is='queue'")
            if self.exchange is not None:
                raise ValueError("exchange must not be provided when is='queue'")
        return self


class AMQPOperationBindings(NonExtendableBaseModel):
    """
    AMQP Operation Binding Object.

    This object contains information about the operation representation in AMQP.

    This object MUST contain only the properties defined below.
    """

    expiration: int | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "TTL (Time-To-Live) for the message. It MUST be greater than or equal to "
            "zero."
        ),
    )
    user_id: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="userId",
        description="Identifies the user who has sent the message.",
    )
    cc: list[str] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "The routing keys the message should be routed to at the time of "
            "publishing."
        ),
    )
    priority: int | None = Field(
        default=None,
        exclude_if=is_null,
        description="A priority for the message.",
    )
    delivery_mode: Literal[1, 2] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="deliveryMode",
        description=(
            "Delivery mode of the message. Its value MUST be either 1 (transient) or 2 "
            "(persistent)."
        ),
    )
    mandatory: bool | None = Field(
        default=None,
        exclude_if=is_null,
        description="Whether the message is mandatory or not.",
    )
    bcc: list[str] | None = Field(
        default=None,
        exclude_if=is_null,
        description="Like cc but consumers will not receive this information.",
    )
    timestamp: bool | None = Field(
        default=None,
        exclude_if=is_null,
        description="Whether the message should include a timestamp or not.",
    )
    ack: bool | None = Field(
        default=None,
        exclude_if=is_null,
        description="Whether the consumer should ack the message or not.",
    )
    binding_version: str = Field(
        default="0.3.0",
        alias="bindingVersion",
        description="The version of this binding. If omitted, 'latest' MUST be assumed",
    )

    @field_validator("expiration")
    @classmethod
    def validate_expiration(cls, expiration: int | None) -> int | None:
        """Validate that expiration is greater than or equal to zero."""
        if expiration is not None and expiration < 0:
            raise ValueError("expiration must be greater than or equal to zero")
        return expiration


class AMQPMessageBindings(NonExtendableBaseModel):
    """
    AMQP Message Binding Object.

    This object contains information about the message representation in AMQP.

    This object MUST contain only the properties defined below.
    """

    content_encoding: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="contentEncoding",
        description="A MIME encoding for the message content.",
    )
    message_type: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="messageType",
        description="Application-specific message type.",
    )
    binding_version: str = Field(
        default="0.3.0",
        alias="bindingVersion",
        description="The version of this binding. If omitted, 'latest' MUST be assumed",
    )
