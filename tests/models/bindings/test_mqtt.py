"""Tests for MQTT bindings models."""

import pytest
import yaml

from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.bindings.mqtt import (
    MQTTChannelBindings,
    MQTTLastWill,
    MQTTMessageBindings,
    MQTTOperationBindings,
    MQTTServerBindings,
)
from asyncapi3.models.schema import Schema


# Server Bindings Test Cases
def case_server_binding_full() -> str:
    """Server binding with all fields."""
    return """
    mqtt:
      clientId: guest
      cleanSession: true
      lastWill:
        topic: /last-wills
        qos: 2
        message: Guest gone offline.
        retain: false
      keepAlive: 60
      sessionExpiryInterval: 600
      maximumPacketSize: 1200
      bindingVersion: 0.2.0
    """


def case_server_binding_with_schema() -> str:
    """Server binding with Schema objects."""
    return """
    mqtt:
      sessionExpiryInterval:
        type: integer
        minimum: 30
        maximum: 1200
      maximumPacketSize:
        type: integer
        minimum: 256
      bindingVersion: 0.2.0
    """


# Operation Bindings Test Cases
def case_operation_binding_publish_full() -> str:
    """Operation binding for publish with all fields."""
    return """
    mqtt:
      qos: 2
      retain: true
      messageExpiryInterval: 60
      bindingVersion: 0.2.0
    """


def case_operation_binding_publish_with_schema() -> str:
    """Operation binding for publish with Schema object."""
    return """
    mqtt:
      messageExpiryInterval:
        type: integer
        minimum: 30
        maximum: 300
      bindingVersion: 0.2.0
    """


def case_operation_binding_subscribe() -> str:
    """Operation binding for subscribe."""
    return """
    mqtt:
      qos: 2
      bindingVersion: 0.2.0
    """


# Message Bindings Test Cases
def case_message_binding_basic() -> str:
    """Message binding with contentType and correlationData."""
    return """
    mqtt:
      contentType: "application/json"
      correlationData:
        type: string
        format: uuid
      bindingVersion: 0.2.0
    """


def case_message_binding_full() -> str:
    """Message binding with all fields."""
    return """
    mqtt:
      payloadFormatIndicator: 1
      contentType: "application/json"
      correlationData:
        type: string
        format: uuid
      responseTopic:
        type: string
        pattern: "response/client/([a-z1-9]+)"
      bindingVersion: 0.2.0
    """


# Serialization Test Cases for Server Bindings
def case_mqtt_server_binding_serialization_empty() -> tuple[MQTTServerBindings, dict]:
    """MQTTServerBindings serialization empty."""
    mqtt_binding = MQTTServerBindings()
    expected = {"bindingVersion": "0.2.0"}
    return mqtt_binding, expected


def case_mqtt_server_binding_serialization_full() -> tuple[MQTTServerBindings, dict]:
    """MQTTServerBindings serialization with all fields."""
    mqtt_binding = MQTTServerBindings(
        client_id="guest",
        clean_session=True,
        last_will=MQTTLastWill(
            topic="/last-wills",
            qos=2,
            message="Guest gone offline.",
            retain=False,
        ),
        keep_alive=60,
        session_expiry_interval=600,
        maximum_packet_size=1200,
    )
    expected = {
        "clientId": "guest",
        "cleanSession": True,
        "lastWill": {
            "topic": "/last-wills",
            "qos": 2,
            "message": "Guest gone offline.",
            "retain": False,
        },
        "keepAlive": 60,
        "sessionExpiryInterval": 600,
        "maximumPacketSize": 1200,
        "bindingVersion": "0.2.0",
    }
    return mqtt_binding, expected


def case_mqtt_server_binding_serialization_with_schema() -> tuple[
    MQTTServerBindings, dict
]:
    """MQTTServerBindings serialization with Schema objects."""
    mqtt_binding = MQTTServerBindings(
        session_expiry_interval=Schema(
            type="integer",
            minimum=30,
            maximum=1200,
        ),
        maximum_packet_size=Schema(
            type="integer",
            minimum=256,
        ),
    )
    expected = {
        "sessionExpiryInterval": {
            "type": "integer",
            "minimum": 30,
            "maximum": 1200,
        },
        "maximumPacketSize": {
            "type": "integer",
            "minimum": 256,
        },
        "bindingVersion": "0.2.0",
    }
    return mqtt_binding, expected


# Serialization Test Cases for Operation Bindings
def case_mqtt_operation_binding_serialization_empty() -> tuple[
    MQTTOperationBindings, dict
]:
    """MQTTOperationBindings serialization empty."""
    mqtt_binding = MQTTOperationBindings()
    expected = {"bindingVersion": "0.2.0"}
    return mqtt_binding, expected


def case_mqtt_operation_binding_serialization_publish_full() -> tuple[
    MQTTOperationBindings, dict
]:
    """MQTTOperationBindings serialization publish with all fields."""
    mqtt_binding = MQTTOperationBindings(
        qos=2,
        retain=True,
        message_expiry_interval=60,
    )
    expected = {
        "qos": 2,
        "retain": True,
        "messageExpiryInterval": 60,
        "bindingVersion": "0.2.0",
    }
    return mqtt_binding, expected


def case_mqtt_operation_binding_serialization_publish_with_schema() -> tuple[
    MQTTOperationBindings, dict
]:
    """MQTTOperationBindings serialization publish with Schema object."""
    mqtt_binding = MQTTOperationBindings(
        message_expiry_interval=Schema(
            type="integer",
            minimum=30,
            maximum=300,
        ),
    )
    expected = {
        "messageExpiryInterval": {
            "type": "integer",
            "minimum": 30,
            "maximum": 300,
        },
        "bindingVersion": "0.2.0",
    }
    return mqtt_binding, expected


def case_mqtt_operation_binding_serialization_subscribe() -> tuple[
    MQTTOperationBindings, dict
]:
    """MQTTOperationBindings serialization subscribe."""
    mqtt_binding = MQTTOperationBindings(qos=2)
    expected = {
        "qos": 2,
        "bindingVersion": "0.2.0",
    }
    return mqtt_binding, expected


# Serialization Test Cases for Message Bindings
def case_mqtt_message_binding_serialization_empty() -> tuple[MQTTMessageBindings, dict]:
    """MQTTMessageBindings serialization empty."""
    mqtt_binding = MQTTMessageBindings()
    expected = {"bindingVersion": "0.2.0"}
    return mqtt_binding, expected


def case_mqtt_message_binding_serialization_basic() -> tuple[MQTTMessageBindings, dict]:
    """MQTTMessageBindings serialization with contentType and correlationData."""
    mqtt_binding = MQTTMessageBindings(
        content_type="application/json",
        correlation_data=Schema(
            type="string",
            format="uuid",
        ),
    )
    expected = {
        "contentType": "application/json",
        "correlationData": {
            "type": "string",
            "format": "uuid",
        },
        "bindingVersion": "0.2.0",
    }
    return mqtt_binding, expected


def case_mqtt_message_binding_serialization_full() -> tuple[MQTTMessageBindings, dict]:
    """MQTTMessageBindings serialization with all fields."""
    mqtt_binding = MQTTMessageBindings(
        payload_format_indicator=1,
        content_type="application/json",
        correlation_data=Schema(
            type="string",
            format="uuid",
        ),
        response_topic=Schema(
            type="string",
            pattern="response/client/([a-z1-9]+)",
        ),
    )
    expected = {
        "payloadFormatIndicator": 1,
        "contentType": "application/json",
        "correlationData": {
            "type": "string",
            "format": "uuid",
        },
        "responseTopic": {
            "type": "string",
            "pattern": "response/client/([a-z1-9]+)",
        },
        "bindingVersion": "0.2.0",
    }
    return mqtt_binding, expected


class TestMQTTServerBindings:
    """Tests for MQTTServerBindings model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_server_binding_full, case_server_binding_with_schema],
    )
    def test_mqtt_server_bindings_validation(self, yaml_data: str) -> None:
        """Test MQTTServerBindings model validation."""
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTServerBindings.model_validate(data["mqtt"])
        assert mqtt_binding is not None
        assert mqtt_binding.binding_version == "0.2.0"

    @parametrize_with_cases(
        "mqtt_binding,expected",
        cases=[
            case_mqtt_server_binding_serialization_empty,
            case_mqtt_server_binding_serialization_full,
            case_mqtt_server_binding_serialization_with_schema,
        ],
    )
    def test_mqtt_server_bindings_serialization(
        self,
        mqtt_binding: MQTTServerBindings,
        expected: dict,
    ) -> None:
        """Test MQTTServerBindings serialization."""
        dumped = mqtt_binding.model_dump()
        assert dumped == expected

    def test_mqtt_server_binding_last_will_validation(self) -> None:
        """Test MQTTServerBindings with lastWill object validation."""
        yaml_data = """
        mqtt:
          lastWill:
            topic: /last-wills
            qos: 2
            message: Guest gone offline.
            retain: false
          bindingVersion: 0.2.0
        """
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTServerBindings.model_validate(data["mqtt"])

        # Verify all fields
        assert mqtt_binding.last_will is not None
        assert isinstance(mqtt_binding.last_will, MQTTLastWill)
        assert mqtt_binding.last_will.topic == "/last-wills"
        assert mqtt_binding.last_will.qos == 2
        assert mqtt_binding.last_will.message == "Guest gone offline."
        assert mqtt_binding.last_will.retain is False
        assert mqtt_binding.binding_version == "0.2.0"

    def test_mqtt_server_binding_session_expiry_interval_schema_validation(
        self,
    ) -> None:
        """Test MQTTServerBindings with sessionExpiryInterval as Schema validation."""
        yaml_data = """
        mqtt:
          sessionExpiryInterval:
            type: integer
            minimum: 30
            maximum: 1200
          bindingVersion: 0.2.0
        """
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTServerBindings.model_validate(data["mqtt"])

        # Verify all fields
        assert mqtt_binding.session_expiry_interval is not None
        assert isinstance(mqtt_binding.session_expiry_interval, Schema)
        assert mqtt_binding.session_expiry_interval.type == "integer"
        assert mqtt_binding.binding_version == "0.2.0"

    def test_mqtt_server_bindings_python_validation_error(self) -> None:
        """Test MQTTServerBindings Python validation error with extra arguments."""
        with pytest.raises(ValidationError):
            MQTTServerBindings(some_field="value")

    def test_mqtt_server_bindings_yaml_validation_error(self) -> None:
        """Test MQTTServerBindings YAML validation error with extra fields."""
        yaml_data = """
        mqtt:
          some_field: value
          bindingVersion: 0.2.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            MQTTServerBindings.model_validate(data["mqtt"])


class TestMQTTChannelBindings:
    """Tests for MQTTChannelBindings model."""

    def test_mqtt_channel_bindings_serialization(self) -> None:
        """Test MQTTChannelBindings serialization."""
        mqtt_binding = MQTTChannelBindings()
        dumped = mqtt_binding.model_dump()
        assert dumped == {}

    def test_mqtt_channel_bindings_python_validation_error(self) -> None:
        """Test MQTTChannelBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            MQTTChannelBindings(some_field="value")

    def test_mqtt_channel_bindings_yaml_validation_error(self) -> None:
        """Test MQTTChannelBindings YAML validation error with any fields."""
        yaml_data = """
        mqtt:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            MQTTChannelBindings.model_validate(data["mqtt"])

    def test_mqtt_channel_bindings_yaml_empty_validation(self) -> None:
        """Test MQTTChannelBindings YAML validation with no fields."""
        yaml_data = """
        mqtt: {}
        """
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTChannelBindings.model_validate(data["mqtt"])
        assert mqtt_binding is not None


class TestMQTTOperationBindings:
    """Tests for MQTTOperationBindings model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[
            case_operation_binding_publish_full,
            case_operation_binding_publish_with_schema,
            case_operation_binding_subscribe,
        ],
    )
    def test_mqtt_operation_bindings_validation(self, yaml_data: str) -> None:
        """Test MQTTOperationBindings model validation."""
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTOperationBindings.model_validate(data["mqtt"])
        assert mqtt_binding is not None
        assert mqtt_binding.binding_version == "0.2.0"

    @parametrize_with_cases(
        "mqtt_binding,expected",
        cases=[
            case_mqtt_operation_binding_serialization_empty,
            case_mqtt_operation_binding_serialization_publish_full,
            case_mqtt_operation_binding_serialization_publish_with_schema,
            case_mqtt_operation_binding_serialization_subscribe,
        ],
    )
    def test_mqtt_operation_bindings_serialization(
        self,
        mqtt_binding: MQTTOperationBindings,
        expected: dict,
    ) -> None:
        """Test MQTTOperationBindings serialization."""
        dumped = mqtt_binding.model_dump()
        assert dumped == expected

    def test_mqtt_operation_binding_message_expiry_interval_schema_validation(
        self,
    ) -> None:
        """Test MQTTOperationBindings with messageExpiryInterval as Schema validation."""
        yaml_data = """
        mqtt:
          messageExpiryInterval:
            type: integer
            minimum: 30
            maximum: 300
          bindingVersion: 0.2.0
        """
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTOperationBindings.model_validate(data["mqtt"])

        # Verify all fields
        assert mqtt_binding.message_expiry_interval is not None
        assert isinstance(mqtt_binding.message_expiry_interval, Schema)
        assert mqtt_binding.message_expiry_interval.type == "integer"
        assert mqtt_binding.binding_version == "0.2.0"

    def test_mqtt_operation_bindings_python_validation_error(self) -> None:
        """Test MQTTOperationBindings Python validation error with extra arguments."""
        with pytest.raises(ValidationError):
            MQTTOperationBindings(some_field="value")

    def test_mqtt_operation_bindings_yaml_validation_error(self) -> None:
        """Test MQTTOperationBindings YAML validation error with extra fields."""
        yaml_data = """
        mqtt:
          some_field: value
          bindingVersion: 0.2.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            MQTTOperationBindings.model_validate(data["mqtt"])


class TestMQTTMessageBindings:
    """Tests for MQTTMessageBindings model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_message_binding_basic, case_message_binding_full],
    )
    def test_mqtt_message_bindings_validation(self, yaml_data: str) -> None:
        """Test MQTTMessageBindings model validation."""
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTMessageBindings.model_validate(data["mqtt"])
        assert mqtt_binding is not None
        assert mqtt_binding.binding_version == "0.2.0"

    @parametrize_with_cases(
        "mqtt_binding,expected",
        cases=[
            case_mqtt_message_binding_serialization_empty,
            case_mqtt_message_binding_serialization_basic,
            case_mqtt_message_binding_serialization_full,
        ],
    )
    def test_mqtt_message_bindings_serialization(
        self,
        mqtt_binding: MQTTMessageBindings,
        expected: dict,
    ) -> None:
        """Test MQTTMessageBindings serialization."""
        dumped = mqtt_binding.model_dump()
        assert dumped == expected

    def test_mqtt_message_binding_correlation_data_schema_validation(self) -> None:
        """Test MQTTMessageBindings with correlationData as Schema validation."""
        yaml_data = """
        mqtt:
          correlationData:
            type: string
            format: uuid
          bindingVersion: 0.2.0
        """
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTMessageBindings.model_validate(data["mqtt"])

        # Verify all fields
        assert mqtt_binding.correlation_data is not None
        assert isinstance(mqtt_binding.correlation_data, Schema)
        assert mqtt_binding.correlation_data.type == "string"
        assert mqtt_binding.correlation_data.format == "uuid"
        assert mqtt_binding.binding_version == "0.2.0"

    def test_mqtt_message_binding_response_topic_schema_validation(self) -> None:
        """Test MQTTMessageBindings with responseTopic as Schema validation."""
        yaml_data = """
        mqtt:
          responseTopic:
            type: string
            pattern: "response/client/([a-z1-9]+)"
          bindingVersion: 0.2.0
        """
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTMessageBindings.model_validate(data["mqtt"])

        # Verify all fields
        assert mqtt_binding.response_topic is not None
        assert isinstance(mqtt_binding.response_topic, Schema)
        assert mqtt_binding.response_topic.type == "string"
        assert mqtt_binding.response_topic.pattern == "response/client/([a-z1-9]+)"
        assert mqtt_binding.binding_version == "0.2.0"

    def test_mqtt_message_bindings_python_validation_error(self) -> None:
        """Test MQTTMessageBindings Python validation error with extra arguments."""
        with pytest.raises(ValidationError):
            MQTTMessageBindings(some_field="value")

    def test_mqtt_message_bindings_yaml_validation_error(self) -> None:
        """Test MQTTMessageBindings YAML validation error with extra fields."""
        yaml_data = """
        mqtt:
          some_field: value
          bindingVersion: 0.2.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            MQTTMessageBindings.model_validate(data["mqtt"])
