"""Kafka bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "KafkaChannelBindings",
    "KafkaMessageBindings",
    "KafkaOperationBindings",
    "KafkaServerBindings",
    "KafkaTopicConfiguration",
]

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from asyncapi3.models.base import Reference
from asyncapi3.models.helpers import is_null
from asyncapi3.models.schema import Schema


class KafkaServerBindings(BaseModel):
    """
    Kafka Server Binding Object.

    This object contains information about the server representation in Kafka.

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

    schema_registry_url: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="schemaRegistryUrl",
        description=(
            "API URL for the Schema Registry used when producing Kafka messages (if a "
            "Schema Registry was used)."
        ),
    )
    schema_registry_vendor: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="schemaRegistryVendor",
        description=(
            "The vendor of Schema Registry and Kafka serdes library that should be "
            "used (e.g. apicurio, confluent, ibm, or karapace). MUST NOT be specified "
            "if schemaRegistryUrl is not specified."
        ),
    )
    binding_version: str = Field(
        default="0.5.0",
        alias="bindingVersion",
        description="The version of this binding.",
    )


class KafkaTopicConfiguration(BaseModel):
    """
    Kafka TopicConfiguration Object.

    This objects contains information about the API relevant topic configuration in
    Kafka.

    This object MAY contain the properties defined below including optional additional
    properties.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    cleanup_policy: list[Literal["delete", "compact"]] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="cleanup.policy",
        description=(
            "The cleanup.policy configuration option. Array may only contain delete "
            "and/or compact."
        ),
    )
    retention_ms: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="retention.ms",
        description="The retention.ms configuration option.",
    )
    retention_bytes: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="retention.bytes",
        description="The retention.bytes configuration option.",
    )
    delete_retention_ms: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="delete.retention.ms",
        description="The delete.retention.ms configuration option.",
    )
    max_message_bytes: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="max.message.bytes",
        description="The max.message.bytes configuration option.",
    )
    confluent_key_schema_validation: bool | None = Field(
        default=None,
        exclude_if=is_null,
        alias="confluent.key.schema.validation",
        description=(
            "It shows whether the schema validation for the message key is enabled. "
            "Vendor specific config."
        ),
    )
    confluent_key_subject_name_strategy: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="confluent.key.subject.name.strategy",
        description=(
            "The name of the schema lookup strategy for the message key. Vendor "
            "specific config. Clients should default to the vendor default if not "
            "supplied."
        ),
    )
    confluent_value_schema_validation: bool | None = Field(
        default=None,
        exclude_if=is_null,
        alias="confluent.value.schema.validation",
        description=(
            "It shows whether the schema validation for the message value is enabled. "
            "Vendor specific config."
        ),
    )
    confluent_value_subject_name_strategy: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="confluent.value.subject.name.strategy",
        description=(
            "The name of the schema lookup strategy for the message value. Vendor "
            "specific config. Clients should default to the vendor default if not "
            "supplied."
        ),
    )


class KafkaChannelBindings(BaseModel):
    """
    Kafka Channel Binding Object.

    This object contains information about the channel representation in Kafka (eg. a
    Kafka topic).

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

    topic: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="Kafka topic name if different from channel name.",
    )
    partitions: int | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Number of partitions configured on this topic (useful to know how many "
            "parallel consumers you may run). Must be positive."
        ),
    )
    replicas: int | None = Field(
        default=None,
        exclude_if=is_null,
        description="Number of replicas configured on this topic. MUST be positive.",
    )
    topic_configuration: KafkaTopicConfiguration | None = Field(
        default=None,
        exclude_if=is_null,
        alias="topicConfiguration",
        description="Topic configuration properties that are relevant for the API.",
    )
    binding_version: str = Field(
        default="0.5.0",
        alias="bindingVersion",
        description="The version of this binding. If omitted, 'latest' MUST be assumed",
    )


class KafkaOperationBindings(BaseModel):
    """
    Kafka Operation Binding Object.

    This object contains information about the operation representation in Kafka
    (eg. the way to consume messages).

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

    group_id: Schema | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="groupId",
        description="Id of the consumer group.",
    )
    client_id: Schema | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="clientId",
        description="Id of the consumer inside a consumer group.",
    )
    binding_version: str = Field(
        default="0.5.0",
        alias="bindingVersion",
        description="The version of this binding. If omitted, 'latest' MUST be assumed",
    )


class KafkaMessageBindings(BaseModel):
    """
    Kafka Message Binding Object.

    This object contains information about the message representation in Kafka.

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

    # TODO: Think about AVRO Schema
    key: Schema | Reference | dict[str, Any] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "The message key. NOTE: You can also use the reference object way."
        ),
    )
    schema_id_location: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="schemaIdLocation",
        description=(
            "If a Schema Registry is used when performing this operation, tells where "
            "the id of schema is stored (e.g. header or payload). MUST NOT be "
            "specified if schemaRegistryUrl is not specified at the Server level."
        ),
    )
    schema_id_payload_encoding: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="schemaIdPayloadEncoding",
        description=(
            "Number of bytes or vendor specific values when schema id is encoded in "
            "payload (e.g confluent/ apicurio-legacy / apicurio-new). MUST NOT be "
            "specified if schemaRegistryUrl is not specified at the Server level."
        ),
    )
    schema_lookup_strategy: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="schemaLookupStrategy",
        description=(
            "Freeform string for any naming strategy class to use. Clients should "
            "default to the vendor default if not supplied. MUST NOT be specified if "
            "schemaRegistryUrl is not specified at the Server level."
        ),
    )
    binding_version: str = Field(
        default="0.5.0",
        alias="bindingVersion",
        description="The version of this binding. If omitted, 'latest' MUST be assumed",
    )
