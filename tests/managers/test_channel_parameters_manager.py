"""Tests for ChannelParametersManager."""

import pytest

from pydantic import ValidationError

from asyncapi3.managers import ChannelParametersManager
from asyncapi3.models.asyncapi import AsyncAPI3
from asyncapi3.models.channel import Channel, Channels, Parameter


class TestChannelParametersManager:
    """Tests for ChannelParametersManager."""

    def test_channel_parameters_manager_processes_root_channels_parameters(
        self,
    ) -> None:
        """Test ChannelParametersManager moves parameters from root channels to components and creates references."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            channels={
                "user_userId": Channel(
                    address="user/{userId}",
                    parameters={
                        "userId": Parameter(
                            description="User ID parameter",
                        ),
                    },
                ),
            },
            extra_converters=[ChannelParametersManager],
        )

        # After model validation and ChannelParametersManager processing, parameters should be moved
        # to components and replaced with references
        spec_data = spec.model_dump()

        assert "parameters" in spec_data["components"]
        assert len(spec_data["components"]["parameters"]) == 1

        # Check that channel parameter reference points to existing parameter
        channel_parameters = spec_data["channels"]["user_userId"]["parameters"]
        parameter_ref = channel_parameters["userId"]["$ref"]
        assert parameter_ref == "#/components/parameters/userId"

        # Check that the parameter was moved to components
        assert "userId" in spec_data["components"]["parameters"]

    def test_channel_parameters_manager_processes_components_channels_parameters(
        self,
    ) -> None:
        """Test ChannelParametersManager processes parameters in components channels."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            components={
                "channels": Channels(
                    {
                        "order_orderId": Channel(
                            address="order/{orderId}",
                            parameters={
                                "orderId": Parameter(
                                    description="Order ID parameter",
                                ),
                            },
                        ),
                    }
                ),
            },
            extra_converters=[ChannelParametersManager],
        )

        # Parameters should be moved from components channels to components parameters
        spec_data = spec.model_dump()

        assert "parameters" in spec_data["components"]
        assert len(spec_data["components"]["parameters"]) == 1

        # Check that channel parameter reference points to existing parameter
        channel_parameters = spec_data["components"]["channels"]["order_orderId"][
            "parameters"
        ]
        parameter_ref = channel_parameters["orderId"]["$ref"]
        assert parameter_ref == "#/components/parameters/orderId"

    def test_channel_parameters_manager_preserves_existing_references(self) -> None:
        """Test ChannelParametersManager preserves existing references in channel parameters."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            channels={
                "user_userId": Channel(
                    address="user/{userId}",
                    parameters={
                        "userId": {"$ref": "#/components/parameters/existingParameter"},
                    },
                ),
            },
            extra_converters=[ChannelParametersManager],
        )

        # Existing references should be preserved
        spec_data = spec.model_dump()
        channel_parameters = spec_data["channels"]["user_userId"]["parameters"]
        parameter_ref = channel_parameters["userId"]["$ref"]
        assert parameter_ref == "#/components/parameters/existingParameter"

    def test_channel_parameters_manager_handles_external_parameter_reference(
        self,
    ) -> None:
        """Test ChannelParametersManager handles external parameter references in components."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            components={
                "parameters": {
                    "externalParam": {"$ref": "https://example.com/parameter.json"},
                },
            },
            channels={
                "user_userId": Channel(
                    address="user/{userId}",
                    parameters={
                        "localParam": Parameter(
                            description="Local parameter",
                        ),
                    },
                ),
            },
            extra_converters=[ChannelParametersManager],
        )

        # External reference should be preserved, new parameter should be added
        spec_data = spec.model_dump()

        # Should have external reference and new local parameter
        assert len(spec_data["components"]["parameters"]) == 2
        assert (
            spec_data["components"]["parameters"]["externalParam"]["$ref"]
            == "https://example.com/parameter.json"
        )
        assert "localParam" in spec_data["components"]["parameters"]

        # Channel should reference the local parameter
        channel_parameters = spec_data["channels"]["user_userId"]["parameters"]
        local_ref = channel_parameters["localParam"]["$ref"]
        assert local_ref == "#/components/parameters/localParam"

    def test_channel_parameters_manager_handles_duplicate_parameters(self) -> None:
        """Test ChannelParametersManager deduplicates identical parameters."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            channels={
                "user_userId": Channel(
                    address="user/{userId}",
                    parameters={
                        "userId": Parameter(
                            description="User ID parameter",
                        ),
                    },
                ),
                "admin_userId": Channel(
                    address="admin/{userId}",
                    parameters={
                        "userId": Parameter(
                            description="User ID parameter",  # Identical
                        ),
                    },
                ),
            },
            extra_converters=[ChannelParametersManager],
        )

        # Identical parameters should be deduplicated
        spec_data = spec.model_dump()

        assert "parameters" in spec_data["components"]
        # Only one parameter should be stored in components (deduplicated)
        assert len(spec_data["components"]["parameters"]) == 1

        # Both channels should reference the same parameter
        user_params = spec_data["channels"]["user_userId"]["parameters"]
        admin_params = spec_data["channels"]["admin_userId"]["parameters"]

        assert user_params["userId"]["$ref"] == "#/components/parameters/userId"
        assert admin_params["userId"]["$ref"] == "#/components/parameters/userId"

    def test_channel_parameters_manager_handles_duplicate_names_different_content(
        self,
    ) -> None:
        """Test ChannelParametersManager raises error for duplicate parameter names with different content."""
        with pytest.raises(
            ValidationError,
            match=r"Parameter name conflict: 'userId' already exists",
        ):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={"title": "Test API", "version": "1.0.0"},
                channels={
                    "user_userId": Channel(
                        address="user/{userId}",
                        parameters={
                            "userId": Parameter(
                                description="User ID parameter",
                            ),
                        },
                    ),
                    "admin_userId": Channel(
                        address="admin/{userId}",
                        parameters={
                            "userId": Parameter(  # Same name but different content
                                description="Different user ID parameter",  # Different description
                            ),
                        },
                    ),
                },
                extra_converters=[ChannelParametersManager],
            )

    def test_channel_parameters_manager_multiple_parameters_in_channel(self) -> None:
        """Test ChannelParametersManager handles multiple parameters in a single channel."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            channels={
                "user_userId_post_postId": Channel(
                    address="user/{userId}/post/{postId}",
                    parameters={
                        "userId": Parameter(
                            description="User ID parameter",
                        ),
                        "postId": Parameter(
                            description="Post ID parameter",
                        ),
                    },
                ),
            },
            extra_converters=[ChannelParametersManager],
        )

        # Both parameters should be moved to components
        spec_data = spec.model_dump()

        assert "parameters" in spec_data["components"]
        assert len(spec_data["components"]["parameters"]) == 2

        # Channel should have two parameter references
        channel_parameters = spec_data["channels"]["user_userId_post_postId"][
            "parameters"
        ]
        assert len(channel_parameters) == 2

        # Check parameter references
        user_id_ref = channel_parameters["userId"]["$ref"]
        post_id_ref = channel_parameters["postId"]["$ref"]

        assert user_id_ref == "#/components/parameters/userId"
        assert post_id_ref == "#/components/parameters/postId"
