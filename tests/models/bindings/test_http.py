"""Tests for HTTP bindings models."""

from typing import Any

import pytest
import yaml

from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.bindings.http import (
    HTTPChannelBindings,
    HTTPMessageBindings,
    HTTPOperationBindings,
    HTTPServerBindings,
)
from asyncapi3.models.schema import Schema


# Operation Bindings Validation Test Cases
def case_operation_binding_get() -> str:
    """Operation binding for GET request."""
    return """
    http:
      method: GET
      query:
        type: object
        required:
          - companyId
        properties:
          companyId:
            type: number
            minimum: 1
            description: The Id of the company.
        additionalProperties: false
      bindingVersion: 0.3.0
    """


def case_operation_binding_post() -> str:
    """Operation binding for POST request."""
    return """
    http:
      method: POST
      bindingVersion: 0.3.0
    """


# Operation Bindings Serialization Test Cases
def case_operation_binding_serialization_post() -> tuple[HTTPOperationBindings, dict]:
    """Operation binding serialization for POST request."""
    http_binding = HTTPOperationBindings(method="POST")
    expected: dict[str, Any] = {
        "method": "POST",
        "bindingVersion": "0.3.0",
    }
    return http_binding, expected


def case_operation_binding_serialization_get() -> tuple[HTTPOperationBindings, dict]:
    """Operation binding serialization for GET request with query Schema."""
    http_binding = HTTPOperationBindings(
        method="GET",
        query=Schema(
            type="object",
            required=["companyId"],
            properties={
                "companyId": Schema(
                    type="number",
                    minimum=1,
                    description="The Id of the company.",
                ),
            },
            additional_properties=False,
        ),
    )
    expected: dict[str, Any] = {
        "method": "GET",
        "query": {
            "type": "object",
            "required": ["companyId"],
            "properties": {
                "companyId": {
                    "type": "number",
                    "minimum": 1,
                    "description": "The Id of the company.",
                },
            },
            "additional_properties": False,
        },
        "bindingVersion": "0.3.0",
    }
    return http_binding, expected


# Message Bindings Validation Test Cases
def case_message_binding_with_headers() -> str:
    """Message binding with headers and statusCode."""
    return """
    http:
      statusCode: 200
      headers:
        type: object
        properties:
          Content-Type:
            type: string
            enum: ['application/json']
      bindingVersion: 0.3.0
    """


# Message Bindings Serialization Test Cases
def case_message_binding_serialization_empty() -> tuple[HTTPMessageBindings, dict]:
    """Message binding serialization empty."""
    http_binding = HTTPMessageBindings()
    expected: dict[str, Any] = {"bindingVersion": "0.3.0"}
    return http_binding, expected


def case_message_binding_serialization_with_headers() -> tuple[
    HTTPMessageBindings, dict
]:
    """Message binding serialization with headers and statusCode."""
    http_binding = HTTPMessageBindings(
        status_code=200,
        headers=Schema(
            type="object",
            properties={
                "Content-Type": Schema(
                    type="string",
                    enum=["application/json"],
                ),
            },
        ),
    )
    expected: dict[str, Any] = {
        "statusCode": 200,
        "headers": {
            "type": "object",
            "properties": {
                "Content-Type": {
                    "type": "string",
                    "enum": ["application/json"],
                },
            },
        },
        "bindingVersion": "0.3.0",
    }
    return http_binding, expected


class TestHTTPServerBindings:
    """Tests for HTTPServerBindings model."""

    def test_http_server_bindings_serialization(self) -> None:
        """Test HTTPServerBindings serialization."""
        http_binding = HTTPServerBindings()
        dumped = http_binding.model_dump()
        assert dumped == {}

    def test_http_server_bindings_python_validation_error(self) -> None:
        """Test HTTPServerBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            HTTPServerBindings(some_field="value")

    def test_http_server_bindings_yaml_validation_error(self) -> None:
        """Test HTTPServerBindings YAML validation error with any fields."""
        yaml_data = """
        http:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            HTTPServerBindings.model_validate(data["http"])

    def test_http_server_bindings_yaml_empty_validation(self) -> None:
        """Test HTTPServerBindings YAML validation with no fields."""
        yaml_data = """
        http: {}
        """
        data = yaml.safe_load(yaml_data)
        http_binding = HTTPServerBindings.model_validate(data["http"])
        assert http_binding is not None


class TestHTTPChannelBindings:
    """Tests for HTTPChannelBindings model."""

    def test_http_channel_bindings_serialization(self) -> None:
        """Test HTTPChannelBindings serialization."""
        http_binding = HTTPChannelBindings()
        dumped = http_binding.model_dump()
        assert dumped == {}

    def test_http_channel_bindings_python_validation_error(self) -> None:
        """Test HTTPChannelBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            HTTPChannelBindings(some_field="value")

    def test_http_channel_bindings_yaml_validation_error(self) -> None:
        """Test HTTPChannelBindings YAML validation error with any fields."""
        yaml_data = """
        http:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            HTTPChannelBindings.model_validate(data["http"])

    def test_http_channel_bindings_yaml_empty_validation(self) -> None:
        """Test HTTPChannelBindings YAML validation with no fields."""
        yaml_data = """
        http: {}
        """
        data = yaml.safe_load(yaml_data)
        http_binding = HTTPChannelBindings.model_validate(data["http"])
        assert http_binding is not None


class TestHTTPOperationBindings:
    """Tests for HTTPOperationBindings model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_operation_binding_get, case_operation_binding_post],
    )
    def test_http_operation_bindings_validation(self, yaml_data: str) -> None:
        """Test HTTPOperationBindings model validation."""
        data = yaml.safe_load(yaml_data)
        http_binding = HTTPOperationBindings.model_validate(data["http"])
        assert http_binding is not None
        assert http_binding.binding_version == "0.3.0"

    @parametrize_with_cases(
        "http_binding,expected",
        cases=[
            case_operation_binding_serialization_post,
            case_operation_binding_serialization_get,
        ],
    )
    def test_http_operation_bindings_serialization(
        self,
        http_binding: HTTPOperationBindings,
        expected: dict,
    ) -> None:
        """Test HTTPOperationBindings serialization."""
        dumped = http_binding.model_dump()
        assert dumped == expected

    def test_http_operation_binding_query_schema_validation(self) -> None:
        """Test HTTPOperationBindings with query as Schema validation."""
        yaml_data = """
        http:
          method: GET
          query:
            type: object
            required:
              - companyId
            properties:
              companyId:
                type: number
                minimum: 1
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        http_binding = HTTPOperationBindings.model_validate(data["http"])

        assert http_binding.method == "GET"
        assert http_binding.query is not None
        assert isinstance(http_binding.query, Schema)
        assert http_binding.query.type == "object"
        assert http_binding.binding_version == "0.3.0"

    def test_http_operation_bindings_python_validation_error(self) -> None:
        """Test HTTPOperationBindings Python validation error with extra arguments."""
        with pytest.raises(ValidationError):
            HTTPOperationBindings(method="GET", some_field="value")

    def test_http_operation_bindings_yaml_validation_error(self) -> None:
        """Test HTTPOperationBindings YAML validation error with extra fields."""
        yaml_data = """
        http:
          method: GET
          some_field: value
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            HTTPOperationBindings.model_validate(data["http"])


class TestHTTPMessageBindings:
    """Tests for HTTPMessageBindings model."""

    @parametrize_with_cases("yaml_data", cases=[case_message_binding_with_headers])
    def test_http_message_bindings_validation(self, yaml_data: str) -> None:
        """Test HTTPMessageBindings model validation."""
        data = yaml.safe_load(yaml_data)
        http_binding = HTTPMessageBindings.model_validate(data["http"])
        assert http_binding is not None
        assert http_binding.binding_version == "0.3.0"

    @parametrize_with_cases(
        "http_binding,expected",
        cases=[
            case_message_binding_serialization_empty,
            case_message_binding_serialization_with_headers,
        ],
    )
    def test_http_message_bindings_serialization(
        self,
        http_binding: HTTPMessageBindings,
        expected: dict,
    ) -> None:
        """Test HTTPMessageBindings serialization."""
        dumped = http_binding.model_dump()
        assert dumped == expected

    def test_http_message_binding_all_fields_validation(self) -> None:
        """Test HTTPMessageBindings with all fields validation."""
        yaml_data = """
        http:
          statusCode: 200
          headers:
            type: object
            properties:
              Content-Type:
                type: string
                enum: ['application/json']
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        http_binding = HTTPMessageBindings.model_validate(data["http"])

        assert http_binding.status_code == 200
        assert http_binding.headers is not None
        assert isinstance(http_binding.headers, Schema)
        assert http_binding.headers.type == "object"
        assert http_binding.binding_version == "0.3.0"

    def test_http_message_bindings_python_validation_error(self) -> None:
        """Test HTTPMessageBindings Python validation error with extra arguments."""
        with pytest.raises(ValidationError):
            HTTPMessageBindings(some_field="value")

    def test_http_message_bindings_yaml_validation_error(self) -> None:
        """Test HTTPMessageBindings YAML validation error with extra fields."""
        yaml_data = """
        http:
          some_field: value
          bindingVersion: 0.3.0
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            HTTPMessageBindings.model_validate(data["http"])
