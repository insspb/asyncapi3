"""Tests for channel models."""

from typing import Any

import pytest
import yaml

from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.base import Reference
from asyncapi3.models.channel import Channel, Channels, Parameter, Parameters


# Channels Validation Test Cases
def case_channels_basic() -> str:
    """Channels with basic channel objects."""
    return """
    channels:
      userChannel:
        address: user/signedup
      adminChannel:
        address: admin/events
    """


def case_channels_with_references() -> str:
    """Channels with references."""
    return """
    channels:
      userChannel:
        $ref: '#/components/channels/userChannel'
      adminChannel:
        $ref: '#/components/channels/adminChannel'
    """


# Channels Validation Error Test Cases
def case_channels_invalid_key_spaces() -> tuple[str, str]:
    """Channels with key containing spaces - should fail validation."""
    yaml_data = """
    channels:
      user channel:
        address: user/signedup
    """
    expected_error = "Field 'user channel' does not match patterned object key pattern. Keys must match \\[A-Za-z0-9\\\\\\.\\\\-_\\]\\+"
    return yaml_data, expected_error


def case_channels_invalid_key_special_chars() -> tuple[str, str]:
    """Channels with key containing special characters - should fail validation."""
    yaml_data = """
    channels:
      user@channel:
        address: user/signedup
    """
    expected_error = "Field 'user@channel' does not match patterned object key pattern. Keys must match \\[A-Za-z0-9\\\\\\.\\\\-_\\]\\+"
    return yaml_data, expected_error


def case_channels_invalid_key_parentheses() -> tuple[str, str]:
    """Channels with key containing parentheses - should fail validation."""
    yaml_data = """
    channels:
      user(channel):
        address: user/signedup
    """
    expected_error = "Field 'user\\(channel\\)' does not match patterned object key pattern. Keys must match \\[A-Za-z0-9\\\\\\.\\\\-_\\]\\+"
    return yaml_data, expected_error


# Parameter Validation Test Cases
def case_parameter_basic() -> str:
    """Parameter with description only."""
    return """
    description: Id of the user.
    """


def case_parameter_full() -> str:
    """Parameter with all fields."""
    return """
    description: Id of the user.
    location: $message.payload#/user/id
    enum:
      - user1
      - user2
    default: user1
    examples:
      - user1
      - user2
    """


def case_parameter_with_enum() -> str:
    """Parameter with enum."""
    return """
    enum:
      - chatMessages
      - events
    description: The resource to consume.
    """


# Parameter Serialization Test Cases
def case_parameter_serialization_empty() -> tuple[Parameter, dict]:
    """Parameter serialization empty."""
    parameter = Parameter()
    expected: dict[str, Any] = {}
    return parameter, expected


def case_parameter_serialization_basic() -> tuple[Parameter, dict]:
    """Parameter serialization with description only."""
    parameter = Parameter(description="Id of the user.")
    expected: dict[str, Any] = {"description": "Id of the user."}
    return parameter, expected


def case_parameter_serialization_full() -> tuple[Parameter, dict]:
    """Parameter serialization with all fields."""
    parameter = Parameter(
        description="Id of the user.",
        location="$message.payload#/user/id",
        enum=["user1", "user2"],
        default="user1",
        examples=["user1", "user2"],
    )
    expected: dict[str, Any] = {
        "description": "Id of the user.",
        "location": "$message.payload#/user/id",
        "enum": ["user1", "user2"],
        "default": "user1",
        "examples": ["user1", "user2"],
    }
    return parameter, expected


def case_parameter_serialization_with_location() -> tuple[Parameter, dict]:
    """Parameter serialization with location."""
    parameter = Parameter(
        description="Id of the user.",
        location="$message.payload#/user/id",
    )
    expected: dict[str, Any] = {
        "description": "Id of the user.",
        "location": "$message.payload#/user/id",
    }
    return parameter, expected


def case_parameter_serialization_with_examples() -> tuple[Parameter, dict]:
    """Parameter serialization with examples."""
    parameter = Parameter(
        description="Id of the Gitter room.",
        examples=["53307860c3599d1de448e19d"],
    )
    expected: dict[str, Any] = {
        "description": "Id of the Gitter room.",
        "examples": ["53307860c3599d1de448e19d"],
    }
    return parameter, expected


# Channel Validation Test Cases
def case_channel_basic() -> str:
    """Channel with address only."""
    return """
    address: user/signedup
    """


def case_channel_full() -> str:
    """Channel with all fields."""
    return """
    address: 'users.{userId}'
    title: Users channel
    description: This channel is used to exchange messages about user events.
    messages:
      userSignedUp:
        $ref: '#/components/messages/userSignedUp'
    parameters:
      userId:
        $ref: '#/components/parameters/userId'
    servers:
      - $ref: '#/servers/rabbitmqInProd'
    tags:
      - name: user
        description: User-related messages
    externalDocs:
      description: 'Find more info here'
      url: 'https://example.com'
    """


def case_channel_with_parameters() -> str:
    """Channel with parameters."""
    return """
    address: '/rooms/{roomId}/{resource}'
    parameters:
      roomId:
        description: Id of the Gitter room.
        examples:
          - 53307860c3599d1de448e19d
      resource:
        enum:
          - chatMessages
          - events
        description: The resource to consume.
    """


# Channel Serialization Test Cases
def case_channel_serialization_empty() -> tuple[Channel, dict]:
    """Channel serialization empty."""
    channel = Channel()
    expected: dict[str, Any] = {}
    return channel, expected


def case_channel_serialization_basic() -> tuple[Channel, dict]:
    """Channel serialization with address only."""
    channel = Channel(address="user/signedup")
    expected: dict[str, Any] = {"address": "user/signedup"}
    return channel, expected


def case_channel_serialization_with_parameters() -> tuple[Channel, dict]:
    """Channel serialization with parameters."""
    channel = Channel(
        address="/rooms/{roomId}/{resource}",
        parameters={
            "roomId": Parameter(
                description="Id of the Gitter room.",
                examples=["53307860c3599d1de448e19d"],
            ),
            "resource": Parameter(
                enum=["chatMessages", "events"],
                description="The resource to consume.",
            ),
        },
    )
    expected: dict[str, Any] = {
        "address": "/rooms/{roomId}/{resource}",
        "parameters": {
            "roomId": {
                "description": "Id of the Gitter room.",
                "examples": ["53307860c3599d1de448e19d"],
            },
            "resource": {
                "enum": ["chatMessages", "events"],
                "description": "The resource to consume.",
            },
        },
    }
    return channel, expected


def case_channel_serialization_with_reference_parameter() -> tuple[Channel, dict]:
    """Channel serialization with parameter as Reference."""
    channel = Channel(
        address="users.{userId}",
        parameters={"userId": Reference(ref="#/components/parameters/userId")},
    )
    expected: dict[str, Any] = {
        "address": "users.{userId}",
        "parameters": {
            "userId": {
                "$ref": "#/components/parameters/userId",
            },
        },
    }
    return channel, expected


def case_channel_serialization_with_servers() -> tuple[Channel, dict]:
    """Channel serialization with servers."""
    channel = Channel(
        address="users.{userId}",
        servers=[
            Reference(ref="#/servers/rabbitmqInProd"),
            Reference(ref="#/servers/rabbitmqInStaging"),
        ],
    )
    expected: dict[str, Any] = {
        "address": "users.{userId}",
        "servers": [
            {"$ref": "#/servers/rabbitmqInProd"},
            {"$ref": "#/servers/rabbitmqInStaging"},
        ],
    }
    return channel, expected


class TestParameter:
    """Tests for Parameter model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_parameter_basic, case_parameter_full, case_parameter_with_enum],
    )
    def test_parameter_validation(self, yaml_data: str) -> None:
        """Test Parameter model validation."""
        data = yaml.safe_load(yaml_data)
        parameter = Parameter.model_validate(data)
        assert parameter is not None
        if "description" in data:
            assert parameter.description == data["description"]

    @parametrize_with_cases(
        "parameter,expected",
        cases=[
            case_parameter_serialization_empty,
            case_parameter_serialization_basic,
            case_parameter_serialization_full,
            case_parameter_serialization_with_location,
            case_parameter_serialization_with_examples,
        ],
    )
    def test_parameter_serialization(
        self, parameter: Parameter, expected: dict
    ) -> None:
        """Test Parameter serialization."""
        dumped = parameter.model_dump()
        assert dumped == expected


# Parameters Validation Test Cases
def case_parameters_basic() -> str:
    """Parameters with basic valid keys."""
    return """
    userId:
      description: Id of the user.
    orderId:
      description: Id of the order.
    """


def case_parameters_with_references() -> str:
    """Parameters with Reference objects."""
    return """
    userId:
      $ref: '#/components/parameters/userId'
    orderId:
      description: Id of the order.
    """


# Parameters Validation Error Test Cases
def case_parameters_invalid_key_spaces() -> tuple[str, str]:
    """Parameters with key containing spaces - should fail validation."""
    yaml_data = """
    user id:
      description: Id of the user.
    """
    expected_error = "Field 'user id' does not match patterned object key pattern. Keys must contain letters, digits, hyphens, and underscores."
    return yaml_data, expected_error


def case_parameters_invalid_key_special_chars() -> tuple[str, str]:
    """Parameters with key containing special characters - should fail validation."""
    yaml_data = """
    user@id:
      description: Id of the user.
    """
    expected_error = "Field 'user@id' does not match patterned object key pattern. Keys must contain letters, digits, hyphens, and underscores."
    return yaml_data, expected_error


def case_parameters_invalid_key_dots() -> tuple[str, str]:
    """Parameters with key containing dots - should fail validation."""
    yaml_data = """
    user.id:
      description: Id of the user.
    """
    expected_error = "Field 'user.id' does not match patterned object key pattern. Keys must contain letters, digits, hyphens, and underscores."
    return yaml_data, expected_error


class TestParameters:
    """Tests for Parameters model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[
            case_parameters_basic,
            case_parameters_with_references,
        ],
    )
    def test_parameters_validation(self, yaml_data: str) -> None:
        """Test Parameters model validation."""
        data = yaml.safe_load(yaml_data)
        parameters = Parameters.model_validate(data)
        assert parameters is not None
        assert isinstance(parameters.root, dict)
        assert len(parameters.root) > 0

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_parameters_invalid_key_spaces,
            case_parameters_invalid_key_special_chars,
            case_parameters_invalid_key_dots,
        ],
    )
    def test_parameters_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test Parameters validation errors for invalid field names."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValueError, match=expected_error):
            Parameters.model_validate(data)

    def test_parameters_empty_dict_validation(self) -> None:
        """Test Parameters with empty dict validation."""
        parameters = Parameters.model_validate({})
        assert parameters is not None
        assert parameters.root == {}
        assert len(parameters.root) == 0

    def test_parameters_iteration(self) -> None:
        """Test Parameters __iter__ method."""
        data: dict[str, Parameter | Reference] = {
            "userId": Parameter(description="Id of the user."),
            "orderId": Parameter(description="Id of the order."),
        }
        parameters = Parameters(root=data)

        keys = list(parameters)
        assert len(keys) == 2
        assert "userId" in keys
        assert "orderId" in keys

    def test_parameters_getitem(self) -> None:
        """Test Parameters __getitem__ method."""
        user_param = Parameter(description="Id of the user.")
        order_param = Parameter(description="Id of the order.")

        data: dict[str, Parameter | Reference] = {
            "userId": user_param,
            "orderId": order_param,
        }
        parameters = Parameters(root=data)

        assert parameters["userId"] == user_param
        assert parameters["orderId"] == order_param

        # Test with Reference
        ref = Reference(ref="#/components/parameters/orderId")
        data_with_ref: dict[str, Parameter | Reference] = {"orderId": ref}
        parameters_with_ref = Parameters(root=data_with_ref)
        assert parameters_with_ref["orderId"] == ref

    def test_parameters_getattr(self) -> None:
        """Test Parameters __getattr__ method."""
        user_param = Parameter(description="Id of the user.")
        order_param = Parameter(description="Id of the order.")

        data: dict[str, Parameter | Reference] = {
            "userId": user_param,
            "orderId": order_param,
        }
        parameters = Parameters(root=data)

        assert parameters.userId == user_param
        assert parameters.orderId == order_param

        # Test with Reference
        ref = Reference(ref="#/components/parameters/orderId")
        data_with_ref: dict[str, Parameter | Reference] = {"orderId": ref}
        parameters_with_ref = Parameters(root=data_with_ref)
        assert parameters_with_ref.orderId == ref


class TestChannel:
    """Tests for Channel model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_channel_basic, case_channel_full, case_channel_with_parameters],
    )
    def test_channel_validation(self, yaml_data: str) -> None:
        """Test Channel model validation."""
        data = yaml.safe_load(yaml_data)
        channel = Channel.model_validate(data)
        assert channel is not None
        if "address" in data:
            assert channel.address == data["address"]

    @parametrize_with_cases(
        "channel,expected",
        cases=[
            case_channel_serialization_empty,
            case_channel_serialization_basic,
            case_channel_serialization_with_parameters,
            case_channel_serialization_with_reference_parameter,
            case_channel_serialization_with_servers,
        ],
    )
    def test_channel_serialization(self, channel: Channel, expected: dict) -> None:
        """Test Channel serialization."""
        dumped = channel.model_dump()
        assert dumped == expected

    def test_channel_with_parameters_validation(self) -> None:
        """Test Channel with parameters validation."""
        yaml_data = """
        address: '/rooms/{roomId}/{resource}'
        parameters:
          roomId:
            description: Id of the Gitter room.
            examples:
              - 53307860c3599d1de448e19d
          resource:
            enum:
              - chatMessages
              - events
            description: The resource to consume.
        """
        data = yaml.safe_load(yaml_data)
        channel = Channel.model_validate(data)

        assert channel.parameters is not None
        assert "roomId" in channel.parameters
        assert isinstance(channel.parameters["roomId"], Parameter)
        assert channel.parameters["roomId"].description == "Id of the Gitter room."
        assert "resource" in channel.parameters
        assert isinstance(channel.parameters["resource"], Parameter)
        assert channel.parameters["resource"].enum == ["chatMessages", "events"]

    def test_channel_with_reference_parameter_validation(self) -> None:
        """Test Channel with parameter as Reference validation."""
        yaml_data = """
        address: 'users.{userId}'
        parameters:
          userId:
            $ref: '#/components/parameters/userId'
        """
        data = yaml.safe_load(yaml_data)
        channel = Channel.model_validate(data)

        assert channel.parameters is not None
        assert "userId" in channel.parameters
        assert isinstance(channel.parameters["userId"], Reference)
        assert channel.parameters["userId"].ref == "#/components/parameters/userId"

    def test_channel_with_servers_validation(self) -> None:
        """Test Channel with servers validation."""
        yaml_data = """
        address: 'users.{userId}'
        servers:
          - $ref: '#/servers/rabbitmqInProd'
          - $ref: '#/servers/rabbitmqInStaging'
        """
        data = yaml.safe_load(yaml_data)
        channel = Channel.model_validate(data)

        assert channel.servers is not None
        assert len(channel.servers) == 2
        assert isinstance(channel.servers[0], Reference)
        assert channel.servers[0].ref == "#/servers/rabbitmqInProd"
        assert isinstance(channel.servers[1], Reference)
        assert channel.servers[1].ref == "#/servers/rabbitmqInStaging"

    def test_channel_parameters_validation_with_address_expressions(self) -> None:
        """Test Channel parameters validation when address contains expressions."""
        yaml_data = """
        address: 'users/{userId}/orders/{orderId}'
        parameters:
          userId:
            description: Id of the user.
          orderId:
            description: Id of the order.
        """
        data = yaml.safe_load(yaml_data)
        channel = Channel.model_validate(data)

        assert channel.parameters is not None
        assert "userId" in channel.parameters
        assert "orderId" in channel.parameters

    def test_channel_parameters_validation_without_address_expressions_error(
        self,
    ) -> None:
        """Test Channel parameters validation error when address has no expressions."""
        yaml_data = """
        address: 'users/orders'
        parameters:
          userId:
            description: Id of the user.
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError) as exc_info:
            Channel.model_validate(data)

        assert (
            "parameters must not be provided when address does not contain Channel Address Expressions"
            in str(exc_info.value)
        )

    def test_channel_parameters_validation_with_null_address_error(self) -> None:
        """Test Channel parameters validation error when address is null."""
        yaml_data = """
        address: null
        parameters:
          userId:
            description: Id of the user.
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError) as exc_info:
            Channel.model_validate(data)

        assert "parameters must not be provided when address is null or absent" in str(
            exc_info.value
        )

    def test_channel_parameters_validation_without_address_error(self) -> None:
        """Test Channel parameters validation error when address is absent."""
        yaml_data = """
        title: Test channel
        parameters:
          userId:
            description: Id of the user.
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError) as exc_info:
            Channel.model_validate(data)

        assert "parameters must not be provided when address is null or absent" in str(
            exc_info.value
        )


class TestChannels:
    """Tests for Channels model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_channels_basic, case_channels_with_references],
    )
    def test_channels_validation(self, yaml_data: str) -> None:
        """Test Channels model validation."""
        data = yaml.safe_load(yaml_data)
        channels = Channels.model_validate(data["channels"])
        assert channels is not None
        assert isinstance(channels.root, dict)
        assert len(channels.root) > 0

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_channels_invalid_key_spaces,
            case_channels_invalid_key_special_chars,
            case_channels_invalid_key_parentheses,
        ],
    )
    def test_channels_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test Channels validation errors for invalid field names."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValueError, match=expected_error):
            Channels.model_validate(data["channels"])

    def test_channels_empty_dict_validation(self) -> None:
        """Test Channels with empty dict validation."""
        channels = Channels.model_validate({})
        assert channels is not None
        assert channels.root == {}
        assert len(channels.root) == 0

    def test_channels_iteration(self) -> None:
        """Test Channels __iter__ method."""
        user_channel = Channel(address="user/signedup")
        admin_channel = Channel(address="admin/events")

        data: dict[str, Channel | Reference] = {
            "userChannel": user_channel,
            "adminChannel": admin_channel,
        }
        channels = Channels(root=data)

        keys = list(channels)
        assert len(keys) == 2
        assert "userChannel" in keys
        assert "adminChannel" in keys

    def test_channels_getitem(self) -> None:
        """Test Channels __getitem__ method."""
        user_channel = Channel(address="user/signedup")
        admin_channel = Channel(address="admin/events")

        data: dict[str, Channel | Reference] = {
            "userChannel": user_channel,
            "adminChannel": admin_channel,
        }
        channels = Channels(root=data)

        assert channels["userChannel"] == user_channel
        assert channels["adminChannel"] == admin_channel

    def test_channels_getattr(self) -> None:
        """Test Channels __getattr__ method."""
        user_channel = Channel(address="user/signedup")
        admin_channel = Channel(address="admin/events")

        data: dict[str, Channel | Reference] = {
            "userChannel": user_channel,
            "adminChannel": admin_channel,
        }
        channels = Channels(root=data)

        assert channels.userChannel == user_channel
        assert channels.adminChannel == admin_channel
