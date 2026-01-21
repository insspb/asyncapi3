"""Tests for TagsRefValidator."""

import logging

import pytest

from _pytest.logging import LogCaptureFixture

from asyncapi3.models.asyncapi import AsyncAPI3
from asyncapi3.validators import TagsRefValidator


class TestTagsRefValidator:
    """Tests for TagsRefValidator."""

    def test_tags_ref_validator_validates_info_tags_refs(self) -> None:
        """Test TagsRefValidator validates tag references in info object."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={
                "title": "Test API",
                "version": "1.0.0",
                "tags": [{"$ref": "#/components/tags/prod"}],
            },
            components={
                "tags": {
                    "prod": {
                        "name": "prod",
                        "description": "Production environment",
                    },
                },
            },
            extra_validators=[TagsRefValidator],
        )

        # run_extra_processors called automatically during creation
        # Should not raise any errors
        assert spec is not None

    def test_tags_ref_validator_invalid_info_tags_ref_path(self) -> None:
        """Test TagsRefValidator raises error for invalid info tags reference path."""
        with pytest.raises(ValueError, match="must point to #/components/tags/"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={
                    "title": "Test API",
                    "version": "1.0.0",
                    "tags": [{"$ref": "#/tags/prod"}],  # Wrong path
                },
                components={
                    "tags": {
                        "prod": {
                            "name": "prod",
                            "description": "Production environment",
                        },
                    },
                },
                extra_validators=[TagsRefValidator],
            )

    def test_tags_ref_validator_info_tags_ref_to_nonexistent_tag(self) -> None:
        """Test TagsRefValidator raises error when info references nonexistent tag."""
        with pytest.raises(ValueError, match="does not exist in components/tags"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={
                    "title": "Test API",
                    "version": "1.0.0",
                    "tags": [{"$ref": "#/components/tags/nonexistent"}],
                },
                components={
                    "tags": {
                        "existing": {
                            "name": "existing",
                            "description": "Existing tag",
                        },
                    },
                },
                extra_validators=[TagsRefValidator],
            )

    def test_tags_ref_validator_validates_channels_tags_refs(self) -> None:
        """Test TagsRefValidator validates tag references in root channels."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            channels={
                "test": {
                    "address": "/test",
                    "tags": [{"$ref": "#/components/tags/prod"}],
                },
            },
            components={
                "tags": {
                    "prod": {
                        "name": "prod",
                        "description": "Production environment",
                    },
                },
            },
            extra_validators=[TagsRefValidator],
        )

        # run_extra_processors called automatically during creation
        # Should not raise any errors
        assert spec is not None

    def test_tags_ref_validator_invalid_channels_tags_ref_path(self) -> None:
        """Test TagsRefValidator raises error for invalid channels tags reference path."""
        with pytest.raises(ValueError, match="must point to #/components/tags/"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                channels={
                    "test": {
                        "address": "/test",
                        "tags": [{"$ref": "#/tags/prod"}],  # Wrong path
                    },
                },
                components={
                    "tags": {
                        "prod": {
                            "name": "prod",
                            "description": "Production environment",
                        },
                    },
                },
                extra_validators=[TagsRefValidator],
            )

    def test_tags_ref_validator_channels_tags_ref_to_nonexistent_tag(self) -> None:
        """Test TagsRefValidator raises error when channel references nonexistent tag."""
        with pytest.raises(ValueError, match="does not exist in components/tags"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                channels={
                    "test": {
                        "address": "/test",
                        "tags": [{"$ref": "#/components/tags/nonexistent"}],
                    },
                },
                components={
                    "tags": {
                        "existing": {
                            "name": "existing",
                            "description": "Existing tag",
                        },
                    },
                },
                extra_validators=[TagsRefValidator],
            )

    def test_tags_ref_validator_validates_operations_tags_refs(self) -> None:
        """Test TagsRefValidator validates tag references in root operations."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            operations={
                "sendMessage": {
                    "action": "send",
                    "channel": {"$ref": "#/channels/test"},
                    "tags": [{"$ref": "#/components/tags/prod"}],
                },
            },
            channels={
                "test": {"address": "/test"},
            },
            components={
                "tags": {
                    "prod": {
                        "name": "prod",
                        "description": "Production environment",
                    },
                },
            },
            extra_validators=[TagsRefValidator],
        )

        # run_extra_processors called automatically during creation
        # Should not raise any errors
        assert spec is not None

    def test_tags_ref_validator_invalid_operations_tags_ref_path(self) -> None:
        """Test TagsRefValidator raises error for invalid operations tags reference path."""
        with pytest.raises(ValueError, match="must point to #/components/tags/"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                operations={
                    "sendMessage": {
                        "action": "send",
                        "channel": {"$ref": "#/channels/test"},
                        "tags": [{"$ref": "#/tags/prod"}],  # Wrong path
                    },
                },
                channels={
                    "test": {"address": "/test"},
                },
                components={
                    "tags": {
                        "prod": {
                            "name": "prod",
                            "description": "Production environment",
                        },
                    },
                },
                extra_validators=[TagsRefValidator],
            )

    def test_tags_ref_validator_operations_tags_ref_to_nonexistent_tag(self) -> None:
        """Test TagsRefValidator raises error when operation references nonexistent tag."""
        with pytest.raises(ValueError, match="does not exist in components/tags"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                operations={
                    "sendMessage": {
                        "action": "send",
                        "channel": {"$ref": "#/channels/test"},
                        "tags": [{"$ref": "#/components/tags/nonexistent"}],
                    },
                },
                channels={
                    "test": {"address": "/test"},
                },
                components={
                    "tags": {
                        "existing": {
                            "name": "existing",
                            "description": "Existing tag",
                        },
                    },
                },
                extra_validators=[TagsRefValidator],
            )

    def test_tags_ref_validator_validates_servers_tags_refs(self) -> None:
        """Test TagsRefValidator validates tag references in root servers."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            servers={
                "prod": {
                    "host": "api.example.com",
                    "protocol": "https",
                    "tags": [{"$ref": "#/components/tags/prod"}],
                },
            },
            components={
                "tags": {
                    "prod": {
                        "name": "prod",
                        "description": "Production environment",
                    },
                },
            },
            extra_validators=[TagsRefValidator],
        )

        # run_extra_processors called automatically during creation
        # Should not raise any errors
        assert spec is not None

    def test_tags_ref_validator_invalid_servers_tags_ref_path(self) -> None:
        """Test TagsRefValidator raises error for invalid servers tags reference path."""
        with pytest.raises(ValueError, match="must point to #/components/tags/"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                servers={
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                        "tags": [{"$ref": "#/tags/prod"}],  # Wrong path
                    },
                },
                components={
                    "tags": {
                        "prod": {
                            "name": "prod",
                            "description": "Production environment",
                        },
                    },
                },
                extra_validators=[TagsRefValidator],
            )

    def test_tags_ref_validator_servers_tags_ref_to_nonexistent_tag(self) -> None:
        """Test TagsRefValidator raises error when server references nonexistent tag."""
        with pytest.raises(ValueError, match="does not exist in components/tags"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                servers={
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                        "tags": [{"$ref": "#/components/tags/nonexistent"}],
                    },
                },
                components={
                    "tags": {
                        "existing": {
                            "name": "existing",
                            "description": "Existing tag",
                        },
                    },
                },
                extra_validators=[TagsRefValidator],
            )

    def test_tags_ref_validator_validates_components_messages_tags_refs(self) -> None:
        """Test TagsRefValidator validates tag references in components messages."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            components={
                "messages": {
                    "testMessage": {
                        "payload": {"type": "string"},
                        "tags": [{"$ref": "#/components/tags/prod"}],
                    },
                },
                "tags": {
                    "prod": {
                        "name": "prod",
                        "description": "Production environment",
                    },
                },
            },
            extra_validators=[TagsRefValidator],
        )

        # run_extra_processors called automatically during creation
        # Should not raise any errors
        assert spec is not None

    def test_tags_ref_validator_components_messages_tags_ref_to_nonexistent_tag(
        self,
    ) -> None:
        """Test TagsRefValidator raises error when components message references nonexistent tag."""
        with pytest.raises(ValueError, match="does not exist in components/tags"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                components={
                    "messages": {
                        "testMessage": {
                            "payload": {"type": "string"},
                            "tags": [{"$ref": "#/components/tags/nonexistent"}],
                        },
                    },
                    "tags": {
                        "existing": {
                            "name": "existing",
                            "description": "Existing tag",
                        },
                    },
                },
                extra_validators=[TagsRefValidator],
            )

    def test_tags_ref_validator_validates_components_channels_tags_refs(self) -> None:
        """Test TagsRefValidator validates tag references in components channels."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            components={
                "channels": {
                    "test": {
                        "address": "/test",
                        "tags": [{"$ref": "#/components/tags/prod"}],
                    },
                },
                "tags": {
                    "prod": {
                        "name": "prod",
                        "description": "Production environment",
                    },
                },
            },
            extra_validators=[TagsRefValidator],
        )

        # run_extra_processors called automatically during creation
        # Should not raise any errors
        assert spec is not None

    def test_tags_ref_validator_components_channels_tags_ref_to_nonexistent_tag(
        self,
    ) -> None:
        """Test TagsRefValidator raises error when components channel references nonexistent tag."""
        with pytest.raises(ValueError, match="does not exist in components/tags"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                components={
                    "channels": {
                        "test": {
                            "address": "/test",
                            "tags": [{"$ref": "#/components/tags/nonexistent"}],
                        },
                    },
                    "tags": {
                        "existing": {
                            "name": "existing",
                            "description": "Existing tag",
                        },
                    },
                },
                extra_validators=[TagsRefValidator],
            )

    def test_tags_ref_validator_validates_components_operations_tags_refs(self) -> None:
        """Test TagsRefValidator validates tag references in components operations."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            channels={
                "test": {"address": "/test"},
            },
            components={
                "operations": {
                    "sendMessage": {
                        "action": "send",
                        "channel": {"$ref": "#/channels/test"},
                        "tags": [{"$ref": "#/components/tags/prod"}],
                    },
                },
                "tags": {
                    "prod": {
                        "name": "prod",
                        "description": "Production environment",
                    },
                },
            },
            extra_validators=[TagsRefValidator],
        )

        # run_extra_processors called automatically during creation
        # Should not raise any errors
        assert spec is not None

    def test_tags_ref_validator_components_operations_tags_ref_to_nonexistent_tag(
        self,
    ) -> None:
        """Test TagsRefValidator raises error when components operation references nonexistent tag."""
        with pytest.raises(ValueError, match="does not exist in components/tags"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                channels={
                    "test": {"address": "/test"},
                },
                components={
                    "operations": {
                        "sendMessage": {
                            "action": "send",
                            "channel": {"$ref": "#/channels/test"},
                            "tags": [{"$ref": "#/components/tags/nonexistent"}],
                        },
                    },
                    "tags": {
                        "existing": {
                            "name": "existing",
                            "description": "Existing tag",
                        },
                    },
                },
                extra_validators=[TagsRefValidator],
            )

    def test_tags_ref_validator_info_without_tags_attr(self) -> None:
        """Test TagsRefValidator handles info without tags attribute."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={
                "title": "Test API",
                "version": "1.0.0",
                # No tags attribute
            },
            extra_validators=[TagsRefValidator],
        )

        # Should not raise any errors - info without tags is skipped
        assert spec is not None

    def test_tags_ref_validator_info_empty_tags(self) -> None:
        """Test TagsRefValidator handles info with empty tags list."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={
                "title": "Test API",
                "version": "1.0.0",
                "tags": [],  # Empty tags list
            },
            extra_validators=[TagsRefValidator],
        )

        # Should not raise any errors - empty tags are skipped
        assert spec is not None

    def test_tags_ref_validator_channels_without_tags_attr(self) -> None:
        """Test TagsRefValidator handles channels without tags attribute."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            channels={
                "test": {
                    "address": "/test",
                    # No tags attribute
                },
            },
            extra_validators=[TagsRefValidator],
        )

        # Should not raise any errors - channels without tags are skipped
        assert spec is not None

    def test_tags_ref_validator_channels_empty_tags(self) -> None:
        """Test TagsRefValidator handles channels with empty tags list."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            channels={
                "test": {
                    "address": "/test",
                    "tags": [],  # Empty tags list
                },
            },
            extra_validators=[TagsRefValidator],
        )

        # Should not raise any errors - empty tags are skipped
        assert spec is not None

    def test_tags_ref_validator_external_info_tags_ref_warning(
        self, caplog: LogCaptureFixture
    ) -> None:
        """Test TagsRefValidator logs warning for external info tags reference."""
        with caplog.at_level(logging.WARNING):
            spec = AsyncAPI3(
                asyncapi="3.0.0",
                info={
                    "title": "Test API",
                    "version": "1.0.0",
                    "tags": [{"$ref": "https://external.example.com/tags/prod"}],
                },
                extra_validators=[TagsRefValidator],
            )

        # Should not raise error but log warning
        assert spec is not None
        assert any(
            "is external. Cannot validate external references" in record.message
            for record in caplog.records
        )

    def test_tags_ref_validator_tags_with_inline_objects_and_refs(self) -> None:
        """Test TagsRefValidator handles mixed inline tag objects and references."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={
                "title": "Test API",
                "version": "1.0.0",
                "tags": [
                    {"name": "inline", "description": "Inline tag"},  # Inline object
                    {"$ref": "#/components/tags/prod"},  # Reference
                ],
            },
            components={
                "tags": {
                    "prod": {
                        "name": "prod",
                        "description": "Production environment",
                    },
                },
            },
            extra_validators=[TagsRefValidator],
        )

        # Should not raise any errors - only references are validated, inline objects are ignored
        assert spec is not None

    def test_tags_ref_validator_missing_components_tags(self) -> None:
        """Test TagsRefValidator raises error when referencing tags but components.tags doesn't exist."""
        with pytest.raises(ValueError, match="does not exist in components/tags"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={
                    "title": "Test API",
                    "version": "1.0.0",
                    "tags": [{"$ref": "#/components/tags/prod"}],
                },
                components={
                    # No tags in components
                },
                extra_validators=[TagsRefValidator],
            )
