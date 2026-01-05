"""Tests for IBM MQ bindings models."""

from typing import Any

import pytest
import yaml

from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.bindings.ibmmq import (
    IBMMQChannelBindings,
    IBMMQMessageBindings,
    IBMMQOperationBindings,
    IBMMQQueue,
    IBMMQServerBindings,
    IBMMQTopic,
)


# Server Bindings Validation Test Cases
def case_server_binding_with_group_id() -> str:
    """Server binding with groupId and cipherSpec."""
    return """
    ibmmq:
      groupId: PRODCLSTR1
      cipherSpec: ANY_TLS12_OR_HIGHER
      bindingVersion: 0.1.0
    """


# Server Bindings Serialization Test Cases
def case_ibmmq_server_binding_serialization_empty() -> tuple[IBMMQServerBindings, dict]:
    """IBMMQServerBindings serialization empty."""
    ibmmq_binding = IBMMQServerBindings()
    expected: dict[str, Any] = {"bindingVersion": "0.1.0"}
    return ibmmq_binding, expected


def case_ibmmq_server_binding_serialization_with_group_id() -> tuple[
    IBMMQServerBindings, dict
]:
    """IBMMQServerBindings serialization with groupId and cipherSpec."""
    ibmmq_binding = IBMMQServerBindings(
        group_id="PRODCLSTR1",
        cipher_spec="ANY_TLS12_OR_HIGHER",
    )
    expected: dict[str, Any] = {
        "groupId": "PRODCLSTR1",
        "cipherSpec": "ANY_TLS12_OR_HIGHER",
        "bindingVersion": "0.1.0",
    }
    return ibmmq_binding, expected


# Channel Bindings Validation Test Cases
def case_channel_binding_topic() -> str:
    """Channel binding with topic."""
    return """
    ibmmq:
      destinationType: topic
      topic:
        objectName: myTopicName
      bindingVersion: 0.1.0
    """


def case_channel_binding_queue() -> str:
    """Channel binding with queue."""
    return """
    ibmmq:
      destinationType: queue
      queue:
        objectName: myQueueName
        isPartitioned: false
        exclusive: false
      bindingVersion: 0.1.0
    """


# Channel Bindings Serialization Test Cases
def case_ibmmq_channel_binding_serialization_topic() -> tuple[
    IBMMQChannelBindings, dict
]:
    """IBMMQChannelBindings serialization with topic."""
    ibmmq_binding = IBMMQChannelBindings(
        destination_type="topic",
        topic=IBMMQTopic(object_name="myTopicName"),
    )
    expected: dict[str, Any] = {
        "destinationType": "topic",
        "topic": {
            "objectName": "myTopicName",
            "durablePermitted": True,
            "lastMsgRetained": False,
        },
        "bindingVersion": "0.1.0",
    }
    return ibmmq_binding, expected


def case_ibmmq_channel_binding_serialization_queue() -> tuple[
    IBMMQChannelBindings, dict
]:
    """IBMMQChannelBindings serialization with queue."""
    ibmmq_binding = IBMMQChannelBindings(
        destination_type="queue",
        queue=IBMMQQueue(
            object_name="myQueueName",
            is_partitioned=False,
            exclusive=False,
        ),
    )
    expected: dict[str, Any] = {
        "destinationType": "queue",
        "queue": {
            "objectName": "myQueueName",
            "isPartitioned": False,
            "exclusive": False,
        },
        "bindingVersion": "0.1.0",
    }
    return ibmmq_binding, expected


# Message Bindings Validation Test Cases
def case_message_binding_string() -> str:
    """Message binding with string type."""
    return """
    ibmmq:
      type: string
      bindingVersion: 0.1.0
    """


# Message Bindings Serialization Test Cases
def case_ibmmq_message_binding_serialization_empty() -> tuple[
    IBMMQMessageBindings, dict
]:
    """IBMMQMessageBindings serialization empty."""
    ibmmq_binding = IBMMQMessageBindings()
    expected: dict[str, Any] = {"bindingVersion": "0.1.0", "type": "string"}
    return ibmmq_binding, expected


def case_ibmmq_message_binding_serialization_string() -> tuple[
    IBMMQMessageBindings, dict
]:
    """IBMMQMessageBindings serialization with string type."""
    ibmmq_binding = IBMMQMessageBindings(type="string")
    expected: dict[str, Any] = {
        "type": "string",
        "bindingVersion": "0.1.0",
    }
    return ibmmq_binding, expected


class TestIBMMQServerBindings:
    """Tests for IBMMQServerBindings model."""

    @parametrize_with_cases("yaml_data", cases=[case_server_binding_with_group_id])
    def test_ibmmq_server_bindings_validation(self, yaml_data: str) -> None:
        """Test IBMMQServerBindings model validation."""
        data = yaml.safe_load(yaml_data)
        ibmmq_binding = IBMMQServerBindings.model_validate(data["ibmmq"])
        assert ibmmq_binding is not None
        assert ibmmq_binding.binding_version == "0.1.0"

    @parametrize_with_cases(
        "ibmmq_binding,expected",
        cases=[
            case_ibmmq_server_binding_serialization_empty,
            case_ibmmq_server_binding_serialization_with_group_id,
        ],
    )
    def test_ibmmq_server_bindings_serialization(
        self,
        ibmmq_binding: IBMMQServerBindings,
        expected: dict,
    ) -> None:
        """Test IBMMQServerBindings serialization."""
        dumped = ibmmq_binding.model_dump()
        assert dumped == expected

    def test_ibmmq_server_bindings_python_validation_error(self) -> None:
        """Test IBMMQServerBindings Python validation error with invalid arguments."""
        with pytest.raises(ValidationError):
            IBMMQServerBindings(group_id="test", invalid_field="value")

    def test_ibmmq_server_bindings_yaml_validation_error(self) -> None:
        """Test IBMMQServerBindings YAML validation error with invalid fields."""
        yaml_data = """
        ibmmq:
          groupId: PRODCLSTR1
          invalid_field: value
          bindingVersion: 0.1.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            IBMMQServerBindings.model_validate(data["ibmmq"])


class TestIBMMQChannelBindings:
    """Tests for IBMMQChannelBindings model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_channel_binding_topic, case_channel_binding_queue],
    )
    def test_ibmmq_channel_bindings_validation(self, yaml_data: str) -> None:
        """Test IBMMQChannelBindings model validation."""
        data = yaml.safe_load(yaml_data)
        ibmmq_binding = IBMMQChannelBindings.model_validate(data["ibmmq"])
        assert ibmmq_binding is not None
        assert ibmmq_binding.binding_version == "0.1.0"

    @parametrize_with_cases(
        "ibmmq_binding,expected",
        cases=[
            case_ibmmq_channel_binding_serialization_topic,
            case_ibmmq_channel_binding_serialization_queue,
        ],
    )
    def test_ibmmq_channel_bindings_serialization(
        self,
        ibmmq_binding: IBMMQChannelBindings,
        expected: dict,
    ) -> None:
        """Test IBMMQChannelBindings serialization."""
        dumped = ibmmq_binding.model_dump()
        assert dumped == expected

    def test_ibmmq_channel_binding_queue_validation(self) -> None:
        """Test IBMMQChannelBindings with queue object validation."""
        yaml_data = """
        ibmmq:
          destinationType: queue
          queue:
            objectName: myQueueName
            isPartitioned: false
            exclusive: false
          bindingVersion: 0.1.0
        """
        data = yaml.safe_load(yaml_data)
        ibmmq_binding = IBMMQChannelBindings.model_validate(data["ibmmq"])

        assert ibmmq_binding.queue is not None
        assert isinstance(ibmmq_binding.queue, IBMMQQueue)
        assert ibmmq_binding.queue.object_name == "myQueueName"
        assert ibmmq_binding.queue.is_partitioned is False
        assert ibmmq_binding.queue.exclusive is False
        assert ibmmq_binding.binding_version == "0.1.0"

    def test_ibmmq_channel_binding_topic_validation(self) -> None:
        """Test IBMMQChannelBindings with topic object validation."""
        yaml_data = """
        ibmmq:
          destinationType: topic
          topic:
            objectName: myTopicName
          bindingVersion: 0.1.0
        """
        data = yaml.safe_load(yaml_data)
        ibmmq_binding = IBMMQChannelBindings.model_validate(data["ibmmq"])

        assert ibmmq_binding.topic is not None
        assert isinstance(ibmmq_binding.topic, IBMMQTopic)
        assert ibmmq_binding.topic.object_name == "myTopicName"
        assert ibmmq_binding.binding_version == "0.1.0"

    def test_ibmmq_channel_bindings_python_validation_error(self) -> None:
        """Test IBMMQChannelBindings Python validation error with invalid arguments."""
        with pytest.raises(ValidationError):
            IBMMQChannelBindings(
                destination_type="queue",
                queue=IBMMQQueue(object_name="test"),
                invalid_field="value",
            )

    def test_ibmmq_channel_bindings_yaml_validation_error(self) -> None:
        """Test IBMMQChannelBindings YAML validation error with invalid fields."""
        yaml_data = """
        ibmmq:
          destinationType: topic
          topic:
            objectName: myTopicName
          invalid_field: value
          bindingVersion: 0.1.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            IBMMQChannelBindings.model_validate(data["ibmmq"])


class TestIBMMQOperationBindings:
    """Tests for IBMMQOperationBindings model."""

    def test_ibmmq_operation_bindings_serialization(self) -> None:
        """Test IBMMQOperationBindings serialization."""
        ibmmq_binding = IBMMQOperationBindings()
        dumped = ibmmq_binding.model_dump()
        assert dumped == {}

    def test_ibmmq_operation_bindings_python_validation_error(self) -> None:
        """Test IBMMQOperationBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            IBMMQOperationBindings(some_field="value")

    def test_ibmmq_operation_bindings_yaml_validation_error(self) -> None:
        """Test IBMMQOperationBindings YAML validation error with any fields."""
        yaml_data = """
        ibmmq:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            IBMMQOperationBindings.model_validate(data["ibmmq"])

    def test_ibmmq_operation_bindings_yaml_empty_validation(self) -> None:
        """Test IBMMQOperationBindings YAML validation with no fields."""
        yaml_data = """
        ibmmq: {}
        """
        data = yaml.safe_load(yaml_data)
        ibmmq_binding = IBMMQOperationBindings.model_validate(data["ibmmq"])
        assert ibmmq_binding is not None


class TestIBMMQMessageBindings:
    """Tests for IBMMQMessageBindings model."""

    @parametrize_with_cases("yaml_data", cases=[case_message_binding_string])
    def test_ibmmq_message_bindings_validation(self, yaml_data: str) -> None:
        """Test IBMMQMessageBindings model validation."""
        data = yaml.safe_load(yaml_data)
        ibmmq_binding = IBMMQMessageBindings.model_validate(data["ibmmq"])
        assert ibmmq_binding is not None
        assert ibmmq_binding.binding_version == "0.1.0"

    @parametrize_with_cases(
        "ibmmq_binding,expected",
        cases=[
            case_ibmmq_message_binding_serialization_empty,
            case_ibmmq_message_binding_serialization_string,
        ],
    )
    def test_ibmmq_message_bindings_serialization(
        self,
        ibmmq_binding: IBMMQMessageBindings,
        expected: dict,
    ) -> None:
        """Test IBMMQMessageBindings serialization."""
        dumped = ibmmq_binding.model_dump()
        assert dumped == expected

    def test_ibmmq_message_bindings_python_validation_error(self) -> None:
        """Test IBMMQMessageBindings Python validation error with invalid arguments."""
        with pytest.raises(ValidationError):
            IBMMQMessageBindings(type="string", invalid_field="value")

    def test_ibmmq_message_bindings_yaml_validation_error(self) -> None:
        """Test IBMMQMessageBindings YAML validation error with invalid fields."""
        yaml_data = """
        ibmmq:
          type: string
          invalid_field: value
          bindingVersion: 0.1.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            IBMMQMessageBindings.model_validate(data["ibmmq"])
