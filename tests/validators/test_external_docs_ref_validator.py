"""Tests for ExternalDocsRefValidator."""

import logging

import pytest

from _pytest.logging import LogCaptureFixture

from asyncapi3.models.asyncapi import AsyncAPI3
from asyncapi3.validators import ExternalDocsRefValidator


class TestExternalDocsRefValidator:
    """Tests for ExternalDocsRefValidator."""

    def test_external_docs_ref_validator_validates_info_refs(self) -> None:
        """Test ExternalDocsRefValidator validates externalDocs references in info object."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={
                "title": "Test API",
                "version": "1.0.0",
                "externalDocs": {"$ref": "#/components/externalDocs/main"},
            },
            components={
                "externalDocs": {
                    "main": {
                        "url": "https://example.com",
                    },
                },
            },
            extra_validators=[ExternalDocsRefValidator],
        )
        assert spec is not None

    def test_external_docs_ref_validator_invalid_path(self) -> None:
        """Test ExternalDocsRefValidator raises error for invalid reference path."""
        with pytest.raises(
            ValueError, match="must point to #/components/externalDocs/"
        ):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={
                    "title": "Test API",
                    "version": "1.0.0",
                    "externalDocs": {"$ref": "#/docs/main"},
                },
                components={
                    "externalDocs": {
                        "main": {"url": "https://example.com"},
                    },
                },
                extra_validators=[ExternalDocsRefValidator],
            )

    def test_external_docs_ref_validator_nonexistent_ref(self) -> None:
        """Test ExternalDocsRefValidator raises error when references nonexistent doc."""
        with pytest.raises(
            ValueError, match="does not exist in components/externalDocs"
        ):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={
                    "title": "Test API",
                    "version": "1.0.0",
                    "externalDocs": {"$ref": "#/components/externalDocs/nonexistent"},
                },
                components={
                    "externalDocs": {
                        "main": {"url": "https://example.com"},
                    },
                },
                extra_validators=[ExternalDocsRefValidator],
            )

    def test_external_docs_ref_validator_validates_servers_refs(self) -> None:
        """Test ExternalDocsRefValidator validates externalDocs references in servers."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0"},
            servers={
                "prod": {
                    "host": "example.com",
                    "protocol": "mqtt",
                    "externalDocs": {"$ref": "#/components/externalDocs/server"},
                }
            },
            components={
                "externalDocs": {
                    "server": {"url": "https://example.com/server"},
                },
            },
            extra_validators=[ExternalDocsRefValidator],
        )
        assert spec is not None

    def test_external_docs_ref_validator_validates_channels_refs(self) -> None:
        """Test ExternalDocsRefValidator validates externalDocs references in channels."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0"},
            channels={
                "user_signup": {
                    "address": "user/signup",
                    "externalDocs": {"$ref": "#/components/externalDocs/channel"},
                }
            },
            components={
                "externalDocs": {
                    "channel": {"url": "https://example.com/channel"},
                },
            },
            extra_validators=[ExternalDocsRefValidator],
        )
        assert spec is not None

    def test_external_docs_ref_validator_validates_operations_refs(self) -> None:
        """Test ExternalDocsRefValidator validates externalDocs references in operations."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0"},
            operations={
                "signup": {
                    "action": "receive",
                    "channel": {"$ref": "#/channels/user_signup"},
                    "externalDocs": {"$ref": "#/components/externalDocs/op"},
                }
            },
            channels={"user_signup": {"address": "user/signup"}},
            components={
                "externalDocs": {
                    "op": {"url": "https://example.com/op"},
                },
            },
            extra_validators=[ExternalDocsRefValidator],
        )
        assert spec is not None

    def test_external_docs_ref_validator_validates_messages_refs(self) -> None:
        """Test ExternalDocsRefValidator validates externalDocs references in messages."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0"},
            channels={
                "test": {
                    "address": "test",
                    "messages": {
                        "msg": {
                            "payload": {"type": "string"},
                            "externalDocs": {"$ref": "#/components/externalDocs/msg"},
                        }
                    },
                }
            },
            components={
                "externalDocs": {
                    "msg": {"url": "https://example.com/msg"},
                },
            },
            extra_validators=[ExternalDocsRefValidator],
        )
        assert spec is not None

    def test_external_docs_ref_validator_validates_tags_refs(self) -> None:
        """Test ExternalDocsRefValidator validates externalDocs references in tags."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={
                "title": "Test",
                "version": "1.0",
                "tags": [
                    {
                        "name": "tag1",
                        "externalDocs": {"$ref": "#/components/externalDocs/tag"},
                    }
                ],
            },
            components={
                "externalDocs": {
                    "tag": {"url": "https://example.com/tag"},
                },
            },
            extra_validators=[ExternalDocsRefValidator],
        )
        assert spec is not None

    def test_external_docs_ref_validator_validates_components_tags_refs(self) -> None:
        """Test ExternalDocsRefValidator validates externalDocs references in components tags."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0"},
            components={
                "tags": {
                    "t1": {
                        "name": "t1",
                        "externalDocs": {"$ref": "#/components/externalDocs/tag"},
                    }
                },
                "externalDocs": {
                    "tag": {"url": "https://example.com/tag"},
                },
            },
            extra_validators=[ExternalDocsRefValidator],
        )
        assert spec is not None

    def test_external_docs_ref_validator_validates_schemas_refs(self) -> None:
        """Test ExternalDocsRefValidator validates externalDocs references in schemas."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0"},
            components={
                "schemas": {
                    "User": {
                        "type": "object",
                        "externalDocs": {"$ref": "#/components/externalDocs/schema"},
                    }
                },
                "externalDocs": {
                    "schema": {"url": "https://example.com/schema"},
                },
            },
            extra_validators=[ExternalDocsRefValidator],
        )
        assert spec is not None

    def test_external_docs_ref_validator_external_warning(
        self, caplog: LogCaptureFixture
    ) -> None:
        """Test ExternalDocsRefValidator logs warning for external references."""
        with caplog.at_level(logging.WARNING):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={
                    "title": "Test",
                    "version": "1.0",
                    "externalDocs": {"$ref": "https://example.com/external.json"},
                },
                extra_validators=[ExternalDocsRefValidator],
            )
        assert "is external. Cannot validate external references" in caplog.text

    def test_external_docs_ref_validator_validates_operation_traits_refs(self) -> None:
        """Test ExternalDocsRefValidator validates externalDocs references in operation traits."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0"},
            components={
                "operationTraits": {
                    "trait1": {
                        "externalDocs": {"$ref": "#/components/externalDocs/trait"},
                    }
                },
                "externalDocs": {
                    "trait": {"url": "https://example.com/trait"},
                },
            },
            extra_validators=[ExternalDocsRefValidator],
        )
        assert spec is not None

    def test_external_docs_ref_validator_validates_message_traits_refs(self) -> None:
        """Test ExternalDocsRefValidator validates externalDocs references in message traits."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0"},
            components={
                "messageTraits": {
                    "trait1": {
                        "externalDocs": {"$ref": "#/components/externalDocs/trait"},
                    }
                },
                "externalDocs": {
                    "trait": {"url": "https://example.com/trait"},
                },
            },
            extra_validators=[ExternalDocsRefValidator],
        )
        assert spec is not None

    def test_external_docs_ref_validator_validates_components_refs(self) -> None:
        """Test ExternalDocsRefValidator validates externalDocs references in components.externalDocs."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0"},
            components={
                "externalDocs": {
                    "doc1": {"$ref": "#/components/externalDocs/doc2"},
                    "doc2": {"url": "https://example.com/2"},
                },
            },
            extra_validators=[ExternalDocsRefValidator],
        )
        assert spec is not None

    def test_external_docs_ref_validator_validates_components_servers_refs(
        self,
    ) -> None:
        """Test ExternalDocsRefValidator validates externalDocs references in components servers."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0"},
            components={
                "servers": {
                    "s1": {
                        "host": "h1",
                        "protocol": "mqtt",
                        "externalDocs": {"$ref": "#/components/externalDocs/d1"},
                    }
                },
                "externalDocs": {
                    "d1": {"url": "https://example.com/d1"},
                },
            },
            extra_validators=[ExternalDocsRefValidator],
        )
        assert spec is not None

    def test_external_docs_ref_validator_validates_components_channels_refs(
        self,
    ) -> None:
        """Test ExternalDocsRefValidator validates externalDocs references in components channels."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0"},
            components={
                "channels": {
                    "c1": {
                        "address": "a1",
                        "externalDocs": {"$ref": "#/components/externalDocs/d1"},
                    }
                },
                "externalDocs": {
                    "d1": {"url": "https://example.com/d1"},
                },
            },
            extra_validators=[ExternalDocsRefValidator],
        )
        assert spec is not None

    def test_external_docs_ref_validator_validates_components_operations_refs(
        self,
    ) -> None:
        """Test ExternalDocsRefValidator validates externalDocs references in components operations."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0"},
            components={
                "operations": {
                    "o1": {
                        "action": "receive",
                        "channel": {"$ref": "#/components/channels/c1"},
                        "externalDocs": {"$ref": "#/components/externalDocs/d1"},
                    }
                },
                "channels": {"c1": {"address": "a1"}},
                "externalDocs": {
                    "d1": {"url": "https://example.com/d1"},
                },
            },
            extra_validators=[ExternalDocsRefValidator],
        )
        assert spec is not None

    def test_external_docs_ref_validator_validates_components_messages_refs(
        self,
    ) -> None:
        """Test ExternalDocsRefValidator validates externalDocs references in components messages."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test", "version": "1.0"},
            components={
                "messages": {
                    "m1": {
                        "payload": {"type": "string"},
                        "externalDocs": {"$ref": "#/components/externalDocs/d1"},
                    }
                },
                "externalDocs": {
                    "d1": {"url": "https://example.com/d1"},
                },
            },
            extra_validators=[ExternalDocsRefValidator],
        )
        assert spec is not None
