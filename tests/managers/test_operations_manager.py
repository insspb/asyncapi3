"""Tests for OperationsManager."""

import pytest

from asyncapi3.managers import OperationsManager
from asyncapi3.models.asyncapi import AsyncAPI3
from asyncapi3.models.operation import Operation


class TestOperationsManager:
    """Tests for OperationsManager."""

    def test_operations_manager_processes_root_operations(self) -> None:
        """Test OperationsManager moves operations from root to components and creates references."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            operations={
                "sendMessage": Operation(
                    action="send",
                    channel={"$ref": "#/channels/userSignup"},
                    description="Send a message operation",
                ),
                "receiveMessage": Operation(
                    action="receive",
                    channel={"$ref": "#/channels/userSignup"},
                    description="Receive a message operation",
                ),
            },
            extra_converters=[OperationsManager],
        )

        # After model validation and OperationsManager processing, operations should be moved
        # to components and replaced with references
        spec_data = spec.model_dump()

        assert "operations" in spec_data["components"]
        assert len(spec_data["components"]["operations"]) == 2

        # Check that references point to existing operations
        for operation_name, operation_ref in spec_data["operations"].items():
            assert operation_ref["$ref"] == f"#/components/operations/{operation_name}"

    def test_operations_manager_preserves_existing_references(self) -> None:
        """Test OperationsManager preserves existing references in root operations."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            operations={
                "sendMessage": {
                    "$ref": "#/components/operations/sendMessageOp",
                },
            },
            extra_converters=[OperationsManager],
        )

        # Existing references should be preserved
        spec_data = spec.model_dump()
        assert (
            spec_data["operations"]["sendMessage"]["$ref"]
            == "#/components/operations/sendMessageOp"
        )

    def test_operations_manager_handles_duplicate_operation_names(self) -> None:
        """Test OperationsManager raises error for duplicate operation names with different content."""
        with pytest.raises(
            ValueError,
            match=(
                r"Value error, Operation name conflict detected: 'sendMessage' exists "
                "with different content."
            ),
        ):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                operations={
                    "sendMessage": {
                        "action": "send",
                        "channel": {"$ref": "#/channels/userSignup"},
                        "description": "Send a message operation",
                    },
                },
                components={
                    "operations": {
                        "sendMessage": {
                            "action": "receive",  # Different content
                            "channel": {"$ref": "#/channels/userSignup"},
                            "description": "Receive a message operation",
                        },
                    },
                },
                extra_converters=[OperationsManager],
            )

    def test_operations_manager_allows_identical_duplicate_operations(self) -> None:
        """Test OperationsManager allows duplicate operation names with identical content."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            operations={
                "sendMessage": {
                    "action": "send",
                    "channel": {"$ref": "#/channels/userSignup"},
                    "description": "Send a message operation",
                },
            },
            components={
                "operations": {
                    "sendMessage": {
                        "action": "send",
                        "channel": {"$ref": "#/channels/userSignup"},
                        "description": "Send a message operation",
                    },
                },
            },
            extra_converters=[OperationsManager],
        )

        # Should not raise an error for identical content
        spec_data = spec.model_dump()
        assert (
            spec_data["operations"]["sendMessage"]["$ref"]
            == "#/components/operations/sendMessage"
        )
