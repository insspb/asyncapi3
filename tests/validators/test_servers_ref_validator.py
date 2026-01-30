"""Tests for ServersRefValidator."""

import logging

import pytest

from _pytest.logging import LogCaptureFixture

from asyncapi3.models.asyncapi import AsyncAPI3
from asyncapi3.validators import ServersRefValidator


class TestServersRefValidator:
    """Tests for ServersRefValidator."""

    def test_servers_ref_validator_validates_root_servers_refs(self) -> None:
        """Test ServersRefValidator validates root servers references."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            servers={
                "prod": {"$ref": "#/components/servers/prod"},
            },
            components={
                "servers": {
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                    },
                },
            },
            extra_validators=[ServersRefValidator],
        )

        # run_extra_processors called automatically during creation
        # Should not raise any errors
        assert spec is not None

    def test_servers_ref_validator_invalid_root_servers_ref_path(self) -> None:
        """Test ServersRefValidator raises error for invalid root servers reference path."""
        with pytest.raises(ValueError, match="must point to #/components/servers/"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                servers={
                    "prod": {
                        "$ref": "#/servers/prod"
                    },  # Wrong path, should be #/components/servers/
                },
                components={
                    "servers": {
                        "prod": {
                            "host": "api.example.com",
                            "protocol": "https",
                        },
                    },
                },
                extra_validators=[ServersRefValidator],
            )

    def test_servers_ref_validator_root_servers_ref_to_nonexistent_server(self) -> None:
        """Test ServersRefValidator raises error when root servers reference nonexistent server."""
        with pytest.raises(ValueError, match="does not exist in components/servers"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                servers={
                    "prod": {"$ref": "#/components/servers/nonexistent"},
                },
                components={
                    "servers": {
                        "existing": {
                            "host": "api.example.com",
                            "protocol": "https",
                        },
                    },
                },
                extra_validators=[ServersRefValidator],
            )

    def test_servers_ref_validator_validates_channels_servers_refs(self) -> None:
        """Test ServersRefValidator validates server references in root channels."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            servers={
                "prod": {"$ref": "#/components/servers/prod"},
            },
            channels={
                "test": {
                    "address": "/test",
                    "servers": [{"$ref": "#/servers/prod"}],
                },
            },
            components={
                "servers": {
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                    },
                },
            },
            extra_validators=[ServersRefValidator],
        )

        # run_extra_processors called automatically during creation
        # Should not raise any errors
        assert spec is not None

    def test_servers_ref_validator_invalid_channels_servers_ref_path(self) -> None:
        """Test ServersRefValidator raises error for invalid channels server reference path."""
        with pytest.raises(ValueError, match="must point to #/servers/"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                servers={
                    "prod": {"$ref": "#/components/servers/prod"},
                },
                channels={
                    "test": {
                        "address": "/test",
                        "servers": [
                            {"$ref": "#/components/servers/prod"}
                        ],  # Wrong path, should be #/servers/
                    },
                },
                components={
                    "servers": {
                        "prod": {
                            "host": "api.example.com",
                            "protocol": "https",
                        },
                    },
                },
                extra_validators=[ServersRefValidator],
            )

    def test_servers_ref_validator_channels_ref_to_nonexistent_root_server(
        self,
    ) -> None:
        """Test ServersRefValidator raises error when channel references nonexistent root server."""
        with pytest.raises(ValueError, match="does not exist in root servers"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                servers={
                    "existing": {"$ref": "#/components/servers/existing"},
                },
                channels={
                    "test": {
                        "address": "/test",
                        "servers": [{"$ref": "#/servers/nonexistent"}],
                    },
                },
                components={
                    "servers": {
                        "existing": {
                            "host": "api.example.com",
                            "protocol": "https",
                        },
                    },
                },
                extra_validators=[ServersRefValidator],
            )

    def test_servers_ref_validator_validates_components_channels_refs(self) -> None:
        """Test ServersRefValidator validates server references in components channels."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            servers={
                "prod": {"$ref": "#/components/servers/prod"},
            },
            components={
                "servers": {
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                    },
                    "dev": {
                        "host": "dev.api.example.com",
                        "protocol": "http",
                    },
                },
                "channels": {
                    "test1": {
                        "address": "/test1",
                        "servers": [
                            {"$ref": "#/servers/prod"}
                        ],  # Reference to root server
                    },
                    "test2": {
                        "address": "/test2",
                        "servers": [
                            {"$ref": "#/components/servers/dev"}
                        ],  # Reference to components server
                    },
                },
            },
            extra_validators=[ServersRefValidator],
        )

        # run_extra_processors called automatically during creation
        # Should not raise any errors
        assert spec is not None

    def test_servers_ref_validator_invalid_components_channels_ref_path(self) -> None:
        """Test ServersRefValidator raises error for invalid components channels server reference path."""
        with pytest.raises(
            ValueError, match="must point to #/servers/ or #/components/servers/"
        ):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                components={
                    "channels": {
                        "test": {
                            "address": "/test",
                            "servers": [{"$ref": "#/invalid/path"}],  # Invalid path
                        },
                    },
                },
                extra_validators=[ServersRefValidator],
            )

    def test_servers_ref_validator_components_channels_ref_to_nonexistent_server(
        self,
    ) -> None:
        """Test ServersRefValidator raises error when components channel references nonexistent server."""
        with pytest.raises(ValueError, match="does not exist in root servers"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                components={
                    "channels": {
                        "test": {
                            "address": "/test",
                            "servers": [{"$ref": "#/servers/nonexistent"}],
                        },
                    },
                },
                extra_validators=[ServersRefValidator],
            )

    def test_servers_ref_validator_root_servers_not_ref_object(self) -> None:
        """Test ServersRefValidator handles root servers that are not Reference objects."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            servers={
                "prod": {  # Not a reference object, regular server definition
                    "host": "api.example.com",
                    "protocol": "https",
                },
            },
            extra_validators=[ServersRefValidator],
        )

        # Should not raise any errors - non-reference objects are skipped
        assert spec is not None

    def test_servers_ref_validator_external_root_servers_ref_warning(
        self, caplog: LogCaptureFixture
    ) -> None:
        """Test ServersRefValidator logs warning for external root servers reference."""
        with caplog.at_level(logging.WARNING):
            spec = AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                servers={
                    "external": {"$ref": "https://external.example.com/servers/prod"},
                },
                extra_validators=[ServersRefValidator],
            )

        # Should not raise error but log warning
        assert spec is not None
        assert any("external reference" in record.message for record in caplog.records)

    def test_servers_ref_validator_channels_without_servers_attr(self) -> None:
        """Test ServersRefValidator handles channels without servers attribute or with empty servers."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            channels={
                "no_servers_attr": {
                    "address": "/test1",
                    # No servers attribute
                },
                "empty_servers": {
                    "address": "/test2",
                    "servers": [],  # Empty servers list
                },
            },
            extra_validators=[ServersRefValidator],
        )

        # Should not raise any errors - channels without servers are skipped
        assert spec is not None

    def test_servers_ref_validator_external_channels_servers_ref_warning(
        self, caplog: LogCaptureFixture
    ) -> None:
        """Test ServersRefValidator logs warning for external channels server reference."""

        with caplog.at_level(logging.WARNING):
            spec = AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                channels={
                    "test": {
                        "address": "/test",
                        "servers": [
                            {"$ref": "https://external.example.com/servers/prod"}
                        ],
                    },
                },
                extra_validators=[ServersRefValidator],
            )

        # Should not raise error but log warning
        assert spec is not None
        assert any(
            "external. Cannot validate external references" in record.message
            for record in caplog.records
        )

    def test_servers_ref_validator_components_channels_without_servers_attr(
        self,
    ) -> None:
        """Test ServersRefValidator handles components channels without servers attribute or with empty servers."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            components={
                "channels": {
                    "no_servers_attr": {
                        "address": "/test1",
                        # No servers attribute
                    },
                    "empty_servers": {
                        "address": "/test2",
                        "servers": [],  # Empty servers list
                    },
                },
            },
            extra_validators=[ServersRefValidator],
        )

        # Should not raise any errors - components channels without servers are skipped
        assert spec is not None

    def test_servers_ref_validator_external_components_channels_servers_ref_warning(
        self, caplog: LogCaptureFixture
    ) -> None:
        """Test ServersRefValidator logs warning for external components channels server reference."""

        with caplog.at_level(logging.WARNING):
            spec = AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                components={
                    "channels": {
                        "test": {
                            "address": "/test",
                            "servers": [
                                {"$ref": "https://external.example.com/servers/prod"}
                            ],
                        },
                    },
                },
                extra_validators=[ServersRefValidator],
            )

        # Should not raise error but log warning
        assert spec is not None
        assert any(
            "is external. Cannot validate external references" in record.message
            for record in caplog.records
        )

    def test_servers_ref_validator_components_channels_ref_to_components_server_missing_components_servers(
        self,
    ) -> None:
        """Test ServersRefValidator raises error when components channel references components server but components.servers doesn't exist."""
        with pytest.raises(ValueError, match="does not exist in components/servers"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                components={
                    "channels": {
                        "test": {
                            "address": "/test",
                            "servers": [{"$ref": "#/components/servers/prod"}],
                        },
                    },
                    # No servers in components
                },
                extra_validators=[ServersRefValidator],
            )
