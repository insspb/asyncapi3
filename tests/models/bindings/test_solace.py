"""Tests for Solace bindings models."""

from typing import Any

import pytest
import yaml

from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.bindings.solace import (
    SolaceChannelBindings,
    SolaceDestination,
    SolaceMessageBindings,
    SolaceOperationBindings,
    SolaceQueue,
    SolaceServerBindings,
    SolaceTopic,
)


# Server Bindings Validation Test Cases
def case_server_binding_with_vpn() -> str:
    """Server binding with msgVpn."""
    return """
    solace:
      msgVpn: my-vpn
      clientName: my-client
      bindingVersion: 0.4.0
    """


# Server Bindings Serialization Test Cases
def case_solace_server_binding_serialization_empty() -> tuple[
    SolaceServerBindings, dict
]:
    """SolaceServerBindings serialization empty."""
    solace_binding = SolaceServerBindings()
    expected: dict[str, Any] = {"bindingVersion": "0.4.0"}
    return solace_binding, expected


def case_solace_server_binding_serialization_with_vpn() -> tuple[
    SolaceServerBindings, dict
]:
    """SolaceServerBindings serialization with msgVpn."""
    solace_binding = SolaceServerBindings(
        msg_vpn="my-vpn",
        client_name="my-client",
    )
    expected: dict[str, Any] = {
        "msgVpn": "my-vpn",
        "clientName": "my-client",
        "bindingVersion": "0.4.0",
    }
    return solace_binding, expected


# Operation Bindings Validation Test Cases
def case_operation_binding_with_destinations() -> str:
    """Operation binding with destinations."""
    return """
    solace:
      destinations:
        - destinationType: queue
          queue:
            name: CreatedHREvents
            topicSubscriptions:
              - person/*/created
      timeToLive: 5000
      priority: 120
      dmqEligible: true
      bindingVersion: 0.4.0
    """


# Operation Bindings Serialization Test Cases
def case_solace_operation_binding_serialization_empty() -> tuple[
    SolaceOperationBindings, dict
]:
    """SolaceOperationBindings serialization empty."""
    solace_binding = SolaceOperationBindings()
    expected: dict[str, Any] = {"bindingVersion": "0.4.0"}
    return solace_binding, expected


def case_solace_operation_binding_serialization_with_destinations() -> tuple[
    SolaceOperationBindings, dict
]:
    """SolaceOperationBindings serialization with destinations."""
    solace_binding = SolaceOperationBindings(
        destinations=[
            SolaceDestination(
                destination_type="queue",
                queue=SolaceQueue(
                    name="CreatedHREvents",
                    topic_subscriptions=["person/*/created"],
                ),
            ),
        ],
        time_to_live=5000,
        priority=120,
        dmq_eligible=True,
    )
    expected: dict[str, Any] = {
        "destinations": [
            {
                "deliveryMode": "persistent",
                "destinationType": "queue",
                "queue": {
                    "name": "CreatedHREvents",
                    "topicSubscriptions": ["person/*/created"],
                },
                "bindingVersion": "0.4.0",
            },
        ],
        "timeToLive": 5000,
        "priority": 120,
        "dmqEligible": True,
        "bindingVersion": "0.4.0",
    }
    return solace_binding, expected


class TestSolaceServerBindings:
    """Tests for SolaceServerBindings model."""

    @parametrize_with_cases("yaml_data", cases=[case_server_binding_with_vpn])
    def test_solace_server_bindings_validation(self, yaml_data: str) -> None:
        """Test SolaceServerBindings model validation."""
        data = yaml.safe_load(yaml_data)
        solace_binding = SolaceServerBindings.model_validate(data["solace"])
        assert solace_binding is not None
        assert solace_binding.binding_version == "0.4.0"

    @parametrize_with_cases(
        "solace_binding,expected",
        cases=[
            case_solace_server_binding_serialization_empty,
            case_solace_server_binding_serialization_with_vpn,
        ],
    )
    def test_solace_server_bindings_serialization(
        self,
        solace_binding: SolaceServerBindings,
        expected: dict,
    ) -> None:
        """Test SolaceServerBindings serialization."""
        dumped = solace_binding.model_dump()
        assert dumped == expected

    def test_solace_server_bindings_client_name_too_long(self) -> None:
        """Test SolaceServerBindings validation error when clientName is too long."""
        # Create a client name that exceeds 160 bytes
        long_client_name = "a" * 161  # 161 characters
        with pytest.raises(ValidationError):
            SolaceServerBindings(client_name=long_client_name)

    def test_solace_server_bindings_client_name_max_length(self) -> None:
        """Test SolaceServerBindings validation with clientName at max length."""
        # Create a client name exactly at max length (160 bytes)
        max_client_name = "a" * 160
        solace_binding = SolaceServerBindings(client_name=max_client_name)
        assert solace_binding.client_name == max_client_name

    def test_solace_server_bindings_empty_creation(self) -> None:
        """Test SolaceServerBindings creation with empty object."""
        solace_binding = SolaceServerBindings()
        assert solace_binding.binding_version == "0.4.0"
        assert solace_binding.msg_vpn is None
        assert solace_binding.client_name is None

    def test_solace_server_bindings_python_extra_fields_error(self) -> None:
        """Test SolaceServerBindings Python validation error with extra fields."""
        with pytest.raises(ValidationError):
            SolaceServerBindings(extra_field="value")

    def test_solace_server_bindings_yaml_extra_fields_error(self) -> None:
        """Test SolaceServerBindings YAML validation error with extra fields."""
        yaml_data = """
        solace:
          msgVpn: my-vpn
          extraField: value
          bindingVersion: 0.4.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            SolaceServerBindings.model_validate(data["solace"])


class TestSolaceChannelBindings:
    """Tests for SolaceChannelBindings model."""

    def test_solace_channel_bindings_serialization_empty(self) -> None:
        """Test SolaceChannelBindings serialization."""
        solace_binding = SolaceChannelBindings()
        dumped = solace_binding.model_dump()
        assert dumped == {}

    def test_solace_channel_bindings_python_validation_error(self) -> None:
        """Test SolaceChannelBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            SolaceChannelBindings(some_field="value")

    def test_solace_channel_bindings_yaml_validation_error(self) -> None:
        """Test SolaceChannelBindings YAML validation error with any fields."""
        yaml_data = """
        solace:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            SolaceChannelBindings.model_validate(data["solace"])

    def test_solace_channel_bindings_yaml_empty_validation(self) -> None:
        """Test SolaceChannelBindings YAML validation with no fields."""
        yaml_data = """
        solace: {}
        """
        data = yaml.safe_load(yaml_data)
        solace_binding = SolaceChannelBindings.model_validate(data["solace"])
        assert solace_binding is not None


class TestSolaceOperationBindings:
    """Tests for SolaceOperationBindings model."""

    @parametrize_with_cases(
        "yaml_data", cases=[case_operation_binding_with_destinations]
    )
    def test_solace_operation_bindings_validation(self, yaml_data: str) -> None:
        """Test SolaceOperationBindings model validation."""
        data = yaml.safe_load(yaml_data)
        solace_binding = SolaceOperationBindings.model_validate(data["solace"])
        assert solace_binding is not None
        assert solace_binding.binding_version == "0.4.0"

    @parametrize_with_cases(
        "solace_binding,expected",
        cases=[
            case_solace_operation_binding_serialization_empty,
            case_solace_operation_binding_serialization_with_destinations,
        ],
    )
    def test_solace_operation_bindings_serialization(
        self,
        solace_binding: SolaceOperationBindings,
        expected: dict,
    ) -> None:
        """Test SolaceOperationBindings serialization."""
        dumped = solace_binding.model_dump()
        assert dumped == expected

    def test_solace_operation_binding_destinations_validation(self) -> None:
        """Test SolaceOperationBindings with destinations validation."""
        yaml_data = """
        solace:
          destinations:
            - destinationType: queue
              queue:
                name: CreatedHREvents
                topicSubscriptions:
                  - person/*/created
          bindingVersion: 0.4.0
        """
        data = yaml.safe_load(yaml_data)
        solace_binding = SolaceOperationBindings.model_validate(data["solace"])

        assert solace_binding.destinations is not None
        assert len(solace_binding.destinations) == 1
        assert isinstance(solace_binding.destinations[0], SolaceDestination)
        assert solace_binding.destinations[0].destination_type == "queue"
        assert solace_binding.binding_version == "0.4.0"

    def test_solace_operation_bindings_priority_too_low(self) -> None:
        """Test SolaceOperationBindings validation error when priority is too low."""
        with pytest.raises(ValidationError):
            SolaceOperationBindings(priority=-1)

    def test_solace_operation_bindings_priority_too_high(self) -> None:
        """Test SolaceOperationBindings validation error when priority is too high."""
        with pytest.raises(ValidationError):
            SolaceOperationBindings(priority=256)

    @pytest.mark.parametrize(
        ("priority_value", "expected_value"),
        [
            (0, 0),
            (255, 255),
            (120, 120),
        ],
        ids=[
            "solace_operation_bindings_priority_min",
            "solace_operation_bindings_priority_max",
            "solace_operation_bindings_priority_middle",
        ],
    )
    def test_solace_operation_bindings_priority_valid_range(
        self,
        priority_value: int,
        expected_value: int,
    ) -> None:
        """Test SolaceOperationBindings validation with priority in valid range."""
        solace_binding = SolaceOperationBindings(priority=priority_value)
        assert solace_binding.priority == expected_value

    def test_solace_operation_bindings_empty_creation(self) -> None:
        """Test SolaceOperationBindings creation with empty object."""
        solace_binding = SolaceOperationBindings()
        assert solace_binding.binding_version == "0.4.0"
        assert solace_binding.destinations is None
        assert solace_binding.time_to_live is None
        assert solace_binding.priority is None
        assert solace_binding.dmq_eligible is None

    def test_solace_operation_bindings_python_extra_fields_error(self) -> None:
        """Test SolaceOperationBindings Python validation error with extra fields."""
        with pytest.raises(ValidationError):
            SolaceOperationBindings(extra_field="value")

    def test_solace_operation_bindings_yaml_extra_fields_error(self) -> None:
        """Test SolaceOperationBindings YAML validation error with extra fields."""
        yaml_data = """
        solace:
          destinations: []
          extraField: value
          bindingVersion: 0.4.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            SolaceOperationBindings.model_validate(data["solace"])


class TestSolaceMessageBindings:
    """Tests for SolaceMessageBindings model."""

    def test_solace_message_bindings_serialization_empty(self) -> None:
        """Test SolaceMessageBindings serialization."""
        solace_binding = SolaceMessageBindings()
        dumped = solace_binding.model_dump()
        assert dumped == {}

    def test_solace_message_bindings_python_validation_error(self) -> None:
        """Test SolaceMessageBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            SolaceMessageBindings(some_field="value")

    def test_solace_message_bindings_yaml_validation_error(self) -> None:
        """Test SolaceMessageBindings YAML validation error with any fields."""
        yaml_data = """
        solace:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            SolaceMessageBindings.model_validate(data["solace"])

    def test_solace_message_bindings_yaml_empty_validation(self) -> None:
        """Test SolaceMessageBindings YAML validation with no fields."""
        yaml_data = """
        solace: {}
        """
        data = yaml.safe_load(yaml_data)
        solace_binding = SolaceMessageBindings.model_validate(data["solace"])
        assert solace_binding is not None


class TestSolaceDestination:
    """Tests for SolaceDestination model."""

    def test_solace_destination_queue_validation_success(self) -> None:
        """Test SolaceDestination validation with queue type."""
        destination = SolaceDestination(
            destination_type="queue", queue=SolaceQueue(name="test_queue")
        )
        assert destination.destination_type == "queue"
        assert destination.queue is not None
        assert destination.topic is None

    def test_solace_destination_topic_validation_success(self) -> None:
        """Test SolaceDestination validation with topic type."""
        destination = SolaceDestination(
            destination_type="topic",
            topic=SolaceTopic(topic_subscriptions=["test/topic"]),
        )
        assert destination.destination_type == "topic"
        assert destination.topic is not None
        assert destination.queue is None

    def test_solace_destination_queue_missing_queue_error(self) -> None:
        """Test SolaceDestination validation error when queue type but no queue provided."""
        with pytest.raises(
            ValueError, match="queue required for destinationType 'queue'"
        ):
            SolaceDestination(destination_type="queue")

    def test_solace_destination_topic_missing_topic_error(self) -> None:
        """Test SolaceDestination validation error when topic type but no topic provided."""
        with pytest.raises(
            ValueError, match="topic required for destinationType 'topic'"
        ):
            SolaceDestination(destination_type="topic")

    def test_solace_destination_queue_with_topic_error(self) -> None:
        """Test SolaceDestination validation error when queue type but topic also provided."""
        with pytest.raises(
            ValueError, match="topic not allowed for destinationType 'queue'"
        ):
            SolaceDestination(
                destination_type="queue",
                queue=SolaceQueue(name="test_queue"),
                topic=SolaceTopic(topic_subscriptions=["test/topic"]),
            )

    def test_solace_destination_topic_with_queue_error(self) -> None:
        """Test SolaceDestination validation error when topic type but queue also provided."""
        with pytest.raises(
            ValueError, match="queue not allowed for destinationType 'topic'"
        ):
            SolaceDestination(
                destination_type="topic",
                topic=SolaceTopic(topic_subscriptions=["test/topic"]),
                queue=SolaceQueue(name="test_queue"),
            )


class TestSolaceTopic:
    """Tests for SolaceTopic model."""

    def test_solace_topic_empty_validation(self) -> None:
        """Test SolaceTopic validation with no topic subscriptions."""
        topic = SolaceTopic()
        assert topic.topic_subscriptions is None

    def test_solace_topic_with_subscriptions_validation(self) -> None:
        """Test SolaceTopic validation with topic subscriptions."""
        subscriptions = ["topic1", "topic2"]
        topic = SolaceTopic(topic_subscriptions=subscriptions)
        assert topic.topic_subscriptions == subscriptions

    def test_solace_topic_serialization_empty(self) -> None:
        """Test SolaceTopic serialization with empty object."""
        topic = SolaceTopic()
        dumped = topic.model_dump()
        assert dumped == {}

    def test_solace_topic_serialization_with_subscriptions(self) -> None:
        """Test SolaceTopic serialization with subscriptions."""
        subscriptions = ["topic1", "topic2"]
        topic = SolaceTopic(topic_subscriptions=subscriptions)
        dumped = topic.model_dump()
        expected = {"topicSubscriptions": subscriptions}
        assert dumped == expected
