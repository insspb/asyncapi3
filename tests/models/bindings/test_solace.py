"""Tests for Solace bindings models."""

from typing import Any

import yaml

from pytest_cases import parametrize_with_cases

from asyncapi3.models.bindings.solace import (
    SolaceChannelBindings,
    SolaceDestination,
    SolaceMessageBindings,
    SolaceOperationBindings,
    SolaceQueue,
    SolaceServerBindings,
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


# Channel Bindings Serialization Test Cases
def case_solace_channel_binding_serialization_empty() -> tuple[
    SolaceChannelBindings, dict
]:
    """SolaceChannelBindings serialization empty."""
    solace_binding = SolaceChannelBindings()
    expected: dict[str, Any] = {}
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


# Message Bindings Serialization Test Cases
def case_solace_message_binding_serialization_empty() -> tuple[
    SolaceMessageBindings, dict
]:
    """SolaceMessageBindings serialization empty."""
    solace_binding = SolaceMessageBindings()
    expected: dict[str, Any] = {}
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


class TestSolaceChannelBindings:
    """Tests for SolaceChannelBindings model."""

    @parametrize_with_cases(
        "solace_binding,expected",
        cases=[case_solace_channel_binding_serialization_empty],
    )
    def test_solace_channel_bindings_serialization(
        self,
        solace_binding: SolaceChannelBindings,
        expected: dict,
    ) -> None:
        """Test SolaceChannelBindings serialization."""
        dumped = solace_binding.model_dump()
        assert dumped == expected


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


class TestSolaceMessageBindings:
    """Tests for SolaceMessageBindings model."""

    @parametrize_with_cases(
        "solace_binding,expected",
        cases=[case_solace_message_binding_serialization_empty],
    )
    def test_solace_message_bindings_serialization(
        self,
        solace_binding: SolaceMessageBindings,
        expected: dict,
    ) -> None:
        """Test SolaceMessageBindings serialization."""
        dumped = solace_binding.model_dump()
        assert dumped == expected
