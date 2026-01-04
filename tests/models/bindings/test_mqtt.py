"""Tests for MQTT bindings models."""

import yaml

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


# Channel Bindings Test Case
def case_channel_binding_empty() -> str:
    """Channel binding is empty object."""
    return """
    mqtt: {}
    """


class TestMQTTServerBindings:
    """Tests for MQTTServerBindings model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_server_binding_full, case_server_binding_with_schema],
    )
    def test_mqtt_server_bindings(self, yaml_data: str) -> None:
        """Test MQTTServerBindings model validation."""
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTServerBindings.model_validate(data["mqtt"])
        assert mqtt_binding is not None
        assert mqtt_binding.binding_version == "0.2.0"

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_server_binding_full, case_server_binding_with_schema],
    )
    def test_mqtt_server_bindings_serialization(self, yaml_data: str) -> None:
        """Test MQTTServerBindings serialization to JSON."""
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTServerBindings.model_validate(data["mqtt"])

        # Serialize to dict and verify structure
        dumped = mqtt_binding.model_dump(by_alias=True, exclude_none=True)
        assert "bindingVersion" in dumped
        assert dumped["bindingVersion"] == "0.2.0"

        # Serialize to JSON string
        json_str = mqtt_binding.model_dump_json(by_alias=True, exclude_none=True)
        assert "bindingVersion" in json_str
        assert "0.2.0" in json_str

    def test_mqtt_server_bindings_empty(self) -> None:
        """Test MQTTServerBindings empty object initialization."""
        mqtt_binding = MQTTServerBindings()

        # Verify default binding_version is included
        dumped = mqtt_binding.model_dump(by_alias=True, exclude_none=True)
        assert dumped == {"bindingVersion": "0.2.0"}

    def test_mqtt_server_binding_last_will(self) -> None:
        """Test MQTTServerBindings with lastWill object."""
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

        # Verify serialization
        dumped = mqtt_binding.model_dump(by_alias=True, exclude_none=True)
        assert "lastWill" in dumped
        assert dumped["lastWill"]["topic"] == "/last-wills"
        assert dumped["lastWill"]["qos"] == 2
        assert dumped["lastWill"]["message"] == "Guest gone offline."
        assert dumped["lastWill"]["retain"] is False

    def test_mqtt_server_binding_session_expiry_interval_schema(self) -> None:
        """Test MQTTServerBindings with sessionExpiryInterval as Schema."""
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

        # Verify serialization
        dumped = mqtt_binding.model_dump(by_alias=True, exclude_none=True)
        assert "sessionExpiryInterval" in dumped
        assert dumped["sessionExpiryInterval"]["type"] == "integer"


class TestMQTTChannelBindings:
    """Tests for MQTTChannelBindings model."""

    @parametrize_with_cases("yaml_data", cases=[case_channel_binding_empty])
    def test_mqtt_channel_bindings(self, yaml_data: str) -> None:
        """Test MQTTChannelBindings model validation."""
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTChannelBindings.model_validate(data["mqtt"])
        assert mqtt_binding is not None

    def test_mqtt_channel_bindings_empty(self) -> None:
        """Test MQTTChannelBindings empty object initialization."""
        mqtt_binding = MQTTChannelBindings()

        # Verify empty object can be serialized
        dumped = mqtt_binding.model_dump(by_alias=True, exclude_none=True)
        assert dumped == {}


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
    def test_mqtt_operation_bindings(self, yaml_data: str) -> None:
        """Test MQTTOperationBindings model validation."""
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTOperationBindings.model_validate(data["mqtt"])
        assert mqtt_binding is not None
        assert mqtt_binding.binding_version == "0.2.0"

    @parametrize_with_cases(
        "yaml_data",
        cases=[
            case_operation_binding_publish_full,
            case_operation_binding_publish_with_schema,
            case_operation_binding_subscribe,
        ],
    )
    def test_mqtt_operation_bindings_serialization(self, yaml_data: str) -> None:
        """Test MQTTOperationBindings serialization to JSON."""
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTOperationBindings.model_validate(data["mqtt"])

        # Serialize to dict and verify structure
        dumped = mqtt_binding.model_dump(by_alias=True, exclude_none=True)
        assert "bindingVersion" in dumped
        assert dumped["bindingVersion"] == "0.2.0"

        # Serialize to JSON string
        json_str = mqtt_binding.model_dump_json(by_alias=True, exclude_none=True)
        assert "bindingVersion" in json_str

    def test_mqtt_operation_bindings_empty(self) -> None:
        """Test MQTTOperationBindings empty object initialization."""
        mqtt_binding = MQTTOperationBindings()

        # Verify default binding_version is included
        dumped = mqtt_binding.model_dump(by_alias=True, exclude_none=True)
        assert dumped == {"bindingVersion": "0.2.0"}

    def test_mqtt_operation_binding_message_expiry_interval_schema(self) -> None:
        """Test MQTTOperationBindings with messageExpiryInterval as Schema."""
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

        # Verify serialization
        dumped = mqtt_binding.model_dump(by_alias=True, exclude_none=True)
        assert "messageExpiryInterval" in dumped
        assert dumped["messageExpiryInterval"]["type"] == "integer"


class TestMQTTMessageBindings:
    """Tests for MQTTMessageBindings model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_message_binding_basic, case_message_binding_full],
    )
    def test_mqtt_message_bindings(self, yaml_data: str) -> None:
        """Test MQTTMessageBindings model validation."""
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTMessageBindings.model_validate(data["mqtt"])
        assert mqtt_binding is not None
        assert mqtt_binding.binding_version == "0.2.0"

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_message_binding_basic, case_message_binding_full],
    )
    def test_mqtt_message_bindings_serialization(self, yaml_data: str) -> None:
        """Test MQTTMessageBindings serialization to JSON."""
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTMessageBindings.model_validate(data["mqtt"])

        # Serialize to dict and verify structure
        dumped = mqtt_binding.model_dump(by_alias=True, exclude_none=True)
        assert "bindingVersion" in dumped
        assert dumped["bindingVersion"] == "0.2.0"

        # Serialize to JSON string
        json_str = mqtt_binding.model_dump_json(by_alias=True, exclude_none=True)
        assert "bindingVersion" in json_str

    def test_mqtt_message_bindings_empty(self) -> None:
        """Test MQTTMessageBindings empty object initialization."""
        mqtt_binding = MQTTMessageBindings()

        # Verify default binding_version is included
        dumped = mqtt_binding.model_dump(by_alias=True, exclude_none=True)
        assert dumped == {"bindingVersion": "0.2.0"}

    def test_mqtt_message_binding_correlation_data_schema(self) -> None:
        """Test MQTTMessageBindings with correlationData as Schema."""
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

        # Verify serialization
        dumped = mqtt_binding.model_dump(by_alias=True, exclude_none=True)
        assert "correlationData" in dumped
        assert dumped["correlationData"]["type"] == "string"
        assert dumped["correlationData"]["format"] == "uuid"

    def test_mqtt_message_binding_response_topic_schema(self) -> None:
        """Test MQTTMessageBindings with responseTopic as Schema."""
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

        # Verify serialization
        dumped = mqtt_binding.model_dump(by_alias=True, exclude_none=True)
        assert "responseTopic" in dumped
        assert dumped["responseTopic"]["type"] == "string"
        assert dumped["responseTopic"]["pattern"] == "response/client/([a-z1-9]+)"
