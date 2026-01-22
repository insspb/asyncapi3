"""Tests for ChannelsManager."""

import pytest

from asyncapi3.managers import ChannelsManager
from asyncapi3.models.asyncapi import AsyncAPI3
from asyncapi3.models.channel import Channel


class TestChannelsManager:
    """Tests for ChannelsManager."""

    def test_channels_manager_processes_root_channels(self) -> None:
        """Test ChannelsManager moves channels from root to components and creates references."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            channels={
                "userSignup": Channel(
                    address="user/signup",
                    description="User signup channel",
                ),
                "userLogin": Channel(
                    address="user/login",
                    description="User login channel",
                ),
            },
            extra_converters=[ChannelsManager],
        )

        # After model validation and ChannelsManager processing, channels should be moved
        # to components and replaced with references
        spec_data = spec.model_dump()

        assert "channels" in spec_data["components"]
        assert len(spec_data["components"]["channels"]) == 2

        # Check that references point to existing channels
        for channel_name, channel_ref in spec_data["channels"].items():
            assert channel_ref["$ref"] == f"#/components/channels/{channel_name}"

    def test_channels_manager_preserves_existing_references(self) -> None:
        """Test ChannelsManager preserves existing references in root channels."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            channels={
                "userSignup": {
                    "$ref": "#/components/channels/userSignupChannel",
                },
            },
            extra_converters=[ChannelsManager],
        )

        # Existing references should be preserved
        spec_data = spec.model_dump()
        assert (
            spec_data["channels"]["userSignup"]["$ref"]
            == "#/components/channels/userSignupChannel"
        )

    def test_channels_manager_handles_duplicate_channel_names(self) -> None:
        """Test ChannelsManager raises error for duplicate channel names with different content."""
        with pytest.raises(
            ValueError,
            match=(
                r"Value error, Channel name conflict detected: 'userSignup' already exists "
                r"with different content."
            ),
        ):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                channels={
                    "userSignup": {
                        "address": "user/signup",
                        "description": "User signup channel",
                    },
                },
                components={
                    "channels": {
                        "userSignup": {
                            "address": "user/different",  # Different content
                            "description": "Different signup channel",
                        },
                    },
                },
                extra_converters=[ChannelsManager],
            )

    def test_channels_manager_allows_identical_duplicate_channels(self) -> None:
        """Test ChannelsManager allows duplicate channel names with identical content."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            channels={
                "userSignup": {
                    "address": "user/signup",
                    "description": "User signup channel",
                },
            },
            components={
                "channels": {
                    "userSignup": {
                        "address": "user/signup",
                        "description": "User signup channel",
                    },
                },
            },
            extra_converters=[ChannelsManager],
        )

        # Should not raise an error for identical content
        spec_data = spec.model_dump()
        channel_ref = spec_data["channels"]["userSignup"]["$ref"]
        assert channel_ref == "#/components/channels/userSignup"
