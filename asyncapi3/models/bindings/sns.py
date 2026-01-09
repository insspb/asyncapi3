"""SNS bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "SNSChannelBindings",
    "SNSConsumer",
    "SNSDeliveryPolicy",
    "SNSIdentifier",
    "SNSMessageBindings",
    "SNSOperationBindings",
    "SNSOrdering",
    "SNSPolicy",
    "SNSRedrivePolicy",
    "SNSServerBindings",
    "SNSStatement",
]

from typing import Any, Literal

from pydantic import Field

from asyncapi3.models.base_models import NonExtendableBaseModel
from asyncapi3.models.helpers import is_null


class SNSServerBindings(NonExtendableBaseModel):
    """
    SNS Server Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class SNSOrdering(NonExtendableBaseModel):
    """
    SNS Ordering.

    Configuration for FIFO SNS Topic.
    """

    type: Literal["standard", "FIFO"] = Field(
        description=(
            "Required. Defines the type of SNS Topic. Can be either standard or FIFO."
        ),
    )
    content_based_deduplication: bool = Field(
        default=False,
        alias="contentBasedDeduplication",
        description=(
            "Whether the de-duplication of messages should be turned on. Defaults to "
            "false."
        ),
    )


class SNSStatement(NonExtendableBaseModel):
    """
    SNS Statement.

    Controls a permission for this topic.
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
            "Required. The SNS permission being allowed or denied e.g. sns:Publish."
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


class SNSPolicy(NonExtendableBaseModel):
    """
    SNS Policy.

    The security policy for the SNS Topic.
    """

    statements: list[SNSStatement] = Field(
        description=(
            "An array of Statement objects, each of which controls a permission for "
            "this topic."
        ),
    )


class SNSChannelBindings(NonExtendableBaseModel):
    """
    SNS Channel Binding Object.

    This object contains information about the channel representation in SNS.

    We represent an AsyncAPI Channel with a Topic in SNS. The bindings here allow
    definition of a topic within SNS. We provide properties on the binding that allow
    creation of a topic in infrastructure-as-code scenarios. Be aware that although the
    binding offers that flexibility, it may be more maintainable to specify properties
    such as SNS Access Control Policy outside of AsyncAPI.

    SNS supports many optional properties. To mark a channel as SNS, but use default
    values for the channel properties, just use an empty object {}.
    """

    name: str = Field(
        description=(
            "Required. The name of the topic. Can be different from the channel name "
            "to allow flexibility around AWS resource naming limitations."
        ),
    )
    ordering: SNSOrdering | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "By default, we assume an unordered SNS topic. This field allows "
            "configuration of a FIFO SNS Topic."
        ),
    )
    policy: SNSPolicy | None = Field(
        default=None,
        exclude_if=is_null,
        description="The security policy for the SNS Topic.",
    )
    tags: dict[str, Any] | None = Field(
        default=None,
        exclude_if=is_null,
        description="Key-value pairs that represent AWS tags on the topic.",
    )
    binding_version: str = Field(
        default="1.0.0",
        alias="bindingVersion",
        description="The version of this binding. Optional, defaults to latest.",
    )


class SNSIdentifier(NonExtendableBaseModel):
    """
    SNS Identifier.

    We provide an Identifier Object to support providing the identifier of an externally
    defined endpoint for this SNS publication to target, or an endpoint on another
    binding against this Operation Object (via the name field).
    """

    url: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="The endpoint is a URL.",
    )
    email: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="The endpoint is an email address.",
    )
    phone: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="The endpoint is a phone number.",
    )
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
            "field called 'name' of a binding for that protocol on the Operation "
            "Object. "
            "For example, if the protocol is 'sqs' then the name refers to the name "
            "field sqs binding. We don't use $ref because we are referring, not "
            "including."
        ),
    )


class SNSDeliveryPolicy(NonExtendableBaseModel):
    """
    SNS Delivery Policy.

    Policy for retries to HTTP.
    """

    min_delay_target: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="minDelayTarget",
        description="The minimum delay for a retry in seconds.",
    )
    max_delay_target: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="maxDelayTarget",
        description="The maximum delay for a retry in seconds.",
    )
    num_retries: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="numRetries",
        description=(
            "The total number of retries, including immediate, pre-backoff, backoff, "
            "and post-backoff retries."
        ),
    )
    num_no_delay_retries: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="numNoDelayRetries",
        description="The number of immediate retries (with no delay).",
    )
    num_min_delay_retries: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="numMinDelayRetries",
        description="The number of immediate retries (with delay).",
    )
    num_max_delay_retries: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="numMaxDelayRetries",
        description=(
            "The number of post-backoff phase retries, with the maximum delay between "
            "retries."
        ),
    )
    backoff_function: (
        Literal["arithmetic", "exponential", "geometric", "linear"] | None
    ) = Field(
        default=None,
        exclude_if=is_null,
        alias="backoffFunction",
        description=(
            "The algorithm for backoff between retries. One of: arithmetic, "
            "exponential, geometric or linear."
        ),
    )
    max_receives_per_second: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="maxReceivesPerSecond",
        description="The maximum number of deliveries per second, per subscription.",
    )


class SNSRedrivePolicy(NonExtendableBaseModel):
    """
    SNS Redrive Policy.

    Prevent poison pill messages by moving un-processable messages to an SQS dead letter
    queue.
    """

    dead_letter_queue: SNSIdentifier = Field(
        alias="deadLetterQueue",
        description=(
            "Required. The SQS queue to use as a dead letter queue (DLQ). Note that "
            "you may have a Redrive Policy to put messages that cannot be delivered "
            "to an SQS queue, even if you use another protocol to consume messages "
            "from the queue, so it is defined at the level of the SNS Operation "
            "Binding Object in a Consumer Object (and is applied as part of an SNS "
            "Subscription). The SQS Binding describes how to define an SQS Binding "
            "that supports defining the target SQS of the Redrive Policy."
        ),
    )
    max_receive_count: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="maxReceiveCount",
        description=(
            "The number of times a message is delivered to the source queue before "
            "being moved to the dead-letter queue. Defaults to 10."
        ),
    )


class SNSConsumer(NonExtendableBaseModel):
    """
    SNS Consumer.

    The protocols that listen to this topic and their endpoints.
    """

    protocol: Literal[
        "http",
        "https",
        "email",
        "email-json",
        "sms",
        "sqs",
        "application",
        "lambda",
        "firehose",
    ] = Field(
        description=(
            "Required. The protocol that this endpoint receives messages by. Can be "
            "http, https, email, email-json, sms, sqs, application, lambda or firehose."
        ),
    )
    endpoint: SNSIdentifier = Field(
        description="Required. The endpoint messages are delivered to.",
    )
    filter_policy: dict[str, Any] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="filterPolicy",
        description=(
            "Only receive a subset of messages from the channel, determined by this "
            "policy."
        ),
    )
    filter_policy_scope: Literal["MessageAttributes", "MessageBody"] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="filterPolicyScope",
        description=(
            "Determines whether the FilterPolicy applies to MessageAttributes "
            "(default) or MessageBody."
        ),
    )
    raw_message_delivery: bool = Field(
        alias="rawMessageDelivery",
        description=(
            "Required. If true AWS SNS attributes are removed from the body, and for "
            "SQS, SNS message attributes are copied to SQS message attributes. If "
            "false the SNS attributes are included in the body."
        ),
    )
    redrive_policy: SNSRedrivePolicy | None = Field(
        default=None,
        exclude_if=is_null,
        alias="redrivePolicy",
        description=(
            "Prevent poison pill messages by moving un-processable messages to an SQS "
            "dead letter queue."
        ),
    )
    delivery_policy: SNSDeliveryPolicy | None = Field(
        default=None,
        exclude_if=is_null,
        alias="deliveryPolicy",
        description=(
            "Policy for retries to HTTP. The parameter is for that SNS Subscription "
            "and overrides any policy on the SNS Topic."
        ),
    )
    display_name: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="displayName",
        description="The display name to use with an SMS subscription.",
    )


class SNSOperationBindings(NonExtendableBaseModel):
    """
    SNS Operation Binding Object.

    This object contains information operation binding in SNS.

    We represent SNS producers via a subscribe Operation Object. In simple cases this
    may not require configuration, and can be shown as an empty SNS Binding Object i.e.
    {} if you need to explicitly indicate how a producer publishes to the channel.

    SNS consumers need an SNS Subscription that defines how they consume from SNS i.e.
    the protocol that they use, and any filters applied.

    The SNS binding does not describe the receiver. If you wish to define the receiver,
    add an Operation Binding Object for that receiver. For example, if you send message
    to an SQS queue from an SNS Topic, you would add a protocol of 'sqs' and an
    Identifier object for the queue. That identifier could be an ARN of a queue defined
    outside of the scope of AsyncAPI, but if you wanted to define the receiver you would
    use the name of a queue defined in an SQS Binding in the Operation Binding Object.

    We support an array of consumers via the consumers field. This allows you to
    represent multiple protocols consuming an SNS Topic in one file. You may also use it
    for multiple consumers with the same protocol, instead of representing each consumer
    in a separate file.
    """

    topic: SNSIdentifier | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Often we can assume that the SNS Topic is the channel name-we provide "
            "this field in case the you need to supply the ARN, or the Topic name is "
            "not the channel name in the AsyncAPI document."
        ),
    )
    consumers: list[SNSConsumer] = Field(
        description=(
            "Required. The protocols that listen to this topic and their endpoints. "
            "Required for receive operations."
        ),
    )
    delivery_policy: SNSDeliveryPolicy | None = Field(
        default=None,
        exclude_if=is_null,
        alias="deliveryPolicy",
        description=(
            "Policy for retries to HTTP. The field is the default for HTTP receivers "
            "of the SNS Topic which may be overridden by a specific consumer. Applies "
            "to send operations."
        ),
    )
    binding_version: str = Field(
        default="1.0.0",
        alias="bindingVersion",
        description="The version of this binding. Optional, defaults to latest.",
    )


class SNSMessageBindings(NonExtendableBaseModel):
    """
    SNS Message Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """
