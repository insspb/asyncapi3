"""SQS bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "SQSChannelBindings",
    "SQSIdentifier",
    "SQSMessageBindings",
    "SQSOperationBindings",
    "SQSPolicy",
    "SQSQueue",
    "SQSRedrivePolicy",
    "SQSServerBindings",
    "SQSStatement",
]

from typing import Any, Literal

from pydantic import Field

from asyncapi3.models.base_models import NonExtendableBaseModel
from asyncapi3.models.helpers import is_null


class SQSServerBindings(NonExtendableBaseModel):
    """
    SQS Server Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class SQSStatement(NonExtendableBaseModel):
    """
    SQS Statement.

    Controls a permission for this queue.
    """

    effect: Literal["Allow", "Deny"] = Field(
        description="Required. Either 'Allow' or 'Deny'.",
    )
    principal: str | dict[str, str | list[str]] = Field(
        description=(
            "Required. The AWS account(s) or resource ARN(s) that the statement "
            "applies to."
        ),
    )
    action: str | list[str] = Field(
        description=(
            "Required. The SQS permission being allowed or denied e.g. sqs:SendMessage."
        ),
    )
    resource: str | list[str] | None = Field(
        default=None,
        exclude_if=is_null,
        description="The resource(s) that this policy applies to.",
    )
    condition: dict[str, Any] | list[dict[str, Any]] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Specific circumstances under which the policy grants permission."
        ),
    )


class SQSPolicy(NonExtendableBaseModel):
    """
    SQS Policy.

    The security policy for the SQS Queue.
    """

    statements: list[SQSStatement] = Field(
        alias="Statements",
        description=(
            "Required. An array of Statement objects, each of which controls a "
            "permission for this queue."
        ),
    )


class SQSIdentifier(NonExtendableBaseModel):
    """
    SQS Identifier.

    Used to identify an endpoint or queue.
    """

    arn: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "The target is an ARN. For example, for SQS, the identifier may be an ARN, "
            "which will be of the form: arn:aws:sqs:{region}:{account-id}:{queueName}."
        ),
    )
    name: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "The endpoint is identified by a name, which corresponds to an identifying "
            "field called 'name' of a binding for that protocol on this publish "
            "Operation Object. For example, if the protocol is 'sqs' then the name "
            "refers to the name field sqs binding."
        ),
    )


class SQSRedrivePolicy(NonExtendableBaseModel):
    """
    SQS Redrive Policy.

    Prevent poison pill messages by moving un-processable messages to an SQS dead letter
    queue.
    """

    dead_letter_queue: SQSIdentifier = Field(
        alias="deadLetterQueue",
        description="The SQS queue to use as a dead letter queue (DLQ).",
    )
    max_receive_count: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="maxReceiveCount",
        description=(
            "The number of times a message is delivered to the source queue before "
            "being moved to the dead-letter queue. Default is 10."
        ),
    )


class SQSQueue(NonExtendableBaseModel):
    """
    SQS Queue.

    A definition of the queue that will be used as the channel.
    """

    name: str = Field(
        description=(
            "Required. The name of the queue. When an SNS Operation Binding Object "
            "references an SQS queue by name, the identifier should be the one in "
            "this field."
        ),
    )
    fifo_queue: bool = Field(
        alias="fifoQueue",
        description="Required. Is this a FIFO queue?",
    )
    deduplication_scope: Literal["messageGroup", "queue"] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="deduplicationScope",
        description=(
            "Specifies whether message deduplication occurs at the message group or "
            "queue level. Valid values are messageGroup and queue. This property "
            "applies only to high throughput for FIFO queues."
        ),
    )
    fifo_throughput_limit: Literal["perQueue", "perMessageGroupId"] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="fifoThroughputLimit",
        description=(
            "Specifies whether the FIFO queue throughput quota applies to the entire "
            "queue or per message group. Valid values are perQueue and "
            "perMessageGroupId. The perMessageGroupId value is allowed only when the "
            "value for DeduplicationScope is messageGroup. Setting both these values "
            "as such will enable high throughput on a FIFO queue. As above, this "
            "property applies only to high throughput for FIFO queues."
        ),
    )
    delivery_delay: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="deliveryDelay",
        description=(
            "The number of seconds to delay before a message sent to the queue can be "
            "received. Used to create a delay queue. Range is 0 to 15 minutes. "
            "Defaults to 0."
        ),
    )
    visibility_timeout: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="visibilityTimeout",
        description=(
            "The length of time, in seconds, that a consumer locks a message - hiding "
            "it from reads - before it is unlocked and can be read again. Range from "
            "0 to 12 hours (43200 seconds). Defaults to 30 seconds."
        ),
    )
    receive_message_wait_time: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="receiveMessageWaitTime",
        description=(
            "Determines if the queue uses short polling or long polling. Set to zero "
            "(the default) the queue reads available messages and returns immediately. "
            "Set to a non-zero integer, long polling waits the specified number of "
            "seconds for messages to arrive before returning."
        ),
    )
    message_retention_period: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="messageRetentionPeriod",
        description=(
            "How long to retain a message on the queue in seconds, unless deleted. The "
            "range is 60 (1 minute) to 1,209,600 (14 days). The default is 345,600 "
            "(4 days)."
        ),
    )
    redrive_policy: SQSRedrivePolicy | None = Field(
        default=None,
        exclude_if=is_null,
        alias="redrivePolicy",
        description=(
            "Prevent poison pill messages by moving un-processable messages to an SQS "
            "dead letter queue."
        ),
    )
    policy: SQSPolicy | None = Field(
        default=None,
        exclude_if=is_null,
        description="The security policy for the SQS Queue.",
    )
    tags: dict[str, Any] | None = Field(
        default=None,
        exclude_if=is_null,
        description="Key-value pairs that represent AWS tags on the queue.",
    )


class SQSChannelBindings(NonExtendableBaseModel):
    """
    SQS Channel Binding Object.

    Use the Channel Binding Operation for Point-to-Point SQS channels.

    There are three likely scenarios for use of the Channel Binding Object:

    - One file defines both publish and subscribe operations, for example if we were
      implementing the work queue pattern to offload work from an HTTP API endpoint to
      a worker process. In this case the channel would be defined on the Channel Object
      in that single file.
    - The producer and consumer both have an AsyncAPI specification file, and the
      producer is raising an event, for example interop between microservices, and the
      producer 'owns' the channel definition and thus has the SQS Binding on its
      Channel Object.
    - The producer and consumer both have an AsyncAPI specification file, and the
      consumer receives commands, for example interop between microservices, and the
      consumer 'owns' the channel definition and thus has the SQS Binding on its
      Channel Object.

    An SQS queue can set up a Dead Letter Queue as part of a Redelivery Policy. To
    support this requirement, the Channel Binding Object allows you to define both a
    Queue Object to use as the Channel or target in a publish Operation and a Dead
    Letter Queue. You can then refer to the Dead letter Queue in the Redrive Policy
    using the Identifier Object and setting the name field to match the name field of
    your Dead Letter Queue Object. (If you define the DLQ externally, the Identifier
    also supports an ARN).
    """

    queue: SQSQueue = Field(
        description=(
            "Required. A definition of the queue that will be used as the channel."
        ),
    )
    dead_letter_queue: SQSQueue | None = Field(
        default=None,
        exclude_if=is_null,
        alias="deadLetterQueue",
        description=(
            "A definition of the queue that will be used for un-processable messages."
        ),
    )
    binding_version: str = Field(
        default="0.3.0",
        alias="bindingVersion",
        description="The version of this binding. Optional, defaults to latest.",
    )


class SQSOperationBindings(NonExtendableBaseModel):
    """
    SQS Operation Binding Object.

    On an Operation Binding Object we support an array of Queue objects. Members of this
    array may be Queue Objects that define the endpoint field required by an SNS
    Operation Binding Object delivering by the SQS protocol or Queue Objects that define
    the Dead Letter Queue used by either the Redrive Policy of the SNS Subscription (see
    the SNS Binding Object) or the Redrive Policy of the SQS Queue. The name of the
    Queue Object is used by an Identifier field on either the endpoint field of the
    SNS Operation Object of deadLetterQueue on the Redrive Policy to identify the
    required member of this array.
    """

    queues: list[SQSQueue] = Field(
        description=(
            "Required. Queue objects that are either the endpoint for an SNS Operation "
            "Binding Object, or the deadLetterQueue of the SQS Operation Binding "
            "Object."
        ),
    )
    binding_version: str = Field(
        default="0.3.0",
        alias="bindingVersion",
        description="The version of this binding. Optional, defaults to latest.",
    )


class SQSMessageBindings(NonExtendableBaseModel):
    """
    SQS Message Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """
