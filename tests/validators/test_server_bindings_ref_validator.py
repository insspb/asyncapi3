"""Tests for ServerBindingsRefValidator."""

import logging

import pytest

from _pytest.logging import LogCaptureFixture

from asyncapi3.models.asyncapi import AsyncAPI3
from asyncapi3.validators import ServerBindingsRefValidator


class TestServerBindingsRefValidator:
    """Tests for ServerBindingsRefValidator."""

    def test_server_bindings_ref_validator_validates_root_servers_bindings_refs(
        self,
    ) -> None:
        """Test ServerBindingsRefValidator validates server binding references in root servers."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            servers={
                "prod": {
                    "host": "api.example.com",
                    "protocol": "https",
                    "bindings": {"$ref": "#/components/serverBindings/http"},
                },
            },
            components={
                "serverBindings": {
                    "http": {
                        "http": {},  # Empty HTTP binding object
                    },
                },
            },
            extra_validators=[ServerBindingsRefValidator],
        )

        # Should not raise any errors
        assert spec is not None

    def test_server_bindings_ref_validator_invalid_root_servers_bindings_ref_path(
        self,
    ) -> None:
        """Test ServerBindingsRefValidator raises error for invalid root server binding reference path."""
        with pytest.raises(
            ValueError, match="must point to #/components/serverBindings/"
        ):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                servers={
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                        "bindings": {"$ref": "#/bindings/http"},  # Wrong path
                    },
                },
                components={
                    "serverBindings": {
                        "http": {
                            "http": {},  # Empty HTTP binding object
                        },
                    },
                },
                extra_validators=[ServerBindingsRefValidator],
            )

    def test_server_bindings_ref_validator_root_servers_bindings_ref_to_nonexistent_binding(
        self,
    ) -> None:
        """Test ServerBindingsRefValidator raises error when root server references nonexistent binding."""
        with pytest.raises(
            ValueError, match="does not exist in components/serverBindings"
        ):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                servers={
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                        "bindings": {"$ref": "#/components/serverBindings/nonexistent"},
                    },
                },
                components={
                    "serverBindings": {
                        "existing": {
                            "http": {},  # Empty HTTP binding object
                        },
                    },
                },
                extra_validators=[ServerBindingsRefValidator],
            )

    def test_server_bindings_ref_validator_validates_components_servers_bindings_refs(
        self,
    ) -> None:
        """Test ServerBindingsRefValidator validates server binding references in components servers."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            components={
                "servers": {
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                        "bindings": {"$ref": "#/components/serverBindings/http"},
                    },
                },
                "serverBindings": {
                    "http": {
                        "http": {},  # Empty HTTP binding object
                    },
                },
            },
            extra_validators=[ServerBindingsRefValidator],
        )

        # Should not raise any errors
        assert spec is not None

    def test_server_bindings_ref_validator_components_servers_bindings_ref_to_nonexistent(
        self,
    ) -> None:
        """Test ServerBindingsRefValidator raises error when components server references nonexistent binding."""
        with pytest.raises(
            ValueError, match="does not exist in components/serverBindings"
        ):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                components={
                    "servers": {
                        "prod": {
                            "host": "api.example.com",
                            "protocol": "https",
                            "bindings": {
                                "$ref": "#/components/serverBindings/nonexistent"
                            },
                        },
                    },
                    "serverBindings": {
                        "existing": {
                            "http": {},  # Empty HTTP binding object
                        },
                    },
                },
                extra_validators=[ServerBindingsRefValidator],
            )

    def test_server_bindings_ref_validator_validates_components_server_bindings_refs(
        self,
    ) -> None:
        """Test ServerBindingsRefValidator validates references within components server bindings."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            components={
                "serverBindings": {
                    "http": {
                        "http": {},  # Empty HTTP binding object
                    },
                    "refBinding": {"$ref": "#/components/serverBindings/http"},
                },
            },
            extra_validators=[ServerBindingsRefValidator],
        )

        # Should not raise any errors
        assert spec is not None

    def test_server_bindings_ref_validator_components_server_bindings_ref_to_nonexistent(
        self,
    ) -> None:
        """Test ServerBindingsRefValidator raises error when components server binding references nonexistent."""
        with pytest.raises(
            ValueError, match="does not exist in components/serverBindings"
        ):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                components={
                    "serverBindings": {
                        "refBinding": {
                            "$ref": "#/components/serverBindings/nonexistent"
                        },
                    },
                },
                extra_validators=[ServerBindingsRefValidator],
            )

    def test_server_bindings_ref_validator_root_server_no_bindings_attr(self) -> None:
        """Test ServerBindingsRefValidator handles root servers without bindings attribute."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            servers={
                "prod": {
                    "host": "api.example.com",
                    "protocol": "https",
                    # No bindings attribute
                },
            },
            extra_validators=[ServerBindingsRefValidator],
        )

        # Should not raise any errors
        assert spec is not None

    def test_server_bindings_ref_validator_root_server_inline_bindings(self) -> None:
        """Test ServerBindingsRefValidator handles root servers with inline bindings."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            servers={
                "prod": {
                    "host": "api.example.com",
                    "protocol": "https",
                    "bindings": {  # Inline bindings object
                        "http": {},  # Empty HTTP binding object
                    },
                },
            },
            extra_validators=[ServerBindingsRefValidator],
        )

        # Should not raise any errors - only references are validated
        assert spec is not None

    def test_server_bindings_ref_validator_external_root_servers_bindings_ref_warning(
        self, caplog: LogCaptureFixture
    ) -> None:
        """Test ServerBindingsRefValidator logs warning for external root server binding reference."""
        with caplog.at_level(logging.WARNING):
            spec = AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                servers={
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                        "bindings": {
                            "$ref": "https://external.example.com/bindings/http"
                        },
                    },
                },
                extra_validators=[ServerBindingsRefValidator],
            )

        # Should not raise error but log warning
        assert spec is not None
        assert any(
            "is external. Cannot validate external references" in record.message
            for record in caplog.records
        )

    def test_server_bindings_ref_validator_components_servers_no_bindings_attr(
        self,
    ) -> None:
        """Test ServerBindingsRefValidator handles components servers without bindings attribute."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            components={
                "servers": {
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                        # No bindings attribute
                    },
                },
            },
            extra_validators=[ServerBindingsRefValidator],
        )

        # Should not raise any errors
        assert spec is not None
