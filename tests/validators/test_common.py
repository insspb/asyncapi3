"""Tests for common validation functions."""

import logging

import pytest

from asyncapi3.models.asyncapi import AsyncAPI3
from asyncapi3.validators.common import (
    is_external_ref,
    validate_component_exists,
    validate_root_channel_ref,
    validate_root_operation_ref,
)


class TestValidateExternalReference:
    """Tests for validate_external_reference function."""

    def test_external_reference_returns_true_and_logs_warning(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that external reference returns True and logs warning."""
        with caplog.at_level(logging.WARNING):
            result = is_external_ref("https://example.com/schema.json", "Test context")

        assert result is True
        assert "Test context contains external reference" in caplog.text
        assert "Cannot validate external references" in caplog.text

    def test_internal_reference_returns_false(self) -> None:
        """Test that internal reference returns False."""
        result = is_external_ref("#/components/schemas/Test", "Test context")
        assert result is False


class TestValidateComponentExists:
    """Tests for validate_component_exists function."""

    def test_valid_component_reference(self) -> None:
        """Test validation of valid component reference."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0.0"},
            components={"schemas": {"TestSchema": {"type": "string"}}},
        )

        # Should not raise any exception
        validate_component_exists(
            spec,
            "#/components/schemas/TestSchema",
            "schemas",
            "Test schema",
        )

    def test_invalid_component_path_raises_error(self) -> None:
        """Test that invalid component path raises ValueError."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0.0"},
            components={"schemas": {"TestSchema": {"type": "string"}}},
        )

        with pytest.raises(ValueError, match="must point to #/components/schemas/"):
            validate_component_exists(
                spec,
                "#/components/other/TestSchema",
                "schemas",
                "Test schema",
            )

    def test_nonexistent_component_raises_error(self) -> None:
        """Test that reference to nonexistent component raises ValueError."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0.0"},
            components={"schemas": {"ExistingSchema": {"type": "string"}}},
        )

        with pytest.raises(
            ValueError, match="component 'NonExistentSchema' does not exist"
        ):
            validate_component_exists(
                spec,
                "#/components/schemas/NonExistentSchema",
                "schemas",
                "Test schema",
            )

    def test_missing_components_raises_error(self) -> None:
        """Test that missing components section raises ValueError."""
        spec = AsyncAPI3(asyncapi="3.0.0", info={"title": "Test", "version": "1.0.0"})

        with pytest.raises(ValueError, match="component 'TestSchema' does not exist"):
            validate_component_exists(
                spec,
                "#/components/schemas/TestSchema",
                "schemas",
                "Test schema",
            )

    def test_missing_component_type_raises_error(self) -> None:
        """Test that missing component type raises ValueError."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0.0"},
            components={
                "messages": {}  # No schemas section
            },
        )

        with pytest.raises(ValueError, match="component 'TestSchema' does not exist"):
            validate_component_exists(
                spec,
                "#/components/schemas/TestSchema",
                "schemas",
                "Test schema",
            )


class TestValidateRootChannelReference:
    """Tests for validate_root_channel_reference function."""

    def test_valid_channel_reference(self) -> None:
        """Test validation of valid root channel reference."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0.0"},
            channels={"test-channel": {"address": "test-channel", "messages": {}}},
        )

        # Should not raise any exception
        validate_root_channel_ref(
            spec,
            "#/channels/test-channel",
            "Test channel",
        )

    def test_invalid_channel_path_raises_error(self) -> None:
        """Test that invalid channel path raises ValueError."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0.0"},
            channels={"test-channel": {"address": "test-channel", "messages": {}}},
        )

        with pytest.raises(ValueError, match="must point to #/channels/"):
            validate_root_channel_ref(
                spec,
                "#/components/channels/test-channel",
                "Test channel",
            )

    def test_nonexistent_channel_raises_error(self) -> None:
        """Test that reference to nonexistent channel raises ValueError."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0.0"},
            channels={
                "existing-channel": {"address": "existing-channel", "messages": {}}
            },
        )

        with pytest.raises(
            ValueError, match="channel 'nonexistent-channel' does not exist"
        ):
            validate_root_channel_ref(
                spec,
                "#/channels/nonexistent-channel",
                "Test channel",
            )

    def test_missing_channels_raises_error(self) -> None:
        """Test that missing channels section raises ValueError."""
        spec = AsyncAPI3(asyncapi="3.0.0", info={"title": "Test", "version": "1.0.0"})

        with pytest.raises(ValueError, match="channel 'test-channel' does not exist"):
            validate_root_channel_ref(
                spec,
                "#/channels/test-channel",
                "Test channel",
            )


class TestValidateRootOperationReference:
    """Tests for validate_root_operation_reference function."""

    def test_valid_operation_reference(self) -> None:
        """Test validation of valid root operation reference."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0.0"},
            operations={
                "test-operation": {
                    "action": "receive",
                    "channel": {"$ref": "#/channels/test-channel"},
                }
            },
            channels={"test-channel": {"address": "test-channel", "messages": {}}},
        )

        # Should not raise any exception
        validate_root_operation_ref(
            spec, "#/operations/test-operation", "Test operation"
        )

    def test_invalid_operation_path_raises_error(self) -> None:
        """Test that invalid operation path raises ValueError."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0.0"},
            operations={
                "test-operation": {
                    "action": "receive",
                    "channel": {"$ref": "#/channels/test-channel"},
                }
            },
        )

        with pytest.raises(ValueError, match="must point to #/operations/"):
            validate_root_operation_ref(
                spec,
                "#/components/operations/test-operation",
                "Test operation",
            )

    def test_nonexistent_operation_raises_error(self) -> None:
        """Test that reference to nonexistent operation raises ValueError."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0.0"},
            operations={
                "existing-operation": {
                    "action": "receive",
                    "channel": {"$ref": "#/channels/test-channel"},
                }
            },
        )

        with pytest.raises(
            ValueError, match="operation 'nonexistent-operation' does not exist"
        ):
            validate_root_operation_ref(
                spec,
                "#/operations/nonexistent-operation",
                "Test operation",
            )

    def test_missing_operations_raises_error(self) -> None:
        """Test that missing operations section raises ValueError."""
        spec = AsyncAPI3(asyncapi="3.0.0", info={"title": "Test", "version": "1.0.0"})

        with pytest.raises(
            ValueError, match="operation 'test-operation' does not exist"
        ):
            validate_root_operation_ref(
                spec,
                "#/operations/test-operation",
                "Test operation",
            )
