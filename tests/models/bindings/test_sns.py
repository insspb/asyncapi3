"""Tests for SNS bindings models."""

from typing import Any

import pytest
import yaml

from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.bindings.sns import (
    SNSChannelBindings,
    SNSConsumer,
    SNSIdentifier,
    SNSMessageBindings,
    SNSOperationBindings,
    SNSOrdering,
    SNSPolicy,
    SNSServerBindings,
    SNSStatement,
)


# Channel Bindings Validation Test Cases
def case_channel_binding_minimal() -> str:
    """Channel binding with minimal fields."""
    return """
    sns:
      name: user-signedup
      bindingVersion: 1.0.0
    """


def case_channel_binding_with_policy() -> str:
    """Channel binding with policy."""
    return """
    sns:
      name: user-signedup
      policy:
        statements:
          - effect: Allow
            principal: '*'
            action: SNS:Publish
      bindingVersion: 1.0.0
    """


# Channel Bindings Serialization Test Cases
def case_sns_channel_binding_serialization_minimal() -> tuple[SNSChannelBindings, dict]:
    """SNSChannelBindings serialization with minimal fields."""
    sns_binding = SNSChannelBindings(name="user-signedup")
    expected: dict[str, Any] = {
        "name": "user-signedup",
        "bindingVersion": "1.0.0",
    }
    return sns_binding, expected


def case_sns_channel_binding_serialization_with_policy() -> tuple[
    SNSChannelBindings, dict
]:
    """SNSChannelBindings serialization with policy."""
    sns_binding = SNSChannelBindings(
        name="user-signedup",
        policy=SNSPolicy(
            statements=[
                SNSStatement(
                    effect="Allow",
                    principal="*",
                    action="SNS:Publish",
                ),
            ],
        ),
    )
    expected: dict[str, Any] = {
        "name": "user-signedup",
        "policy": {
            "statements": [
                {
                    "effect": "Allow",
                    "principal": "*",
                    "action": "SNS:Publish",
                },
            ],
        },
        "bindingVersion": "1.0.0",
    }
    return sns_binding, expected


def case_sns_channel_binding_serialization_with_ordering() -> tuple[
    SNSChannelBindings, dict
]:
    """SNSChannelBindings serialization with ordering."""
    sns_binding = SNSChannelBindings(
        name="user-signedup-fifo",
        ordering=SNSOrdering(
            type="FIFO",
            content_based_deduplication=True,
        ),
    )
    expected: dict[str, Any] = {
        "name": "user-signedup-fifo",
        "ordering": {
            "type": "FIFO",
            "contentBasedDeduplication": True,
        },
        "bindingVersion": "1.0.0",
    }
    return sns_binding, expected


def case_sns_channel_binding_serialization_with_tags() -> tuple[
    SNSChannelBindings, dict
]:
    """SNSChannelBindings serialization with tags."""
    sns_binding = SNSChannelBindings(
        name="user-signedup",
        tags={
            "Environment": "production",
            "Team": "backend",
        },
    )
    expected: dict[str, Any] = {
        "name": "user-signedup",
        "tags": {
            "Environment": "production",
            "Team": "backend",
        },
        "bindingVersion": "1.0.0",
    }
    return sns_binding, expected


# Operation Bindings Validation Test Cases
def case_operation_binding_with_consumers() -> str:
    """Operation binding with consumers."""
    return """
    sns:
      consumers:
        - protocol: sqs
          endpoint:
            name: myQueue
          rawMessageDelivery: false
      bindingVersion: 1.0.0
    """


# Operation Bindings Serialization Test Cases
def case_sns_operation_binding_serialization_with_consumers() -> tuple[
    SNSOperationBindings, dict
]:
    """SNSOperationBindings serialization with consumers."""
    sns_binding = SNSOperationBindings(
        consumers=[
            SNSConsumer(
                protocol="sqs",
                endpoint=SNSIdentifier(name="myQueue"),
                raw_message_delivery=False,
            ),
        ],
    )
    expected: dict[str, Any] = {
        "consumers": [
            {
                "protocol": "sqs",
                "endpoint": {
                    "name": "myQueue",
                },
                "rawMessageDelivery": False,
            },
        ],
        "bindingVersion": "1.0.0",
    }
    return sns_binding, expected


def case_sns_operation_binding_serialization_with_topic() -> tuple[
    SNSOperationBindings, dict
]:
    """SNSOperationBindings serialization with topic."""
    sns_binding = SNSOperationBindings(
        topic=SNSIdentifier(arn="arn:aws:sns:us-east-1:123456789012:my-topic"),
        consumers=[
            SNSConsumer(
                protocol="sqs",
                endpoint=SNSIdentifier(name="myQueue"),
                raw_message_delivery=False,
            ),
        ],
    )
    expected: dict[str, Any] = {
        "topic": {
            "arn": "arn:aws:sns:us-east-1:123456789012:my-topic",
        },
        "consumers": [
            {
                "protocol": "sqs",
                "endpoint": {
                    "name": "myQueue",
                },
                "rawMessageDelivery": False,
            },
        ],
        "bindingVersion": "1.0.0",
    }
    return sns_binding, expected


class TestSNSServerBindings:
    """Tests for SNSServerBindings model."""

    def test_sns_server_bindings_serialization(self) -> None:
        """Test SNSServerBindings serialization."""
        sns_binding = SNSServerBindings()
        dumped = sns_binding.model_dump()
        assert dumped == {}

    def test_sns_server_bindings_python_validation_error(self) -> None:
        """Test SNSServerBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            SNSServerBindings(some_field="value")

    def test_sns_server_bindings_yaml_validation_error(self) -> None:
        """Test SNSServerBindings YAML validation error with any fields."""
        yaml_data = """
        sns:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            SNSServerBindings.model_validate(data["sns"])

    def test_sns_server_bindings_yaml_empty_validation(self) -> None:
        """Test SNSServerBindings YAML validation with no fields."""
        yaml_data = """
        sns: {}
        """
        data = yaml.safe_load(yaml_data)
        sns_binding = SNSServerBindings.model_validate(data["sns"])
        assert sns_binding is not None


class TestSNSChannelBindings:
    """Tests for SNSChannelBindings model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_channel_binding_minimal, case_channel_binding_with_policy],
    )
    def test_sns_channel_bindings_validation(self, yaml_data: str) -> None:
        """Test SNSChannelBindings model validation."""
        data = yaml.safe_load(yaml_data)
        sns_binding = SNSChannelBindings.model_validate(data["sns"])
        assert sns_binding is not None
        assert sns_binding.binding_version == "1.0.0"

    @parametrize_with_cases(
        "sns_binding,expected",
        cases=[
            case_sns_channel_binding_serialization_minimal,
            case_sns_channel_binding_serialization_with_policy,
            case_sns_channel_binding_serialization_with_ordering,
            case_sns_channel_binding_serialization_with_tags,
        ],
    )
    def test_sns_channel_bindings_serialization(
        self,
        sns_binding: SNSChannelBindings,
        expected: dict,
    ) -> None:
        """Test SNSChannelBindings serialization."""
        dumped = sns_binding.model_dump()
        assert dumped == expected

    def test_sns_channel_binding_policy_validation(self) -> None:
        """Test SNSChannelBindings with policy validation."""
        yaml_data = """
        sns:
          name: user-signedup
          policy:
            statements:
              - effect: Allow
                principal: '*'
                action: SNS:Publish
          bindingVersion: 1.0.0
        """
        data = yaml.safe_load(yaml_data)
        sns_binding = SNSChannelBindings.model_validate(data["sns"])

        assert sns_binding.name == "user-signedup"
        assert sns_binding.policy is not None
        assert isinstance(sns_binding.policy, SNSPolicy)
        assert sns_binding.binding_version == "1.0.0"

    def test_sns_channel_binding_ordering_validation(self) -> None:
        """Test SNSChannelBindings with ordering validation."""
        yaml_data = """
        sns:
          name: user-signedup-fifo
          ordering:
            type: FIFO
            contentBasedDeduplication: true
          bindingVersion: 1.0.0
        """
        data = yaml.safe_load(yaml_data)
        sns_binding = SNSChannelBindings.model_validate(data["sns"])

        assert sns_binding.name == "user-signedup-fifo"
        assert sns_binding.ordering is not None
        assert isinstance(sns_binding.ordering, SNSOrdering)
        assert sns_binding.ordering.type == "FIFO"
        assert sns_binding.ordering.content_based_deduplication is True
        assert sns_binding.binding_version == "1.0.0"

    def test_sns_channel_binding_tags_validation(self) -> None:
        """Test SNSChannelBindings with tags validation."""
        yaml_data = """
        sns:
          name: user-signedup
          tags:
            Environment: production
            Team: backend
          bindingVersion: 1.0.0
        """
        data = yaml.safe_load(yaml_data)
        sns_binding = SNSChannelBindings.model_validate(data["sns"])

        assert sns_binding.name == "user-signedup"
        assert sns_binding.tags == {"Environment": "production", "Team": "backend"}
        assert sns_binding.binding_version == "1.0.0"

    def test_sns_channel_bindings_python_validation_error(self) -> None:
        """Test SNSChannelBindings Python validation error with invalid arguments."""
        with pytest.raises(ValidationError):
            SNSChannelBindings(name="test", invalid_field="value")

    def test_sns_channel_bindings_yaml_validation_error(self) -> None:
        """Test SNSChannelBindings YAML validation error with invalid fields."""
        yaml_data = """
        sns:
          name: user-signedup
          invalid_field: value
          bindingVersion: 1.0.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            SNSChannelBindings.model_validate(data["sns"])


class TestSNSOperationBindings:
    """Tests for SNSOperationBindings model."""

    @parametrize_with_cases("yaml_data", cases=[case_operation_binding_with_consumers])
    def test_sns_operation_bindings_validation(self, yaml_data: str) -> None:
        """Test SNSOperationBindings model validation."""
        data = yaml.safe_load(yaml_data)
        sns_binding = SNSOperationBindings.model_validate(data["sns"])
        assert sns_binding is not None
        assert sns_binding.binding_version == "1.0.0"

    @parametrize_with_cases(
        "sns_binding,expected",
        cases=[
            case_sns_operation_binding_serialization_with_consumers,
            case_sns_operation_binding_serialization_with_topic,
        ],
    )
    def test_sns_operation_bindings_serialization(
        self,
        sns_binding: SNSOperationBindings,
        expected: dict,
    ) -> None:
        """Test SNSOperationBindings serialization."""
        dumped = sns_binding.model_dump()
        assert dumped == expected

    def test_sns_operation_binding_consumers_validation(self) -> None:
        """Test SNSOperationBindings with consumers validation."""
        yaml_data = """
        sns:
          consumers:
            - protocol: sqs
              endpoint:
                name: myQueue
              rawMessageDelivery: false
          bindingVersion: 1.0.0
        """
        data = yaml.safe_load(yaml_data)
        sns_binding = SNSOperationBindings.model_validate(data["sns"])

        assert sns_binding.consumers is not None
        assert len(sns_binding.consumers) == 1
        assert isinstance(sns_binding.consumers[0], SNSConsumer)
        assert sns_binding.consumers[0].protocol == "sqs"
        assert sns_binding.binding_version == "1.0.0"

    def test_sns_operation_binding_topic_validation(self) -> None:
        """Test SNSOperationBindings with topic validation."""
        yaml_data = """
        sns:
          topic:
            arn: arn:aws:sns:us-east-1:123456789012:my-topic
          consumers:
            - protocol: sqs
              endpoint:
                name: myQueue
              rawMessageDelivery: false
          bindingVersion: 1.0.0
        """
        data = yaml.safe_load(yaml_data)
        sns_binding = SNSOperationBindings.model_validate(data["sns"])

        assert sns_binding.topic is not None
        assert isinstance(sns_binding.topic, SNSIdentifier)
        assert sns_binding.topic.arn == "arn:aws:sns:us-east-1:123456789012:my-topic"
        assert sns_binding.consumers is not None
        assert len(sns_binding.consumers) == 1
        assert isinstance(sns_binding.consumers[0], SNSConsumer)
        assert sns_binding.consumers[0].protocol == "sqs"
        assert sns_binding.binding_version == "1.0.0"

    def test_sns_operation_bindings_python_validation_error(self) -> None:
        """Test SNSOperationBindings Python validation error with invalid arguments."""
        with pytest.raises(ValidationError):
            SNSOperationBindings(consumers=[], invalid_field="value")

    def test_sns_operation_bindings_yaml_validation_error(self) -> None:
        """Test SNSOperationBindings YAML validation error with invalid fields."""
        yaml_data = """
        sns:
          consumers:
            - protocol: sqs
              endpoint:
                name: myQueue
              rawMessageDelivery: false
          invalid_field: value
          bindingVersion: 1.0.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            SNSOperationBindings.model_validate(data["sns"])


class TestSNSMessageBindings:
    """Tests for SNSMessageBindings model."""

    def test_sns_message_bindings_serialization(self) -> None:
        """Test SNSMessageBindings serialization."""
        sns_binding = SNSMessageBindings()
        dumped = sns_binding.model_dump()
        assert dumped == {}

    def test_sns_message_bindings_python_validation_error(self) -> None:
        """Test SNSMessageBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            SNSMessageBindings(some_field="value")

    def test_sns_message_bindings_yaml_validation_error(self) -> None:
        """Test SNSMessageBindings YAML validation error with any fields."""
        yaml_data = """
        sns:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            SNSMessageBindings.model_validate(data["sns"])

    def test_sns_message_bindings_yaml_empty_validation(self) -> None:
        """Test SNSMessageBindings YAML validation with no fields."""
        yaml_data = """
        sns: {}
        """
        data = yaml.safe_load(yaml_data)
        sns_binding = SNSMessageBindings.model_validate(data["sns"])
        assert sns_binding is not None
