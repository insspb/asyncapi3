"""Tests for ChannelMessagesManager."""

import pytest

from pydantic import ValidationError

from asyncapi3.managers import ChannelMessagesManager
from asyncapi3.models.asyncapi import AsyncAPI3
from asyncapi3.models.channel import Channel
from asyncapi3.models.message import Message


class TestChannelMessagesManager:
    """Tests for ChannelMessagesManager."""

    def test_channel_messages_manager_processes_root_channels_messages(self) -> None:
        """Test ChannelMessagesManager moves messages from root channels to components and creates references."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            channels={
                "userSignup": Channel(
                    address="user/signup",
                    messages={
                        "userData": Message(
                            name="userData",
                            title="User Data Message",
                            payload={"type": "object"},
                        ),
                    },
                ),
            },
            extra_converters=[ChannelMessagesManager],
        )

        # After model validation and ChannelMessagesManager processing, messages should be moved
        # to components and replaced with references
        spec_data = spec.model_dump()

        assert "messages" in spec_data["components"]
        assert len(spec_data["components"]["messages"]) == 1

        # Check that channel message reference points to existing message
        channel_messages = spec_data["channels"]["userSignup"]["messages"]
        message_ref = channel_messages["userData"]["$ref"]
        assert message_ref == "#/components/messages/userData"

        # Check that the message was moved to components
        assert "userData" in spec_data["components"]["messages"]

    def test_channel_messages_manager_processes_components_channels_messages(
        self,
    ) -> None:
        """Test ChannelMessagesManager processes messages in components channels."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            components={
                "channels": {
                    "userLogin": {
                        "address": "user/login",
                        "messages": {
                            "loginData": {
                                "name": "loginData",
                                "title": "Login Data Message",
                                "payload": {"type": "object"},
                            },
                        },
                    },
                },
            },
            extra_converters=[ChannelMessagesManager],
        )

        # Messages should be moved from components channels to components messages
        spec_data = spec.model_dump()

        assert "messages" in spec_data["components"]
        assert len(spec_data["components"]["messages"]) == 1

        # Check that channel message reference points to existing message
        channel_messages = spec_data["components"]["channels"]["userLogin"]["messages"]
        message_ref = channel_messages["loginData"]["$ref"]
        assert message_ref == "#/components/messages/loginData"

    def test_channel_messages_manager_preserves_existing_references(self) -> None:
        """Test ChannelMessagesManager preserves existing references in channel messages."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            channels={
                "userSignup": Channel(
                    address="user/signup",
                    messages={
                        "userData": {"$ref": "#/components/messages/existingMessage"},
                    },
                ),
            },
            extra_converters=[ChannelMessagesManager],
        )

        # Existing references should be preserved
        spec_data = spec.model_dump()
        channel_messages = spec_data["channels"]["userSignup"]["messages"]
        message_ref = channel_messages["userData"]["$ref"]
        assert message_ref == "#/components/messages/existingMessage"

    def test_channel_messages_manager_handles_external_message_reference(self) -> None:
        """Test ChannelMessagesManager handles external message references in components."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            components={
                "messages": {
                    "externalMessage": {"$ref": "https://example.com/message.json"},
                },
            },
            channels={
                "userSignup": Channel(
                    address="user/signup",
                    messages={
                        "localMessage": Message(
                            name="localMessage",
                            title="Local Message",
                            payload={"type": "object"},
                        ),
                    },
                ),
            },
            extra_converters=[ChannelMessagesManager],
        )

        # External reference should be preserved, new message should be added
        spec_data = spec.model_dump()

        # Should have external reference and new local message
        assert len(spec_data["components"]["messages"]) == 2
        assert (
            spec_data["components"]["messages"]["externalMessage"]["$ref"]
            == "https://example.com/message.json"
        )
        assert "localMessage" in spec_data["components"]["messages"]

        # Channel should reference the local message
        channel_messages = spec_data["channels"]["userSignup"]["messages"]
        local_ref = channel_messages["localMessage"]["$ref"]
        assert local_ref == "#/components/messages/localMessage"

    def test_channel_messages_manager_handles_duplicate_messages(self) -> None:
        """Test ChannelMessagesManager deduplicates identical messages."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            channels={
                "userSignup": Channel(
                    address="user/signup",
                    messages={
                        "userData": Message(
                            name="userData",
                            title="User Data Message",
                            payload={"type": "object"},
                        ),
                    },
                ),
                "userUpdate": Channel(
                    address="user/update",
                    messages={
                        "userData": Message(
                            name="userData",  # Same name but identical content
                            title="User Data Message",
                            payload={"type": "object"},
                        ),
                    },
                ),
            },
            extra_converters=[ChannelMessagesManager],
        )

        # Identical messages should be deduplicated
        spec_data = spec.model_dump()

        assert "messages" in spec_data["components"]
        # Only one message should be stored in components (deduplicated)
        assert len(spec_data["components"]["messages"]) == 1

        # Both channels should reference the same message
        signup_messages = spec_data["channels"]["userSignup"]["messages"]
        update_messages = spec_data["channels"]["userUpdate"]["messages"]

        assert signup_messages["userData"]["$ref"] == "#/components/messages/userData"
        assert update_messages["userData"]["$ref"] == "#/components/messages/userData"

    def test_channel_messages_manager_multiple_messages_in_channel(self) -> None:
        """Test ChannelMessagesManager handles multiple messages in a single channel."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            channels={
                "userEvents": Channel(
                    address="user/events",
                    messages={
                        "userCreated": Message(
                            name="userCreated",
                            title="User Created Event",
                            payload={"type": "object"},
                        ),
                        "userUpdated": Message(
                            name="userUpdated",
                            title="User Updated Event",
                            payload={"type": "object"},
                        ),
                    },
                ),
            },
            extra_converters=[ChannelMessagesManager],
        )

        # Both messages should be moved to components
        spec_data = spec.model_dump()

        assert "messages" in spec_data["components"]
        assert len(spec_data["components"]["messages"]) == 2

        # Channel should have two message references
        channel_messages = spec_data["channels"]["userEvents"]["messages"]
        assert len(channel_messages) == 2

        # Check message references
        created_ref = channel_messages["userCreated"]["$ref"]
        updated_ref = channel_messages["userUpdated"]["$ref"]

        assert created_ref == "#/components/messages/userCreated"
        assert updated_ref == "#/components/messages/userUpdated"

    def test_channel_messages_manager_handles_duplicate_names_different_content(
        self,
    ) -> None:
        """Test ChannelMessagesManager raises error for duplicate message names with different content."""
        with pytest.raises(
            ValidationError,
            match=r"Message name conflict detected: 'userData' already exists",
        ):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                channels={
                    "userSignup": Channel(
                        address="user/signup",
                        messages={
                            "userData": Message(
                                name="userData",
                                title="User Data Message",
                                payload={"type": "object"},
                            ),
                        },
                    ),
                    "userUpdate": Channel(
                        address="user/update",
                        messages={
                            "userData": Message(  # Same name but different content
                                name="userData",
                                title="Different User Data Message",  # Different title
                                payload={"type": "string"},  # Different payload
                            ),
                        },
                    ),
                },
                extra_converters=[ChannelMessagesManager],
            )
