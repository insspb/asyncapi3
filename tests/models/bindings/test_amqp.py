"""Tests for AMQP bindings models."""

from typing import Any

import pytest
import yaml

from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.bindings.amqp import (
    AMQPChannelBindings,
    AMQPExchange,
    AMQPMessageBindings,
    AMQPOperationBindings,
    AMQPQueue,
    AMQPServerBindings,
)


# Channel Bindings Validation Test Cases
def case_channel_binding_routing_key() -> str:
    """Channel binding with routingKey and exchange."""
    return """
    amqp:
      is: routingKey
      exchange:
        name: myExchange
        type: topic
        durable: true
        autoDelete: false
        vhost: /
      bindingVersion: 0.3.0
    """


def case_channel_binding_queue() -> str:
    """Channel binding with queue."""
    return """
    amqp:
      is: queue
      queue:
        name: my-queue-name
        durable: true
        exclusive: true
        autoDelete: false
        vhost: /
      bindingVersion: 0.3.0
    """


# Channel Bindings Serialization Test Cases
def case_amqp_channel_binding_serialization_routing_key() -> tuple[
    AMQPChannelBindings, dict
]:
    """AMQPChannelBindings serialization with routingKey and exchange."""
    amqp_binding = AMQPChannelBindings(
        is_="routingKey",
        exchange=AMQPExchange(
            name="myExchange",
            type="topic",
            durable=True,
            auto_delete=False,
            vhost="/",
        ),
    )
    expected: dict[str, Any] = {
        "is": "routingKey",
        "exchange": {
            "name": "myExchange",
            "type": "topic",
            "durable": True,
            "autoDelete": False,
            "vhost": "/",
        },
        "bindingVersion": "0.3.0",
    }
    return amqp_binding, expected


def case_amqp_channel_binding_serialization_queue() -> tuple[AMQPChannelBindings, dict]:
    """AMQPChannelBindings serialization with queue."""
    amqp_binding = AMQPChannelBindings(
        is_="queue",
        queue=AMQPQueue(
            name="my-queue-name",
            durable=True,
            exclusive=True,
            auto_delete=False,
            vhost="/",
        ),
    )
    expected: dict[str, Any] = {
        "is": "queue",
        "queue": {
            "name": "my-queue-name",
            "durable": True,
            "exclusive": True,
            "autoDelete": False,
            "vhost": "/",
        },
        "bindingVersion": "0.3.0",
    }
    return amqp_binding, expected


# Operation Bindings Validation Test Cases
def case_operation_binding_full() -> str:
    """Operation binding with all fields."""
    return """
    amqp:
      expiration: 100000
      userId: guest
      cc: ['user.logs']
      priority: 10
      deliveryMode: 2
      mandatory: false
      bcc: ['external.audit']
      timestamp: true
      ack: false
      bindingVersion: 0.3.0
    """


# Operation Bindings Serialization Test Cases
def case_amqp_operation_binding_serialization_empty() -> tuple[
    AMQPOperationBindings, dict
]:
    """AMQPOperationBindings serialization empty."""
    amqp_binding = AMQPOperationBindings()
    expected: dict[str, Any] = {"bindingVersion": "0.3.0"}
    return amqp_binding, expected


def case_amqp_operation_binding_serialization_full() -> tuple[
    AMQPOperationBindings, dict
]:
    """AMQPOperationBindings serialization with all fields."""
    amqp_binding = AMQPOperationBindings(
        expiration=100000,
        user_id="guest",
        cc=["user.logs"],
        priority=10,
        delivery_mode=2,
        mandatory=False,
        bcc=["external.audit"],
        timestamp=True,
        ack=False,
    )
    expected: dict[str, Any] = {
        "expiration": 100000,
        "userId": "guest",
        "cc": ["user.logs"],
        "priority": 10,
        "deliveryMode": 2,
        "mandatory": False,
        "bcc": ["external.audit"],
        "timestamp": True,
        "ack": False,
        "bindingVersion": "0.3.0",
    }
    return amqp_binding, expected


# Message Bindings Validation Test Cases
def case_message_binding_full() -> str:
    """Message binding with all fields."""
    return """
    amqp:
      contentEncoding: gzip
      messageType: 'user.signup'
      bindingVersion: 0.3.0
    """


# Message Bindings Serialization Test Cases
def case_amqp_message_binding_serialization_empty() -> tuple[AMQPMessageBindings, dict]:
    """AMQPMessageBindings serialization empty."""
    amqp_binding = AMQPMessageBindings()
    expected: dict[str, Any] = {"bindingVersion": "0.3.0"}
    return amqp_binding, expected


def case_amqp_message_binding_serialization_full() -> tuple[AMQPMessageBindings, dict]:
    """AMQPMessageBindings serialization with all fields."""
    amqp_binding = AMQPMessageBindings(
        content_encoding="gzip",
        message_type="user.signup",
    )
    expected: dict[str, Any] = {
        "contentEncoding": "gzip",
        "messageType": "user.signup",
        "bindingVersion": "0.3.0",
    }
    return amqp_binding, expected


# Server Bindings Serialization Test Cases
def case_amqp_server_binding_serialization_empty() -> tuple[AMQPServerBindings, dict]:
    """AMQPServerBindings serialization empty."""
    amqp_binding = AMQPServerBindings()
    expected: dict[str, Any] = {}
    return amqp_binding, expected


class TestAMQPServerBindings:
    """Tests for AMQPServerBindings model."""

    def test_amqp_server_bindings_serialization(self) -> None:
        """Test AMQPServerBindings serialization."""
        amqp_binding = AMQPServerBindings()
        dumped = amqp_binding.model_dump()
        assert dumped == {}

    def test_amqp_server_bindings_python_validation_error(self) -> None:
        """Test AMQPServerBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            AMQPServerBindings(some_field="value")

    def test_amqp_server_bindings_yaml_validation_error(self) -> None:
        """Test AMQPServerBindings YAML validation error with any fields."""
        yaml_data = """
        amqp:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            AMQPServerBindings.model_validate(data["amqp"])

    def test_amqp_server_bindings_yaml_empty_validation(self) -> None:
        """Test AMQPServerBindings YAML validation with no fields."""
        yaml_data = """
        amqp: {}
        """
        data = yaml.safe_load(yaml_data)
        amqp_binding = AMQPServerBindings.model_validate(data["amqp"])
        assert amqp_binding is not None


class TestAMQPChannelBindings:
    """Tests for AMQPChannelBindings model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_channel_binding_routing_key, case_channel_binding_queue],
    )
    def test_amqp_channel_bindings_validation(self, yaml_data: str) -> None:
        """Test AMQPChannelBindings model validation."""
        data = yaml.safe_load(yaml_data)
        amqp_binding = AMQPChannelBindings.model_validate(data["amqp"])
        assert amqp_binding is not None
        assert amqp_binding.binding_version == "0.3.0"

    @parametrize_with_cases(
        "amqp_binding,expected",
        cases=[
            case_amqp_channel_binding_serialization_routing_key,
            case_amqp_channel_binding_serialization_queue,
        ],
    )
    def test_amqp_channel_bindings_serialization(
        self,
        amqp_binding: AMQPChannelBindings,
        expected: dict,
    ) -> None:
        """Test AMQPChannelBindings serialization."""
        dumped = amqp_binding.model_dump()
        assert dumped == expected

    def test_amqp_channel_binding_exchange_validation(self) -> None:
        """Test AMQPChannelBindings with exchange object validation."""
        yaml_data = """
        amqp:
          is: routingKey
          exchange:
            name: myExchange
            type: topic
            durable: true
            autoDelete: false
            vhost: /
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        amqp_binding = AMQPChannelBindings.model_validate(data["amqp"])

        assert amqp_binding.exchange is not None
        assert isinstance(amqp_binding.exchange, AMQPExchange)
        assert amqp_binding.exchange.name == "myExchange"
        assert amqp_binding.exchange.type == "topic"
        assert amqp_binding.exchange.durable is True
        assert amqp_binding.exchange.auto_delete is False
        assert amqp_binding.exchange.vhost == "/"
        assert amqp_binding.binding_version == "0.3.0"

    def test_amqp_channel_binding_queue_validation(self) -> None:
        """Test AMQPChannelBindings with queue object validation."""
        yaml_data = """
        amqp:
          is: queue
          queue:
            name: my-queue-name
            durable: true
            exclusive: true
            autoDelete: false
            vhost: /
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        amqp_binding = AMQPChannelBindings.model_validate(data["amqp"])

        assert amqp_binding.queue is not None
        assert isinstance(amqp_binding.queue, AMQPQueue)
        assert amqp_binding.queue.name == "my-queue-name"
        assert amqp_binding.queue.durable is True
        assert amqp_binding.queue.exclusive is True
        assert amqp_binding.queue.auto_delete is False
        assert amqp_binding.queue.vhost == "/"
        assert amqp_binding.binding_version == "0.3.0"

    def test_amqp_channel_bindings_python_validation_error(self) -> None:
        """Test AMQPChannelBindings Python validation error with invalid arguments."""
        with pytest.raises(ValidationError):
            AMQPChannelBindings(invalid_field="value")

    def test_amqp_channel_bindings_yaml_validation_error(self) -> None:
        """Test AMQPChannelBindings YAML validation error with invalid fields."""
        yaml_data = """
        amqp:
          is: routingKey
          exchange:
            name: myExchange
            type: topic
          invalid_field: value
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            AMQPChannelBindings.model_validate(data["amqp"])


# Validation error test cases for AMQPChannelBindings validator
def case_amqp_channel_binding_validator_routing_key_without_exchange() -> tuple[
    str, str
]:
    """RoutingKey without exchange - should fail validation."""
    yaml_data = """
    amqp:
      is: routingKey
      bindingVersion: 0.3.0
    """
    expected_error = "exchange must be provided when is='routingKey'"
    return yaml_data, expected_error


def case_amqp_channel_binding_validator_routing_key_with_queue() -> tuple[str, str]:
    """RoutingKey with queue - should fail validation."""
    yaml_data = """
    amqp:
      is: routingKey
      exchange:
        name: myExchange
        type: topic
      queue:
        name: myQueue
      bindingVersion: 0.3.0
    """
    expected_error = "queue must not be provided when is='routingKey'"
    return yaml_data, expected_error


def case_amqp_channel_binding_validator_queue_without_queue() -> tuple[str, str]:
    """Queue binding without queue - should fail validation."""
    yaml_data = """
    amqp:
      is: queue
      bindingVersion: 0.3.0
    """
    expected_error = "queue must be provided when is='queue'"
    return yaml_data, expected_error


def case_amqp_channel_binding_validator_queue_with_exchange() -> tuple[str, str]:
    """Queue binding with exchange - should fail validation."""
    yaml_data = """
    amqp:
      is: queue
      queue:
        name: myQueue
      exchange:
        name: myExchange
        type: topic
      bindingVersion: 0.3.0
    """
    expected_error = "exchange must not be provided when is='queue'"
    return yaml_data, expected_error


class TestAMQPChannelBindingsValidator:
    """Tests for AMQPChannelBindings model validator."""

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_amqp_channel_binding_validator_routing_key_without_exchange,
            case_amqp_channel_binding_validator_routing_key_with_queue,
            case_amqp_channel_binding_validator_queue_without_queue,
            case_amqp_channel_binding_validator_queue_with_exchange,
        ],
    )
    def test_amqp_channel_bindings_validator_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test AMQPChannelBindings validator errors for invalid field combinations."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValueError, match=expected_error):
            AMQPChannelBindings.model_validate(data["amqp"])


class TestAMQPOperationBindings:
    """Tests for AMQPOperationBindings model."""

    @parametrize_with_cases("yaml_data", cases=[case_operation_binding_full])
    def test_amqp_operation_bindings_validation(self, yaml_data: str) -> None:
        """Test AMQPOperationBindings model validation."""
        data = yaml.safe_load(yaml_data)
        amqp_binding = AMQPOperationBindings.model_validate(data["amqp"])
        assert amqp_binding is not None
        assert amqp_binding.binding_version == "0.3.0"

    def test_amqp_operation_binding_expiration_negative_validation_error(self) -> None:
        """Test AMQPOperationBindings validation error for negative expiration."""
        yaml_data = """
        amqp:
          expiration: -100
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(
            ValidationError, match="expiration must be greater than or equal to zero"
        ):
            AMQPOperationBindings.model_validate(data["amqp"])

    @parametrize_with_cases(
        "amqp_binding,expected",
        cases=[
            case_amqp_operation_binding_serialization_empty,
            case_amqp_operation_binding_serialization_full,
        ],
    )
    def test_amqp_operation_bindings_serialization(
        self,
        amqp_binding: AMQPOperationBindings,
        expected: dict,
    ) -> None:
        """Test AMQPOperationBindings serialization."""
        dumped = amqp_binding.model_dump()
        assert dumped == expected

    def test_amqp_operation_binding_all_fields_validation(self) -> None:
        """Test AMQPOperationBindings with all fields validation."""
        yaml_data = """
        amqp:
          expiration: 100000
          userId: guest
          cc: ['user.logs']
          priority: 10
          deliveryMode: 2
          mandatory: false
          bcc: ['external.audit']
          timestamp: true
          ack: false
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        amqp_binding = AMQPOperationBindings.model_validate(data["amqp"])

        assert amqp_binding.expiration == 100000
        assert amqp_binding.user_id == "guest"
        assert amqp_binding.cc == ["user.logs"]
        assert amqp_binding.priority == 10
        assert amqp_binding.delivery_mode == 2
        assert amqp_binding.mandatory is False
        assert amqp_binding.bcc == ["external.audit"]
        assert amqp_binding.timestamp is True
        assert amqp_binding.ack is False
        assert amqp_binding.binding_version == "0.3.0"

    def test_amqp_operation_bindings_python_validation_error(self) -> None:
        """Test AMQPOperationBindings Python validation error with invalid arguments."""
        with pytest.raises(ValidationError):
            AMQPOperationBindings(invalid_field="value")

    def test_amqp_operation_bindings_yaml_validation_error(self) -> None:
        """Test AMQPOperationBindings YAML validation error with invalid fields."""
        yaml_data = """
        amqp:
          expiration: 100000
          invalid_field: value
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            AMQPOperationBindings.model_validate(data["amqp"])


class TestAMQPMessageBindings:
    """Tests for AMQPMessageBindings model."""

    @parametrize_with_cases("yaml_data", cases=[case_message_binding_full])
    def test_amqp_message_bindings_validation(self, yaml_data: str) -> None:
        """Test AMQPMessageBindings model validation."""
        data = yaml.safe_load(yaml_data)
        amqp_binding = AMQPMessageBindings.model_validate(data["amqp"])
        assert amqp_binding is not None
        assert amqp_binding.binding_version == "0.3.0"

    @parametrize_with_cases(
        "amqp_binding,expected",
        cases=[
            case_amqp_message_binding_serialization_empty,
            case_amqp_message_binding_serialization_full,
        ],
    )
    def test_amqp_message_bindings_serialization(
        self,
        amqp_binding: AMQPMessageBindings,
        expected: dict,
    ) -> None:
        """Test AMQPMessageBindings serialization."""
        dumped = amqp_binding.model_dump()
        assert dumped == expected

    def test_amqp_message_binding_all_fields_validation(self) -> None:
        """Test AMQPMessageBindings with all fields validation."""
        yaml_data = """
        amqp:
          contentEncoding: gzip
          messageType: 'user.signup'
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        amqp_binding = AMQPMessageBindings.model_validate(data["amqp"])

        assert amqp_binding.content_encoding == "gzip"
        assert amqp_binding.message_type == "user.signup"
        assert amqp_binding.binding_version == "0.3.0"

    def test_amqp_message_bindings_python_validation_error(self) -> None:
        """Test AMQPMessageBindings Python validation error with invalid arguments."""
        with pytest.raises(ValidationError):
            AMQPMessageBindings(invalid_field="value")

    def test_amqp_message_bindings_yaml_validation_error(self) -> None:
        """Test AMQPMessageBindings YAML validation error with invalid fields."""
        yaml_data = """
        amqp:
          contentEncoding: gzip
          invalid_field: value
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            AMQPMessageBindings.model_validate(data["amqp"])
