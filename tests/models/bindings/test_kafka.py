"""Tests for Kafka bindings models."""

from typing import Any

import yaml

from pytest_cases import parametrize_with_cases

from asyncapi3.models.bindings.kafka import (
    KafkaChannelBindings,
    KafkaMessageBindings,
    KafkaOperationBindings,
    KafkaServerBindings,
    KafkaTopicConfiguration,
)
from asyncapi3.models.schema import Schema


# Server Bindings Serialization Test Cases
def case_kafka_server_binding_serialization_empty() -> tuple[KafkaServerBindings, dict]:
    """KafkaServerBindings serialization empty."""
    kafka_binding = KafkaServerBindings()
    expected: dict[str, Any] = {"bindingVersion": "0.5.0"}
    return kafka_binding, expected


def case_kafka_server_binding_serialization_full() -> tuple[KafkaServerBindings, dict]:
    """KafkaServerBindings serialization with all fields."""
    kafka_binding = KafkaServerBindings(
        schema_registry_url="https://my-schema-registry.com",
        schema_registry_vendor="confluent",
    )
    expected: dict[str, Any] = {
        "schemaRegistryUrl": "https://my-schema-registry.com",
        "schemaRegistryVendor": "confluent",
        "bindingVersion": "0.5.0",
    }
    return kafka_binding, expected


# Channel Bindings Serialization Test Cases
def case_kafka_channel_binding_serialization_empty() -> tuple[
    KafkaChannelBindings, dict
]:
    """KafkaChannelBindings serialization empty."""
    kafka_binding = KafkaChannelBindings()
    expected: dict[str, Any] = {"bindingVersion": "0.5.0"}
    return kafka_binding, expected


def case_kafka_channel_binding_serialization_minimal() -> tuple[
    KafkaChannelBindings, dict
]:
    """KafkaChannelBindings serialization with minimal fields."""
    kafka_binding = KafkaChannelBindings(topic="my-topic")
    expected: dict[str, Any] = {
        "topic": "my-topic",
        "bindingVersion": "0.5.0",
    }
    return kafka_binding, expected


def case_kafka_channel_binding_serialization_full() -> tuple[
    KafkaChannelBindings, dict
]:
    """KafkaChannelBindings serialization with all fields."""
    kafka_binding = KafkaChannelBindings(
        topic="my-specific-topic-name",
        partitions=20,
        replicas=3,
        topic_configuration=KafkaTopicConfiguration(
            cleanup_policy=["delete", "compact"],
            retention_ms=604800000,
            retention_bytes=1000000000,
            delete_retention_ms=86400000,
            max_message_bytes=1048588,
        ),
    )
    expected: dict[str, Any] = {
        "topic": "my-specific-topic-name",
        "partitions": 20,
        "replicas": 3,
        "topicConfiguration": {
            "cleanup.policy": ["delete", "compact"],
            "retention.ms": 604800000,
            "retention.bytes": 1000000000,
            "delete.retention.ms": 86400000,
            "max.message.bytes": 1048588,
        },
        "bindingVersion": "0.5.0",
    }
    return kafka_binding, expected


# Operation Bindings Serialization Test Cases
def case_kafka_operation_binding_serialization_empty() -> tuple[
    KafkaOperationBindings, dict
]:
    """KafkaOperationBindings serialization empty."""
    kafka_binding = KafkaOperationBindings()
    expected: dict[str, Any] = {"bindingVersion": "0.5.0"}
    return kafka_binding, expected


def case_kafka_operation_binding_serialization_with_schemas() -> tuple[
    KafkaOperationBindings, dict
]:
    """KafkaOperationBindings serialization with groupId and clientId as Schema."""
    kafka_binding = KafkaOperationBindings(
        group_id=Schema(type="string", enum=["myGroupId"]),
        client_id=Schema(type="string", enum=["myClientId"]),
    )
    expected: dict[str, Any] = {
        "groupId": {
            "type": "string",
            "enum": ["myGroupId"],
        },
        "clientId": {
            "type": "string",
            "enum": ["myClientId"],
        },
        "bindingVersion": "0.5.0",
    }
    return kafka_binding, expected


# Message Bindings Serialization Test Cases
def case_kafka_message_binding_serialization_empty() -> tuple[
    KafkaMessageBindings, dict
]:
    """KafkaMessageBindings serialization empty."""
    kafka_binding = KafkaMessageBindings()
    expected: dict[str, Any] = {"bindingVersion": "0.5.0"}
    return kafka_binding, expected


def case_kafka_message_binding_serialization_confluent() -> tuple[
    KafkaMessageBindings, dict
]:
    """KafkaMessageBindings serialization for Confluent schema registry."""
    kafka_binding = KafkaMessageBindings(
        key=Schema(type="string", enum=["myKey"]),
        schema_id_location="payload",
        schema_id_payload_encoding="4",
    )
    expected: dict[str, Any] = {
        "key": {
            "type": "string",
            "enum": ["myKey"],
        },
        "schemaIdLocation": "payload",
        "schemaIdPayloadEncoding": "4",
        "bindingVersion": "0.5.0",
    }
    return kafka_binding, expected


def case_kafka_message_binding_serialization_apicurio() -> tuple[
    KafkaMessageBindings, dict
]:
    """KafkaMessageBindings serialization for Apicurio schema registry."""
    kafka_binding = KafkaMessageBindings(
        key=Schema(type="string", enum=["myKey"]),
        schema_id_location="payload",
        schema_id_payload_encoding="apicurio-new",
        schema_lookup_strategy="TopicIdStrategy",
    )
    expected: dict[str, Any] = {
        "key": {
            "type": "string",
            "enum": ["myKey"],
        },
        "schemaIdLocation": "payload",
        "schemaIdPayloadEncoding": "apicurio-new",
        "schemaLookupStrategy": "TopicIdStrategy",
        "bindingVersion": "0.5.0",
    }
    return kafka_binding, expected


# Topic Configuration Serialization Test Cases
def case_kafka_topic_configuration_serialization_empty() -> tuple[
    KafkaTopicConfiguration, dict
]:
    """KafkaTopicConfiguration serialization empty."""
    topic_config = KafkaTopicConfiguration()
    expected: dict[str, Any] = {}
    return topic_config, expected


def case_kafka_topic_configuration_serialization_full() -> tuple[
    KafkaTopicConfiguration, dict
]:
    """KafkaTopicConfiguration serialization with all fields."""
    topic_config = KafkaTopicConfiguration(
        cleanup_policy=["delete", "compact"],
        retention_ms=604800000,
        retention_bytes=1000000000,
        delete_retention_ms=86400000,
        max_message_bytes=1048588,
        confluent_key_schema_validation=True,
        confluent_key_subject_name_strategy="TopicNameStrategy",
        confluent_value_schema_validation=True,
        confluent_value_subject_name_strategy="TopicNameStrategy",
    )
    expected: dict[str, Any] = {
        "cleanup.policy": ["delete", "compact"],
        "retention.ms": 604800000,
        "retention.bytes": 1000000000,
        "delete.retention.ms": 86400000,
        "max.message.bytes": 1048588,
        "confluent.key.schema.validation": True,
        "confluent.key.subject.name.strategy": "TopicNameStrategy",
        "confluent.value.schema.validation": True,
        "confluent.value.subject.name.strategy": "TopicNameStrategy",
    }
    return topic_config, expected


class TestKafkaServerBindings:
    """Tests for KafkaServerBindings model."""

    def test_kafka_server_bindings_validation_empty(self) -> None:
        """Test KafkaServerBindings model validation with empty fields."""
        yaml_data = """
        kafka:
          bindingVersion: '0.5.0'
        """
        data = yaml.safe_load(yaml_data)
        kafka_binding = KafkaServerBindings.model_validate(data["kafka"])

        # Verify all fields
        assert kafka_binding.binding_version == "0.5.0"
        assert kafka_binding.schema_registry_url is None
        assert kafka_binding.schema_registry_vendor is None

    def test_kafka_server_bindings_validation_full(self) -> None:
        """Test KafkaServerBindings model validation with all fields."""
        yaml_data = """
        kafka:
          schemaRegistryUrl: 'https://my-schema-registry.com'
          schemaRegistryVendor: 'confluent'
          bindingVersion: '0.5.0'
        """
        data = yaml.safe_load(yaml_data)
        kafka_binding = KafkaServerBindings.model_validate(data["kafka"])

        # Verify all fields
        assert kafka_binding.binding_version == "0.5.0"
        assert kafka_binding.schema_registry_url == "https://my-schema-registry.com"
        assert kafka_binding.schema_registry_vendor == "confluent"

    @parametrize_with_cases(
        "kafka_binding,expected",
        cases=[
            case_kafka_server_binding_serialization_empty,
            case_kafka_server_binding_serialization_full,
        ],
    )
    def test_kafka_server_bindings_serialization(
        self,
        kafka_binding: KafkaServerBindings,
        expected: dict,
    ) -> None:
        """Test KafkaServerBindings serialization."""
        dumped = kafka_binding.model_dump()
        assert dumped == expected


class TestKafkaChannelBindings:
    """Tests for KafkaChannelBindings model."""

    def test_kafka_channel_bindings_validation_empty(self) -> None:
        """Test KafkaChannelBindings model validation with empty fields."""
        yaml_data = """
        kafka:
          bindingVersion: '0.5.0'
        """
        data = yaml.safe_load(yaml_data)
        kafka_binding = KafkaChannelBindings.model_validate(data["kafka"])

        # Verify all fields
        assert kafka_binding.binding_version == "0.5.0"
        assert kafka_binding.topic is None
        assert kafka_binding.partitions is None
        assert kafka_binding.replicas is None
        assert kafka_binding.topic_configuration is None

    def test_kafka_channel_bindings_validation_minimal(self) -> None:
        """Test KafkaChannelBindings model validation with minimal fields."""
        yaml_data = """
        kafka:
          topic: 'my-topic'
          bindingVersion: '0.5.0'
        """
        data = yaml.safe_load(yaml_data)
        kafka_binding = KafkaChannelBindings.model_validate(data["kafka"])

        # Verify all fields
        assert kafka_binding.binding_version == "0.5.0"
        assert kafka_binding.topic == "my-topic"
        assert kafka_binding.partitions is None
        assert kafka_binding.replicas is None
        assert kafka_binding.topic_configuration is None

    def test_kafka_channel_bindings_validation_full(self) -> None:
        """Test KafkaChannelBindings model validation with all fields."""
        yaml_data = """
        kafka:
          topic: 'my-specific-topic-name'
          partitions: 20
          replicas: 3
          topicConfiguration:
            cleanup.policy: ["delete", "compact"]
            retention.ms: 604800000
            retention.bytes: 1000000000
            delete.retention.ms: 86400000
            max.message.bytes: 1048588
          bindingVersion: '0.5.0'
        """
        data = yaml.safe_load(yaml_data)
        kafka_binding = KafkaChannelBindings.model_validate(data["kafka"])

        # Verify all fields
        assert kafka_binding.binding_version == "0.5.0"
        assert kafka_binding.topic == "my-specific-topic-name"
        assert kafka_binding.partitions == 20
        assert kafka_binding.replicas == 3
        assert kafka_binding.topic_configuration is not None
        assert isinstance(kafka_binding.topic_configuration, KafkaTopicConfiguration)
        assert kafka_binding.topic_configuration.cleanup_policy == [
            "delete",
            "compact",
        ]
        assert kafka_binding.topic_configuration.retention_ms == 604800000
        assert kafka_binding.topic_configuration.retention_bytes == 1000000000
        assert kafka_binding.topic_configuration.delete_retention_ms == 86400000
        assert kafka_binding.topic_configuration.max_message_bytes == 1048588

    @parametrize_with_cases(
        "kafka_binding,expected",
        cases=[
            case_kafka_channel_binding_serialization_empty,
            case_kafka_channel_binding_serialization_minimal,
            case_kafka_channel_binding_serialization_full,
        ],
    )
    def test_kafka_channel_bindings_serialization(
        self,
        kafka_binding: KafkaChannelBindings,
        expected: dict,
    ) -> None:
        """Test KafkaChannelBindings serialization."""
        dumped = kafka_binding.model_dump()
        assert dumped == expected


class TestKafkaTopicConfiguration:
    """Tests for KafkaTopicConfiguration model."""

    @parametrize_with_cases(
        "topic_config,expected",
        cases=[
            case_kafka_topic_configuration_serialization_empty,
            case_kafka_topic_configuration_serialization_full,
        ],
    )
    def test_kafka_topic_configuration_serialization(
        self,
        topic_config: KafkaTopicConfiguration,
        expected: dict,
    ) -> None:
        """Test KafkaTopicConfiguration serialization."""
        dumped = topic_config.model_dump()
        assert dumped == expected


class TestKafkaOperationBindings:
    """Tests for KafkaOperationBindings model."""

    def test_kafka_operation_bindings_validation_empty(self) -> None:
        """Test KafkaOperationBindings model validation with empty fields."""
        yaml_data = """
        kafka:
          bindingVersion: '0.5.0'
        """
        data = yaml.safe_load(yaml_data)
        kafka_binding = KafkaOperationBindings.model_validate(data["kafka"])

        # Verify all fields
        assert kafka_binding.binding_version == "0.5.0"
        assert kafka_binding.group_id is None
        assert kafka_binding.client_id is None

    def test_kafka_operation_bindings_validation_with_schemas(self) -> None:
        """Test KafkaOperationBindings model validation with groupId and clientId as Schema."""
        yaml_data = """
        kafka:
          groupId:
            type: string
            enum: ['myGroupId']
          clientId:
            type: string
            enum: ['myClientId']
          bindingVersion: '0.5.0'
        """
        data = yaml.safe_load(yaml_data)
        kafka_binding = KafkaOperationBindings.model_validate(data["kafka"])

        # Verify all fields
        assert kafka_binding.binding_version == "0.5.0"
        assert kafka_binding.group_id is not None
        assert isinstance(kafka_binding.group_id, Schema)
        assert kafka_binding.group_id.type == "string"
        assert kafka_binding.group_id.enum == ["myGroupId"]
        assert kafka_binding.client_id is not None
        assert isinstance(kafka_binding.client_id, Schema)
        assert kafka_binding.client_id.type == "string"
        assert kafka_binding.client_id.enum == ["myClientId"]

    @parametrize_with_cases(
        "kafka_binding,expected",
        cases=[
            case_kafka_operation_binding_serialization_empty,
            case_kafka_operation_binding_serialization_with_schemas,
        ],
    )
    def test_kafka_operation_bindings_serialization(
        self,
        kafka_binding: KafkaOperationBindings,
        expected: dict,
    ) -> None:
        """Test KafkaOperationBindings serialization."""
        dumped = kafka_binding.model_dump()
        assert dumped == expected


class TestKafkaMessageBindings:
    """Tests for KafkaMessageBindings model."""

    def test_kafka_message_bindings_validation_empty(self) -> None:
        """Test KafkaMessageBindings model validation with empty fields."""
        yaml_data = """
        kafka:
          bindingVersion: '0.5.0'
        """
        data = yaml.safe_load(yaml_data)
        kafka_binding = KafkaMessageBindings.model_validate(data["kafka"])

        # Verify all fields
        assert kafka_binding.binding_version == "0.5.0"
        assert kafka_binding.key is None
        assert kafka_binding.schema_id_location is None
        assert kafka_binding.schema_id_payload_encoding is None
        assert kafka_binding.schema_lookup_strategy is None

    def test_kafka_message_bindings_validation_confluent(self) -> None:
        """Test KafkaMessageBindings model validation for Confluent schema registry."""
        yaml_data = """
        kafka:
          key:
            type: string
            enum: ['myKey']
          schemaIdLocation: 'payload'
          schemaIdPayloadEncoding: '4'
          bindingVersion: '0.5.0'
        """
        data = yaml.safe_load(yaml_data)
        kafka_binding = KafkaMessageBindings.model_validate(data["kafka"])

        # Verify all fields
        assert kafka_binding.binding_version == "0.5.0"
        assert kafka_binding.key is not None
        assert isinstance(kafka_binding.key, Schema)
        assert kafka_binding.key.type == "string"
        assert kafka_binding.key.enum == ["myKey"]
        assert kafka_binding.schema_id_location == "payload"
        assert kafka_binding.schema_id_payload_encoding == "4"
        assert kafka_binding.schema_lookup_strategy is None

    def test_kafka_message_bindings_validation_apicurio(self) -> None:
        """Test KafkaMessageBindings model validation for Apicurio schema registry."""
        yaml_data = """
        kafka:
          key:
            type: string
            enum: ['myKey']
          schemaIdLocation: 'payload'
          schemaIdPayloadEncoding: 'apicurio-new'
          schemaLookupStrategy: 'TopicIdStrategy'
          bindingVersion: '0.5.0'
        """
        data = yaml.safe_load(yaml_data)
        kafka_binding = KafkaMessageBindings.model_validate(data["kafka"])

        # Verify all fields
        assert kafka_binding.binding_version == "0.5.0"
        assert kafka_binding.key is not None
        assert isinstance(kafka_binding.key, Schema)
        assert kafka_binding.key.type == "string"
        assert kafka_binding.key.enum == ["myKey"]
        assert kafka_binding.schema_id_location == "payload"
        assert kafka_binding.schema_id_payload_encoding == "apicurio-new"
        assert kafka_binding.schema_lookup_strategy == "TopicIdStrategy"

    @parametrize_with_cases(
        "kafka_binding,expected",
        cases=[
            case_kafka_message_binding_serialization_empty,
            case_kafka_message_binding_serialization_confluent,
            case_kafka_message_binding_serialization_apicurio,
        ],
    )
    def test_kafka_message_bindings_serialization(
        self,
        kafka_binding: KafkaMessageBindings,
        expected: dict,
    ) -> None:
        """Test KafkaMessageBindings serialization."""
        dumped = kafka_binding.model_dump()
        assert dumped == expected
