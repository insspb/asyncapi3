"""Tests for components model."""

from typing import Any

import pytest
import yaml

from pydantic import AnyUrl, ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.base import ExternalDocumentation, Reference, Tag
from asyncapi3.models.channel import Channel, Parameter
from asyncapi3.models.components import (
    Channels,
    Components,
    CorrelationIDs,
    ExternalDocs,
    Messages,
    MessageTraits,
    Operations,
    OperationTraits,
    Parameters,
    Replies,
    ReplyAddresses,
    Schemas,
    SecuritySchemes,
    Servers,
    ServerVariables,
    Tags,
)
from asyncapi3.models.message import Message, MessageTrait
from asyncapi3.models.operation import (
    Operation,
    OperationReply,
    OperationReplyAddress,
    OperationTrait,
)
from asyncapi3.models.schema import MultiFormatSchema, Schema
from asyncapi3.models.security import CorrelationID, SecurityScheme
from asyncapi3.models.server import Server, ServerVariable


# Components Validation Test Cases
def case_components_empty() -> str:
    """Components empty object."""
    return """
    {}
    """


def case_components_with_messages() -> str:
    """Components with messages only."""
    return """
    messages:
      UserSignedUp:
        payload:
          type: object
          properties:
            displayName:
              type: string
            email:
              type: string
              format: email
    """


def case_components_full() -> str:
    """Components with multiple sections."""
    return """
    schemas:
      User:
        type: object
        properties:
          name:
            type: string
    servers:
      production:
        host: kafka.in.mycompany.com:9092
        protocol: kafka
    channels:
      userChannel:
        address: user/signedup
    operations:
      sendUserSignup:
        action: send
        channel:
          $ref: '#/channels/userChannel'
    messages:
      UserSignedUp:
        payload:
          type: object
    securitySchemes:
      apiKey:
        type: apiKey
        in: user
        name: api_key
    parameters:
      userId:
        description: Id of the user.
    correlationIds:
      default:
        location: $message.header#/correlationId
    tags:
      user:
        name: user
    """


# Components Serialization Test Cases
def case_components_serialization_empty() -> tuple[Components, dict]:
    """Components serialization empty."""
    components = Components()
    expected: dict[str, Any] = {}
    return components, expected


def case_components_serialization_with_messages() -> tuple[Components, dict]:
    """Components serialization with messages only."""
    components = Components(
        messages=Messages(
            root={
                "UserSignedUp": Message(
                    payload=Schema(
                        type="object",
                        properties={
                            "displayName": Schema(type="string"),
                            "email": Schema(type="string", format="email"),
                        },
                    ),
                ),
            }
        ),
    )
    expected: dict[str, Any] = {
        "messages": {
            "UserSignedUp": {
                "payload": {
                    "type": "object",
                    "properties": {
                        "displayName": {"type": "string"},
                        "email": {"type": "string", "format": "email"},
                    },
                },
            },
        },
    }
    return components, expected


def case_components_serialization_with_schemas() -> tuple[Components, dict]:
    """Components serialization with schemas."""
    components = Components(
        schemas={
            "User": Schema(
                type="object",
                properties={"name": Schema(type="string")},
            ),
        },
    )
    expected: dict[str, Any] = {
        "schemas": {
            "User": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                    },
                },
            },
        },
    }
    return components, expected


def case_components_serialization_with_servers() -> tuple[Components, dict]:
    """Components serialization with servers."""
    components = Components(
        servers={
            "production": Server(
                host="kafka.in.mycompany.com:9092",
                protocol="kafka",
            ),
        },
    )
    expected: dict[str, Any] = {
        "servers": {
            "production": {
                "host": "kafka.in.mycompany.com:9092",
                "protocol": "kafka",
            },
        },
    }
    return components, expected


def case_components_serialization_with_channels() -> tuple[Components, dict]:
    """Components serialization with channels."""
    components = Components(
        channels={
            "userChannel": Channel(address="user/signedup"),
        },
    )
    expected: dict[str, Any] = {
        "channels": {
            "userChannel": {
                "address": "user/signedup",
            },
        },
    }
    return components, expected


def case_components_serialization_with_operations() -> tuple[Components, dict]:
    """Components serialization with operations."""
    components = Components(
        operations={
            "sendUserSignup": Operation(
                action="send",
                channel=Reference(ref="#/channels/userChannel"),
            ),
        },
    )
    expected: dict[str, Any] = {
        "operations": {
            "sendUserSignup": {
                "action": "send",
                "channel": {
                    "$ref": "#/channels/userChannel",
                },
            },
        },
    }
    return components, expected


def case_components_serialization_with_parameters() -> tuple[Components, dict]:
    """Components serialization with parameters."""
    components = Components(
        parameters={
            "userId": Parameter(description="Id of the user."),
        },
    )
    expected: dict[str, Any] = {
        "parameters": {
            "userId": {
                "description": "Id of the user.",
            },
        },
    }
    return components, expected


def case_components_serialization_with_correlation_ids() -> tuple[Components, dict]:
    """Components serialization with correlationIds."""
    components = Components(
        correlation_ids={
            "default": CorrelationID(location="$message.header#/correlationId"),
        },
    )
    expected: dict[str, Any] = {
        "correlationIds": {
            "default": {
                "location": "$message.header#/correlationId",
            },
        },
    }
    return components, expected


def case_components_serialization_with_security_schemes() -> tuple[Components, dict]:
    """Components serialization with securitySchemes."""
    components = Components(
        security_schemes={
            "apiKey": SecurityScheme(
                type_="apiKey",
                in_="user",
                name="api_key",
            ),
        },
    )
    expected: dict[str, Any] = {
        "securitySchemes": {
            "apiKey": {
                "type": "apiKey",
                "in": "user",
                "name": "api_key",
            },
        },
    }
    return components, expected


def case_components_serialization_with_server_variables() -> tuple[Components, dict]:
    """Components serialization with serverVariables."""
    components = Components(
        server_variables={
            "port": ServerVariable(default="1883", enum=["1883", "8883"]),
        },
    )
    expected: dict[str, Any] = {
        "serverVariables": {
            "port": {
                "default": "1883",
                "enum": ["1883", "8883"],
            },
        },
    }
    return components, expected


def case_components_serialization_with_replies() -> tuple[Components, dict]:
    """Components serialization with replies."""
    components = Components(
        replies={
            "userReply": OperationReply(
                address=OperationReplyAddress(location="$message.header#/replyTo")
            ),
        },
    )
    expected: dict[str, Any] = {
        "replies": {
            "userReply": {
                "address": {
                    "location": "$message.header#/replyTo",
                },
            },
        },
    }
    return components, expected


def case_components_serialization_with_reply_addresses() -> tuple[Components, dict]:
    """Components serialization with replyAddresses."""
    components = Components(
        reply_addresses={
            "userReplyAddress": OperationReplyAddress(
                location="$message.header#/replyTo"
            ),
        },
    )
    expected: dict[str, Any] = {
        "replyAddresses": {
            "userReplyAddress": {
                "location": "$message.header#/replyTo",
            },
        },
    }
    return components, expected


def case_components_serialization_with_external_docs() -> tuple[Components, dict]:
    """Components serialization with externalDocs."""

    components = Components(
        external_docs={
            "apiDocs": ExternalDocumentation(
                url="https://example.com", description="API documentation"
            ),
        },
    )
    expected: dict[str, Any] = {
        "externalDocs": {
            "apiDocs": {
                "url": AnyUrl("https://example.com/"),
                "description": "API documentation",
            },
        },
    }
    return components, expected


def case_components_serialization_with_tags() -> tuple[Components, dict]:
    """Components serialization with tags."""
    components = Components(
        tags={
            "user": Tag(name="user", description="User operations"),
        },
    )
    expected: dict[str, Any] = {
        "tags": {
            "user": {
                "name": "user",
                "description": "User operations",
            },
        },
    }
    return components, expected


def case_components_serialization_with_operation_traits() -> tuple[Components, dict]:
    """Components serialization with operationTraits."""
    components = Components(
        operation_traits={
            "httpTrait": OperationTrait(
                bindings={"http": {"method": "POST"}},
                summary="HTTP operation trait",
            ),
        },
    )
    expected: dict[str, Any] = {
        "operationTraits": {
            "httpTrait": {
                "bindings": {
                    "http": {
                        "method": "POST",
                        "bindingVersion": "0.3.0",
                    },
                },
                "summary": "HTTP operation trait",
            },
        },
    }
    return components, expected


def case_components_serialization_with_message_traits() -> tuple[Components, dict]:
    """Components serialization with messageTraits."""
    components = Components(
        message_traits={
            "commonHeaders": MessageTrait(
                content_type="application/json",
                headers=Schema(
                    type="object",
                    properties={"eventId": Schema(type="string")},
                ),
            ),
        },
    )
    expected: dict[str, Any] = {
        "messageTraits": {
            "commonHeaders": {
                "contentType": "application/json",
                "headers": {
                    "type": "object",
                    "properties": {
                        "eventId": {"type": "string"},
                    },
                },
            },
        },
    }
    return components, expected


# Schemas Validation Test Cases
def case_schemas_basic() -> str:
    """Schemas with basic schema objects."""
    return """
    schemas:
      user:
        type: object
        properties:
          name:
            type: string
      order:
        type: object
        properties:
          id:
            type: integer
    """


def case_schemas_with_references() -> str:
    """Schemas with references."""
    return """
    schemas:
      user:
        $ref: '#/components/schemas/user'
      order:
        $ref: '#/components/schemas/order'
    """


# Schemas Validation Error Test Cases
def case_schemas_invalid_key_spaces() -> tuple[str, str]:
    """Schemas with key containing spaces - should fail validation."""
    yaml_data = """
    schemas:
      user schema:
        type: object
    """
    expected_error = "Field 'user schema' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_schemas_invalid_key_special_chars() -> tuple[str, str]:
    """Schemas with key containing special characters - should fail validation."""
    yaml_data = """
    schemas:
      user@schema:
        type: object
    """
    expected_error = "Field 'user@schema' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_schemas_invalid_key_parentheses() -> tuple[str, str]:
    """Schemas with key containing parentheses - should fail validation."""
    yaml_data = """
    schemas:
      user(schema):
        type: object
    """
    expected_error = "Field 'user(schema)' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


class TestSchemas:
    """Tests for Schemas model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_schemas_basic, case_schemas_with_references],
    )
    def test_schemas_validation(self, yaml_data: str) -> None:
        """Test Schemas model validation."""
        data = yaml.safe_load(yaml_data)
        schemas = Schemas.model_validate(data["schemas"])
        assert schemas is not None
        assert isinstance(schemas.root, dict)
        assert len(schemas.root) > 0

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_schemas_invalid_key_spaces,
            case_schemas_invalid_key_special_chars,
            case_schemas_invalid_key_parentheses,
        ],
    )
    def test_schemas_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test Schemas validation errors for invalid field names."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError) as exc_info:
            Schemas.model_validate(data["schemas"])
        assert expected_error in str(exc_info.value)

    def test_schemas_empty_dict_validation(self) -> None:
        """Test Schemas with empty dict validation."""
        schemas = Schemas.model_validate({})
        assert schemas is not None
        assert schemas.root == {}
        assert len(schemas.root) == 0

    def test_schemas_iteration(self) -> None:
        """Test Schemas __iter__ method."""
        user_schema = Schema(type="object", properties={"name": Schema(type="string")})
        order_schema = Schema(type="object", properties={"id": Schema(type="integer")})

        data: dict[str, MultiFormatSchema | Schema | Reference] = {
            "user": user_schema,
            "order": order_schema,
        }
        schemas = Schemas(root=data)

        keys = list(schemas)
        assert len(keys) == 2
        assert "user" in keys
        assert "order" in keys

    def test_schemas_getitem(self) -> None:
        """Test Schemas __getitem__ method."""
        user_schema = Schema(type="object", properties={"name": Schema(type="string")})
        order_schema = Schema(type="object", properties={"id": Schema(type="integer")})

        data: dict[str, MultiFormatSchema | Schema | Reference] = {
            "user": user_schema,
            "order": order_schema,
        }
        schemas = Schemas(root=data)

        assert schemas["user"] == user_schema
        assert schemas["order"] == order_schema

    def test_schemas_getattr(self) -> None:
        """Test Schemas __getattr__ method."""
        user_schema = Schema(type="object", properties={"name": Schema(type="string")})
        order_schema = Schema(type="object", properties={"id": Schema(type="integer")})

        data: dict[str, MultiFormatSchema | Schema | Reference] = {
            "user": user_schema,
            "order": order_schema,
        }
        schemas = Schemas(root=data)

        assert schemas.user == user_schema
        assert schemas.order == order_schema


# Servers Validation Test Cases
def case_servers_basic() -> str:
    """Servers with basic server objects."""
    return """
    servers:
      production:
        host: kafka.in.mycompany.com:9092
        protocol: kafka
      staging:
        host: kafka.staging.mycompany.com:9092
        protocol: kafka
    """


def case_servers_with_references() -> str:
    """Servers with references."""
    return """
    servers:
      production:
        $ref: '#/components/servers/production'
      staging:
        $ref: '#/components/servers/staging'
    """


# Servers Validation Error Test Cases
def case_servers_invalid_key_spaces() -> tuple[str, str]:
    """Servers with key containing spaces - should fail validation."""
    yaml_data = """
    servers:
      production server:
        host: kafka.in.mycompany.com:9092
        protocol: kafka
    """
    expected_error = "Field 'production server' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


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
    expected_error = "Field 'user channel' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_channels_invalid_key_special_chars() -> tuple[str, str]:
    """Channels with key containing special characters - should fail validation."""
    yaml_data = """
    channels:
      user@channel:
        address: user/signedup
    """
    expected_error = "Field 'user@channel' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_channels_invalid_key_parentheses() -> tuple[str, str]:
    """Channels with key containing parentheses - should fail validation."""
    yaml_data = """
    channels:
      user(channel):
        address: user/signedup
    """
    expected_error = "Field 'user(channel)' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


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
        with pytest.raises(ValidationError) as exc_info:
            Channels.model_validate(data["channels"])
        assert expected_error in str(exc_info.value)

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


# Operations Validation Test Cases
def case_operations_basic() -> str:
    """Operations with basic operation objects."""
    return """
    operations:
      sendUserSignup:
        action: send
        channel:
          $ref: '#/channels/userChannel'
      receiveUserSignup:
        action: receive
        channel:
          $ref: '#/channels/userChannel'
    """


def case_operations_with_references() -> str:
    """Operations with references."""
    return """
    operations:
      sendUserSignup:
        $ref: '#/components/operations/sendUserSignup'
      receiveUserSignup:
        $ref: '#/components/operations/receiveUserSignup'
    """


# Operations Validation Error Test Cases
def case_operations_invalid_key_spaces() -> tuple[str, str]:
    """Operations with key containing spaces - should fail validation."""
    yaml_data = """
    operations:
      send user signup:
        action: send
        channel:
          $ref: '#/channels/userChannel'
    """
    expected_error = "Field 'send user signup' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_operations_invalid_key_special_chars() -> tuple[str, str]:
    """Operations with key containing special characters - should fail validation."""
    yaml_data = """
    operations:
      send@user@signup:
        action: send
        channel:
          $ref: '#/channels/userChannel'
    """
    expected_error = "Field 'send@user@signup' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_operations_invalid_key_parentheses() -> tuple[str, str]:
    """Operations with key containing parentheses - should fail validation."""
    yaml_data = """
    operations:
      send(user)signup:
        action: send
        channel:
          $ref: '#/channels/userChannel'
    """
    expected_error = "Field 'send(user)signup' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


class TestOperations:
    """Tests for Operations model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_operations_basic, case_operations_with_references],
    )
    def test_operations_validation(self, yaml_data: str) -> None:
        """Test Operations model validation."""
        data = yaml.safe_load(yaml_data)
        operations = Operations.model_validate(data["operations"])
        assert operations is not None
        assert isinstance(operations.root, dict)
        assert len(operations.root) > 0

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_operations_invalid_key_spaces,
            case_operations_invalid_key_special_chars,
            case_operations_invalid_key_parentheses,
        ],
    )
    def test_operations_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test Operations validation errors for invalid field names."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError) as exc_info:
            Operations.model_validate(data["operations"])
        assert expected_error in str(exc_info.value)

    def test_operations_empty_dict_validation(self) -> None:
        """Test Operations with empty dict validation."""
        operations = Operations.model_validate({})
        assert operations is not None
        assert operations.root == {}
        assert len(operations.root) == 0

    def test_operations_iteration(self) -> None:
        """Test Operations __iter__ method."""
        send_operation = Operation(
            action="send", channel=Reference(ref="#/channels/userChannel")
        )
        receive_operation = Operation(
            action="receive", channel=Reference(ref="#/channels/userChannel")
        )

        data: dict[str, Operation | Reference] = {
            "sendUserSignup": send_operation,
            "receiveUserSignup": receive_operation,
        }
        operations = Operations(root=data)

        keys = list(operations)
        assert len(keys) == 2
        assert "sendUserSignup" in keys
        assert "receiveUserSignup" in keys

    def test_operations_getitem(self) -> None:
        """Test Operations __getitem__ method."""
        send_operation = Operation(
            action="send", channel=Reference(ref="#/channels/userChannel")
        )
        receive_operation = Operation(
            action="receive", channel=Reference(ref="#/channels/userChannel")
        )

        data: dict[str, Operation | Reference] = {
            "sendUserSignup": send_operation,
            "receiveUserSignup": receive_operation,
        }
        operations = Operations(root=data)

        assert operations["sendUserSignup"] == send_operation
        assert operations["receiveUserSignup"] == receive_operation

    def test_operations_getattr(self) -> None:
        """Test Operations __getattr__ method."""
        send_operation = Operation(
            action="send", channel=Reference(ref="#/channels/userChannel")
        )
        receive_operation = Operation(
            action="receive", channel=Reference(ref="#/channels/userChannel")
        )

        data: dict[str, Operation | Reference] = {
            "sendUserSignup": send_operation,
            "receiveUserSignup": receive_operation,
        }
        operations = Operations(root=data)

        assert operations.sendUserSignup == send_operation
        assert operations.receiveUserSignup == receive_operation


# Messages Validation Test Cases
def case_messages_basic() -> str:
    """Messages with basic message objects."""
    return """
    messages:
      UserSignedUp:
        payload:
          type: object
          properties:
            displayName:
              type: string
            email:
              type: string
              format: email
      UserLoggedOut:
        payload:
          type: object
          properties:
            userId:
              type: string
    """


def case_messages_with_references() -> str:
    """Messages with references."""
    return """
    messages:
      UserSignedUp:
        $ref: '#/components/messages/UserSignedUp'
      UserLoggedOut:
        $ref: '#/components/messages/UserLoggedOut'
    """


# Messages Validation Error Test Cases
def case_messages_invalid_key_spaces() -> tuple[str, str]:
    """Messages with key containing spaces - should fail validation."""
    yaml_data = """
    messages:
      user signed up:
        payload:
          type: object
          properties:
            displayName:
              type: string
    """
    expected_error = "Field 'user signed up' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_messages_invalid_key_special_chars() -> tuple[str, str]:
    """Messages with key containing special characters - should fail validation."""
    yaml_data = """
    messages:
      user@signed@up:
        payload:
          type: object
          properties:
            displayName:
              type: string
    """
    expected_error = "Field 'user@signed@up' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_messages_invalid_key_parentheses() -> tuple[str, str]:
    """Messages with key containing parentheses - should fail validation."""
    yaml_data = """
    messages:
      user(signed)up:
        payload:
          type: object
          properties:
            displayName:
              type: string
    """
    expected_error = "Field 'user(signed)up' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


class TestMessages:
    """Tests for Messages model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_messages_basic, case_messages_with_references],
    )
    def test_messages_validation(self, yaml_data: str) -> None:
        """Test Messages model validation."""
        data = yaml.safe_load(yaml_data)
        messages = Messages.model_validate(data["messages"])
        assert messages is not None
        assert isinstance(messages.root, dict)
        assert len(messages.root) > 0

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_messages_invalid_key_spaces,
            case_messages_invalid_key_special_chars,
            case_messages_invalid_key_parentheses,
        ],
    )
    def test_messages_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test Messages validation errors for invalid field names."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError) as exc_info:
            Messages.model_validate(data["messages"])
        assert expected_error in str(exc_info.value)

    def test_messages_empty_dict_validation(self) -> None:
        """Test Messages with empty dict validation."""
        messages = Messages.model_validate({})
        assert messages is not None
        assert messages.root == {}
        assert len(messages.root) == 0

    def test_messages_iteration(self) -> None:
        """Test Messages __iter__ method."""
        user_signed_up = Message(
            payload=Schema(
                type="object",
                properties={
                    "displayName": Schema(type="string"),
                    "email": Schema(type="string", format="email"),
                },
            ),
        )
        user_logged_out = Message(
            payload=Schema(
                type="object",
                properties={"userId": Schema(type="string")},
            ),
        )

        data: dict[str, Message | Reference] = {
            "UserSignedUp": user_signed_up,
            "UserLoggedOut": user_logged_out,
        }
        messages = Messages(root=data)

        keys = list(messages)
        assert len(keys) == 2
        assert "UserSignedUp" in keys
        assert "UserLoggedOut" in keys

    def test_messages_getitem(self) -> None:
        """Test Messages __getitem__ method."""
        user_signed_up = Message(
            payload=Schema(
                type="object",
                properties={
                    "displayName": Schema(type="string"),
                    "email": Schema(type="string", format="email"),
                },
            ),
        )
        user_logged_out = Message(
            payload=Schema(
                type="object",
                properties={"userId": Schema(type="string")},
            ),
        )

        data: dict[str, Message | Reference] = {
            "UserSignedUp": user_signed_up,
            "UserLoggedOut": user_logged_out,
        }
        messages = Messages(root=data)

        assert messages["UserSignedUp"] == user_signed_up
        assert messages["UserLoggedOut"] == user_logged_out

    def test_messages_getattr(self) -> None:
        """Test Messages __getattr__ method."""
        user_signed_up = Message(
            payload=Schema(
                type="object",
                properties={
                    "displayName": Schema(type="string"),
                    "email": Schema(type="string", format="email"),
                },
            ),
        )
        user_logged_out = Message(
            payload=Schema(
                type="object",
                properties={"userId": Schema(type="string")},
            ),
        )

        data: dict[str, Message | Reference] = {
            "UserSignedUp": user_signed_up,
            "UserLoggedOut": user_logged_out,
        }
        messages = Messages(root=data)

        assert messages.UserSignedUp == user_signed_up
        assert messages.UserLoggedOut == user_logged_out


# SecuritySchemes Validation Test Cases
def case_security_schemes_basic() -> str:
    """SecuritySchemes with basic security scheme objects."""
    return """
    securitySchemes:
      apiKey:
        type: apiKey
        in: user
        name: api_key
      basicAuth:
        type: http
        scheme: basic
    """


def case_security_schemes_with_references() -> str:
    """SecuritySchemes with references."""
    return """
    securitySchemes:
      apiKey:
        $ref: '#/components/securitySchemes/apiKey'
      basicAuth:
        $ref: '#/components/securitySchemes/basicAuth'
    """


# SecuritySchemes Validation Error Test Cases
def case_security_schemes_invalid_key_spaces() -> tuple[str, str]:
    """SecuritySchemes with key containing spaces - should fail validation."""
    yaml_data = """
    securitySchemes:
      api key:
        type: apiKey
        in: user
        name: api_key
    """
    expected_error = "Field 'api key' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_security_schemes_invalid_key_special_chars() -> tuple[str, str]:
    """SecuritySchemes with key containing special characters - should fail validation."""
    yaml_data = """
    securitySchemes:
      api@key:
        type: apiKey
        in: user
        name: api_key
    """
    expected_error = "Field 'api@key' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_security_schemes_invalid_key_parentheses() -> tuple[str, str]:
    """SecuritySchemes with key containing parentheses - should fail validation."""
    yaml_data = """
    securitySchemes:
      api(key):
        type: apiKey
        in: user
        name: api_key
    """
    expected_error = "Field 'api(key)' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


class TestSecuritySchemes:
    """Tests for SecuritySchemes model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_security_schemes_basic, case_security_schemes_with_references],
    )
    def test_security_schemes_validation(self, yaml_data: str) -> None:
        """Test SecuritySchemes model validation."""
        data = yaml.safe_load(yaml_data)
        security_schemes = SecuritySchemes.model_validate(data["securitySchemes"])
        assert security_schemes is not None
        assert isinstance(security_schemes.root, dict)
        assert len(security_schemes.root) > 0

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_security_schemes_invalid_key_spaces,
            case_security_schemes_invalid_key_special_chars,
            case_security_schemes_invalid_key_parentheses,
        ],
    )
    def test_security_schemes_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test SecuritySchemes validation errors for invalid field names."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError) as exc_info:
            SecuritySchemes.model_validate(data["securitySchemes"])
        assert expected_error in str(exc_info.value)

    def test_security_schemes_empty_dict_validation(self) -> None:
        """Test SecuritySchemes with empty dict validation."""
        security_schemes = SecuritySchemes.model_validate({})
        assert security_schemes is not None
        assert security_schemes.root == {}
        assert len(security_schemes.root) == 0

    def test_security_schemes_iteration(self) -> None:
        """Test SecuritySchemes __iter__ method."""
        api_key_scheme = SecurityScheme(
            type_="apiKey",
            in_="user",
            name="api_key",
        )
        basic_auth_scheme = SecurityScheme(
            type_="http",
            scheme="basic",
        )

        data: dict[str, SecurityScheme | Reference] = {
            "apiKey": api_key_scheme,
            "basicAuth": basic_auth_scheme,
        }
        security_schemes = SecuritySchemes(root=data)

        keys = list(security_schemes)
        assert len(keys) == 2
        assert "apiKey" in keys
        assert "basicAuth" in keys

    def test_security_schemes_getitem(self) -> None:
        """Test SecuritySchemes __getitem__ method."""
        api_key_scheme = SecurityScheme(
            type_="apiKey",
            in_="user",
            name="api_key",
        )
        basic_auth_scheme = SecurityScheme(
            type_="http",
            scheme="basic",
        )

        data: dict[str, SecurityScheme | Reference] = {
            "apiKey": api_key_scheme,
            "basicAuth": basic_auth_scheme,
        }
        security_schemes = SecuritySchemes(root=data)

        assert security_schemes["apiKey"] == api_key_scheme
        assert security_schemes["basicAuth"] == basic_auth_scheme

    def test_security_schemes_getattr(self) -> None:
        """Test SecuritySchemes __getattr__ method."""
        api_key_scheme = SecurityScheme(
            type_="apiKey",
            in_="user",
            name="api_key",
        )
        basic_auth_scheme = SecurityScheme(
            type_="http",
            scheme="basic",
        )

        data: dict[str, SecurityScheme | Reference] = {
            "apiKey": api_key_scheme,
            "basicAuth": basic_auth_scheme,
        }
        security_schemes = SecuritySchemes(root=data)

        assert security_schemes.apiKey == api_key_scheme
        assert security_schemes.basicAuth == basic_auth_scheme


# ServerVariables Validation Test Cases
def case_server_variables_basic() -> str:
    """ServerVariables with basic server variable objects."""
    return """
    serverVariables:
      port:
        default: '1883'
        enum:
          - '1883'
          - '8883'
      username:
        default: guest
    """


def case_server_variables_with_references() -> str:
    """ServerVariables with references."""
    return """
    serverVariables:
      port:
        $ref: '#/components/serverVariables/port'
      username:
        $ref: '#/components/serverVariables/username'
    """


# ServerVariables Validation Error Test Cases
def case_server_variables_invalid_key_spaces() -> tuple[str, str]:
    """ServerVariables with key containing spaces - should fail validation."""
    yaml_data = """
    serverVariables:
      server port:
        default: '1883'
    """
    expected_error = "Field 'server port' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_server_variables_invalid_key_special_chars() -> tuple[str, str]:
    """ServerVariables with key containing special characters - should fail validation."""
    yaml_data = """
    serverVariables:
      server@port:
        default: '1883'
    """
    expected_error = "Field 'server@port' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_server_variables_invalid_key_parentheses() -> tuple[str, str]:
    """ServerVariables with key containing parentheses - should fail validation."""
    yaml_data = """
    serverVariables:
      server(port):
        default: '1883'
    """
    expected_error = "Field 'server(port)' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


class TestServerVariables:
    """Tests for ServerVariables model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_server_variables_basic, case_server_variables_with_references],
    )
    def test_server_variables_validation(self, yaml_data: str) -> None:
        """Test ServerVariables model validation."""
        data = yaml.safe_load(yaml_data)
        server_variables = ServerVariables.model_validate(data["serverVariables"])
        assert server_variables is not None
        assert isinstance(server_variables.root, dict)
        assert len(server_variables.root) > 0

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_server_variables_invalid_key_spaces,
            case_server_variables_invalid_key_special_chars,
            case_server_variables_invalid_key_parentheses,
        ],
    )
    def test_server_variables_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test ServerVariables validation errors for invalid field names."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError) as exc_info:
            ServerVariables.model_validate(data["serverVariables"])
        assert expected_error in str(exc_info.value)

    def test_server_variables_empty_dict_validation(self) -> None:
        """Test ServerVariables with empty dict validation."""
        server_variables = ServerVariables.model_validate({})
        assert server_variables is not None
        assert server_variables.root == {}
        assert len(server_variables.root) == 0

    def test_server_variables_iteration(self) -> None:
        """Test ServerVariables __iter__ method."""
        port_var = ServerVariable(default="1883", enum=["1883", "8883"])
        username_var = ServerVariable(default="guest")

        data: dict[str, ServerVariable | Reference] = {
            "port": port_var,
            "username": username_var,
        }
        server_variables = ServerVariables(root=data)

        keys = list(server_variables)
        assert len(keys) == 2
        assert "port" in keys
        assert "username" in keys

    def test_server_variables_getitem(self) -> None:
        """Test ServerVariables __getitem__ method."""
        port_var = ServerVariable(default="1883", enum=["1883", "8883"])
        username_var = ServerVariable(default="guest")

        data: dict[str, ServerVariable | Reference] = {
            "port": port_var,
            "username": username_var,
        }
        server_variables = ServerVariables(root=data)

        assert server_variables["port"] == port_var
        assert server_variables["username"] == username_var

    def test_server_variables_getattr(self) -> None:
        """Test ServerVariables __getattr__ method."""
        port_var = ServerVariable(default="1883", enum=["1883", "8883"])
        username_var = ServerVariable(default="guest")

        data: dict[str, ServerVariable | Reference] = {
            "port": port_var,
            "username": username_var,
        }
        server_variables = ServerVariables(root=data)

        assert server_variables.port == port_var
        assert server_variables.username == username_var


# Parameters Validation Test Cases
def case_parameters_basic() -> str:
    """Parameters with basic parameter objects."""
    return """
    parameters:
      userId:
        description: Id of the user.
      channelId:
        description: Id of the channel.
    """


def case_parameters_with_references() -> str:
    """Parameters with references."""
    return """
    parameters:
      userId:
        $ref: '#/components/parameters/userId'
      channelId:
        $ref: '#/components/parameters/channelId'
    """


# Parameters Validation Error Test Cases
def case_parameters_invalid_key_spaces() -> tuple[str, str]:
    """Parameters with key containing spaces - should fail validation."""
    yaml_data = """
    parameters:
      user id:
        description: Id of the user.
    """
    expected_error = "Field 'user id' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_parameters_invalid_key_special_chars() -> tuple[str, str]:
    """Parameters with key containing special characters - should fail validation."""
    yaml_data = """
    parameters:
      user@id:
        description: Id of the user.
    """
    expected_error = "Field 'user@id' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_parameters_invalid_key_parentheses() -> tuple[str, str]:
    """Parameters with key containing parentheses - should fail validation."""
    yaml_data = """
    parameters:
      user(id):
        description: Id of the user.
    """
    expected_error = "Field 'user(id)' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


class TestParameters:
    """Tests for Parameters model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_parameters_basic, case_parameters_with_references],
    )
    def test_parameters_validation(self, yaml_data: str) -> None:
        """Test Parameters model validation."""
        data = yaml.safe_load(yaml_data)
        parameters = Parameters.model_validate(data["parameters"])
        assert parameters is not None
        assert isinstance(parameters.root, dict)
        assert len(parameters.root) > 0

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_parameters_invalid_key_spaces,
            case_parameters_invalid_key_special_chars,
            case_parameters_invalid_key_parentheses,
        ],
    )
    def test_parameters_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test Parameters validation errors for invalid field names."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError) as exc_info:
            Parameters.model_validate(data["parameters"])
        assert expected_error in str(exc_info.value)

    def test_parameters_empty_dict_validation(self) -> None:
        """Test Parameters with empty dict validation."""
        parameters = Parameters.model_validate({})
        assert parameters is not None
        assert parameters.root == {}
        assert len(parameters.root) == 0

    def test_parameters_iteration(self) -> None:
        """Test Parameters __iter__ method."""
        user_id_param = Parameter(description="Id of the user.")
        channel_id_param = Parameter(description="Id of the channel.")

        data: dict[str, Parameter | Reference] = {
            "userId": user_id_param,
            "channelId": channel_id_param,
        }
        parameters = Parameters(root=data)

        keys = list(parameters)
        assert len(keys) == 2
        assert "userId" in keys
        assert "channelId" in keys

    def test_parameters_getitem(self) -> None:
        """Test Parameters __getitem__ method."""
        user_id_param = Parameter(description="Id of the user.")
        channel_id_param = Parameter(description="Id of the channel.")

        data: dict[str, Parameter | Reference] = {
            "userId": user_id_param,
            "channelId": channel_id_param,
        }
        parameters = Parameters(root=data)

        assert parameters["userId"] == user_id_param
        assert parameters["channelId"] == channel_id_param

    def test_parameters_getattr(self) -> None:
        """Test Parameters __getattr__ method."""
        user_id_param = Parameter(description="Id of the user.")
        channel_id_param = Parameter(description="Id of the channel.")

        data: dict[str, Parameter | Reference] = {
            "userId": user_id_param,
            "channelId": channel_id_param,
        }
        parameters = Parameters(root=data)

        assert parameters.userId == user_id_param
        assert parameters.channelId == channel_id_param


# CorrelationIDs Validation Test Cases
def case_correlation_ids_basic() -> str:
    """CorrelationIDs with basic correlation id objects."""
    return """
    correlationIds:
      default:
        location: $message.header#/correlationId
      requestId:
        location: $message.header#/requestId
    """


def case_correlation_ids_with_references() -> str:
    """CorrelationIDs with references."""
    return """
    correlationIds:
      default:
        $ref: '#/components/correlationIds/default'
      requestId:
        $ref: '#/components/correlationIds/requestId'
    """


# CorrelationIDs Validation Error Test Cases
def case_correlation_ids_invalid_key_spaces() -> tuple[str, str]:
    """CorrelationIDs with key containing spaces - should fail validation."""
    yaml_data = """
    correlationIds:
      default id:
        location: $message.header#/correlationId
    """
    expected_error = "Field 'default id' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_correlation_ids_invalid_key_special_chars() -> tuple[str, str]:
    """CorrelationIDs with key containing special characters - should fail validation."""
    yaml_data = """
    correlationIds:
      default@id:
        location: $message.header#/correlationId
    """
    expected_error = "Field 'default@id' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_correlation_ids_invalid_key_parentheses() -> tuple[str, str]:
    """CorrelationIDs with key containing parentheses - should fail validation."""
    yaml_data = """
    correlationIds:
      default(id):
        location: $message.header#/correlationId
    """
    expected_error = "Field 'default(id)' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


class TestCorrelationIDs:
    """Tests for CorrelationIDs model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_correlation_ids_basic, case_correlation_ids_with_references],
    )
    def test_correlation_ids_validation(self, yaml_data: str) -> None:
        """Test CorrelationIDs model validation."""
        data = yaml.safe_load(yaml_data)
        correlation_ids = CorrelationIDs.model_validate(data["correlationIds"])
        assert correlation_ids is not None
        assert isinstance(correlation_ids.root, dict)
        assert len(correlation_ids.root) > 0

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_correlation_ids_invalid_key_spaces,
            case_correlation_ids_invalid_key_special_chars,
            case_correlation_ids_invalid_key_parentheses,
        ],
    )
    def test_correlation_ids_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test CorrelationIDs validation errors for invalid field names."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError) as exc_info:
            CorrelationIDs.model_validate(data["correlationIds"])
        assert expected_error in str(exc_info.value)

    def test_correlation_ids_empty_dict_validation(self) -> None:
        """Test CorrelationIDs with empty dict validation."""
        correlation_ids = CorrelationIDs.model_validate({})
        assert correlation_ids is not None
        assert correlation_ids.root == {}
        assert len(correlation_ids.root) == 0

    def test_correlation_ids_iteration(self) -> None:
        """Test CorrelationIDs __iter__ method."""
        default_corr_id = CorrelationID(location="$message.header#/correlationId")
        request_id_corr_id = CorrelationID(location="$message.header#/requestId")

        data: dict[str, CorrelationID | Reference] = {
            "default": default_corr_id,
            "requestId": request_id_corr_id,
        }
        correlation_ids = CorrelationIDs(root=data)

        keys = list(correlation_ids)
        assert len(keys) == 2
        assert "default" in keys
        assert "requestId" in keys

    def test_correlation_ids_getitem(self) -> None:
        """Test CorrelationIDs __getitem__ method."""
        default_corr_id = CorrelationID(location="$message.header#/correlationId")
        request_id_corr_id = CorrelationID(location="$message.header#/requestId")

        data: dict[str, CorrelationID | Reference] = {
            "default": default_corr_id,
            "requestId": request_id_corr_id,
        }
        correlation_ids = CorrelationIDs(root=data)

        assert correlation_ids["default"] == default_corr_id
        assert correlation_ids["requestId"] == request_id_corr_id

    def test_correlation_ids_getattr(self) -> None:
        """Test CorrelationIDs __getattr__ method."""
        default_corr_id = CorrelationID(location="$message.header#/correlationId")
        request_id_corr_id = CorrelationID(location="$message.header#/requestId")

        data: dict[str, CorrelationID | Reference] = {
            "default": default_corr_id,
            "requestId": request_id_corr_id,
        }
        correlation_ids = CorrelationIDs(root=data)

        assert correlation_ids.default == default_corr_id
        assert correlation_ids.requestId == request_id_corr_id


# Replies Validation Test Cases
def case_replies_basic() -> str:
    """Replies with basic operation reply objects."""
    return """
    replies:
      userReply:
        address:
          location: $message.header#/replyTo
      adminReply:
        address:
          location: $message.header#/adminReplyTo
    """


def case_replies_with_references() -> str:
    """Replies with references."""
    return """
    replies:
      userReply:
        $ref: '#/components/replies/userReply'
      adminReply:
        $ref: '#/components/replies/adminReply'
    """


# Replies Validation Error Test Cases
def case_replies_invalid_key_spaces() -> tuple[str, str]:
    """Replies with key containing spaces - should fail validation."""
    yaml_data = """
    replies:
      user reply:
        address:
          location: $message.header#/replyTo
    """
    expected_error = "Field 'user reply' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_replies_invalid_key_special_chars() -> tuple[str, str]:
    """Replies with key containing special characters - should fail validation."""
    yaml_data = """
    replies:
      user@reply:
        address:
          location: $message.header#/replyTo
    """
    expected_error = "Field 'user@reply' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_replies_invalid_key_parentheses() -> tuple[str, str]:
    """Replies with key containing parentheses - should fail validation."""
    yaml_data = """
    replies:
      user(reply):
        address:
          location: $message.header#/replyTo
    """
    expected_error = "Field 'user(reply)' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


class TestReplies:
    """Tests for Replies model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_replies_basic, case_replies_with_references],
    )
    def test_replies_validation(self, yaml_data: str) -> None:
        """Test Replies model validation."""
        data = yaml.safe_load(yaml_data)
        replies = Replies.model_validate(data["replies"])
        assert replies is not None
        assert isinstance(replies.root, dict)
        assert len(replies.root) > 0

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_replies_invalid_key_spaces,
            case_replies_invalid_key_special_chars,
            case_replies_invalid_key_parentheses,
        ],
    )
    def test_replies_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test Replies validation errors for invalid field names."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError) as exc_info:
            Replies.model_validate(data["replies"])
        assert expected_error in str(exc_info.value)

    def test_replies_empty_dict_validation(self) -> None:
        """Test Replies with empty dict validation."""
        replies = Replies.model_validate({})
        assert replies is not None
        assert replies.root == {}
        assert len(replies.root) == 0

    def test_replies_iteration(self) -> None:
        """Test Replies __iter__ method."""
        user_reply = OperationReply(
            address=OperationReplyAddress(location="$message.header#/replyTo")
        )
        admin_reply = OperationReply(
            address=OperationReplyAddress(location="$message.header#/adminReplyTo")
        )

        data: dict[str, OperationReply | Reference] = {
            "userReply": user_reply,
            "adminReply": admin_reply,
        }
        replies = Replies(root=data)

        keys = list(replies)
        assert len(keys) == 2
        assert "userReply" in keys
        assert "adminReply" in keys

    def test_replies_getitem(self) -> None:
        """Test Replies __getitem__ method."""
        user_reply = OperationReply(
            address=OperationReplyAddress(location="$message.header#/replyTo")
        )
        admin_reply = OperationReply(
            address=OperationReplyAddress(location="$message.header#/adminReplyTo")
        )

        data: dict[str, OperationReply | Reference] = {
            "userReply": user_reply,
            "adminReply": admin_reply,
        }
        replies = Replies(root=data)

        assert replies["userReply"] == user_reply
        assert replies["adminReply"] == admin_reply

    def test_replies_getattr(self) -> None:
        """Test Replies __getattr__ method."""
        user_reply = OperationReply(
            address=OperationReplyAddress(location="$message.header#/replyTo")
        )
        admin_reply = OperationReply(
            address=OperationReplyAddress(location="$message.header#/adminReplyTo")
        )

        data: dict[str, OperationReply | Reference] = {
            "userReply": user_reply,
            "adminReply": admin_reply,
        }
        replies = Replies(root=data)

        assert replies.userReply == user_reply
        assert replies.adminReply == admin_reply


# ReplyAddresses Validation Test Cases
def case_reply_addresses_basic() -> str:
    """ReplyAddresses with basic operation reply address objects."""
    return """
    replyAddresses:
      userReplyAddress:
        location: $message.header#/replyTo
      adminReplyAddress:
        location: $message.header#/adminReplyTo
    """


def case_reply_addresses_with_references() -> str:
    """ReplyAddresses with references."""
    return """
    replyAddresses:
      userReplyAddress:
        $ref: '#/components/replyAddresses/userReplyAddress'
      adminReplyAddress:
        $ref: '#/components/replyAddresses/adminReplyAddress'
    """


# ReplyAddresses Validation Error Test Cases
def case_reply_addresses_invalid_key_spaces() -> tuple[str, str]:
    """ReplyAddresses with key containing spaces - should fail validation."""
    yaml_data = """
    replyAddresses:
      user reply address:
        location: $message.header#/replyTo
    """
    expected_error = "Field 'user reply address' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_reply_addresses_invalid_key_special_chars() -> tuple[str, str]:
    """ReplyAddresses with key containing special characters - should fail validation."""
    yaml_data = """
    replyAddresses:
      user@reply@address:
        location: $message.header#/replyTo
    """
    expected_error = "Field 'user@reply@address' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_reply_addresses_invalid_key_parentheses() -> tuple[str, str]:
    """ReplyAddresses with key containing parentheses - should fail validation."""
    yaml_data = """
    replyAddresses:
      user(reply)address:
        location: $message.header#/replyTo
    """
    expected_error = "Field 'user(reply)address' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


class TestReplyAddresses:
    """Tests for ReplyAddresses model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_reply_addresses_basic, case_reply_addresses_with_references],
    )
    def test_reply_addresses_validation(self, yaml_data: str) -> None:
        """Test ReplyAddresses model validation."""
        data = yaml.safe_load(yaml_data)
        reply_addresses = ReplyAddresses.model_validate(data["replyAddresses"])
        assert reply_addresses is not None
        assert isinstance(reply_addresses.root, dict)
        assert len(reply_addresses.root) > 0

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_reply_addresses_invalid_key_spaces,
            case_reply_addresses_invalid_key_special_chars,
            case_reply_addresses_invalid_key_parentheses,
        ],
    )
    def test_reply_addresses_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test ReplyAddresses validation errors for invalid field names."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError) as exc_info:
            ReplyAddresses.model_validate(data["replyAddresses"])
        assert expected_error in str(exc_info.value)

    def test_reply_addresses_empty_dict_validation(self) -> None:
        """Test ReplyAddresses with empty dict validation."""
        reply_addresses = ReplyAddresses.model_validate({})
        assert reply_addresses is not None
        assert reply_addresses.root == {}
        assert len(reply_addresses.root) == 0

    def test_reply_addresses_iteration(self) -> None:
        """Test ReplyAddresses __iter__ method."""
        user_reply_address = OperationReplyAddress(location="$message.header#/replyTo")
        admin_reply_address = OperationReplyAddress(
            location="$message.header#/adminReplyTo"
        )

        data: dict[str, OperationReplyAddress | Reference] = {
            "userReplyAddress": user_reply_address,
            "adminReplyAddress": admin_reply_address,
        }
        reply_addresses = ReplyAddresses(root=data)

        keys = list(reply_addresses)
        assert len(keys) == 2
        assert "userReplyAddress" in keys
        assert "adminReplyAddress" in keys

    def test_reply_addresses_getitem(self) -> None:
        """Test ReplyAddresses __getitem__ method."""
        user_reply_address = OperationReplyAddress(location="$message.header#/replyTo")
        admin_reply_address = OperationReplyAddress(
            location="$message.header#/adminReplyTo"
        )

        data: dict[str, OperationReplyAddress | Reference] = {
            "userReplyAddress": user_reply_address,
            "adminReplyAddress": admin_reply_address,
        }
        reply_addresses = ReplyAddresses(root=data)

        assert reply_addresses["userReplyAddress"] == user_reply_address
        assert reply_addresses["adminReplyAddress"] == admin_reply_address

    def test_reply_addresses_getattr(self) -> None:
        """Test ReplyAddresses __getattr__ method."""
        user_reply_address = OperationReplyAddress(location="$message.header#/replyTo")
        admin_reply_address = OperationReplyAddress(
            location="$message.header#/adminReplyTo"
        )

        data: dict[str, OperationReplyAddress | Reference] = {
            "userReplyAddress": user_reply_address,
            "adminReplyAddress": admin_reply_address,
        }
        reply_addresses = ReplyAddresses(root=data)

        assert reply_addresses.userReplyAddress == user_reply_address
        assert reply_addresses.adminReplyAddress == admin_reply_address


# ExternalDocs Validation Test Cases
def case_external_docs_basic() -> str:
    """ExternalDocs with basic external documentation objects."""
    return """
    externalDocs:
      infoDocs:
        url: https://example.com
        description: API documentation
      userDocs:
        url: https://example.com/users
    """


def case_external_docs_with_references() -> str:
    """ExternalDocs with references."""
    return """
    externalDocs:
      infoDocs:
        $ref: '#/components/externalDocs/infoDocs'
      userDocs:
        $ref: '#/components/externalDocs/userDocs'
    """


# ExternalDocs Validation Error Test Cases
def case_external_docs_invalid_key_spaces() -> tuple[str, str]:
    """ExternalDocs with key containing spaces - should fail validation."""
    yaml_data = """
    externalDocs:
      info docs:
        url: https://example.com
    """
    expected_error = "Field 'info docs' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_external_docs_invalid_key_special_chars() -> tuple[str, str]:
    """ExternalDocs with key containing special characters - should fail validation."""
    yaml_data = """
    externalDocs:
      info@docs:
        url: https://example.com
    """
    expected_error = "Field 'info@docs' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_external_docs_invalid_key_parentheses() -> tuple[str, str]:
    """ExternalDocs with key containing parentheses - should fail validation."""
    yaml_data = """
    externalDocs:
      info(docs):
        url: https://example.com
    """
    expected_error = "Field 'info(docs)' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


class TestExternalDocs:
    """Tests for ExternalDocs model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_external_docs_basic, case_external_docs_with_references],
    )
    def test_external_docs_validation(self, yaml_data: str) -> None:
        """Test ExternalDocs model validation."""
        data = yaml.safe_load(yaml_data)
        external_docs = ExternalDocs.model_validate(data["externalDocs"])
        assert external_docs is not None
        assert isinstance(external_docs.root, dict)
        assert len(external_docs.root) > 0

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_external_docs_invalid_key_spaces,
            case_external_docs_invalid_key_special_chars,
            case_external_docs_invalid_key_parentheses,
        ],
    )
    def test_external_docs_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test ExternalDocs validation errors for invalid field names."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError) as exc_info:
            ExternalDocs.model_validate(data["externalDocs"])
        assert expected_error in str(exc_info.value)

    def test_external_docs_empty_dict_validation(self) -> None:
        """Test ExternalDocs with empty dict validation."""
        external_docs = ExternalDocs.model_validate({})
        assert external_docs is not None
        assert external_docs.root == {}
        assert len(external_docs.root) == 0

    def test_external_docs_iteration(self) -> None:
        """Test ExternalDocs __iter__ method."""
        info_docs = ExternalDocumentation(
            url="https://example.com", description="API documentation"
        )
        user_docs = ExternalDocumentation(url="https://example.com/users")

        data: dict[str, ExternalDocumentation | Reference] = {
            "infoDocs": info_docs,
            "userDocs": user_docs,
        }
        external_docs = ExternalDocs(root=data)

        keys = list(external_docs)
        assert len(keys) == 2
        assert "infoDocs" in keys
        assert "userDocs" in keys

    def test_external_docs_getitem(self) -> None:
        """Test ExternalDocs __getitem__ method."""
        info_docs = ExternalDocumentation(
            url="https://example.com", description="API documentation"
        )
        user_docs = ExternalDocumentation(url="https://example.com/users")

        data: dict[str, ExternalDocumentation | Reference] = {
            "infoDocs": info_docs,
            "userDocs": user_docs,
        }
        external_docs = ExternalDocs(root=data)

        assert external_docs["infoDocs"] == info_docs
        assert external_docs["userDocs"] == user_docs

    def test_external_docs_getattr(self) -> None:
        """Test ExternalDocs __getattr__ method."""
        info_docs = ExternalDocumentation(
            url="https://example.com", description="API documentation"
        )
        user_docs = ExternalDocumentation(url="https://example.com/users")

        data: dict[str, ExternalDocumentation | Reference] = {
            "infoDocs": info_docs,
            "userDocs": user_docs,
        }
        external_docs = ExternalDocs(root=data)

        assert external_docs.infoDocs == info_docs
        assert external_docs.userDocs == user_docs


# Tags Validation Test Cases
def case_tags_basic() -> str:
    """Tags with basic tag objects."""
    return """
    tags:
      user:
        name: user
        description: User related operations
      admin:
        name: admin
        description: Admin related operations
    """


def case_tags_with_references() -> str:
    """Tags with references."""
    return """
    tags:
      user:
        $ref: '#/components/tags/user'
      admin:
        $ref: '#/components/tags/admin'
    """


# Tags Validation Error Test Cases
def case_tags_invalid_key_spaces() -> tuple[str, str]:
    """Tags with key containing spaces - should fail validation."""
    yaml_data = """
    tags:
      user tag:
        name: user
    """
    expected_error = "Field 'user tag' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_tags_invalid_key_special_chars() -> tuple[str, str]:
    """Tags with key containing special characters - should fail validation."""
    yaml_data = """
    tags:
      user@tag:
        name: user
    """
    expected_error = "Field 'user@tag' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_tags_invalid_key_parentheses() -> tuple[str, str]:
    """Tags with key containing parentheses - should fail validation."""
    yaml_data = """
    tags:
      user(tag):
        name: user
    """
    expected_error = "Field 'user(tag)' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


class TestTags:
    """Tests for Tags model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_tags_basic, case_tags_with_references],
    )
    def test_tags_validation(self, yaml_data: str) -> None:
        """Test Tags model validation."""
        data = yaml.safe_load(yaml_data)
        tags = Tags.model_validate(data["tags"])
        assert tags is not None
        assert isinstance(tags.root, dict)
        assert len(tags.root) > 0

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_tags_invalid_key_spaces,
            case_tags_invalid_key_special_chars,
            case_tags_invalid_key_parentheses,
        ],
    )
    def test_tags_validation_errors(self, yaml_data: str, expected_error: str) -> None:
        """Test Tags validation errors for invalid field names."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError) as exc_info:
            Tags.model_validate(data["tags"])
        assert expected_error in str(exc_info.value)

    def test_tags_empty_dict_validation(self) -> None:
        """Test Tags with empty dict validation."""
        tags = Tags.model_validate({})
        assert tags is not None
        assert tags.root == {}
        assert len(tags.root) == 0

    def test_tags_iteration(self) -> None:
        """Test Tags __iter__ method."""
        user_tag = Tag(name="user", description="User related operations")
        admin_tag = Tag(name="admin", description="Admin related operations")

        data: dict[str, Tag | Reference] = {
            "user": user_tag,
            "admin": admin_tag,
        }
        tags = Tags(root=data)

        keys = list(tags)
        assert len(keys) == 2
        assert "user" in keys
        assert "admin" in keys

    def test_tags_getitem(self) -> None:
        """Test Tags __getitem__ method."""
        user_tag = Tag(name="user", description="User related operations")
        admin_tag = Tag(name="admin", description="Admin related operations")

        data: dict[str, Tag | Reference] = {
            "user": user_tag,
            "admin": admin_tag,
        }
        tags = Tags(root=data)

        assert tags["user"] == user_tag
        assert tags["admin"] == admin_tag

    def test_tags_getattr(self) -> None:
        """Test Tags __getattr__ method."""
        user_tag = Tag(name="user", description="User related operations")
        admin_tag = Tag(name="admin", description="Admin related operations")

        data: dict[str, Tag | Reference] = {
            "user": user_tag,
            "admin": admin_tag,
        }
        tags = Tags(root=data)

        assert tags.user == user_tag
        assert tags.admin == admin_tag


# OperationTraits Validation Test Cases
def case_operation_traits_basic() -> str:
    """OperationTraits with basic operation trait objects."""
    return """
    operationTraits:
      httpTrait:
        bindings:
          http:
            method: POST
      summaryTrait:
        summary: "A summary of the operation"
    """


def case_operation_traits_with_references() -> str:
    """OperationTraits with references."""
    return """
    operationTraits:
      kafkaTrait:
        $ref: '#/components/operationTraits/kafkaTrait'
      httpTrait:
        $ref: '#/components/operationTraits/httpTrait'
    """


# OperationTraits Validation Error Test Cases
def case_operation_traits_invalid_key_spaces() -> tuple[str, str]:
    """OperationTraits with key containing spaces - should fail validation."""
    yaml_data = """
    operationTraits:
      kafka trait:
        summary: "A summary"
    """
    expected_error = "Field 'kafka trait' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_operation_traits_invalid_key_special_chars() -> tuple[str, str]:
    """OperationTraits with key containing special characters - should fail validation."""
    yaml_data = """
    operationTraits:
      kafka@trait:
        summary: "A summary"
    """
    expected_error = "Field 'kafka@trait' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_operation_traits_invalid_key_parentheses() -> tuple[str, str]:
    """OperationTraits with key containing parentheses - should fail validation."""
    yaml_data = """
    operationTraits:
      kafka(trait):
        summary: "A summary"
    """
    expected_error = "Field 'kafka(trait)' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


class TestOperationTraits:
    """Tests for OperationTraits model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_operation_traits_basic, case_operation_traits_with_references],
    )
    def test_operation_traits_validation(self, yaml_data: str) -> None:
        """Test OperationTraits model validation."""
        data = yaml.safe_load(yaml_data)
        operation_traits = OperationTraits.model_validate(data["operationTraits"])
        assert operation_traits is not None
        assert isinstance(operation_traits.root, dict)
        assert len(operation_traits.root) > 0

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_operation_traits_invalid_key_spaces,
            case_operation_traits_invalid_key_special_chars,
            case_operation_traits_invalid_key_parentheses,
        ],
    )
    def test_operation_traits_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test OperationTraits validation errors for invalid field names."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError) as exc_info:
            OperationTraits.model_validate(data["operationTraits"])
        assert expected_error in str(exc_info.value)

    def test_operation_traits_empty_dict_validation(self) -> None:
        """Test OperationTraits with empty dict validation."""
        operation_traits = OperationTraits.model_validate({})
        assert operation_traits is not None
        assert operation_traits.root == {}
        assert len(operation_traits.root) == 0

    def test_operation_traits_iteration(self) -> None:
        """Test OperationTraits __iter__ method."""
        http_trait = OperationTrait(bindings={"http": {"method": "POST"}})
        summary_trait = OperationTrait(summary="A summary of the operation")

        data: dict[str, OperationTrait | Reference] = {
            "httpTrait": http_trait,
            "summaryTrait": summary_trait,
        }
        operation_traits = OperationTraits(root=data)

        keys = list(operation_traits)
        assert len(keys) == 2
        assert "httpTrait" in keys
        assert "summaryTrait" in keys

    def test_operation_traits_getitem(self) -> None:
        """Test OperationTraits __getitem__ method."""
        http_trait = OperationTrait(bindings={"http": {"method": "POST"}})
        summary_trait = OperationTrait(summary="A summary of the operation")

        data: dict[str, OperationTrait | Reference] = {
            "httpTrait": http_trait,
            "summaryTrait": summary_trait,
        }
        operation_traits = OperationTraits(root=data)

        assert operation_traits["httpTrait"] == http_trait
        assert operation_traits["summaryTrait"] == summary_trait

    def test_operation_traits_getattr(self) -> None:
        """Test OperationTraits __getattr__ method."""
        http_trait = OperationTrait(bindings={"http": {"method": "POST"}})
        summary_trait = OperationTrait(summary="A summary of the operation")

        data: dict[str, OperationTrait | Reference] = {
            "httpTrait": http_trait,
            "summaryTrait": summary_trait,
        }
        operation_traits = OperationTraits(root=data)

        assert operation_traits.httpTrait == http_trait
        assert operation_traits.summaryTrait == summary_trait


# MessageTraits Validation Test Cases
def case_message_traits_basic() -> str:
    """MessageTraits with basic message trait objects."""
    return """
    messageTraits:
      commonHeaders:
        contentType: application/json
      eventHeaders:
        headers:
          type: object
          properties:
            eventId:
              type: string
    """


def case_message_traits_with_references() -> str:
    """MessageTraits with references."""
    return """
    messageTraits:
      commonHeaders:
        $ref: '#/components/messageTraits/commonHeaders'
      eventHeaders:
        $ref: '#/components/messageTraits/eventHeaders'
    """


# MessageTraits Validation Error Test Cases
def case_message_traits_invalid_key_spaces() -> tuple[str, str]:
    """MessageTraits with key containing spaces - should fail validation."""
    yaml_data = """
    messageTraits:
      common headers:
        contentType: application/json
    """
    expected_error = "Field 'common headers' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_message_traits_invalid_key_special_chars() -> tuple[str, str]:
    """MessageTraits with key containing special characters - should fail validation."""
    yaml_data = """
    messageTraits:
      common@headers:
        contentType: application/json
    """
    expected_error = "Field 'common@headers' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


def case_message_traits_invalid_key_parentheses() -> tuple[str, str]:
    """MessageTraits with key containing parentheses - should fail validation."""
    yaml_data = """
    messageTraits:
      common(headers):
        contentType: application/json
    """
    expected_error = "Field 'common(headers)' does not match patterned object key pattern. Keys must match [A-Za-z0-9\\.\\-_]+"
    return yaml_data, expected_error


class TestMessageTraits:
    """Tests for MessageTraits model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_message_traits_basic, case_message_traits_with_references],
    )
    def test_message_traits_validation(self, yaml_data: str) -> None:
        """Test MessageTraits model validation."""
        data = yaml.safe_load(yaml_data)
        message_traits = MessageTraits.model_validate(data["messageTraits"])
        assert message_traits is not None
        assert isinstance(message_traits.root, dict)
        assert len(message_traits.root) > 0

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_message_traits_invalid_key_spaces,
            case_message_traits_invalid_key_special_chars,
            case_message_traits_invalid_key_parentheses,
        ],
    )
    def test_message_traits_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test MessageTraits validation errors for invalid field names."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError) as exc_info:
            MessageTraits.model_validate(data["messageTraits"])
        assert expected_error in str(exc_info.value)

    def test_message_traits_empty_dict_validation(self) -> None:
        """Test MessageTraits with empty dict validation."""
        message_traits = MessageTraits.model_validate({})
        assert message_traits is not None
        assert message_traits.root == {}
        assert len(message_traits.root) == 0

    def test_message_traits_iteration(self) -> None:
        """Test MessageTraits __iter__ method."""
        common_headers = MessageTrait(content_type="application/json")
        event_headers = MessageTrait(
            headers=Schema(
                type="object",
                properties={"eventId": Schema(type="string")},
            ),
        )

        data: dict[str, MessageTrait | Reference] = {
            "commonHeaders": common_headers,
            "eventHeaders": event_headers,
        }
        message_traits = MessageTraits(root=data)

        keys = list(message_traits)
        assert len(keys) == 2
        assert "commonHeaders" in keys
        assert "eventHeaders" in keys

    def test_message_traits_getitem(self) -> None:
        """Test MessageTraits __getitem__ method."""
        common_headers = MessageTrait(content_type="application/json")
        event_headers = MessageTrait(
            headers=Schema(
                type="object",
                properties={"eventId": Schema(type="string")},
            ),
        )

        data: dict[str, MessageTrait | Reference] = {
            "commonHeaders": common_headers,
            "eventHeaders": event_headers,
        }
        message_traits = MessageTraits(root=data)

        assert message_traits["commonHeaders"] == common_headers
        assert message_traits["eventHeaders"] == event_headers

    def test_message_traits_getattr(self) -> None:
        """Test MessageTraits __getattr__ method."""
        common_headers = MessageTrait(content_type="application/json")
        event_headers = MessageTrait(
            headers=Schema(
                type="object",
                properties={"eventId": Schema(type="string")},
            ),
        )

        data: dict[str, MessageTrait | Reference] = {
            "commonHeaders": common_headers,
            "eventHeaders": event_headers,
        }
        message_traits = MessageTraits(root=data)

        assert message_traits.commonHeaders == common_headers
        assert message_traits.eventHeaders == event_headers


class TestServers:
    """Tests for Servers model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_servers_basic, case_servers_with_references],
    )
    def test_servers_validation(self, yaml_data: str) -> None:
        """Test Servers model validation."""
        data = yaml.safe_load(yaml_data)
        servers = Servers.model_validate(data["servers"])
        assert servers is not None
        assert isinstance(servers.root, dict)
        assert len(servers.root) > 0

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[case_servers_invalid_key_spaces],
    )
    def test_servers_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test Servers validation errors for invalid field names."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError) as exc_info:
            Servers.model_validate(data["servers"])
        assert expected_error in str(exc_info.value)

    def test_servers_empty_dict_validation(self) -> None:
        """Test Servers with empty dict validation."""
        servers = Servers.model_validate({})
        assert servers is not None
        assert servers.root == {}
        assert len(servers.root) == 0


class TestComponents:
    """Tests for Components model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[
            case_components_empty,
            case_components_with_messages,
            case_components_full,
        ],
    )
    def test_components_validation(self, yaml_data: str) -> None:
        """Test Components model validation."""
        data = yaml.safe_load(yaml_data)
        components = Components.model_validate(data)
        assert components is not None

    @parametrize_with_cases(
        "components,expected",
        cases=[
            case_components_serialization_empty,
            case_components_serialization_with_messages,
            case_components_serialization_with_schemas,
            case_components_serialization_with_servers,
            case_components_serialization_with_channels,
            case_components_serialization_with_operations,
            case_components_serialization_with_parameters,
            case_components_serialization_with_correlation_ids,
            case_components_serialization_with_security_schemes,
            case_components_serialization_with_server_variables,
            case_components_serialization_with_replies,
            case_components_serialization_with_reply_addresses,
            case_components_serialization_with_external_docs,
            case_components_serialization_with_tags,
            case_components_serialization_with_operation_traits,
            case_components_serialization_with_message_traits,
        ],
    )
    def test_components_serialization(
        self,
        components: Components,
        expected: dict,
    ) -> None:
        """Test Components serialization."""
        dumped = components.model_dump()
        assert dumped == expected

    def test_components_with_all_sections_validation(self) -> None:
        """Test Components with all sections validation."""

        yaml_data = """
        schemas:
          User:
            type: object
        servers:
          production:
            host: kafka.in.mycompany.com:9092
            protocol: kafka
        channels:
          userChannel:
            address: user/signedup
        operations:
          sendUserSignup:
            action: send
            channel:
              $ref: '#/channels/userChannel'
        messages:
          UserSignedUp:
            payload:
              type: object
        securitySchemes:
          apiKey:
            type: apiKey
            in: user
            name: api_key
        serverVariables:
          port:
            default: '1883'
        parameters:
          userId:
            description: Id of the user.
        correlationIds:
          default:
            location: $message.header#/correlationId
        replies:
          userReply:
            address:
              location: $message.header#/replyTo
        replyAddresses:
          userReplyAddress:
            location: $message.header#/replyTo
        externalDocs:
          infoDocs:
            url: https://example.com
        tags:
          user:
            name: user
        operationTraits:
          kafka:
            bindings:
              http:
                method: POST
        messageTraits:
          commonHeaders:
            contentType: application/json
        serverBindings:
          http:
            http: {}
        channelBindings:
          http:
            http: {}
        operationBindings:
          http:
            http:
              method: POST
        messageBindings:
          http:
            http:
              headers:
                type: object
        """
        data = yaml.safe_load(yaml_data)
        components = Components.model_validate(data)

        assert components.schemas is not None
        assert components.servers is not None
        assert components.channels is not None
        assert components.operations is not None
        assert components.messages is not None
        assert components.security_schemes is not None
        assert components.server_variables is not None
        assert components.parameters is not None
        assert components.correlation_ids is not None
        assert components.replies is not None
        assert components.reply_addresses is not None
        assert components.external_docs is not None
        assert components.tags is not None
        assert components.operation_traits is not None
        assert components.message_traits is not None
        assert components.server_bindings is not None
        assert components.channel_bindings is not None
        assert components.operation_bindings is not None
        assert components.message_bindings is not None
