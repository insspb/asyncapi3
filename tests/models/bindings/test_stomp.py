"""Tests for STOMP bindings models."""

import pytest
import yaml

from pydantic import ValidationError

from asyncapi3.models.bindings.stomp import (
    STOMPChannelBindings,
    STOMPMessageBindings,
    STOMPOperationBindings,
    STOMPServerBindings,
)


class TestSTOMPServerBindings:
    """Tests for STOMPServerBindings model."""

    def test_stomp_server_bindings_serialization(self) -> None:
        """Test STOMPServerBindings serialization."""
        stomp_binding = STOMPServerBindings()
        dumped = stomp_binding.model_dump()
        assert dumped == {}

    def test_stomp_server_bindings_python_validation_error(self) -> None:
        """Test STOMPServerBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            STOMPServerBindings(some_field="value")

    def test_stomp_server_bindings_yaml_validation_error(self) -> None:
        """Test STOMPServerBindings YAML validation error with any fields."""
        yaml_data = """
        stomp:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            STOMPServerBindings.model_validate(data["stomp"])

    def test_stomp_server_bindings_yaml_empty_validation(self) -> None:
        """Test STOMPServerBindings YAML validation with no fields."""
        yaml_data = """
        stomp: {}
        """
        data = yaml.safe_load(yaml_data)
        stomp_binding = STOMPServerBindings.model_validate(data["stomp"])
        assert stomp_binding is not None


class TestSTOMPChannelBindings:
    """Tests for STOMPChannelBindings model."""

    def test_stomp_channel_bindings_serialization(self) -> None:
        """Test STOMPChannelBindings serialization."""
        stomp_binding = STOMPChannelBindings()
        dumped = stomp_binding.model_dump()
        assert dumped == {}

    def test_stomp_channel_bindings_python_validation_error(self) -> None:
        """Test STOMPChannelBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            STOMPChannelBindings(some_field="value")

    def test_stomp_channel_bindings_yaml_validation_error(self) -> None:
        """Test STOMPChannelBindings YAML validation error with any fields."""
        yaml_data = """
        stomp:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            STOMPChannelBindings.model_validate(data["stomp"])

    def test_stomp_channel_bindings_yaml_empty_validation(self) -> None:
        """Test STOMPChannelBindings YAML validation with no fields."""
        yaml_data = """
        stomp: {}
        """
        data = yaml.safe_load(yaml_data)
        stomp_binding = STOMPChannelBindings.model_validate(data["stomp"])
        assert stomp_binding is not None


class TestSTOMPOperationBindings:
    """Tests for STOMPOperationBindings model."""

    def test_stomp_operation_bindings_serialization(self) -> None:
        """Test STOMPOperationBindings serialization."""
        stomp_binding = STOMPOperationBindings()
        dumped = stomp_binding.model_dump()
        assert dumped == {}

    def test_stomp_operation_bindings_python_validation_error(self) -> None:
        """Test STOMPOperationBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            STOMPOperationBindings(some_field="value")

    def test_stomp_operation_bindings_yaml_validation_error(self) -> None:
        """Test STOMPOperationBindings YAML validation error with any fields."""
        yaml_data = """
        stomp:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            STOMPOperationBindings.model_validate(data["stomp"])

    def test_stomp_operation_bindings_yaml_empty_validation(self) -> None:
        """Test STOMPOperationBindings YAML validation with no fields."""
        yaml_data = """
        stomp: {}
        """
        data = yaml.safe_load(yaml_data)
        stomp_binding = STOMPOperationBindings.model_validate(data["stomp"])
        assert stomp_binding is not None


class TestSTOMPMessageBindings:
    """Tests for STOMPMessageBindings model."""

    def test_stomp_message_bindings_serialization(self) -> None:
        """Test STOMPMessageBindings serialization."""
        stomp_binding = STOMPMessageBindings()
        dumped = stomp_binding.model_dump()
        assert dumped == {}

    def test_stomp_message_bindings_python_validation_error(self) -> None:
        """Test STOMPMessageBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            STOMPMessageBindings(some_field="value")

    def test_stomp_message_bindings_yaml_validation_error(self) -> None:
        """Test STOMPMessageBindings YAML validation error with any fields."""
        yaml_data = """
        stomp:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            STOMPMessageBindings.model_validate(data["stomp"])

    def test_stomp_message_bindings_yaml_empty_validation(self) -> None:
        """Test STOMPMessageBindings YAML validation with no fields."""
        yaml_data = """
        stomp: {}
        """
        data = yaml.safe_load(yaml_data)
        stomp_binding = STOMPMessageBindings.model_validate(data["stomp"])
        assert stomp_binding is not None
