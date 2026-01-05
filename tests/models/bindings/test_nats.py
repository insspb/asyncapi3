"""Tests for NATS bindings models."""

from typing import Any

import pytest
import yaml

from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.bindings.nats import (
    NATSChannelBindings,
    NATSMessageBindings,
    NATSOperationBindings,
    NATSServerBindings,
)


# Operation Bindings Validation Test Cases
def case_operation_binding_with_queue() -> str:
    """Operation binding with queue."""
    return """
    nats:
      queue: my-queue
      bindingVersion: 0.1.0
    """


# Operation Bindings Serialization Test Cases
def case_nats_operation_binding_serialization_empty() -> tuple[
    NATSOperationBindings, dict
]:
    """NATSOperationBindings serialization empty."""
    nats_binding = NATSOperationBindings()
    expected: dict[str, Any] = {"bindingVersion": "0.1.0"}
    return nats_binding, expected


def case_nats_operation_binding_serialization_with_queue() -> tuple[
    NATSOperationBindings, dict
]:
    """NATSOperationBindings serialization with queue."""
    nats_binding = NATSOperationBindings(queue="my-queue")
    expected: dict[str, Any] = {
        "queue": "my-queue",
        "bindingVersion": "0.1.0",
    }
    return nats_binding, expected


class TestNATSServerBindings:
    """Tests for NATSServerBindings model."""

    def test_nats_server_bindings_serialization(self) -> None:
        """Test NATSServerBindings serialization."""
        nats_binding = NATSServerBindings()
        dumped = nats_binding.model_dump()
        assert dumped == {}

    def test_nats_server_bindings_python_validation_error(self) -> None:
        """Test NATSServerBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            NATSServerBindings(some_field="value")

    def test_nats_server_bindings_yaml_validation_error(self) -> None:
        """Test NATSServerBindings YAML validation error with any fields."""
        yaml_data = """
        nats:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            NATSServerBindings.model_validate(data["nats"])

    def test_nats_server_bindings_yaml_empty_validation(self) -> None:
        """Test NATSServerBindings YAML validation with no fields."""
        yaml_data = """
        nats: {}
        """
        data = yaml.safe_load(yaml_data)
        nats_binding = NATSServerBindings.model_validate(data["nats"])
        assert nats_binding is not None


class TestNATSChannelBindings:
    """Tests for NATSChannelBindings model."""

    def test_nats_channel_bindings_serialization(self) -> None:
        """Test NATSChannelBindings serialization."""
        nats_binding = NATSChannelBindings()
        dumped = nats_binding.model_dump()
        assert dumped == {}

    def test_nats_channel_bindings_python_validation_error(self) -> None:
        """Test NATSChannelBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            NATSChannelBindings(some_field="value")

    def test_nats_channel_bindings_yaml_validation_error(self) -> None:
        """Test NATSChannelBindings YAML validation error with any fields."""
        yaml_data = """
        nats:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            NATSChannelBindings.model_validate(data["nats"])

    def test_nats_channel_bindings_yaml_empty_validation(self) -> None:
        """Test NATSChannelBindings YAML validation with no fields."""
        yaml_data = """
        nats: {}
        """
        data = yaml.safe_load(yaml_data)
        nats_binding = NATSChannelBindings.model_validate(data["nats"])
        assert nats_binding is not None


class TestNATSOperationBindings:
    """Tests for NATSOperationBindings model."""

    @parametrize_with_cases("yaml_data", cases=[case_operation_binding_with_queue])
    def test_nats_operation_bindings_validation(self, yaml_data: str) -> None:
        """Test NATSOperationBindings model validation."""
        data = yaml.safe_load(yaml_data)
        nats_binding = NATSOperationBindings.model_validate(data["nats"])
        assert nats_binding is not None
        assert nats_binding.binding_version == "0.1.0"

    @parametrize_with_cases(
        "nats_binding,expected",
        cases=[
            case_nats_operation_binding_serialization_empty,
            case_nats_operation_binding_serialization_with_queue,
        ],
    )
    def test_nats_operation_bindings_serialization(
        self,
        nats_binding: NATSOperationBindings,
        expected: dict,
    ) -> None:
        """Test NATSOperationBindings serialization."""
        dumped = nats_binding.model_dump()
        assert dumped == expected

    def test_nats_operation_binding_queue_validation(self) -> None:
        """Test NATSOperationBindings with queue field validation."""
        yaml_data = """
        nats:
          queue: my-queue
          bindingVersion: 0.1.0
        """
        data = yaml.safe_load(yaml_data)
        nats_binding = NATSOperationBindings.model_validate(data["nats"])

        assert nats_binding.queue == "my-queue"
        assert nats_binding.binding_version == "0.1.0"

    def test_nats_operation_bindings_python_validation_error(self) -> None:
        """Test NATSOperationBindings Python validation error with invalid arguments."""
        with pytest.raises(ValidationError):
            NATSOperationBindings(invalid_field="value")

    def test_nats_operation_bindings_yaml_validation_error(self) -> None:
        """Test NATSOperationBindings YAML validation error with invalid fields."""
        yaml_data = """
        nats:
          queue: my-queue
          invalid_field: value
          bindingVersion: 0.1.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            NATSOperationBindings.model_validate(data["nats"])


class TestNATSMessageBindings:
    """Tests for NATSMessageBindings model."""

    def test_nats_message_bindings_serialization(self) -> None:
        """Test NATSMessageBindings serialization."""
        nats_binding = NATSMessageBindings()
        dumped = nats_binding.model_dump()
        assert dumped == {}

    def test_nats_message_bindings_python_validation_error(self) -> None:
        """Test NATSMessageBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            NATSMessageBindings(some_field="value")

    def test_nats_message_bindings_yaml_validation_error(self) -> None:
        """Test NATSMessageBindings YAML validation error with any fields."""
        yaml_data = """
        nats:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            NATSMessageBindings.model_validate(data["nats"])

    def test_nats_message_bindings_yaml_empty_validation(self) -> None:
        """Test NATSMessageBindings YAML validation with no fields."""
        yaml_data = """
        nats: {}
        """
        data = yaml.safe_load(yaml_data)
        nats_binding = NATSMessageBindings.model_validate(data["nats"])
        assert nats_binding is not None
