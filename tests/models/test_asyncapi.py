"""Tests for AsyncAPI3 root model."""

from typing import Any

import pytest
import yaml

from pydantic import AnyUrl, ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.asyncapi import AsyncAPI3
from asyncapi3.models.base import Reference
from asyncapi3.models.channel import Channel
from asyncapi3.models.components import Components
from asyncapi3.models.info import Info
from asyncapi3.models.message import Message
from asyncapi3.models.operation import Operation
from asyncapi3.models.schema import Schema
from asyncapi3.models.server import Server


# AsyncAPI3 Validation Test Cases
def case_asyncapi_minimal() -> str:
    """AsyncAPI3 with required fields only."""
    return """
    asyncapi: 3.0.0
    info:
      title: Account Service
      version: 1.0.0
    """


def case_asyncapi_full() -> str:
    """AsyncAPI3 with all fields."""
    return """
    asyncapi: 3.0.0
    id: 'tag:stream.gitter.im,2022:api'
    info:
      title: Gitter Streaming API
      version: 1.0.0
      description: This is a sample app.
    servers:
      production:
        host: stream.gitter.im
        pathname: /v1
        protocol: https
    defaultContentType: application/json
    channels:
      rooms:
        address: '/rooms/{roomId}/{resource}'
        messages:
          chatMessage:
            $ref: '#/components/messages/chatMessage'
    operations:
      sendRoomInfo:
        action: send
        channel:
          $ref: '#/channels/rooms'
        messages:
          - $ref: '#/channels/rooms/messages/chatMessage'
    components:
      messages:
        chatMessage:
          payload:
            type: object
    """


def case_asyncapi_with_defaults() -> str:
    """AsyncAPI3 with default values."""
    return """
    asyncapi: 3.0.0
    info:
      title: My App
      version: 1.0.0
    """


def case_asyncapi_with_id() -> str:
    """AsyncAPI3 with id field."""
    return """
    asyncapi: 3.0.0
    id: 'https://example.com/my-api'
    info:
      title: My App
      version: 1.0.0
    """


def case_asyncapi_with_extensions() -> str:
    """AsyncAPI3 with specification extensions."""
    return """
    asyncapi: 3.0.0
    info:
      title: My App
      version: 1.0.0
    x-custom-extension: custom value
    x-another-extension:
      nested: value
    """


# AsyncAPI3 Validation Error Test Cases
def case_asyncapi_invalid_version() -> tuple[str, str]:
    """AsyncAPI3 with invalid version format."""
    yaml_data = """
    asyncapi: invalid.version
    info:
      title: My App
      version: 1.0.0
    """
    expected_error = (
        "asyncapi must be in semantic versioning format: major.minor.patch[-suffix]"
    )
    return yaml_data, expected_error


def case_asyncapi_invalid_id() -> tuple[str, str]:
    """AsyncAPI3 with invalid id (not a URI)."""
    yaml_data = """
    asyncapi: 3.0.0
    id: not-a-valid-uri
    info:
      title: My App
      version: 1.0.0
    """
    expected_error = "Input should be a valid URL"
    return yaml_data, expected_error


def case_asyncapi_unsupported_version() -> tuple[str, str]:
    """AsyncAPI3 with unsupported major version (not 3.x.x)."""
    yaml_data = """
    asyncapi: 2.6.0
    info:
      title: My App
      version: 1.0.0
    """
    expected_error = (
        "asyncapi version 2.6.0 is not supported. "
        "This application only supports AsyncAPI 3.x.x versions"
    )
    return yaml_data, expected_error


# AsyncAPI3 Serialization Test Cases
def case_asyncapi_serialization_minimal() -> tuple[AsyncAPI3, dict]:
    """AsyncAPI3 serialization with minimal required fields."""

    asyncapi = AsyncAPI3(info=Info(title="AsyncAPI Sample App", version="0.0.1"))
    expected: dict[str, Any] = {
        "asyncapi": "3.0.0",
        "info": {
            "title": "AsyncAPI Sample App",
            "version": "0.0.1",
        },
    }
    return asyncapi, expected


def case_asyncapi_serialization_with_id() -> tuple[AsyncAPI3, dict]:
    """AsyncAPI3 serialization with id field."""
    asyncapi = AsyncAPI3(
        id=AnyUrl("https://example.com/my-api"),
        info=Info(title="My App", version="1.0.0"),
    )
    expected: dict[str, Any] = {
        "asyncapi": "3.0.0",
        "id": "https://example.com/my-api",
        "info": {
            "title": "My App",
            "version": "1.0.0",
        },
    }
    return asyncapi, expected


def case_asyncapi_serialization_with_servers() -> tuple[AsyncAPI3, dict]:
    """AsyncAPI3 serialization with servers."""
    asyncapi = AsyncAPI3(
        info=Info(title="My App", version="1.0.0"),
        servers={
            "production": Server(host="kafka.in.mycompany.com:9092", protocol="kafka")
        },
    )
    expected: dict[str, Any] = {
        "asyncapi": "3.0.0",
        "info": {
            "title": "My App",
            "version": "1.0.0",
        },
        "servers": {
            "production": {
                "host": "kafka.in.mycompany.com:9092",
                "protocol": "kafka",
            },
        },
    }
    return asyncapi, expected


def case_asyncapi_serialization_with_channels() -> tuple[AsyncAPI3, dict]:
    """AsyncAPI3 serialization with channels."""
    asyncapi = AsyncAPI3(
        info=Info(title="My App", version="1.0.0"),
        channels={"userSignedup": Channel(address="user/signedup")},
    )
    expected: dict[str, Any] = {
        "asyncapi": "3.0.0",
        "info": {
            "title": "My App",
            "version": "1.0.0",
        },
        "channels": {
            "userSignedup": {
                "address": "user/signedup",
            },
        },
    }
    return asyncapi, expected


def case_asyncapi_serialization_with_operations_ref() -> tuple[AsyncAPI3, dict]:
    """AsyncAPI3 serialization with operations using Reference."""
    asyncapi = AsyncAPI3(
        info=Info(title="My App", version="1.0.0"),
        channels={"userSignedup": Channel(address="user/signedup")},
        operations={
            "sendUserSignedup": Operation(
                action="send",
                channel=Reference(ref="#/channels/userSignedup"),
            ),
        },
    )
    expected: dict[str, Any] = {
        "asyncapi": "3.0.0",
        "info": {
            "title": "My App",
            "version": "1.0.0",
        },
        "channels": {
            "userSignedup": {
                "address": "user/signedup",
            },
        },
        "operations": {
            "sendUserSignedup": {
                "action": "send",
                "channel": {
                    "$ref": "#/channels/userSignedup",
                },
            },
        },
    }
    return asyncapi, expected


def case_asyncapi_serialization_with_operations_multiple() -> tuple[AsyncAPI3, dict]:
    """AsyncAPI3 serialization with multiple operations."""
    asyncapi = AsyncAPI3(
        info=Info(title="My App", version="1.0.0"),
        channels={"userSignedup": Channel(address="user/signedup")},
        operations={
            "sendUserSignedup": Operation(
                action="send",
                channel=Reference(ref="#/channels/userSignedup"),
            ),
            "receiveUserSignedup": Operation(
                action="receive",
                channel=Reference(ref="#/channels/userSignedup"),
            ),
        },
    )
    expected: dict[str, Any] = {
        "asyncapi": "3.0.0",
        "info": {
            "title": "My App",
            "version": "1.0.0",
        },
        "channels": {
            "userSignedup": {
                "address": "user/signedup",
            },
        },
        "operations": {
            "sendUserSignedup": {
                "action": "send",
                "channel": {
                    "$ref": "#/channels/userSignedup",
                },
            },
            "receiveUserSignedup": {
                "action": "receive",
                "channel": {
                    "$ref": "#/channels/userSignedup",
                },
            },
        },
    }
    return asyncapi, expected


def case_asyncapi_serialization_with_components() -> tuple[AsyncAPI3, dict]:
    """AsyncAPI3 serialization with components."""
    asyncapi = AsyncAPI3(
        info=Info(title="My App", version="1.0.0"),
        components=Components(
            messages={"UserSignedUp": Message(payload=Schema(type="object"))},
        ),
    )
    expected: dict[str, Any] = {
        "asyncapi": "3.0.0",
        "info": {
            "title": "My App",
            "version": "1.0.0",
        },
        "components": {
            "messages": {
                "UserSignedUp": {
                    "payload": {
                        "type": "object",
                    },
                },
            },
        },
    }
    return asyncapi, expected


class TestAsyncAPI3:
    """Tests for AsyncAPI3 model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[
            case_asyncapi_minimal,
            case_asyncapi_full,
            case_asyncapi_with_defaults,
            case_asyncapi_with_id,
            case_asyncapi_with_extensions,
        ],
    )
    def test_asyncapi3_validation(self, yaml_data: str) -> None:
        """Test AsyncAPI3 model validation."""
        data = yaml.safe_load(yaml_data)
        asyncapi = AsyncAPI3.model_validate(data)
        assert asyncapi is not None
        assert asyncapi.asyncapi == "3.0.0"
        assert asyncapi.info is not None

    @parametrize_with_cases(
        "asyncapi,expected",
        cases=[
            case_asyncapi_serialization_minimal,
            case_asyncapi_serialization_with_servers,
            case_asyncapi_serialization_with_channels,
            case_asyncapi_serialization_with_operations_ref,
            case_asyncapi_serialization_with_operations_multiple,
            case_asyncapi_serialization_with_components,
            case_asyncapi_serialization_with_id,
        ],
    )
    def test_asyncapi3_serialization(self, asyncapi: AsyncAPI3, expected: dict) -> None:
        """Test AsyncAPI3 serialization."""
        dumped = asyncapi.model_dump(mode="json")
        assert dumped == expected

    def test_asyncapi3_with_servers_validation(self) -> None:
        """Test AsyncAPI3 with servers validation."""
        yaml_data = """
        asyncapi: 3.0.0
        info:
          title: My App
          version: 1.0.0
        servers:
          production:
            host: kafka.in.mycompany.com:9092
            protocol: kafka
        """
        data = yaml.safe_load(yaml_data)
        asyncapi = AsyncAPI3.model_validate(data)

        assert asyncapi.servers is not None
        assert "production" in asyncapi.servers
        assert asyncapi.servers["production"].host == "kafka.in.mycompany.com:9092"
        assert asyncapi.servers["production"].protocol == "kafka"

    def test_asyncapi3_with_channels_validation(self) -> None:
        """Test AsyncAPI3 with channels validation."""
        yaml_data = """
        asyncapi: 3.0.0
        info:
          title: My App
          version: 1.0.0
        channels:
          userSignedup:
            address: user/signedup
        """
        data = yaml.safe_load(yaml_data)
        asyncapi = AsyncAPI3.model_validate(data)

        assert asyncapi.channels is not None
        assert "userSignedup" in asyncapi.channels
        assert asyncapi.channels["userSignedup"].address == "user/signedup"

    def test_asyncapi3_with_operations_validation(self) -> None:
        """Test AsyncAPI3 with operations validation."""
        yaml_data = """
        asyncapi: 3.0.0
        info:
          title: My App
          version: 1.0.0
        channels:
          userSignedup:
            address: user/signedup
        operations:
          sendUserSignedup:
            action: send
            channel:
              $ref: '#/channels/userSignedup'
        """
        data = yaml.safe_load(yaml_data)
        asyncapi = AsyncAPI3.model_validate(data)

        assert asyncapi.operations is not None
        assert "sendUserSignedup" in asyncapi.operations
        assert asyncapi.operations["sendUserSignedup"].action == "send"

    def test_asyncapi3_with_components_validation(self) -> None:
        """Test AsyncAPI3 with components validation."""
        yaml_data = """
        asyncapi: 3.0.0
        info:
          title: My App
          version: 1.0.0
        components:
          messages:
            UserSignedUp:
              payload:
                type: object
        """
        data = yaml.safe_load(yaml_data)
        asyncapi = AsyncAPI3.model_validate(data)

        assert asyncapi.components is not None
        assert asyncapi.components.messages is not None
        assert "UserSignedUp" in asyncapi.components.messages

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_asyncapi_invalid_version,
            case_asyncapi_invalid_id,
            case_asyncapi_unsupported_version,
        ],
    )
    def test_asyncapi3_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test AsyncAPI3 validation error cases."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError) as exc_info:
            AsyncAPI3.model_validate(data)
        # Check that the expected error message is contained in the validation error
        assert expected_error in str(exc_info.value)

    def test_asyncapi3_extensions_validation(self) -> None:
        """Test AsyncAPI3 extensions validation."""
        yaml_data = """
        asyncapi: 3.0.0
        info:
          title: My App
          version: 1.0.0
        x-custom-extension: custom value
        x-another-extension:
          nested: value
        """
        data = yaml.safe_load(yaml_data)
        asyncapi = AsyncAPI3.model_validate(data)

        # Check that extensions are preserved (Pydantic v2 uses __pydantic_extra__)
        assert hasattr(asyncapi, "__pydantic_extra__")
        assert asyncapi.__pydantic_extra__ is not None
        assert "x-custom-extension" in asyncapi.__pydantic_extra__
        assert asyncapi.__pydantic_extra__["x-custom-extension"] == "custom value"
        assert "x-another-extension" in asyncapi.__pydantic_extra__
        assert asyncapi.__pydantic_extra__["x-another-extension"] == {"nested": "value"}
