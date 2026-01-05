"""Tests for AMQP1 bindings models."""

import pytest
import yaml

from pydantic import ValidationError

from asyncapi3.models.bindings.amqp1 import (
    AMQP1ChannelBindings,
    AMQP1MessageBindings,
    AMQP1OperationBindings,
    AMQP1ServerBindings,
)


class TestAMQP1ServerBindings:
    """Tests for AMQP1ServerBindings model."""

    def test_amqp1_server_bindings_serialization(self) -> None:
        """Test AMQP1ServerBindings serialization."""
        amqp1_binding = AMQP1ServerBindings()
        dumped = amqp1_binding.model_dump()
        assert dumped == {}

    def test_amqp1_server_bindings_python_validation_error(self) -> None:
        """Test AMQP1ServerBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            AMQP1ServerBindings(some_field="value")

    def test_amqp1_server_bindings_yaml_validation_error(self) -> None:
        """Test AMQP1ServerBindings YAML validation error with any fields."""
        yaml_data = """
        amqp1:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            AMQP1ServerBindings.model_validate(data["amqp1"])

    def test_amqp1_server_bindings_yaml_empty_validation(self) -> None:
        """Test AMQP1ServerBindings YAML validation with no fields."""
        yaml_data = """
        amqp1: {}
        """
        data = yaml.safe_load(yaml_data)
        amqp1_binding = AMQP1ServerBindings.model_validate(data["amqp1"])
        assert amqp1_binding is not None


class TestAMQP1ChannelBindings:
    """Tests for AMQP1ChannelBindings model."""

    def test_amqp1_channel_bindings_serialization(self) -> None:
        """Test AMQP1ChannelBindings serialization."""
        amqp1_binding = AMQP1ChannelBindings()
        dumped = amqp1_binding.model_dump()
        assert dumped == {}

    def test_amqp1_channel_bindings_python_validation_error(self) -> None:
        """Test AMQP1ChannelBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            AMQP1ChannelBindings(some_field="value")

    def test_amqp1_channel_bindings_yaml_validation_error(self) -> None:
        """Test AMQP1ChannelBindings YAML validation error with any fields."""
        yaml_data = """
        amqp1:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            AMQP1ChannelBindings.model_validate(data["amqp1"])

    def test_amqp1_channel_bindings_yaml_empty_validation(self) -> None:
        """Test AMQP1ChannelBindings YAML validation with no fields."""
        yaml_data = """
        amqp1: {}
        """
        data = yaml.safe_load(yaml_data)
        amqp1_binding = AMQP1ChannelBindings.model_validate(data["amqp1"])
        assert amqp1_binding is not None


class TestAMQP1OperationBindings:
    """Tests for AMQP1OperationBindings model."""

    def test_amqp1_operation_bindings_serialization(self) -> None:
        """Test AMQP1OperationBindings serialization."""
        amqp1_binding = AMQP1OperationBindings()
        dumped = amqp1_binding.model_dump()
        assert dumped == {}

    def test_amqp1_operation_bindings_python_validation_error(self) -> None:
        """Test AMQP1OperationBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            AMQP1OperationBindings(some_field="value")

    def test_amqp1_operation_bindings_yaml_validation_error(self) -> None:
        """Test AMQP1OperationBindings YAML validation error with any fields."""
        yaml_data = """
        amqp1:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            AMQP1OperationBindings.model_validate(data["amqp1"])

    def test_amqp1_operation_bindings_yaml_empty_validation(self) -> None:
        """Test AMQP1OperationBindings YAML validation with no fields."""
        yaml_data = """
        amqp1: {}
        """
        data = yaml.safe_load(yaml_data)
        amqp1_binding = AMQP1OperationBindings.model_validate(data["amqp1"])
        assert amqp1_binding is not None


class TestAMQP1MessageBindings:
    """Tests for AMQP1MessageBindings model."""

    def test_amqp1_message_bindings_serialization(self) -> None:
        """Test AMQP1MessageBindings serialization."""
        amqp1_binding = AMQP1MessageBindings()
        dumped = amqp1_binding.model_dump()
        assert dumped == {}

    def test_amqp1_message_bindings_python_validation_error(self) -> None:
        """Test AMQP1MessageBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            AMQP1MessageBindings(some_field="value")

    def test_amqp1_message_bindings_yaml_validation_error(self) -> None:
        """Test AMQP1MessageBindings YAML validation error with any fields."""
        yaml_data = """
        amqp1:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            AMQP1MessageBindings.model_validate(data["amqp1"])

    def test_amqp1_message_bindings_yaml_empty_validation(self) -> None:
        """Test AMQP1MessageBindings YAML validation with no fields."""
        yaml_data = """
        amqp1: {}
        """
        data = yaml.safe_load(yaml_data)
        amqp1_binding = AMQP1MessageBindings.model_validate(data["amqp1"])
        assert amqp1_binding is not None
