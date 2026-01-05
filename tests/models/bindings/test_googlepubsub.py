"""Tests for GooglePubSub bindings models."""

from typing import Any

import pytest
import yaml

from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.bindings.googlepubsub import (
    GooglePubSubChannelBindings,
    GooglePubSubMessageBindings,
    GooglePubSubMessageStoragePolicy,
    GooglePubSubOperationBindings,
    GooglePubSubSchemaDefinition,
    GooglePubSubSchemaSettings,
    GooglePubSubServerBindings,
)


# Channel Bindings Serialization Test Cases
def case_googlepubsub_channel_binding_serialization_empty() -> tuple[
    GooglePubSubChannelBindings, dict
]:
    """GooglePubSubChannelBindings serialization empty."""
    gps_binding = GooglePubSubChannelBindings()
    expected: dict[str, Any] = {"bindingVersion": "0.2.0"}
    return gps_binding, expected


def case_googlepubsub_channel_binding_serialization_with_schema_settings() -> tuple[
    GooglePubSubChannelBindings, dict
]:
    """GooglePubSubChannelBindings serialization with schemaSettings."""
    gps_binding = GooglePubSubChannelBindings(
        schema_settings=GooglePubSubSchemaSettings(
            encoding="JSON",
            name="projects/your-project/schemas/message-avro",
        ),
    )
    expected: dict[str, Any] = {
        "schemaSettings": {
            "encoding": "JSON",
            "name": "projects/your-project/schemas/message-avro",
        },
        "bindingVersion": "0.2.0",
    }
    return gps_binding, expected


def case_googlepubsub_channel_binding_serialization_full() -> tuple[
    GooglePubSubChannelBindings, dict
]:
    """GooglePubSubChannelBindings serialization with all fields."""
    gps_binding = GooglePubSubChannelBindings(
        message_retention_duration="86400s",
        message_storage_policy=GooglePubSubMessageStoragePolicy(
            allowed_persistence_regions=["us-central1", "us-central2"],
        ),
        schema_settings=GooglePubSubSchemaSettings(
            encoding="BINARY",
            name="projects/your-project/schemas/message-proto",
        ),
    )
    expected: dict[str, Any] = {
        "messageRetentionDuration": "86400s",
        "messageStoragePolicy": {
            "allowedPersistenceRegions": ["us-central1", "us-central2"],
        },
        "schemaSettings": {
            "encoding": "BINARY",
            "name": "projects/your-project/schemas/message-proto",
        },
        "bindingVersion": "0.2.0",
    }
    return gps_binding, expected


# Message Bindings Serialization Test Cases
def case_googlepubsub_message_binding_serialization_empty() -> tuple[
    GooglePubSubMessageBindings, dict
]:
    """GooglePubSubMessageBindings serialization empty."""
    gps_binding = GooglePubSubMessageBindings()
    expected: dict[str, Any] = {"bindingVersion": "0.2.0"}
    return gps_binding, expected


def case_googlepubsub_message_binding_serialization_with_schema() -> tuple[
    GooglePubSubMessageBindings, dict
]:
    """GooglePubSubMessageBindings serialization with schema."""
    gps_binding = GooglePubSubMessageBindings(
        schema=GooglePubSubSchemaDefinition(
            name="projects/your-project/schemas/message-avro",
        ),
    )
    expected: dict[str, Any] = {
        "schema": {
            "name": "projects/your-project/schemas/message-avro",
        },
        "bindingVersion": "0.2.0",
    }
    return gps_binding, expected


class TestGooglePubSubServerBindings:
    """Tests for GooglePubSubServerBindings model."""

    def test_googlepubsub_server_bindings_serialization(self) -> None:
        """Test GooglePubSubServerBindings serialization."""
        gps_binding = GooglePubSubServerBindings()
        dumped = gps_binding.model_dump()
        assert dumped == {}

    def test_googlepubsub_server_bindings_python_validation_error(self) -> None:
        """Test GooglePubSubServerBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            GooglePubSubServerBindings(some_field="value")

    def test_googlepubsub_server_bindings_yaml_validation_error(self) -> None:
        """Test GooglePubSubServerBindings YAML validation error with any fields."""
        yaml_data = """
        googlepubsub:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            GooglePubSubServerBindings.model_validate(data["googlepubsub"])

    def test_googlepubsub_server_bindings_yaml_empty_validation(self) -> None:
        """Test GooglePubSubServerBindings YAML validation with no fields."""
        yaml_data = """
        googlepubsub: {}
        """
        data = yaml.safe_load(yaml_data)
        gps_binding = GooglePubSubServerBindings.model_validate(data["googlepubsub"])
        assert gps_binding is not None


class TestGooglePubSubChannelBindings:
    """Tests for GooglePubSubChannelBindings model."""

    def test_googlepubsub_channel_binding_minimal_validation(self) -> None:
        """Test GooglePubSubChannelBindings with minimal fields validation."""
        yaml_data = """
        googlepubsub:
          schemaSettings:
            encoding: JSON
            name: projects/your-project/schemas/message-avro
          bindingVersion: 0.2.0
        """
        data = yaml.safe_load(yaml_data)
        gps_binding = GooglePubSubChannelBindings.model_validate(data["googlepubsub"])

        # Verify all fields
        assert gps_binding.schema_settings is not None
        assert isinstance(gps_binding.schema_settings, GooglePubSubSchemaSettings)
        assert gps_binding.schema_settings.encoding == "JSON"
        assert (
            gps_binding.schema_settings.name
            == "projects/your-project/schemas/message-avro"
        )
        assert gps_binding.binding_version == "0.2.0"

    def test_googlepubsub_channel_binding_full_validation(self) -> None:
        """Test GooglePubSubChannelBindings with all fields validation."""
        yaml_data = """
        googlepubsub:
          messageRetentionDuration: 86400s
          messageStoragePolicy:
            allowedPersistenceRegions:
              - us-central1
              - us-central2
          schemaSettings:
            encoding: BINARY
            name: projects/your-project/schemas/message-proto
          bindingVersion: 0.2.0
        """
        data = yaml.safe_load(yaml_data)
        gps_binding = GooglePubSubChannelBindings.model_validate(data["googlepubsub"])

        # Verify all fields
        assert gps_binding.message_retention_duration == "86400s"
        assert gps_binding.message_storage_policy is not None
        assert isinstance(
            gps_binding.message_storage_policy, GooglePubSubMessageStoragePolicy
        )
        assert gps_binding.message_storage_policy.allowed_persistence_regions == [
            "us-central1",
            "us-central2",
        ]
        assert gps_binding.schema_settings is not None
        assert isinstance(gps_binding.schema_settings, GooglePubSubSchemaSettings)
        assert gps_binding.schema_settings.encoding == "BINARY"
        assert (
            gps_binding.schema_settings.name
            == "projects/your-project/schemas/message-proto"
        )
        assert gps_binding.binding_version == "0.2.0"

    def test_googlepubsub_channel_bindings_validation_error_extra_fields(self) -> None:
        """Test GooglePubSubChannelBindings validation error with extra fields."""
        yaml_data = """
        googlepubsub:
          bindingVersion: 0.2.0
          extra_field: invalid
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            GooglePubSubChannelBindings.model_validate(data["googlepubsub"])

    def test_googlepubsub_channel_bindings_validation_error_invalid_encoding(
        self,
    ) -> None:
        """Test GooglePubSubChannelBindings validation error with invalid encoding."""
        yaml_data = """
        googlepubsub:
          schemaSettings:
            encoding: INVALID_ENCODING
            name: projects/your-project/schemas/message-avro
          bindingVersion: 0.2.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            GooglePubSubChannelBindings.model_validate(data["googlepubsub"])

    @parametrize_with_cases(
        "gps_binding,expected",
        cases=[
            case_googlepubsub_channel_binding_serialization_empty,
            case_googlepubsub_channel_binding_serialization_with_schema_settings,
            case_googlepubsub_channel_binding_serialization_full,
        ],
    )
    def test_googlepubsub_channel_bindings_serialization(
        self,
        gps_binding: GooglePubSubChannelBindings,
        expected: dict,
    ) -> None:
        """Test GooglePubSubChannelBindings serialization."""
        dumped = gps_binding.model_dump()
        assert dumped == expected


class TestGooglePubSubOperationBindings:
    """Tests for GooglePubSubOperationBindings model."""

    def test_googlepubsub_operation_bindings_serialization(self) -> None:
        """Test GooglePubSubOperationBindings serialization."""
        gps_binding = GooglePubSubOperationBindings()
        dumped = gps_binding.model_dump()
        assert dumped == {}

    def test_googlepubsub_operation_bindings_python_validation_error(self) -> None:
        """Test GooglePubSubOperationBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            GooglePubSubOperationBindings(some_field="value")

    def test_googlepubsub_operation_bindings_yaml_validation_error(self) -> None:
        """Test GooglePubSubOperationBindings YAML validation error with any fields."""
        yaml_data = """
        googlepubsub:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            GooglePubSubOperationBindings.model_validate(data["googlepubsub"])

    def test_googlepubsub_operation_bindings_yaml_empty_validation(self) -> None:
        """Test GooglePubSubOperationBindings YAML validation with no fields."""
        yaml_data = """
        googlepubsub: {}
        """
        data = yaml.safe_load(yaml_data)
        gps_binding = GooglePubSubOperationBindings.model_validate(data["googlepubsub"])
        assert gps_binding is not None


class TestGooglePubSubMessageBindings:
    """Tests for GooglePubSubMessageBindings model."""

    def test_googlepubsub_message_binding_with_schema_validation(self) -> None:
        """Test GooglePubSubMessageBindings with schema validation."""
        yaml_data = """
        googlepubsub:
          schema:
            name: projects/your-project/schemas/message-avro
          bindingVersion: 0.2.0
        """
        data = yaml.safe_load(yaml_data)
        gps_binding = GooglePubSubMessageBindings.model_validate(data["googlepubsub"])

        # Verify all fields
        assert gps_binding.schema is not None
        assert isinstance(gps_binding.schema, GooglePubSubSchemaDefinition)
        assert gps_binding.schema.name == "projects/your-project/schemas/message-avro"
        assert gps_binding.binding_version == "0.2.0"

    def test_googlepubsub_message_bindings_validation_error_extra_fields(self) -> None:
        """Test GooglePubSubMessageBindings validation error with extra fields."""
        yaml_data = """
        googlepubsub:
          bindingVersion: 0.2.0
          extra_field: invalid
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            GooglePubSubMessageBindings.model_validate(data["googlepubsub"])

    @parametrize_with_cases(
        "gps_binding,expected",
        cases=[
            case_googlepubsub_message_binding_serialization_empty,
            case_googlepubsub_message_binding_serialization_with_schema,
        ],
    )
    def test_googlepubsub_message_bindings_serialization(
        self,
        gps_binding: GooglePubSubMessageBindings,
        expected: dict,
    ) -> None:
        """Test GooglePubSubMessageBindings serialization."""
        dumped = gps_binding.model_dump()
        assert dumped == expected
