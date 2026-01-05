"""Tests for message models."""

from typing import Any

import pytest
import yaml

from pytest_cases import parametrize_with_cases

from asyncapi3.models.base import Reference
from asyncapi3.models.message import Message, MessageExample, MessageTrait
from asyncapi3.models.schema import Schema


# MessageExample Validation Test Cases
def case_message_example_basic() -> str:
    """MessageExample with headers and payload."""
    return """
    headers:
      correlationId: my-correlation-id
      applicationInstanceId: myInstanceId
    payload:
      user:
        someUserKey: someUserValue
    """


def case_message_example_full() -> str:
    """MessageExample with all fields."""
    return """
    name: SimpleSignup
    summary: A simple UserSignup example message
    headers:
      correlationId: my-correlation-id
      applicationInstanceId: myInstanceId
    payload:
      user:
        someUserKey: someUserValue
      signup:
        someSignupKey: someSignupValue
    """


# MessageExample Serialization Test Cases
def case_message_example_serialization_basic() -> tuple[MessageExample, dict]:
    """MessageExample serialization with headers and payload."""
    message_example = MessageExample(
        headers={
            "correlationId": "my-correlation-id",
            "applicationInstanceId": "myInstanceId",
        },
        payload={"user": {"someUserKey": "someUserValue"}},
    )
    expected: dict[str, Any] = {
        "headers": {
            "correlationId": "my-correlation-id",
            "applicationInstanceId": "myInstanceId",
        },
        "payload": {"user": {"someUserKey": "someUserValue"}},
    }
    return message_example, expected


def case_message_example_serialization_full() -> tuple[MessageExample, dict]:
    """MessageExample serialization with all fields."""
    message_example = MessageExample(
        name="SimpleSignup",
        summary="A simple UserSignup example message",
        headers={
            "correlationId": "my-correlation-id",
            "applicationInstanceId": "myInstanceId",
        },
        payload={
            "user": {"someUserKey": "someUserValue"},
            "signup": {"someSignupKey": "someSignupValue"},
        },
    )
    expected: dict[str, Any] = {
        "name": "SimpleSignup",
        "summary": "A simple UserSignup example message",
        "headers": {
            "correlationId": "my-correlation-id",
            "applicationInstanceId": "myInstanceId",
        },
        "payload": {
            "user": {"someUserKey": "someUserValue"},
            "signup": {"someSignupKey": "someSignupValue"},
        },
    }
    return message_example, expected


def case_message_example_serialization_headers_only() -> tuple[MessageExample, dict]:
    """MessageExample serialization with headers only."""
    message_example = MessageExample(
        headers={"correlationId": "my-correlation-id"},
    )
    expected: dict[str, Any] = {
        "headers": {"correlationId": "my-correlation-id"},
    }
    return message_example, expected


def case_message_example_serialization_payload_only() -> tuple[MessageExample, dict]:
    """MessageExample serialization with payload only."""
    message_example = MessageExample(
        payload={"user": {"someUserKey": "someUserValue"}},
    )
    expected: dict[str, Any] = {
        "payload": {"user": {"someUserKey": "someUserValue"}},
    }
    return message_example, expected


# MessageTrait Validation Test Cases
def case_message_trait_basic() -> str:
    """MessageTrait with contentType only."""
    return """
    contentType: application/json
    """


def case_message_trait_full() -> str:
    """MessageTrait with multiple fields."""
    return """
    contentType: application/json
    name: CommonMessage
    title: Common Message
    summary: Common message trait
    description: A common message trait
    headers:
      type: object
      properties:
        correlationId:
          type: string
    """


# MessageTrait Serialization Test Cases
def case_message_trait_serialization_empty() -> tuple[MessageTrait, dict]:
    """MessageTrait serialization empty."""
    message_trait = MessageTrait()
    expected: dict[str, Any] = {}
    return message_trait, expected


def case_message_trait_serialization_basic() -> tuple[MessageTrait, dict]:
    """MessageTrait serialization with contentType only."""
    message_trait = MessageTrait(content_type="application/json")
    expected: dict[str, Any] = {"contentType": "application/json"}
    return message_trait, expected


def case_message_trait_serialization_with_headers() -> tuple[MessageTrait, dict]:
    """MessageTrait serialization with headers Schema."""
    message_trait = MessageTrait(
        content_type="application/json",
        headers=Schema(
            type="object",
            properties={"correlationId": Schema(type="string")},
        ),
    )
    expected: dict[str, Any] = {
        "contentType": "application/json",
        "headers": {
            "type": "object",
            "properties": {
                "correlationId": {
                    "type": "string",
                },
            },
        },
    }
    return message_trait, expected


# Message Validation Test Cases
def case_message_basic() -> str:
    """Message with payload only."""
    return """
    payload:
      type: object
      properties:
        displayName:
          type: string
        email:
          type: string
          format: email
    """


def case_message_full() -> str:
    """Message with all fields."""
    return """
    name: UserSignup
    title: User signup
    summary: Action to sign a user up.
    description: A longer description
    contentType: application/json
    tags:
      - name: user
      - name: signup
    headers:
      type: object
      properties:
        correlationId:
          description: Correlation ID set by application
          type: string
    payload:
      type: object
      properties:
        user:
          $ref: '#/components/schemas/userCreate'
    correlationId:
      description: Default Correlation ID
      location: $message.header#/correlationId
    examples:
      - name: SimpleSignup
        summary: A simple UserSignup example message
        headers:
          correlationId: my-correlation-id
        payload:
          user:
            someUserKey: someUserValue
    """


# Message Serialization Test Cases
def case_message_serialization_empty() -> tuple[Message, dict]:
    """Message serialization empty."""
    message = Message()
    expected: dict[str, Any] = {}
    return message, expected


def case_message_serialization_basic() -> tuple[Message, dict]:
    """Message serialization with payload only."""
    message = Message(
        payload=Schema(
            type="object",
            properties={
                "displayName": Schema(type="string"),
                "email": Schema(type="string", format="email"),
            },
        ),
    )
    expected: dict[str, Any] = {
        "payload": {
            "type": "object",
            "properties": {
                "displayName": {"type": "string"},
                "email": {"type": "string", "format": "email"},
            },
        },
    }
    return message, expected


def case_message_serialization_with_reference_payload() -> tuple[Message, dict]:
    """Message serialization with payload as Reference."""
    message = Message(
        payload=Reference(ref="#/components/schemas/userCreate"),
    )
    expected: dict[str, Any] = {
        "payload": {
            "$ref": "#/components/schemas/userCreate",
        },
    }
    return message, expected


def case_message_serialization_with_examples() -> tuple[Message, dict]:
    """Message serialization with examples."""
    message = Message(
        payload=Schema(type="object"),
        examples=[
            MessageExample(
                name="SimpleSignup",
                summary="A simple UserSignup example message",
                headers={"correlationId": "my-correlation-id"},
                payload={"user": {"someUserKey": "someUserValue"}},
            ),
        ],
    )
    expected: dict[str, Any] = {
        "payload": {"type": "object"},
        "examples": [
            {
                "name": "SimpleSignup",
                "summary": "A simple UserSignup example message",
                "headers": {"correlationId": "my-correlation-id"},
                "payload": {"user": {"someUserKey": "someUserValue"}},
            },
        ],
    }
    return message, expected


def case_message_serialization_with_traits() -> tuple[Message, dict]:
    """Message serialization with traits."""
    message = Message(
        payload=Schema(type="object"),
        traits=[Reference(ref="#/components/messageTraits/commonHeaders")],
    )
    expected: dict[str, Any] = {
        "payload": {"type": "object"},
        "traits": [
            {
                "$ref": "#/components/messageTraits/commonHeaders",
            },
        ],
    }
    return message, expected


class TestMessageExample:
    """Tests for MessageExample model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_message_example_basic, case_message_example_full],
    )
    def test_message_example_validation(self, yaml_data: str) -> None:
        """Test MessageExample model validation."""
        data = yaml.safe_load(yaml_data)
        message_example = MessageExample.model_validate(data)
        assert message_example is not None
        assert (
            message_example.headers is not None or message_example.payload is not None
        )

    @parametrize_with_cases(
        "message_example,expected",
        cases=[
            case_message_example_serialization_basic,
            case_message_example_serialization_full,
            case_message_example_serialization_headers_only,
            case_message_example_serialization_payload_only,
        ],
    )
    def test_message_example_serialization(
        self,
        message_example: MessageExample,
        expected: dict,
    ) -> None:
        """Test MessageExample serialization."""
        dumped = message_example.model_dump()
        assert dumped == expected

    def test_message_example_validation_error_no_headers_or_payload(self) -> None:
        """Test MessageExample validation error when neither headers nor payload are provided."""
        yaml_data = """
        name: InvalidExample
        summary: This should fail validation
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(
            ValueError,
            match="MessageExample MUST contain either headers and/or payload fields",
        ):
            MessageExample.model_validate(data)


class TestMessageTrait:
    """Tests for MessageTrait model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_message_trait_basic, case_message_trait_full],
    )
    def test_message_trait_validation(self, yaml_data: str) -> None:
        """Test MessageTrait model validation."""
        data = yaml.safe_load(yaml_data)
        message_trait = MessageTrait.model_validate(data)
        assert message_trait is not None
        if "contentType" in data:
            assert message_trait.content_type == data["contentType"]

    @parametrize_with_cases(
        "message_trait,expected",
        cases=[
            case_message_trait_serialization_empty,
            case_message_trait_serialization_basic,
            case_message_trait_serialization_with_headers,
        ],
    )
    def test_message_trait_serialization(
        self,
        message_trait: MessageTrait,
        expected: dict,
    ) -> None:
        """Test MessageTrait serialization."""
        dumped = message_trait.model_dump()
        assert dumped == expected

    def test_message_trait_with_headers_validation(self) -> None:
        """Test MessageTrait with headers Schema validation."""
        yaml_data = """
        contentType: application/json
        headers:
          type: object
          properties:
            correlationId:
              type: string
        """
        data = yaml.safe_load(yaml_data)
        message_trait = MessageTrait.model_validate(data)

        assert message_trait.content_type == "application/json"
        assert message_trait.headers is not None
        assert isinstance(message_trait.headers, Schema)
        assert message_trait.headers.type == "object"


class TestMessage:
    """Tests for Message model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_message_basic, case_message_full],
    )
    def test_message_validation(self, yaml_data: str) -> None:
        """Test Message model validation."""
        data = yaml.safe_load(yaml_data)
        message = Message.model_validate(data)
        assert message is not None
        if "payload" in data:
            assert message.payload is not None

    @parametrize_with_cases(
        "message,expected",
        cases=[
            case_message_serialization_empty,
            case_message_serialization_basic,
            case_message_serialization_with_reference_payload,
            case_message_serialization_with_examples,
            case_message_serialization_with_traits,
        ],
    )
    def test_message_serialization(self, message: Message, expected: dict) -> None:
        """Test Message serialization."""
        dumped = message.model_dump()
        assert dumped == expected

    def test_message_with_examples_validation(self) -> None:
        """Test Message with examples validation."""
        yaml_data = """
        payload:
          type: object
        examples:
          - name: SimpleSignup
            summary: A simple UserSignup example message
            headers:
              correlationId: my-correlation-id
            payload:
              user:
                someUserKey: someUserValue
        """
        data = yaml.safe_load(yaml_data)
        message = Message.model_validate(data)

        assert message.examples is not None
        assert len(message.examples) == 1
        assert isinstance(message.examples[0], MessageExample)
        assert message.examples[0].name == "SimpleSignup"
        assert message.examples[0].summary == "A simple UserSignup example message"

    def test_message_with_traits_validation(self) -> None:
        """Test Message with traits validation."""
        yaml_data = """
        payload:
          type: object
        traits:
          - $ref: '#/components/messageTraits/commonHeaders'
        """
        data = yaml.safe_load(yaml_data)
        message = Message.model_validate(data)

        assert message.traits is not None
        assert len(message.traits) == 1
        assert isinstance(message.traits[0], Reference)
        assert message.traits[0].ref == "#/components/messageTraits/commonHeaders"

    def test_message_with_reference_payload_validation(self) -> None:
        """Test Message with payload as Reference validation."""
        yaml_data = """
        payload:
          $ref: '#/components/schemas/userCreate'
        """
        data = yaml.safe_load(yaml_data)
        message = Message.model_validate(data)

        assert message.payload is not None
        assert isinstance(message.payload, Reference)
        assert message.payload.ref == "#/components/schemas/userCreate"
