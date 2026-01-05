"""Tests for WebSockets bindings models."""

from typing import Any

import pytest
import yaml

from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.bindings.websockets import (
    WebSocketsChannelBindings,
    WebSocketsMessageBindings,
    WebSocketsOperationBindings,
    WebSocketsServerBindings,
)
from asyncapi3.models.schema import Schema


# Channel Bindings Validation Test Cases
def case_channel_binding_get() -> str:
    """Channel binding with GET method."""
    return """
    ws:
      method: GET
      bindingVersion: 0.1.0
    """


def case_channel_binding_post_with_query() -> str:
    """Channel binding with POST method and query Schema."""
    return """
    ws:
      method: POST
      query:
        type: object
        properties:
          token:
            type: string
      bindingVersion: 0.1.0
    """


def case_channel_binding_with_headers() -> str:
    """Channel binding with headers Schema."""
    return """
    ws:
      method: GET
      headers:
        type: object
        properties:
          Authorization:
            type: string
      bindingVersion: 0.1.0
    """


# Channel Bindings Serialization Test Cases
def case_websockets_channel_binding_serialization_empty() -> tuple[
    WebSocketsChannelBindings, dict
]:
    """WebSocketsChannelBindings serialization empty."""
    ws_binding = WebSocketsChannelBindings()
    expected: dict[str, Any] = {"bindingVersion": "0.1.0"}
    return ws_binding, expected


def case_websockets_channel_binding_serialization_get() -> tuple[
    WebSocketsChannelBindings, dict
]:
    """WebSocketsChannelBindings serialization with GET method."""
    ws_binding = WebSocketsChannelBindings(method="GET")
    expected: dict[str, Any] = {
        "method": "GET",
        "bindingVersion": "0.1.0",
    }
    return ws_binding, expected


def case_websockets_channel_binding_serialization_with_query() -> tuple[
    WebSocketsChannelBindings, dict
]:
    """WebSocketsChannelBindings serialization with POST method and query Schema."""
    ws_binding = WebSocketsChannelBindings(
        method="POST",
        query=Schema(
            type="object",
            properties={"token": Schema(type="string")},
        ),
    )
    expected: dict[str, Any] = {
        "method": "POST",
        "query": {
            "type": "object",
            "properties": {
                "token": {
                    "type": "string",
                },
            },
        },
        "bindingVersion": "0.1.0",
    }
    return ws_binding, expected


def case_websockets_channel_binding_serialization_with_headers() -> tuple[
    WebSocketsChannelBindings, dict
]:
    """WebSocketsChannelBindings serialization with headers Schema."""
    ws_binding = WebSocketsChannelBindings(
        method="GET",
        headers=Schema(
            type="object",
            properties={"Authorization": Schema(type="string")},
        ),
    )
    expected: dict[str, Any] = {
        "method": "GET",
        "headers": {
            "type": "object",
            "properties": {
                "Authorization": {
                    "type": "string",
                },
            },
        },
        "bindingVersion": "0.1.0",
    }
    return ws_binding, expected


class TestWebSocketsServerBindings:
    """Tests for WebSocketsServerBindings model."""

    def test_websockets_server_bindings_serialization(self) -> None:
        """Test WebSocketsServerBindings serialization."""
        ws_binding = WebSocketsServerBindings()
        dumped = ws_binding.model_dump()
        assert dumped == {}

    def test_websockets_server_bindings_python_validation_error(self) -> None:
        """Test WebSocketsServerBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            WebSocketsServerBindings(some_field="value")

    def test_websockets_server_bindings_yaml_validation_error(self) -> None:
        """Test WebSocketsServerBindings YAML validation error with any fields."""
        yaml_data = """
        ws:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            WebSocketsServerBindings.model_validate(data["ws"])

    def test_websockets_server_bindings_yaml_empty_validation(self) -> None:
        """Test WebSocketsServerBindings YAML validation with no fields."""
        yaml_data = """
        ws: {}
        """
        data = yaml.safe_load(yaml_data)
        ws_binding = WebSocketsServerBindings.model_validate(data["ws"])
        assert ws_binding is not None


class TestWebSocketsChannelBindings:
    """Tests for WebSocketsChannelBindings model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[
            case_channel_binding_get,
            case_channel_binding_post_with_query,
            case_channel_binding_with_headers,
        ],
    )
    def test_websockets_channel_bindings_validation(self, yaml_data: str) -> None:
        """Test WebSocketsChannelBindings model validation."""
        data = yaml.safe_load(yaml_data)
        ws_binding = WebSocketsChannelBindings.model_validate(data["ws"])
        assert ws_binding is not None
        assert ws_binding.binding_version == "0.1.0"

    @parametrize_with_cases(
        "ws_binding,expected",
        cases=[
            case_websockets_channel_binding_serialization_empty,
            case_websockets_channel_binding_serialization_get,
            case_websockets_channel_binding_serialization_with_query,
            case_websockets_channel_binding_serialization_with_headers,
        ],
    )
    def test_websockets_channel_bindings_serialization(
        self,
        ws_binding: WebSocketsChannelBindings,
        expected: dict,
    ) -> None:
        """Test WebSocketsChannelBindings serialization."""
        dumped = ws_binding.model_dump()
        assert dumped == expected

    def test_websockets_channel_binding_query_schema_validation(self) -> None:
        """Test WebSocketsChannelBindings with query as Schema validation."""
        yaml_data = """
        ws:
          method: POST
          query:
            type: object
            properties:
              token:
                type: string
          bindingVersion: 0.1.0
        """
        data = yaml.safe_load(yaml_data)
        ws_binding = WebSocketsChannelBindings.model_validate(data["ws"])

        assert ws_binding.method == "POST"
        assert ws_binding.query is not None
        assert isinstance(ws_binding.query, Schema)
        assert ws_binding.query.type == "object"
        assert ws_binding.binding_version == "0.1.0"

    def test_websockets_channel_binding_headers_schema_validation(self) -> None:
        """Test WebSocketsChannelBindings with headers as Schema validation."""
        yaml_data = """
        ws:
          method: GET
          headers:
            type: object
            properties:
              Authorization:
                type: string
          bindingVersion: 0.1.0
        """
        data = yaml.safe_load(yaml_data)
        ws_binding = WebSocketsChannelBindings.model_validate(data["ws"])

        assert ws_binding.method == "GET"
        assert ws_binding.headers is not None
        assert isinstance(ws_binding.headers, Schema)
        assert ws_binding.headers.type == "object"
        assert ws_binding.binding_version == "0.1.0"

    def test_websockets_channel_bindings_python_validation_error(self) -> None:
        """Test WebSocketsChannelBindings Python validation error with invalid arguments."""
        with pytest.raises(ValidationError):
            WebSocketsChannelBindings(method="GET", invalid_field="value")

    def test_websockets_channel_bindings_yaml_validation_error(self) -> None:
        """Test WebSocketsChannelBindings YAML validation error with invalid fields."""
        yaml_data = """
        ws:
          method: GET
          invalid_field: value
          bindingVersion: 0.1.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            WebSocketsChannelBindings.model_validate(data["ws"])


class TestWebSocketsOperationBindings:
    """Tests for WebSocketsOperationBindings model."""

    def test_websockets_operation_bindings_serialization(self) -> None:
        """Test WebSocketsOperationBindings serialization."""
        ws_binding = WebSocketsOperationBindings()
        dumped = ws_binding.model_dump()
        assert dumped == {}

    def test_websockets_operation_bindings_python_validation_error(self) -> None:
        """Test WebSocketsOperationBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            WebSocketsOperationBindings(some_field="value")

    def test_websockets_operation_bindings_yaml_validation_error(self) -> None:
        """Test WebSocketsOperationBindings YAML validation error with any fields."""
        yaml_data = """
        ws:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            WebSocketsOperationBindings.model_validate(data["ws"])

    def test_websockets_operation_bindings_yaml_empty_validation(self) -> None:
        """Test WebSocketsOperationBindings YAML validation with no fields."""
        yaml_data = """
        ws: {}
        """
        data = yaml.safe_load(yaml_data)
        ws_binding = WebSocketsOperationBindings.model_validate(data["ws"])
        assert ws_binding is not None


class TestWebSocketsMessageBindings:
    """Tests for WebSocketsMessageBindings model."""

    def test_websockets_message_bindings_serialization(self) -> None:
        """Test WebSocketsMessageBindings serialization."""
        ws_binding = WebSocketsMessageBindings()
        dumped = ws_binding.model_dump()
        assert dumped == {}

    def test_websockets_message_bindings_python_validation_error(self) -> None:
        """Test WebSocketsMessageBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            WebSocketsMessageBindings(some_field="value")

    def test_websockets_message_bindings_yaml_validation_error(self) -> None:
        """Test WebSocketsMessageBindings YAML validation error with any fields."""
        yaml_data = """
        ws:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            WebSocketsMessageBindings.model_validate(data["ws"])

    def test_websockets_message_bindings_yaml_empty_validation(self) -> None:
        """Test WebSocketsMessageBindings YAML validation with no fields."""
        yaml_data = """
        ws: {}
        """
        data = yaml.safe_load(yaml_data)
        ws_binding = WebSocketsMessageBindings.model_validate(data["ws"])
        assert ws_binding is not None
