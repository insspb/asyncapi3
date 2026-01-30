"""Tests for ServerVariablesRefValidator."""

import logging

import pytest

from _pytest.logging import LogCaptureFixture

from asyncapi3.models.asyncapi import AsyncAPI3
from asyncapi3.validators import ServerVariablesRefValidator


class TestServerVariablesRefValidator:
    """Tests for ServerVariablesRefValidator."""

    def test_server_variables_ref_validator_validates_root_servers_variables_refs_to_root(
        self,
    ) -> None:
        """Test ServerVariablesRefValidator validates root server variable references to root variables."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            servers={
                "prod": {
                    "host": "api.example.com",
                    "protocol": "https",
                    "variables": {
                        "port": {"$ref": "#/servers/prod/variables/port"},
                        "version": {"default": "v1"},
                    },
                },
            },
            extra_validators=[ServerVariablesRefValidator],
        )

        # Should not raise any errors
        assert spec is not None

    def test_server_variables_ref_validator_validates_root_servers_variables_refs_to_components(
        self,
    ) -> None:
        """Test ServerVariablesRefValidator validates root server variable references to components variables."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            servers={
                "prod": {
                    "host": "api.example.com",
                    "protocol": "https",
                    "variables": {
                        "port": {"$ref": "#/components/serverVariables/portVar"},
                    },
                },
            },
            components={
                "serverVariables": {
                    "portVar": {
                        "default": "8080",
                        "description": "Port number",
                    },
                },
            },
            extra_validators=[ServerVariablesRefValidator],
        )

        # Should not raise any errors
        assert spec is not None

    def test_server_variables_ref_validator_validates_root_servers_variables_refs_to_components_servers(
        self,
    ) -> None:
        """Test ServerVariablesRefValidator validates root server variable references to components server variables."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            servers={
                "prod": {
                    "host": "api.example.com",
                    "protocol": "https",
                    "variables": {
                        "port": {
                            "$ref": "#/components/servers/prodServer/variables/port"
                        },
                    },
                },
            },
            components={
                "servers": {
                    "prodServer": {
                        "host": "internal.api.example.com",
                        "protocol": "http",
                        "variables": {
                            "port": {"default": "8080"},
                        },
                    },
                },
            },
            extra_validators=[ServerVariablesRefValidator],
        )

        # Should not raise any errors
        assert spec is not None

    def test_server_variables_ref_validator_invalid_root_servers_variables_ref_path(
        self,
    ) -> None:
        """Test ServerVariablesRefValidator raises error for invalid root server variable reference path."""
        with pytest.raises(
            ValueError,
            match=r"must point to #/servers/.*variables/.* or #/components/serverVariables/",
        ):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                servers={
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                        "variables": {
                            "port": {"$ref": "#/invalid/path"},
                        },
                    },
                },
                extra_validators=[ServerVariablesRefValidator],
            )

    def test_server_variables_ref_validator_root_servers_variables_ref_to_nonexistent_root_var(
        self,
    ) -> None:
        """Test ServerVariablesRefValidator raises error when root server references nonexistent root variable."""
        with pytest.raises(ValueError, match="variable does not exist"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                servers={
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                        "variables": {
                            "port": {"$ref": "#/servers/prod/variables/nonexistent"},
                        },
                    },
                },
                extra_validators=[ServerVariablesRefValidator],
            )

    def test_server_variables_ref_validator_root_servers_variables_ref_to_nonexistent_root_server(
        self,
    ) -> None:
        """Test ServerVariablesRefValidator raises error when root server references nonexistent root server."""
        with pytest.raises(ValueError, match="server does not exist in root servers"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                servers={
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                        "variables": {
                            "port": {"$ref": "#/servers/nonexistent/variables/port"},
                        },
                    },
                },
                extra_validators=[ServerVariablesRefValidator],
            )

    def test_server_variables_ref_validator_root_servers_variables_ref_to_components_nonexistent(
        self,
    ) -> None:
        """Test ServerVariablesRefValidator raises error when root server references nonexistent components variable."""
        with pytest.raises(
            ValueError, match="does not exist in #/components/serverVariables"
        ):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                servers={
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                        "variables": {
                            "port": {
                                "$ref": "#/components/serverVariables/nonexistent"
                            },
                        },
                    },
                },
                components={
                    "serverVariables": {
                        "existing": {
                            "default": "8080",
                        },
                    },
                },
                extra_validators=[ServerVariablesRefValidator],
            )

    def test_server_variables_ref_validator_root_servers_variables_ref_to_components_servers_nonexistent(
        self,
    ) -> None:
        """Test ServerVariablesRefValidator raises error when root server references nonexistent components server variable."""
        with pytest.raises(ValueError, match="variable does not exist"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                servers={
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                        "variables": {
                            "port": {
                                "$ref": "#/components/servers/prodServer/variables/nonexistent"
                            },
                        },
                    },
                },
                components={
                    "servers": {
                        "prodServer": {
                            "host": "internal.api.example.com",
                            "protocol": "http",
                            "variables": {
                                "existing": {"default": "8080"},
                            },
                        },
                    },
                },
                extra_validators=[ServerVariablesRefValidator],
            )

    def test_server_variables_ref_validator_validates_components_servers_variables_refs(
        self,
    ) -> None:
        """Test ServerVariablesRefValidator validates components server variable references."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            components={
                "servers": {
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                        "variables": {
                            "port": {"$ref": "#/components/serverVariables/portVar"},
                        },
                    },
                },
                "serverVariables": {
                    "portVar": {
                        "default": "8080",
                        "description": "Port number",
                    },
                },
            },
            extra_validators=[ServerVariablesRefValidator],
        )

        # Should not raise any errors
        assert spec is not None

    def test_server_variables_ref_validator_components_servers_variables_ref_to_nonexistent(
        self,
    ) -> None:
        """Test ServerVariablesRefValidator raises error when components server references nonexistent variable."""
        with pytest.raises(
            ValueError, match="does not exist in #/components/serverVariables"
        ):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                components={
                    "servers": {
                        "prod": {
                            "host": "api.example.com",
                            "protocol": "https",
                            "variables": {
                                "port": {
                                    "$ref": "#/components/serverVariables/nonexistent"
                                },
                            },
                        },
                    },
                    "serverVariables": {
                        "existing": {
                            "default": "8080",
                        },
                    },
                },
                extra_validators=[ServerVariablesRefValidator],
            )

    def test_server_variables_ref_validator_validates_components_server_variables_refs(
        self,
    ) -> None:
        """Test ServerVariablesRefValidator validates references within components server variables."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            components={
                "serverVariables": {
                    "portVar": {
                        "default": "8080",
                        "description": "Port number",
                    },
                    "refVar": {"$ref": "#/components/serverVariables/portVar"},
                },
            },
            extra_validators=[ServerVariablesRefValidator],
        )

        # Should not raise any errors
        assert spec is not None

    def test_server_variables_ref_validator_components_server_variables_ref_to_nonexistent(
        self,
    ) -> None:
        """Test ServerVariablesRefValidator raises error when components server variable references nonexistent."""
        with pytest.raises(
            ValueError, match="does not exist in #/components/serverVariables"
        ):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                components={
                    "serverVariables": {
                        "refVar": {"$ref": "#/components/serverVariables/nonexistent"},
                    },
                },
                extra_validators=[ServerVariablesRefValidator],
            )

    def test_server_variables_ref_validator_invalid_root_server_variable_ref_format(
        self,
    ) -> None:
        """Test ServerVariablesRefValidator raises error for invalid root server variable reference format."""
        with pytest.raises(ValueError, match="must follow the format"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                servers={
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                        "variables": {
                            "port": {"$ref": "#/servers/prod/invalid/port"},
                        },
                    },
                },
                extra_validators=[ServerVariablesRefValidator],
            )

    def test_server_variables_ref_validator_root_server_no_variables_attr(self) -> None:
        """Test ServerVariablesRefValidator handles root servers without variables attribute."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            servers={
                "prod": {
                    "host": "api.example.com",
                    "protocol": "https",
                    # No variables attribute
                },
            },
            extra_validators=[ServerVariablesRefValidator],
        )

        # Should not raise any errors
        assert spec is not None

    def test_server_variables_ref_validator_root_server_empty_variables(self) -> None:
        """Test ServerVariablesRefValidator handles root servers with empty variables dict."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            servers={
                "prod": {
                    "host": "api.example.com",
                    "protocol": "https",
                    "variables": {},  # Empty variables dict
                },
            },
            extra_validators=[ServerVariablesRefValidator],
        )

        # Should not raise any errors
        assert spec is not None

    def test_server_variables_ref_validator_external_root_servers_variables_ref_warning(
        self, caplog: LogCaptureFixture
    ) -> None:
        """Test ServerVariablesRefValidator logs warning for external root server variable reference."""
        with caplog.at_level(logging.WARNING):
            spec = AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                servers={
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                        "variables": {
                            "port": {"$ref": "https://external.example.com/vars/port"},
                        },
                    },
                },
                extra_validators=[ServerVariablesRefValidator],
            )

        # Should not raise error but log warning
        assert spec is not None
        assert any(
            "is external. Cannot validate external references" in record.message
            for record in caplog.records
        )

    def test_server_variables_ref_validator_root_server_variables_inline_objects(
        self,
    ) -> None:
        """Test ServerVariablesRefValidator handles inline server variable objects."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            servers={
                "prod": {
                    "host": "api.example.com",
                    "protocol": "https",
                    "variables": {
                        "port": {"default": "8080"},  # Inline object, not reference
                        "version": {"$ref": "#/components/serverVariables/versionVar"},
                    },
                },
            },
            components={
                "serverVariables": {
                    "versionVar": {
                        "default": "v1",
                        "description": "API version",
                    },
                },
            },
            extra_validators=[ServerVariablesRefValidator],
        )

        # Should not raise any errors - only references are validated
        assert spec is not None
