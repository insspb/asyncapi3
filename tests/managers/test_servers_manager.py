"""Tests for ServersManager."""

import pytest

from asyncapi3.managers import ServersManager
from asyncapi3.models.asyncapi import AsyncAPI3
from asyncapi3.models.server import Server


class TestServersManager:
    """Tests for ServersManager."""

    def test_servers_manager_processes_root_servers(self) -> None:
        """Test ServersManager moves servers from root to components and creates references."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            servers={
                "prod": Server(
                    host="api.example.com",
                    protocol="https",
                    description="Production server",
                ),
                "dev": Server(
                    host="dev.api.example.com",
                    protocol="http",
                    description="Development server",
                ),
            },
            extra_converters=[ServersManager],
        )

        # After model validation and ServersManager processing, servers should be moved
        # to components and replaced with references
        spec_data = spec.model_dump()

        assert "servers" in spec_data["components"]
        assert len(spec_data["components"]["servers"]) == 2

        # # Check that references point to existing servers
        for server_name, server_ref in spec_data["servers"].items():
            assert server_ref["$ref"] == f"#/components/servers/{server_name}"

    def test_servers_manager_preserves_existing_references(self) -> None:
        """Test ServersManager preserves existing references in root servers."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            servers={
                "prod": {
                    "$ref": "#/components/servers/production",
                },
            },
            extra_converters=[ServersManager],
        )

        # Existing references should be preserved
        spec_data = spec.model_dump()
        assert spec_data["servers"]["prod"]["$ref"] == "#/components/servers/production"

    def test_servers_manager_handles_duplicate_server_names(self) -> None:
        """Test ServersManager raises error for duplicate server names with different content."""
        with pytest.raises(
            ValueError,
            match=(
                r"Value error, Server name conflict detected: 'prod' already exists "
                r"with different content."
            ),
        ):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                servers={
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                        "description": "Production server",
                    },
                },
                components={
                    "servers": {
                        "prod": {
                            "host": "different.api.example.com",  # Different content
                            "protocol": "https",
                            "description": "Different production server",
                        },
                    },
                },
                extra_converters=[ServersManager],
            )

    def test_servers_manager_allows_identical_duplicate_servers(self) -> None:
        """Test ServersManager allows duplicate server names with identical content."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            servers={
                "prod": {
                    "host": "api.example.com",
                    "protocol": "https",
                    "description": "Production server",
                },
            },
            components={
                "servers": {
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                        "description": "Production server",  # Same content
                    },
                },
            },
            extra_converters=[ServersManager],
        )

        # Should not raise error and should work normally
        spec_data = spec.model_dump()
        assert len(spec_data["servers"]) == 1
        assert "servers" in spec_data["components"]
