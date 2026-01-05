"""Tests for MQTT5 bindings models."""

from typing import Any

import pytest
import yaml

from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.bindings.mqtt5 import (
    MQTT5ChannelBindings,
    MQTT5MessageBindings,
    MQTT5OperationBindings,
    MQTT5ServerBindings,
)
from asyncapi3.models.schema import Schema


# Server Bindings Validation Test Cases
def case_server_binding_integer() -> str:
    """Server binding with sessionExpiryInterval as integer."""
    return """
    mqtt5:
      sessionExpiryInterval: 60
      bindingVersion: 0.2.0
    """


def case_server_binding_schema() -> str:
    """Server binding with sessionExpiryInterval as Schema."""
    return """
    mqtt5:
      sessionExpiryInterval:
        type: integer
        minimum: 100
      bindingVersion: 0.2.0
    """


# Server Bindings Serialization Test Cases
def case_mqtt5_server_binding_serialization_empty() -> tuple[MQTT5ServerBindings, dict]:
    """MQTT5ServerBindings serialization empty."""
    mqtt5_binding = MQTT5ServerBindings()
    expected: dict[str, Any] = {"bindingVersion": "0.2.0"}
    return mqtt5_binding, expected


def case_mqtt5_server_binding_serialization_integer() -> tuple[
    MQTT5ServerBindings, dict
]:
    """MQTT5ServerBindings serialization with sessionExpiryInterval as integer."""
    mqtt5_binding = MQTT5ServerBindings(session_expiry_interval=60)
    expected: dict[str, Any] = {
        "sessionExpiryInterval": 60,
        "bindingVersion": "0.2.0",
    }
    return mqtt5_binding, expected


def case_mqtt5_server_binding_serialization_schema() -> tuple[
    MQTT5ServerBindings, dict
]:
    """MQTT5ServerBindings serialization with sessionExpiryInterval as Schema."""
    mqtt5_binding = MQTT5ServerBindings(
        session_expiry_interval=Schema(type="integer", minimum=100),
    )
    expected: dict[str, Any] = {
        "sessionExpiryInterval": {
            "type": "integer",
            "minimum": 100,
        },
        "bindingVersion": "0.2.0",
    }
    return mqtt5_binding, expected


class TestMQTT5ServerBindings:
    """Tests for MQTT5ServerBindings model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_server_binding_integer, case_server_binding_schema],
    )
    def test_mqtt5_server_bindings_validation(self, yaml_data: str) -> None:
        """Test MQTT5ServerBindings model validation."""
        data = yaml.safe_load(yaml_data)
        mqtt5_binding = MQTT5ServerBindings.model_validate(data["mqtt5"])
        assert mqtt5_binding is not None
        assert mqtt5_binding.binding_version == "0.2.0"

    @parametrize_with_cases(
        "mqtt5_binding,expected",
        cases=[
            case_mqtt5_server_binding_serialization_empty,
            case_mqtt5_server_binding_serialization_integer,
            case_mqtt5_server_binding_serialization_schema,
        ],
    )
    def test_mqtt5_server_bindings_serialization(
        self,
        mqtt5_binding: MQTT5ServerBindings,
        expected: dict,
    ) -> None:
        """Test MQTT5ServerBindings serialization."""
        dumped = mqtt5_binding.model_dump()
        assert dumped == expected

    def test_mqtt5_server_binding_session_expiry_interval_schema_validation(
        self,
    ) -> None:
        """Test MQTT5ServerBindings with sessionExpiryInterval as Schema validation."""
        yaml_data = """
        mqtt5:
          sessionExpiryInterval:
            type: integer
            minimum: 100
          bindingVersion: 0.2.0
        """
        data = yaml.safe_load(yaml_data)
        mqtt5_binding = MQTT5ServerBindings.model_validate(data["mqtt5"])

        assert mqtt5_binding.session_expiry_interval is not None
        assert isinstance(mqtt5_binding.session_expiry_interval, Schema)
        assert mqtt5_binding.session_expiry_interval.type == "integer"
        assert mqtt5_binding.binding_version == "0.2.0"

    def test_mqtt5_server_bindings_python_validation_error(self) -> None:
        """Test MQTT5ServerBindings Python validation error with extra arguments."""
        with pytest.raises(ValidationError):
            MQTT5ServerBindings(some_field="value")

    def test_mqtt5_server_bindings_yaml_validation_error(self) -> None:
        """Test MQTT5ServerBindings YAML validation error with extra fields."""
        yaml_data = """
        mqtt5:
          some_field: value
          bindingVersion: 0.2.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            MQTT5ServerBindings.model_validate(data["mqtt5"])


class TestMQTT5ChannelBindings:
    """Tests for MQTT5ChannelBindings model."""

    def test_mqtt5_channel_bindings_serialization(self) -> None:
        """Test MQTT5ChannelBindings serialization."""
        mqtt5_binding = MQTT5ChannelBindings()
        dumped = mqtt5_binding.model_dump()
        assert dumped == {}

    def test_mqtt5_channel_bindings_python_validation_error(self) -> None:
        """Test MQTT5ChannelBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            MQTT5ChannelBindings(some_field="value")

    def test_mqtt5_channel_bindings_yaml_validation_error(self) -> None:
        """Test MQTT5ChannelBindings YAML validation error with any fields."""
        yaml_data = """
        mqtt5:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            MQTT5ChannelBindings.model_validate(data["mqtt5"])

    def test_mqtt5_channel_bindings_yaml_empty_validation(self) -> None:
        """Test MQTT5ChannelBindings YAML validation with no fields."""
        yaml_data = """
        mqtt5: {}
        """
        data = yaml.safe_load(yaml_data)
        mqtt5_binding = MQTT5ChannelBindings.model_validate(data["mqtt5"])
        assert mqtt5_binding is not None


class TestMQTT5OperationBindings:
    """Tests for MQTT5OperationBindings model."""

    def test_mqtt5_operation_bindings_serialization(self) -> None:
        """Test MQTT5OperationBindings serialization."""
        mqtt5_binding = MQTT5OperationBindings()
        dumped = mqtt5_binding.model_dump()
        assert dumped == {}

    def test_mqtt5_operation_bindings_python_validation_error(self) -> None:
        """Test MQTT5OperationBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            MQTT5OperationBindings(some_field="value")

    def test_mqtt5_operation_bindings_yaml_validation_error(self) -> None:
        """Test MQTT5OperationBindings YAML validation error with any fields."""
        yaml_data = """
        mqtt5:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            MQTT5OperationBindings.model_validate(data["mqtt5"])

    def test_mqtt5_operation_bindings_yaml_empty_validation(self) -> None:
        """Test MQTT5OperationBindings YAML validation with no fields."""
        yaml_data = """
        mqtt5: {}
        """
        data = yaml.safe_load(yaml_data)
        mqtt5_binding = MQTT5OperationBindings.model_validate(data["mqtt5"])
        assert mqtt5_binding is not None


class TestMQTT5MessageBindings:
    """Tests for MQTT5MessageBindings model."""

    def test_mqtt5_message_bindings_serialization(self) -> None:
        """Test MQTT5MessageBindings serialization."""
        mqtt5_binding = MQTT5MessageBindings()
        dumped = mqtt5_binding.model_dump()
        assert dumped == {}

    def test_mqtt5_message_bindings_python_validation_error(self) -> None:
        """Test MQTT5MessageBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            MQTT5MessageBindings(some_field="value")

    def test_mqtt5_message_bindings_yaml_validation_error(self) -> None:
        """Test MQTT5MessageBindings YAML validation error with any fields."""
        yaml_data = """
        mqtt5:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            MQTT5MessageBindings.model_validate(data["mqtt5"])

    def test_mqtt5_message_bindings_yaml_empty_validation(self) -> None:
        """Test MQTT5MessageBindings YAML validation with no fields."""
        yaml_data = """
        mqtt5: {}
        """
        data = yaml.safe_load(yaml_data)
        mqtt5_binding = MQTT5MessageBindings.model_validate(data["mqtt5"])
        assert mqtt5_binding is not None
