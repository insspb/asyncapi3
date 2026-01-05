"""Tests for JMS bindings models."""

from typing import Any

import pytest
import yaml

from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.bindings.jms import (
    JMSChannelBindings,
    JMSMessageBindings,
    JMSOperationBindings,
    JMSServerBindings,
)
from asyncapi3.models.schema import Schema


# Server Bindings Validation Test Cases
def case_server_binding_full() -> str:
    """Server binding with all fields."""
    return """
    jms:
      jmsConnectionFactory: org.apache.activemq.ActiveMQConnectionFactory
      properties:
        - name: disableTimeStampsByDefault
          value: false
      clientID: my-application-1
      bindingVersion: 0.0.1
    """


# Server Bindings Serialization Test Cases
def case_jms_server_binding_serialization_full() -> tuple[JMSServerBindings, dict]:
    """JMSServerBindings serialization with all fields."""
    jms_binding = JMSServerBindings(
        jms_connection_factory="org.apache.activemq.ActiveMQConnectionFactory",
        properties=[
            Schema(
                type="object",
                properties={
                    "name": Schema(type="string", const="disableTimeStampsByDefault"),
                    "value": Schema(type="boolean", const=False),
                },
            ),
        ],
        client_id="my-application-1",
    )
    expected: dict[str, Any] = {
        "jmsConnectionFactory": "org.apache.activemq.ActiveMQConnectionFactory",
        "properties": [
            {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "const": "disableTimeStampsByDefault",
                    },
                    "value": {
                        "type": "boolean",
                        "const": False,
                    },
                },
            },
        ],
        "clientID": "my-application-1",
        "bindingVersion": "0.0.1",
    }
    return jms_binding, expected


# Channel Bindings Validation Test Cases
def case_channel_binding_fifo_queue() -> str:
    """Channel binding with fifo-queue destination type."""
    return """
    jms:
      destination: user-sign-up
      destinationType: fifo-queue
      bindingVersion: 0.0.1
    """


# Channel Bindings Serialization Test Cases
def case_jms_channel_binding_serialization_empty() -> tuple[JMSChannelBindings, dict]:
    """JMSChannelBindings serialization empty."""
    jms_binding = JMSChannelBindings()
    expected: dict[str, Any] = {"bindingVersion": "0.0.1"}
    return jms_binding, expected


def case_jms_channel_binding_serialization_fifo_queue() -> tuple[
    JMSChannelBindings, dict
]:
    """JMSChannelBindings serialization with fifo-queue."""
    jms_binding = JMSChannelBindings(
        destination="user-sign-up",
        destination_type="fifo-queue",
    )
    expected: dict[str, Any] = {
        "destination": "user-sign-up",
        "destinationType": "fifo-queue",
        "bindingVersion": "0.0.1",
    }
    return jms_binding, expected


# Message Bindings Validation Test Cases
def case_message_binding_with_headers() -> str:
    """Message binding with headers Schema."""
    return """
    jms:
      headers:
        required:
          - JMSMessageID
        properties:
          JMSMessageID:
            name: JMSMessageID
            description: A unique message identifier.
            type: string
          JMSReplyTo:
            name: JMSReplyTo
            description: The queue or topic that the message sender expects replies to.
            type: string
      bindingVersion: 0.0.1
    """


# Message Bindings Serialization Test Cases
def case_jms_message_binding_serialization_empty() -> tuple[JMSMessageBindings, dict]:
    """JMSMessageBindings serialization empty."""
    jms_binding = JMSMessageBindings()
    expected: dict[str, Any] = {"bindingVersion": "0.0.1"}
    return jms_binding, expected


def case_jms_message_binding_serialization_with_headers() -> tuple[
    JMSMessageBindings, dict
]:
    """JMSMessageBindings serialization with headers Schema."""
    jms_binding = JMSMessageBindings(
        headers=Schema(
            type="object",
            required=["JMSMessageID"],
            properties={
                "JMSMessageID": Schema(
                    name="JMSMessageID",
                    description="A unique message identifier.",
                    type="string",
                ),
                "JMSReplyTo": Schema(
                    name="JMSReplyTo",
                    description="The queue or topic that the message sender expects replies to.",
                    type="string",
                ),
            },
        ),
    )
    expected: dict[str, Any] = {
        "headers": {
            "type": "object",
            "required": ["JMSMessageID"],
            "properties": {
                "JMSMessageID": {
                    "name": "JMSMessageID",
                    "description": "A unique message identifier.",
                    "type": "string",
                },
                "JMSReplyTo": {
                    "name": "JMSReplyTo",
                    "description": "The queue or topic that the message sender expects replies to.",
                    "type": "string",
                },
            },
        },
        "bindingVersion": "0.0.1",
    }
    return jms_binding, expected


class TestJMSServerBindings:
    """Tests for JMSServerBindings model."""

    @parametrize_with_cases("yaml_data", cases=[case_server_binding_full])
    def test_jms_server_bindings_validation(self, yaml_data: str) -> None:
        """Test JMSServerBindings model validation."""
        data = yaml.safe_load(yaml_data)
        jms_binding = JMSServerBindings.model_validate(data["jms"])
        assert jms_binding is not None
        assert jms_binding.binding_version == "0.0.1"

    @parametrize_with_cases(
        "jms_binding,expected",
        cases=[case_jms_server_binding_serialization_full],
    )
    def test_jms_server_bindings_serialization(
        self,
        jms_binding: JMSServerBindings,
        expected: dict,
    ) -> None:
        """Test JMSServerBindings serialization."""
        dumped = jms_binding.model_dump()
        assert dumped == expected

    def test_jms_server_binding_all_fields_validation(self) -> None:
        """Test JMSServerBindings with all fields validation."""
        yaml_data = """
        jms:
          jmsConnectionFactory: org.apache.activemq.ActiveMQConnectionFactory
          properties:
            - name: disableTimeStampsByDefault
              value: false
          clientID: my-application-1
          bindingVersion: 0.0.1
        """
        data = yaml.safe_load(yaml_data)
        jms_binding = JMSServerBindings.model_validate(data["jms"])

        assert (
            jms_binding.jms_connection_factory
            == "org.apache.activemq.ActiveMQConnectionFactory"
        )
        assert jms_binding.properties is not None
        assert len(jms_binding.properties) == 1
        assert jms_binding.client_id == "my-application-1"
        assert jms_binding.binding_version == "0.0.1"

    def test_jms_server_bindings_python_validation_error(self) -> None:
        """Test JMSServerBindings Python validation error with extra arguments."""
        with pytest.raises(ValidationError):
            JMSServerBindings(jms_connection_factory="test.factory", some_field="value")

    def test_jms_server_bindings_yaml_validation_error(self) -> None:
        """Test JMSServerBindings YAML validation error with extra fields."""
        yaml_data = """
        jms:
          jmsConnectionFactory: test.factory
          some_field: value
          bindingVersion: 0.0.1
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            JMSServerBindings.model_validate(data["jms"])


class TestJMSChannelBindings:
    """Tests for JMSChannelBindings model."""

    @parametrize_with_cases("yaml_data", cases=[case_channel_binding_fifo_queue])
    def test_jms_channel_bindings_validation(self, yaml_data: str) -> None:
        """Test JMSChannelBindings model validation."""
        data = yaml.safe_load(yaml_data)
        jms_binding = JMSChannelBindings.model_validate(data["jms"])
        assert jms_binding is not None
        assert jms_binding.binding_version == "0.0.1"

    @parametrize_with_cases(
        "jms_binding,expected",
        cases=[
            case_jms_channel_binding_serialization_empty,
            case_jms_channel_binding_serialization_fifo_queue,
        ],
    )
    def test_jms_channel_bindings_serialization(
        self,
        jms_binding: JMSChannelBindings,
        expected: dict,
    ) -> None:
        """Test JMSChannelBindings serialization."""
        dumped = jms_binding.model_dump()
        assert dumped == expected

    def test_jms_channel_binding_all_fields_validation(self) -> None:
        """Test JMSChannelBindings with all fields validation."""
        yaml_data = """
        jms:
          destination: user-sign-up
          destinationType: fifo-queue
          bindingVersion: 0.0.1
        """
        data = yaml.safe_load(yaml_data)
        jms_binding = JMSChannelBindings.model_validate(data["jms"])

        assert jms_binding.destination == "user-sign-up"
        assert jms_binding.destination_type == "fifo-queue"
        assert jms_binding.binding_version == "0.0.1"

    def test_jms_channel_bindings_python_validation_error(self) -> None:
        """Test JMSChannelBindings Python validation error with extra arguments."""
        with pytest.raises(ValidationError):
            JMSChannelBindings(some_field="value")

    def test_jms_channel_bindings_yaml_validation_error(self) -> None:
        """Test JMSChannelBindings YAML validation error with extra fields."""
        yaml_data = """
        jms:
          some_field: value
          bindingVersion: 0.0.1
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            JMSChannelBindings.model_validate(data["jms"])


class TestJMSOperationBindings:
    """Tests for JMSOperationBindings model."""

    def test_jms_operation_bindings_serialization(self) -> None:
        """Test JMSOperationBindings serialization."""
        jms_binding = JMSOperationBindings()
        dumped = jms_binding.model_dump()
        assert dumped == {}

    def test_jms_operation_bindings_python_validation_error(self) -> None:
        """Test JMSOperationBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            JMSOperationBindings(some_field="value")

    def test_jms_operation_bindings_yaml_validation_error(self) -> None:
        """Test JMSOperationBindings YAML validation error with any fields."""
        yaml_data = """
        jms:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            JMSOperationBindings.model_validate(data["jms"])

    def test_jms_operation_bindings_yaml_empty_validation(self) -> None:
        """Test JMSOperationBindings YAML validation with no fields."""
        yaml_data = """
        jms: {}
        """
        data = yaml.safe_load(yaml_data)
        jms_binding = JMSOperationBindings.model_validate(data["jms"])
        assert jms_binding is not None


class TestJMSMessageBindings:
    """Tests for JMSMessageBindings model."""

    @parametrize_with_cases("yaml_data", cases=[case_message_binding_with_headers])
    def test_jms_message_bindings_validation(self, yaml_data: str) -> None:
        """Test JMSMessageBindings model validation."""
        data = yaml.safe_load(yaml_data)
        jms_binding = JMSMessageBindings.model_validate(data["jms"])
        assert jms_binding is not None
        assert jms_binding.binding_version == "0.0.1"

    @parametrize_with_cases(
        "jms_binding,expected",
        cases=[
            case_jms_message_binding_serialization_empty,
            case_jms_message_binding_serialization_with_headers,
        ],
    )
    def test_jms_message_bindings_serialization(
        self,
        jms_binding: JMSMessageBindings,
        expected: dict,
    ) -> None:
        """Test JMSMessageBindings serialization."""
        dumped = jms_binding.model_dump()
        assert dumped == expected

    def test_jms_message_binding_headers_schema_validation(self) -> None:
        """Test JMSMessageBindings with headers as Schema validation."""
        yaml_data = """
        jms:
          headers:
            type: object
            required:
              - JMSMessageID
            properties:
              JMSMessageID:
                name: JMSMessageID
                description: A unique message identifier.
                type: string
          bindingVersion: 0.0.1
        """
        data = yaml.safe_load(yaml_data)
        jms_binding = JMSMessageBindings.model_validate(data["jms"])

        assert jms_binding.headers is not None
        assert isinstance(jms_binding.headers, Schema)
        assert jms_binding.binding_version == "0.0.1"

    def test_jms_message_bindings_python_validation_error(self) -> None:
        """Test JMSMessageBindings Python validation error with extra arguments."""
        with pytest.raises(ValidationError):
            JMSMessageBindings(some_field="value")

    def test_jms_message_bindings_yaml_validation_error(self) -> None:
        """Test JMSMessageBindings YAML validation error with extra fields."""
        yaml_data = """
        jms:
          some_field: value
          bindingVersion: 0.0.1
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            JMSMessageBindings.model_validate(data["jms"])
