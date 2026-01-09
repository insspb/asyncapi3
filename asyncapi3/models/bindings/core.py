"""Core bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "ChannelBindingsObject",
    "MessageBindingsObject",
    "OperationBindingsObject",
    "ServerBindingsObject",
]

from pydantic import Field

from asyncapi3.models.base_models import ExtendableBaseModel
from asyncapi3.models.bindings.amqp import (
    AMQPChannelBindings,
    AMQPMessageBindings,
    AMQPOperationBindings,
    AMQPServerBindings,
)
from asyncapi3.models.bindings.amqp1 import (
    AMQP1ChannelBindings,
    AMQP1MessageBindings,
    AMQP1OperationBindings,
    AMQP1ServerBindings,
)
from asyncapi3.models.bindings.anypointmq import (
    AnypointMQChannelBindings,
    AnypointMQMessageBindings,
    AnypointMQOperationBindings,
    AnypointMQServerBindings,
)
from asyncapi3.models.bindings.googlepubsub import (
    GooglePubSubChannelBindings,
    GooglePubSubMessageBindings,
    GooglePubSubOperationBindings,
    GooglePubSubServerBindings,
)
from asyncapi3.models.bindings.http import (
    HTTPChannelBindings,
    HTTPMessageBindings,
    HTTPOperationBindings,
    HTTPServerBindings,
)
from asyncapi3.models.bindings.ibmmq import (
    IBMMQChannelBindings,
    IBMMQMessageBindings,
    IBMMQOperationBindings,
    IBMMQServerBindings,
)
from asyncapi3.models.bindings.jms import (
    JMSChannelBindings,
    JMSMessageBindings,
    JMSOperationBindings,
    JMSServerBindings,
)
from asyncapi3.models.bindings.kafka import (
    KafkaChannelBindings,
    KafkaMessageBindings,
    KafkaOperationBindings,
    KafkaServerBindings,
)
from asyncapi3.models.bindings.mercure import (
    MercureChannelBindings,
    MercureMessageBindings,
    MercureOperationBindings,
    MercureServerBindings,
)
from asyncapi3.models.bindings.mqtt import (
    MQTTChannelBindings,
    MQTTMessageBindings,
    MQTTOperationBindings,
    MQTTServerBindings,
)
from asyncapi3.models.bindings.mqtt5 import (
    MQTT5ChannelBindings,
    MQTT5MessageBindings,
    MQTT5OperationBindings,
    MQTT5ServerBindings,
)
from asyncapi3.models.bindings.nats import (
    NATSChannelBindings,
    NATSMessageBindings,
    NATSOperationBindings,
    NATSServerBindings,
)
from asyncapi3.models.bindings.pulsar import (
    PulsarChannelBindings,
    PulsarMessageBindings,
    PulsarOperationBindings,
    PulsarServerBindings,
)
from asyncapi3.models.bindings.redis import (
    RedisChannelBindings,
    RedisMessageBindings,
    RedisOperationBindings,
    RedisServerBindings,
)
from asyncapi3.models.bindings.sns import (
    SNSChannelBindings,
    SNSMessageBindings,
    SNSOperationBindings,
    SNSServerBindings,
)
from asyncapi3.models.bindings.solace import (
    SolaceChannelBindings,
    SolaceMessageBindings,
    SolaceOperationBindings,
    SolaceServerBindings,
)
from asyncapi3.models.bindings.sqs import (
    SQSChannelBindings,
    SQSMessageBindings,
    SQSOperationBindings,
    SQSServerBindings,
)
from asyncapi3.models.bindings.stomp import (
    STOMPChannelBindings,
    STOMPMessageBindings,
    STOMPOperationBindings,
    STOMPServerBindings,
)
from asyncapi3.models.bindings.websockets import (
    WebSocketsChannelBindings,
    WebSocketsMessageBindings,
    WebSocketsOperationBindings,
    WebSocketsServerBindings,
)
from asyncapi3.models.helpers import is_null


class ServerBindingsObject(ExtendableBaseModel):
    """
    Server Bindings Object.

    Map describing protocol-specific definitions for a server.

    This object MAY be extended with Specification Extensions.
    """

    http: HTTPServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an HTTP server.",
    )
    ws: WebSocketsServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a WebSockets server.",
    )
    kafka: KafkaServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Kafka server.",
    )
    anypointmq: AnypointMQServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an Anypoint MQ server.",
    )
    amqp: AMQPServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an AMQP 0-9-1 server.",
    )
    amqp1: AMQP1ServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an AMQP 1.0 server.",
    )
    mqtt: MQTTServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an MQTT server.",
    )
    mqtt5: MQTT5ServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an MQTT 5 server.",
    )
    nats: NATSServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a NATS server.",
    )
    jms: JMSServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a JMS server.",
    )
    sns: SNSServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an SNS server.",
    )
    solace: SolaceServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Solace server.",
    )
    sqs: SQSServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an SQS server.",
    )
    stomp: STOMPServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a STOMP server.",
    )
    redis: RedisServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Redis server.",
    )
    mercure: MercureServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Mercure server.",
    )
    ibmmq: IBMMQServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an IBM MQ server.",
    )
    googlepubsub: GooglePubSubServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Google Cloud Pub/Sub server.",
    )
    pulsar: PulsarServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Pulsar server.",
    )


class ChannelBindingsObject(ExtendableBaseModel):
    """
    Channel Bindings Object.

    Map describing protocol-specific definitions for a channel.

    This object MAY be extended with Specification Extensions.
    """

    http: HTTPChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an HTTP channel.",
    )
    ws: WebSocketsChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a WebSockets channel.",
    )
    kafka: KafkaChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Kafka channel.",
    )
    anypointmq: AnypointMQChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an Anypoint MQ channel.",
    )
    amqp: AMQPChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an AMQP 0-9-1 channel.",
    )
    amqp1: AMQP1ChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an AMQP 1.0 channel.",
    )
    mqtt: MQTTChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an MQTT channel.",
    )
    mqtt5: MQTT5ChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an MQTT 5 channel.",
    )
    nats: NATSChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a NATS channel.",
    )
    jms: JMSChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a JMS channel.",
    )
    sns: SNSChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an SNS channel.",
    )
    solace: SolaceChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Solace channel.",
    )
    sqs: SQSChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an SQS channel.",
    )
    stomp: STOMPChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a STOMP channel.",
    )
    redis: RedisChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Redis channel.",
    )
    mercure: MercureChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Mercure channel.",
    )
    ibmmq: IBMMQChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an IBM MQ channel.",
    )
    googlepubsub: GooglePubSubChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Google Cloud Pub/Sub channel.",
    )
    pulsar: PulsarChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Pulsar channel.",
    )


class OperationBindingsObject(ExtendableBaseModel):
    """
    Operation Bindings Object.

    Map describing protocol-specific definitions for an operation.

    This object MAY be extended with Specification Extensions.
    """

    http: HTTPOperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an HTTP operation.",
    )
    ws: WebSocketsOperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a WebSockets operation.",
    )
    kafka: KafkaOperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Kafka operation.",
    )
    anypointmq: AnypointMQOperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an Anypoint MQ operation.",
    )
    amqp: AMQPOperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an AMQP 0-9-1 operation.",
    )
    amqp1: AMQP1OperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an AMQP 1.0 operation.",
    )
    mqtt: MQTTOperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an MQTT operation.",
    )
    mqtt5: MQTT5OperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an MQTT 5 operation.",
    )
    nats: NATSOperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a NATS operation.",
    )
    jms: JMSOperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a JMS operation.",
    )
    sns: SNSOperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an SNS operation.",
    )
    solace: SolaceOperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Solace operation.",
    )
    sqs: SQSOperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an SQS operation.",
    )
    stomp: STOMPOperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a STOMP operation.",
    )
    redis: RedisOperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Redis operation.",
    )
    mercure: MercureOperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Mercure operation.",
    )
    ibmmq: IBMMQOperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an IBM MQ operation.",
    )
    googlepubsub: GooglePubSubOperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Protocol-specific information for a Google Cloud Pub/Sub operation."
        ),
    )
    pulsar: PulsarOperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Pulsar operation.",
    )


class MessageBindingsObject(ExtendableBaseModel):
    """
    Message Bindings Object.

    Map describing protocol-specific definitions for a message.

    This object MAY be extended with Specification Extensions.
    """

    http: HTTPMessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Protocol-specific information for an HTTP message, i.e., a request or a "
            "response."
        ),
    )
    ws: WebSocketsMessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a WebSockets message.",
    )
    kafka: KafkaMessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Kafka message.",
    )
    anypointmq: AnypointMQMessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an Anypoint MQ message.",
    )
    amqp: AMQPMessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an AMQP 0-9-1 message.",
    )
    amqp1: AMQP1MessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an AMQP 1.0 message.",
    )
    mqtt: MQTTMessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an MQTT message.",
    )
    mqtt5: MQTT5MessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an MQTT 5 message.",
    )
    nats: NATSMessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a NATS message.",
    )
    jms: JMSMessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a JMS message.",
    )
    sns: SNSMessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an SNS message.",
    )
    solace: SolaceMessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Solace message.",
    )
    sqs: SQSMessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an SQS message.",
    )
    stomp: STOMPMessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a STOMP message.",
    )
    redis: RedisMessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Redis message.",
    )
    mercure: MercureMessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Mercure message.",
    )
    ibmmq: IBMMQMessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for an IBM MQ message.",
    )
    googlepubsub: GooglePubSubMessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Google Cloud Pub/Sub message.",
    )
    pulsar: PulsarMessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        description="Protocol-specific information for a Pulsar message.",
    )
