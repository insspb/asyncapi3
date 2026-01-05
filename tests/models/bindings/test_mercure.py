"""Tests for Mercure bindings models."""

import pytest
import yaml

from pydantic import ValidationError

from asyncapi3.models.bindings.mercure import (
    MercureChannelBindings,
    MercureMessageBindings,
    MercureOperationBindings,
    MercureServerBindings,
)


class TestMercureServerBindings:
    """Tests for MercureServerBindings model."""

    def test_mercure_server_bindings_serialization(self) -> None:
        """Test MercureServerBindings serialization."""
        mercure_binding = MercureServerBindings()
        dumped = mercure_binding.model_dump()
        assert dumped == {}

    def test_mercure_server_bindings_python_validation_error(self) -> None:
        """Test MercureServerBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            MercureServerBindings(some_field="value")

    def test_mercure_server_bindings_yaml_validation_error(self) -> None:
        """Test MercureServerBindings YAML validation error with any fields."""
        yaml_data = """
        mercure:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            MercureServerBindings.model_validate(data["mercure"])

    def test_mercure_server_bindings_yaml_empty_validation(self) -> None:
        """Test MercureServerBindings YAML validation with no fields."""
        yaml_data = """
        mercure: {}
        """
        data = yaml.safe_load(yaml_data)
        mercure_binding = MercureServerBindings.model_validate(data["mercure"])
        assert mercure_binding is not None


class TestMercureChannelBindings:
    """Tests for MercureChannelBindings model."""

    def test_mercure_channel_bindings_serialization(self) -> None:
        """Test MercureChannelBindings serialization."""
        mercure_binding = MercureChannelBindings()
        dumped = mercure_binding.model_dump()
        assert dumped == {}

    def test_mercure_channel_bindings_python_validation_error(self) -> None:
        """Test MercureChannelBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            MercureChannelBindings(some_field="value")

    def test_mercure_channel_bindings_yaml_validation_error(self) -> None:
        """Test MercureChannelBindings YAML validation error with any fields."""
        yaml_data = """
        mercure:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            MercureChannelBindings.model_validate(data["mercure"])

    def test_mercure_channel_bindings_yaml_empty_validation(self) -> None:
        """Test MercureChannelBindings YAML validation with no fields."""
        yaml_data = """
        mercure: {}
        """
        data = yaml.safe_load(yaml_data)
        mercure_binding = MercureChannelBindings.model_validate(data["mercure"])
        assert mercure_binding is not None


class TestMercureOperationBindings:
    """Tests for MercureOperationBindings model."""

    def test_mercure_operation_bindings_serialization(self) -> None:
        """Test MercureOperationBindings serialization."""
        mercure_binding = MercureOperationBindings()
        dumped = mercure_binding.model_dump()
        assert dumped == {}

    def test_mercure_operation_bindings_python_validation_error(self) -> None:
        """Test MercureOperationBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            MercureOperationBindings(some_field="value")

    def test_mercure_operation_bindings_yaml_validation_error(self) -> None:
        """Test MercureOperationBindings YAML validation error with any fields."""
        yaml_data = """
        mercure:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            MercureOperationBindings.model_validate(data["mercure"])

    def test_mercure_operation_bindings_yaml_empty_validation(self) -> None:
        """Test MercureOperationBindings YAML validation with no fields."""
        yaml_data = """
        mercure: {}
        """
        data = yaml.safe_load(yaml_data)
        mercure_binding = MercureOperationBindings.model_validate(data["mercure"])
        assert mercure_binding is not None


class TestMercureMessageBindings:
    """Tests for MercureMessageBindings model."""

    def test_mercure_message_bindings_serialization(self) -> None:
        """Test MercureMessageBindings serialization."""
        mercure_binding = MercureMessageBindings()
        dumped = mercure_binding.model_dump()
        assert dumped == {}

    def test_mercure_message_bindings_python_validation_error(self) -> None:
        """Test MercureMessageBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            MercureMessageBindings(some_field="value")

    def test_mercure_message_bindings_yaml_validation_error(self) -> None:
        """Test MercureMessageBindings YAML validation error with any fields."""
        yaml_data = """
        mercure:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            MercureMessageBindings.model_validate(data["mercure"])

    def test_mercure_message_bindings_yaml_empty_validation(self) -> None:
        """Test MercureMessageBindings YAML validation with no fields."""
        yaml_data = """
        mercure: {}
        """
        data = yaml.safe_load(yaml_data)
        mercure_binding = MercureMessageBindings.model_validate(data["mercure"])
        assert mercure_binding is not None
