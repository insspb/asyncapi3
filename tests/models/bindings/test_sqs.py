"""Tests for SQS bindings models."""

from typing import Any

import pytest
import yaml

from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.bindings.sqs import (
    SQSChannelBindings,
    SQSMessageBindings,
    SQSOperationBindings,
    SQSQueue,
    SQSServerBindings,
)


# Channel Bindings Validation Test Cases
def case_channel_binding_with_queue() -> str:
    """Channel binding with queue."""
    return """
    sqs:
      queue:
        name: user-signedup-queue
        fifoQueue: false
        receiveMessageWaitTime: 4
      bindingVersion: 0.3.0
    """


# Channel Bindings Serialization Test Cases
def case_sqs_channel_binding_serialization_with_queue() -> tuple[
    SQSChannelBindings, dict
]:
    """SQSChannelBindings serialization with queue."""
    sqs_binding = SQSChannelBindings(
        queue=SQSQueue(
            name="user-signedup-queue",
            fifo_queue=False,
            receive_message_wait_time=4,
        ),
    )
    expected: dict[str, Any] = {
        "queue": {
            "name": "user-signedup-queue",
            "fifoQueue": False,
            "receiveMessageWaitTime": 4,
        },
        "bindingVersion": "0.3.0",
    }
    return sqs_binding, expected


def case_sqs_channel_binding_serialization_with_dead_letter_queue() -> tuple[
    SQSChannelBindings, dict
]:
    """SQSChannelBindings serialization with dead letter queue."""
    sqs_binding = SQSChannelBindings(
        queue=SQSQueue(
            name="user-signedup-queue",
            fifo_queue=False,
        ),
        dead_letter_queue=SQSQueue(
            name="user-signedup-dlq",
            fifo_queue=False,
        ),
    )
    expected: dict[str, Any] = {
        "queue": {
            "name": "user-signedup-queue",
            "fifoQueue": False,
        },
        "deadLetterQueue": {
            "name": "user-signedup-dlq",
            "fifoQueue": False,
        },
        "bindingVersion": "0.3.0",
    }
    return sqs_binding, expected


# Operation Bindings Validation Test Cases
def case_operation_binding_with_queues() -> str:
    """Operation binding with queues."""
    return """
    sqs:
      queues:
        - name: my-queue
          fifoQueue: false
      bindingVersion: 0.3.0
    """


# Operation Bindings Serialization Test Cases
def case_sqs_operation_binding_serialization_with_queues() -> tuple[
    SQSOperationBindings, dict
]:
    """SQSOperationBindings serialization with queues."""
    sqs_binding = SQSOperationBindings(
        queues=[
            SQSQueue(
                name="my-queue",
                fifo_queue=False,
            ),
        ],
    )
    expected: dict[str, Any] = {
        "queues": [
            {
                "name": "my-queue",
                "fifoQueue": False,
            },
        ],
        "bindingVersion": "0.3.0",
    }
    return sqs_binding, expected


def case_sqs_operation_binding_serialization_with_multiple_queues() -> tuple[
    SQSOperationBindings, dict
]:
    """SQSOperationBindings serialization with multiple queues."""
    sqs_binding = SQSOperationBindings(
        queues=[
            SQSQueue(
                name="primary-queue",
                fifo_queue=False,
                visibility_timeout=30,
            ),
            SQSQueue(
                name="dlq-queue",
                fifo_queue=False,
                message_retention_period=345600,
            ),
        ],
    )
    expected: dict[str, Any] = {
        "queues": [
            {
                "name": "primary-queue",
                "fifoQueue": False,
                "visibilityTimeout": 30,
            },
            {
                "name": "dlq-queue",
                "fifoQueue": False,
                "messageRetentionPeriod": 345600,
            },
        ],
        "bindingVersion": "0.3.0",
    }
    return sqs_binding, expected


class TestSQSServerBindings:
    """Tests for SQSServerBindings model."""

    def test_sqs_server_bindings_serialization(self) -> None:
        """Test SQSServerBindings serialization."""
        sqs_binding = SQSServerBindings()
        dumped = sqs_binding.model_dump()
        assert dumped == {}

    def test_sqs_server_bindings_python_validation_error(self) -> None:
        """Test SQSServerBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            SQSServerBindings(some_field="value")

    def test_sqs_server_bindings_yaml_validation_error(self) -> None:
        """Test SQSServerBindings YAML validation error with any fields."""
        yaml_data = """
        sqs:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            SQSServerBindings.model_validate(data["sqs"])

    def test_sqs_server_bindings_yaml_empty_validation(self) -> None:
        """Test SQSServerBindings YAML validation with no fields."""
        yaml_data = """
        sqs: {}
        """
        data = yaml.safe_load(yaml_data)
        sqs_binding = SQSServerBindings.model_validate(data["sqs"])
        assert sqs_binding is not None


class TestSQSChannelBindings:
    """Tests for SQSChannelBindings model."""

    @parametrize_with_cases("yaml_data", cases=[case_channel_binding_with_queue])
    def test_sqs_channel_bindings_validation(self, yaml_data: str) -> None:
        """Test SQSChannelBindings model validation."""
        data = yaml.safe_load(yaml_data)
        sqs_binding = SQSChannelBindings.model_validate(data["sqs"])
        assert sqs_binding is not None
        assert sqs_binding.binding_version == "0.3.0"

    @parametrize_with_cases(
        "sqs_binding,expected",
        cases=[
            case_sqs_channel_binding_serialization_with_queue,
            case_sqs_channel_binding_serialization_with_dead_letter_queue,
        ],
    )
    def test_sqs_channel_bindings_serialization(
        self,
        sqs_binding: SQSChannelBindings,
        expected: dict,
    ) -> None:
        """Test SQSChannelBindings serialization."""
        dumped = sqs_binding.model_dump()
        assert dumped == expected

    def test_sqs_channel_binding_queue_validation(self) -> None:
        """Test SQSChannelBindings with queue object validation."""
        yaml_data = """
        sqs:
          queue:
            name: user-signedup-queue
            fifoQueue: false
            receiveMessageWaitTime: 4
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        sqs_binding = SQSChannelBindings.model_validate(data["sqs"])

        assert sqs_binding.queue is not None
        assert isinstance(sqs_binding.queue, SQSQueue)
        assert sqs_binding.queue.name == "user-signedup-queue"
        assert sqs_binding.queue.fifo_queue is False
        assert sqs_binding.queue.receive_message_wait_time == 4
        assert sqs_binding.binding_version == "0.3.0"

    def test_sqs_channel_binding_dead_letter_queue_validation(self) -> None:
        """Test SQSChannelBindings with dead letter queue validation."""
        yaml_data = """
        sqs:
          queue:
            name: user-signedup-queue
            fifoQueue: false
          deadLetterQueue:
            name: user-signedup-dlq
            fifoQueue: false
            messageRetentionPeriod: 345600
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        sqs_binding = SQSChannelBindings.model_validate(data["sqs"])

        assert sqs_binding.queue is not None
        assert isinstance(sqs_binding.queue, SQSQueue)
        assert sqs_binding.queue.name == "user-signedup-queue"
        assert sqs_binding.dead_letter_queue is not None
        assert isinstance(sqs_binding.dead_letter_queue, SQSQueue)
        assert sqs_binding.dead_letter_queue.name == "user-signedup-dlq"
        assert sqs_binding.dead_letter_queue.message_retention_period == 345600
        assert sqs_binding.binding_version == "0.3.0"

    def test_sqs_channel_bindings_python_validation_error(self) -> None:
        """Test SQSChannelBindings Python validation error with invalid arguments."""
        with pytest.raises(ValidationError):
            SQSChannelBindings(
                queue=SQSQueue(name="test", fifo_queue=False),
                invalid_field="value",
            )

    def test_sqs_channel_bindings_yaml_validation_error(self) -> None:
        """Test SQSChannelBindings YAML validation error with invalid fields."""
        yaml_data = """
        sqs:
          queue:
            name: user-signedup-queue
            fifoQueue: false
          invalid_field: value
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            SQSChannelBindings.model_validate(data["sqs"])


class TestSQSOperationBindings:
    """Tests for SQSOperationBindings model."""

    @parametrize_with_cases("yaml_data", cases=[case_operation_binding_with_queues])
    def test_sqs_operation_bindings_validation(self, yaml_data: str) -> None:
        """Test SQSOperationBindings model validation."""
        data = yaml.safe_load(yaml_data)
        sqs_binding = SQSOperationBindings.model_validate(data["sqs"])
        assert sqs_binding is not None
        assert sqs_binding.binding_version == "0.3.0"

    @parametrize_with_cases(
        "sqs_binding,expected",
        cases=[
            case_sqs_operation_binding_serialization_with_queues,
            case_sqs_operation_binding_serialization_with_multiple_queues,
        ],
    )
    def test_sqs_operation_bindings_serialization(
        self,
        sqs_binding: SQSOperationBindings,
        expected: dict,
    ) -> None:
        """Test SQSOperationBindings serialization."""
        dumped = sqs_binding.model_dump()
        assert dumped == expected

    def test_sqs_operation_binding_queues_validation(self) -> None:
        """Test SQSOperationBindings with queues validation."""
        yaml_data = """
        sqs:
          queues:
            - name: my-queue
              fifoQueue: false
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        sqs_binding = SQSOperationBindings.model_validate(data["sqs"])

        assert sqs_binding.queues is not None
        assert len(sqs_binding.queues) == 1
        assert isinstance(sqs_binding.queues[0], SQSQueue)
        assert sqs_binding.queues[0].name == "my-queue"
        assert sqs_binding.binding_version == "0.3.0"

    def test_sqs_operation_binding_multiple_queues_validation(self) -> None:
        """Test SQSOperationBindings with multiple queues validation."""
        yaml_data = """
        sqs:
          queues:
            - name: primary-queue
              fifoQueue: false
              visibilityTimeout: 30
            - name: dlq-queue
              fifoQueue: false
              messageRetentionPeriod: 345600
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        sqs_binding = SQSOperationBindings.model_validate(data["sqs"])

        assert sqs_binding.queues is not None
        assert len(sqs_binding.queues) == 2
        assert isinstance(sqs_binding.queues[0], SQSQueue)
        assert sqs_binding.queues[0].name == "primary-queue"
        assert sqs_binding.queues[0].visibility_timeout == 30
        assert isinstance(sqs_binding.queues[1], SQSQueue)
        assert sqs_binding.queues[1].name == "dlq-queue"
        assert sqs_binding.queues[1].message_retention_period == 345600
        assert sqs_binding.binding_version == "0.3.0"

    def test_sqs_operation_bindings_python_validation_error(self) -> None:
        """Test SQSOperationBindings Python validation error with invalid arguments."""
        with pytest.raises(ValidationError):
            SQSOperationBindings(
                queues=[SQSQueue(name="test", fifo_queue=False)],
                invalid_field="value",
            )

    def test_sqs_operation_bindings_yaml_validation_error(self) -> None:
        """Test SQSOperationBindings YAML validation error with invalid fields."""
        yaml_data = """
        sqs:
          queues:
            - name: my-queue
              fifoQueue: false
          invalid_field: value
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            SQSOperationBindings.model_validate(data["sqs"])


class TestSQSMessageBindings:
    """Tests for SQSMessageBindings model."""

    def test_sqs_message_bindings_serialization(self) -> None:
        """Test SQSMessageBindings serialization."""
        sqs_binding = SQSMessageBindings()
        dumped = sqs_binding.model_dump()
        assert dumped == {}

    def test_sqs_message_bindings_python_validation_error(self) -> None:
        """Test SQSMessageBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            SQSMessageBindings(some_field="value")

    def test_sqs_message_bindings_yaml_validation_error(self) -> None:
        """Test SQSMessageBindings YAML validation error with any fields."""
        yaml_data = """
        sqs:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            SQSMessageBindings.model_validate(data["sqs"])

    def test_sqs_message_bindings_yaml_empty_validation(self) -> None:
        """Test SQSMessageBindings YAML validation with no fields."""
        yaml_data = """
        sqs: {}
        """
        data = yaml.safe_load(yaml_data)
        sqs_binding = SQSMessageBindings.model_validate(data["sqs"])
        assert sqs_binding is not None
