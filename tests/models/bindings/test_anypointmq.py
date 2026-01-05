"""Tests for AnypointMQ bindings models."""

from typing import Any

import pytest
import yaml

from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.bindings.anypointmq import (
    AnypointMQChannelBindings,
    AnypointMQMessageBindings,
    AnypointMQOperationBindings,
    AnypointMQServerBindings,
)
from asyncapi3.models.schema import Schema


# Channel Bindings Validation Test Cases
def case_channel_binding_exchange() -> str:
    """Channel binding with exchange destination type."""
    return """
    anypointmq:
      destination: user-signup-exchg
      destinationType: exchange
      bindingVersion: 0.1.0
    """


def case_channel_binding_fifo_queue() -> str:
    """Channel binding with fifo-queue destination type."""
    return """
    anypointmq:
      destination: user-signup-queue
      destinationType: fifo-queue
      bindingVersion: 0.1.0
    """


# Channel Bindings Serialization Test Cases
def case_anypointmq_channel_binding_serialization_empty() -> tuple[
    AnypointMQChannelBindings, dict
]:
    """AnypointMQChannelBindings serialization empty."""
    anypointmq_binding = AnypointMQChannelBindings()
    expected: dict[str, Any] = {"destinationType": "queue", "bindingVersion": "0.1.0"}
    return anypointmq_binding, expected


def case_anypointmq_channel_binding_serialization_exchange() -> tuple[
    AnypointMQChannelBindings, dict
]:
    """AnypointMQChannelBindings serialization with exchange."""
    anypointmq_binding = AnypointMQChannelBindings(
        destination="user-signup-exchg",
        destination_type="exchange",
    )
    expected: dict[str, Any] = {
        "destination": "user-signup-exchg",
        "destinationType": "exchange",
        "bindingVersion": "0.1.0",
    }
    return anypointmq_binding, expected


def case_anypointmq_channel_binding_serialization_fifo_queue() -> tuple[
    AnypointMQChannelBindings, dict
]:
    """AnypointMQChannelBindings serialization with fifo-queue."""
    anypointmq_binding = AnypointMQChannelBindings(
        destination="user-signup-queue",
        destination_type="fifo-queue",
    )
    expected: dict[str, Any] = {
        "destination": "user-signup-queue",
        "destinationType": "fifo-queue",
        "bindingVersion": "0.1.0",
    }
    return anypointmq_binding, expected


# Message Bindings Validation Test Cases
def case_message_binding_with_headers() -> str:
    """Message binding with headers Schema."""
    return """
    anypointmq:
      headers:
        type: object
        properties:
          messageId:
            type: string
      bindingVersion: 0.1.0
    """


# Message Bindings Serialization Test Cases
def case_anypointmq_message_binding_serialization_empty() -> tuple[
    AnypointMQMessageBindings, dict
]:
    """AnypointMQMessageBindings serialization empty."""
    anypointmq_binding = AnypointMQMessageBindings()
    expected: dict[str, Any] = {"bindingVersion": "0.1.0"}
    return anypointmq_binding, expected


def case_anypointmq_message_binding_serialization_with_headers() -> tuple[
    AnypointMQMessageBindings, dict
]:
    """AnypointMQMessageBindings serialization with headers Schema."""
    anypointmq_binding = AnypointMQMessageBindings(
        headers=Schema(
            type="object",
            properties={"messageId": Schema(type="string")},
        ),
    )
    expected: dict[str, Any] = {
        "headers": {
            "type": "object",
            "properties": {
                "messageId": {
                    "type": "string",
                },
            },
        },
        "bindingVersion": "0.1.0",
    }
    return anypointmq_binding, expected


class TestAnypointMQServerBindings:
    """Tests for AnypointMQServerBindings model."""

    def test_anypointmq_server_bindings_serialization(self) -> None:
        """Test AnypointMQServerBindings serialization."""
        anypointmq_binding = AnypointMQServerBindings()
        dumped = anypointmq_binding.model_dump()
        assert dumped == {}

    def test_anypointmq_server_bindings_python_validation_error(self) -> None:
        """Test AnypointMQServerBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            AnypointMQServerBindings(some_field="value")

    def test_anypointmq_server_bindings_yaml_validation_error(self) -> None:
        """Test AnypointMQServerBindings YAML validation error with any fields."""
        yaml_data = """
        anypointmq:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            AnypointMQServerBindings.model_validate(data["anypointmq"])

    def test_anypointmq_server_bindings_yaml_empty_validation(self) -> None:
        """Test AnypointMQServerBindings YAML validation with no fields."""
        yaml_data = """
        anypointmq: {}
        """
        data = yaml.safe_load(yaml_data)
        anypointmq_binding = AnypointMQServerBindings.model_validate(data["anypointmq"])
        assert anypointmq_binding is not None


class TestAnypointMQChannelBindings:
    """Tests for AnypointMQChannelBindings model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_channel_binding_exchange, case_channel_binding_fifo_queue],
    )
    def test_anypointmq_channel_bindings_validation(self, yaml_data: str) -> None:
        """Test AnypointMQChannelBindings model validation."""
        data = yaml.safe_load(yaml_data)
        anypointmq_binding = AnypointMQChannelBindings.model_validate(
            data["anypointmq"]
        )
        assert anypointmq_binding is not None
        assert anypointmq_binding.binding_version == "0.1.0"

    @parametrize_with_cases(
        "anypointmq_binding,expected",
        cases=[
            case_anypointmq_channel_binding_serialization_empty,
            case_anypointmq_channel_binding_serialization_exchange,
            case_anypointmq_channel_binding_serialization_fifo_queue,
        ],
    )
    def test_anypointmq_channel_bindings_serialization(
        self,
        anypointmq_binding: AnypointMQChannelBindings,
        expected: dict,
    ) -> None:
        """Test AnypointMQChannelBindings serialization."""
        dumped = anypointmq_binding.model_dump()
        assert dumped == expected

    def test_anypointmq_channel_binding_all_fields_validation(self) -> None:
        """Test AnypointMQChannelBindings with all fields validation."""
        yaml_data = """
        anypointmq:
          destination: user-signup-queue
          destinationType: fifo-queue
          bindingVersion: 0.1.0
        """
        data = yaml.safe_load(yaml_data)
        anypointmq_binding = AnypointMQChannelBindings.model_validate(
            data["anypointmq"]
        )

        assert anypointmq_binding.destination == "user-signup-queue"
        assert anypointmq_binding.destination_type == "fifo-queue"
        assert anypointmq_binding.binding_version == "0.1.0"

    def test_anypointmq_channel_bindings_python_validation_error(self) -> None:
        """Test AnypointMQChannelBindings Python validation error with extra arguments."""
        with pytest.raises(ValidationError):
            AnypointMQChannelBindings(some_field="value")

    def test_anypointmq_channel_bindings_yaml_validation_error(self) -> None:
        """Test AnypointMQChannelBindings YAML validation error with extra fields."""
        yaml_data = """
        anypointmq:
          some_field: value
          bindingVersion: 0.1.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            AnypointMQChannelBindings.model_validate(data["anypointmq"])


class TestAnypointMQOperationBindings:
    """Tests for AnypointMQOperationBindings model."""

    def test_anypointmq_operation_bindings_serialization(self) -> None:
        """Test AnypointMQOperationBindings serialization."""
        anypointmq_binding = AnypointMQOperationBindings()
        dumped = anypointmq_binding.model_dump()
        assert dumped == {}

    def test_anypointmq_operation_bindings_python_validation_error(self) -> None:
        """Test AnypointMQOperationBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            AnypointMQOperationBindings(some_field="value")

    def test_anypointmq_operation_bindings_yaml_validation_error(self) -> None:
        """Test AnypointMQOperationBindings YAML validation error with any fields."""
        yaml_data = """
        anypointmq:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            AnypointMQOperationBindings.model_validate(data["anypointmq"])

    def test_anypointmq_operation_bindings_yaml_empty_validation(self) -> None:
        """Test AnypointMQOperationBindings YAML validation with no fields."""
        yaml_data = """
        anypointmq: {}
        """
        data = yaml.safe_load(yaml_data)
        anypointmq_binding = AnypointMQOperationBindings.model_validate(
            data["anypointmq"]
        )
        assert anypointmq_binding is not None


class TestAnypointMQMessageBindings:
    """Tests for AnypointMQMessageBindings model."""

    @parametrize_with_cases("yaml_data", cases=[case_message_binding_with_headers])
    def test_anypointmq_message_bindings_validation(self, yaml_data: str) -> None:
        """Test AnypointMQMessageBindings model validation."""
        data = yaml.safe_load(yaml_data)
        anypointmq_binding = AnypointMQMessageBindings.model_validate(
            data["anypointmq"]
        )
        assert anypointmq_binding is not None
        assert anypointmq_binding.binding_version == "0.1.0"

    @parametrize_with_cases(
        "anypointmq_binding,expected",
        cases=[
            case_anypointmq_message_binding_serialization_empty,
            case_anypointmq_message_binding_serialization_with_headers,
        ],
    )
    def test_anypointmq_message_bindings_serialization(
        self,
        anypointmq_binding: AnypointMQMessageBindings,
        expected: dict,
    ) -> None:
        """Test AnypointMQMessageBindings serialization."""
        dumped = anypointmq_binding.model_dump()
        assert dumped == expected

    def test_anypointmq_message_binding_headers_schema_validation(self) -> None:
        """Test AnypointMQMessageBindings with headers as Schema validation."""
        yaml_data = """
        anypointmq:
          headers:
            type: object
            properties:
              messageId:
                type: string
          bindingVersion: 0.1.0
        """
        data = yaml.safe_load(yaml_data)
        anypointmq_binding = AnypointMQMessageBindings.model_validate(
            data["anypointmq"]
        )

        assert anypointmq_binding.headers is not None
        assert isinstance(anypointmq_binding.headers, Schema)
        assert anypointmq_binding.headers.type == "object"
        assert anypointmq_binding.binding_version == "0.1.0"

    def test_anypointmq_message_bindings_python_validation_error(self) -> None:
        """Test AnypointMQMessageBindings Python validation error with extra arguments."""
        with pytest.raises(ValidationError):
            AnypointMQMessageBindings(some_field="value")

    def test_anypointmq_message_bindings_yaml_validation_error(self) -> None:
        """Test AnypointMQMessageBindings YAML validation error with extra fields."""
        yaml_data = """
        anypointmq:
          some_field: value
          bindingVersion: 0.1.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            AnypointMQMessageBindings.model_validate(data["anypointmq"])
