"""Tests for Pulsar bindings models."""

from typing import Any

import pytest
import yaml

from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.bindings.pulsar import (
    PulsarChannelBindings,
    PulsarMessageBindings,
    PulsarOperationBindings,
    PulsarRetention,
    PulsarServerBindings,
)


# Server Bindings Validation Test Cases
def case_server_binding_with_tenant() -> str:
    """Server binding with tenant."""
    return """
    pulsar:
      tenant: contoso
      bindingVersion: 0.1.0
    """


# Server Bindings Serialization Test Cases
def case_pulsar_server_binding_serialization_default() -> tuple[
    PulsarServerBindings, dict
]:
    """PulsarServerBindings serialization with default tenant."""
    pulsar_binding = PulsarServerBindings()
    expected: dict[str, Any] = {
        "tenant": "public",
        "bindingVersion": "0.1.0",
    }
    return pulsar_binding, expected


def case_pulsar_server_binding_serialization_with_tenant() -> tuple[
    PulsarServerBindings, dict
]:
    """PulsarServerBindings serialization with tenant."""
    pulsar_binding = PulsarServerBindings(tenant="contoso")
    expected: dict[str, Any] = {
        "tenant": "contoso",
        "bindingVersion": "0.1.0",
    }
    return pulsar_binding, expected


# Retention Serialization Test Cases
def case_pulsar_retention_serialization_empty() -> tuple[PulsarRetention, dict]:
    """PulsarRetention serialization empty."""
    retention = PulsarRetention()
    expected: dict[str, Any] = {
        "time": 0,
        "size": 0,
    }
    return retention, expected


def case_pulsar_retention_serialization_full() -> tuple[PulsarRetention, dict]:
    """PulsarRetention serialization with all fields."""
    retention = PulsarRetention(time=7, size=1000)
    expected: dict[str, Any] = {
        "time": 7,
        "size": 1000,
    }
    return retention, expected


# Channel Bindings Serialization Test Cases
def case_pulsar_channel_binding_serialization_minimal() -> tuple[
    PulsarChannelBindings, dict
]:
    """PulsarChannelBindings serialization with required fields only."""
    pulsar_binding = PulsarChannelBindings(
        namespace="staging",
        persistence="persistent",
    )
    expected: dict[str, Any] = {
        "namespace": "staging",
        "persistence": "persistent",
        "bindingVersion": "0.1.0",
    }
    return pulsar_binding, expected


def case_pulsar_channel_binding_serialization_full() -> tuple[
    PulsarChannelBindings, dict
]:
    """PulsarChannelBindings serialization with all fields."""
    pulsar_binding = PulsarChannelBindings(
        namespace="staging",
        persistence="persistent",
        compaction=1000,
        geo_replication=["us-east1", "us-west1"],
        retention=PulsarRetention(time=7, size=1000),
        ttl=360,
        deduplication=False,
    )
    expected: dict[str, Any] = {
        "namespace": "staging",
        "persistence": "persistent",
        "compaction": 1000,
        "geo-replication": ["us-east1", "us-west1"],
        "retention": {
            "time": 7,
            "size": 1000,
        },
        "ttl": 360,
        "deduplication": False,
        "bindingVersion": "0.1.0",
    }
    return pulsar_binding, expected


class TestPulsarServerBindings:
    """Tests for PulsarServerBindings model."""

    @parametrize_with_cases("yaml_data", cases=[case_server_binding_with_tenant])
    def test_pulsar_server_bindings_validation(self, yaml_data: str) -> None:
        """Test PulsarServerBindings model validation."""
        data = yaml.safe_load(yaml_data)
        pulsar_binding = PulsarServerBindings.model_validate(data["pulsar"])

        # Verify all fields
        assert pulsar_binding.tenant == "contoso"
        assert pulsar_binding.binding_version == "0.1.0"

    def test_pulsar_server_bindings_validation_error_extra_fields(self) -> None:
        """Test PulsarServerBindings validation error with extra fields."""
        yaml_data = """
        pulsar:
          tenant: contoso
          bindingVersion: 0.1.0
          extra_field: invalid
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            PulsarServerBindings.model_validate(data["pulsar"])

    @parametrize_with_cases(
        "pulsar_binding,expected",
        cases=[
            case_pulsar_server_binding_serialization_default,
            case_pulsar_server_binding_serialization_with_tenant,
        ],
    )
    def test_pulsar_server_bindings_serialization(
        self,
        pulsar_binding: PulsarServerBindings,
        expected: dict,
    ) -> None:
        """Test PulsarServerBindings serialization."""
        dumped = pulsar_binding.model_dump()
        assert dumped == expected


class TestPulsarRetention:
    """Tests for PulsarRetention model."""

    @parametrize_with_cases(
        "retention,expected",
        cases=[
            case_pulsar_retention_serialization_empty,
            case_pulsar_retention_serialization_full,
        ],
    )
    def test_pulsar_retention_serialization(
        self,
        retention: PulsarRetention,
        expected: dict,
    ) -> None:
        """Test PulsarRetention serialization."""
        dumped = retention.model_dump()
        assert dumped == expected

    def test_pulsar_retention_full_validation(self) -> None:
        """Test PulsarRetention with all fields validation."""
        yaml_data = """
        time: 7
        size: 1000
        """
        data = yaml.safe_load(yaml_data)
        retention = PulsarRetention.model_validate(data)

        assert retention.time == 7
        assert retention.size == 1000

    def test_pulsar_retention_validation_error_extra_fields(self) -> None:
        """Test PulsarRetention validation error with extra fields."""
        yaml_data = """
        time: 7
        size: 1000
        extra_field: invalid
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            PulsarRetention.model_validate(data)


class TestPulsarChannelBindings:
    """Tests for PulsarChannelBindings model."""

    def test_pulsar_channel_binding_minimal_validation(self) -> None:
        """Test PulsarChannelBindings with minimal fields validation."""
        yaml_data = """
        pulsar:
          namespace: staging
          persistence: persistent
          bindingVersion: 0.1.0
        """
        data = yaml.safe_load(yaml_data)
        pulsar_binding = PulsarChannelBindings.model_validate(data["pulsar"])

        # Verify all fields
        assert pulsar_binding.namespace == "staging"
        assert pulsar_binding.persistence == "persistent"
        assert pulsar_binding.binding_version == "0.1.0"

    def test_pulsar_channel_binding_full_validation(self) -> None:
        """Test PulsarChannelBindings with all fields validation."""
        yaml_data = """
        pulsar:
          namespace: staging
          persistence: persistent
          compaction: 1000
          geo-replication:
            - us-east1
            - us-west1
          retention:
            time: 7
            size: 1000
          ttl: 360
          deduplication: false
          bindingVersion: 0.1.0
        """
        data = yaml.safe_load(yaml_data)
        pulsar_binding = PulsarChannelBindings.model_validate(data["pulsar"])

        # Verify all fields
        assert pulsar_binding.namespace == "staging"
        assert pulsar_binding.persistence == "persistent"
        assert pulsar_binding.compaction == 1000
        assert pulsar_binding.geo_replication == ["us-east1", "us-west1"]
        assert pulsar_binding.retention is not None
        assert isinstance(pulsar_binding.retention, PulsarRetention)
        assert pulsar_binding.retention.time == 7
        assert pulsar_binding.retention.size == 1000
        assert pulsar_binding.ttl == 360
        assert pulsar_binding.deduplication is False
        assert pulsar_binding.binding_version == "0.1.0"

    def test_pulsar_channel_bindings_validation_error_extra_fields(self) -> None:
        """Test PulsarChannelBindings validation error with extra fields."""
        yaml_data = """
        pulsar:
          namespace: staging
          persistence: persistent
          bindingVersion: 0.1.0
          extra_field: invalid
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            PulsarChannelBindings.model_validate(data["pulsar"])

    def test_pulsar_channel_bindings_validation_error_invalid_persistence(self) -> None:
        """Test PulsarChannelBindings validation error with invalid persistence value."""
        yaml_data = """
        pulsar:
          namespace: staging
          persistence: invalid_value
          bindingVersion: 0.1.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            PulsarChannelBindings.model_validate(data["pulsar"])

    @parametrize_with_cases(
        "pulsar_binding,expected",
        cases=[
            case_pulsar_channel_binding_serialization_minimal,
            case_pulsar_channel_binding_serialization_full,
        ],
    )
    def test_pulsar_channel_bindings_serialization(
        self,
        pulsar_binding: PulsarChannelBindings,
        expected: dict,
    ) -> None:
        """Test PulsarChannelBindings serialization."""
        dumped = pulsar_binding.model_dump()
        assert dumped == expected


class TestPulsarOperationBindings:
    """Tests for PulsarOperationBindings model."""

    def test_pulsar_operation_bindings_serialization(self) -> None:
        """Test PulsarOperationBindings serialization."""
        pulsar_binding = PulsarOperationBindings()
        dumped = pulsar_binding.model_dump()
        assert dumped == {}

    def test_pulsar_operation_bindings_python_validation_error(self) -> None:
        """Test PulsarOperationBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            PulsarOperationBindings(some_field="value")

    def test_pulsar_operation_bindings_yaml_validation_error(self) -> None:
        """Test PulsarOperationBindings YAML validation error with any fields."""
        yaml_data = """
        pulsar:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            PulsarOperationBindings.model_validate(data["pulsar"])

    def test_pulsar_operation_bindings_yaml_empty_validation(self) -> None:
        """Test PulsarOperationBindings YAML validation with no fields."""
        yaml_data = """
        pulsar: {}
        """
        data = yaml.safe_load(yaml_data)
        pulsar_binding = PulsarOperationBindings.model_validate(data["pulsar"])
        assert pulsar_binding is not None


class TestPulsarMessageBindings:
    """Tests for PulsarMessageBindings model."""

    def test_pulsar_message_bindings_serialization(self) -> None:
        """Test PulsarMessageBindings serialization."""
        pulsar_binding = PulsarMessageBindings()
        dumped = pulsar_binding.model_dump()
        assert dumped == {}

    def test_pulsar_message_bindings_python_validation_error(self) -> None:
        """Test PulsarMessageBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            PulsarMessageBindings(some_field="value")

    def test_pulsar_message_bindings_yaml_validation_error(self) -> None:
        """Test PulsarMessageBindings YAML validation error with any fields."""
        yaml_data = """
        pulsar:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            PulsarMessageBindings.model_validate(data["pulsar"])

    def test_pulsar_message_bindings_yaml_empty_validation(self) -> None:
        """Test PulsarMessageBindings YAML validation with no fields."""
        yaml_data = """
        pulsar: {}
        """
        data = yaml.safe_load(yaml_data)
        pulsar_binding = PulsarMessageBindings.model_validate(data["pulsar"])
        assert pulsar_binding is not None
