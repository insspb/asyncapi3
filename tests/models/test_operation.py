"""Tests for operation models."""

from typing import Any

import yaml

from pytest_cases import parametrize_with_cases

from asyncapi3.models.base import Reference
from asyncapi3.models.operation import (
    Operation,
    OperationReply,
    OperationReplyAddress,
    OperationTrait,
)


# OperationReplyAddress Validation Test Cases
def case_operation_reply_address_basic() -> str:
    """OperationReplyAddress with location only."""
    return """
    location: '$message.header#/replyTo'
    """


def case_operation_reply_address_full() -> str:
    """OperationReplyAddress with location and description."""
    return """
    location: '$message.header#/replyTo'
    description: Reply address location
    """


# OperationReplyAddress Serialization Test Cases
def case_operation_reply_address_serialization_basic() -> tuple[
    OperationReplyAddress, dict
]:
    """OperationReplyAddress serialization with location only."""
    reply_address = OperationReplyAddress(location="$message.header#/replyTo")
    expected: dict[str, Any] = {"location": "$message.header#/replyTo"}
    return reply_address, expected


def case_operation_reply_address_serialization_full() -> tuple[
    OperationReplyAddress, dict
]:
    """OperationReplyAddress serialization with location and description."""
    reply_address = OperationReplyAddress(
        location="$message.header#/replyTo",
        description="Reply address location",
    )
    expected: dict[str, Any] = {
        "location": "$message.header#/replyTo",
        "description": "Reply address location",
    }
    return reply_address, expected


# OperationReply Validation Test Cases
def case_operation_reply_basic() -> str:
    """OperationReply with address only."""
    return """
    address:
      location: '$message.header#/replyTo'
    """


def case_operation_reply_full() -> str:
    """OperationReply with all fields."""
    return """
    address:
      location: '$message.header#/replyTo'
      description: Reply address location
    channel:
      $ref: '#/channels/userSignupReply'
    messages:
      - $ref: '#/channels/userSignupReply/messages/userSignedUpReply'
    """


# OperationReply Serialization Test Cases
def case_operation_reply_serialization_basic() -> tuple[OperationReply, dict]:
    """OperationReply serialization with address only."""
    reply = OperationReply(
        address=OperationReplyAddress(location="$message.header#/replyTo"),
    )
    expected: dict[str, Any] = {
        "address": {
            "location": "$message.header#/replyTo",
        },
    }
    return reply, expected


def case_operation_reply_serialization_with_reference_channel() -> tuple[
    OperationReply, dict
]:
    """OperationReply serialization with channel as Reference."""
    reply = OperationReply(
        address=OperationReplyAddress(location="$message.header#/replyTo"),
        channel=Reference(ref="#/channels/userSignupReply"),
    )
    expected: dict[str, Any] = {
        "address": {
            "location": "$message.header#/replyTo",
        },
        "channel": {
            "$ref": "#/channels/userSignupReply",
        },
    }
    return reply, expected


def case_operation_reply_serialization_full() -> tuple[OperationReply, dict]:
    """OperationReply serialization with all fields."""
    reply = OperationReply(
        address=OperationReplyAddress(
            location="$message.header#/replyTo",
            description="Reply address location",
        ),
        channel=Reference(ref="#/channels/userSignupReply"),
        messages=[
            Reference(ref="#/channels/userSignupReply/messages/userSignedUpReply"),
        ],
    )
    expected: dict[str, Any] = {
        "address": {
            "location": "$message.header#/replyTo",
            "description": "Reply address location",
        },
        "channel": {
            "$ref": "#/channels/userSignupReply",
        },
        "messages": [
            {
                "$ref": "#/channels/userSignupReply/messages/userSignedUpReply",
            },
        ],
    }
    return reply, expected


# OperationTrait Validation Test Cases
def case_operation_trait_basic() -> str:
    """OperationTrait with bindings only."""
    return """
    bindings:
      amqp:
        ack: false
    """


def case_operation_trait_full() -> str:
    """OperationTrait with multiple fields."""
    return """
    title: User sign up
    summary: Action to sign a user up.
    description: A longer description
    bindings:
      amqp:
        ack: false
    """


# OperationTrait Serialization Test Cases
def case_operation_trait_serialization_empty() -> tuple[OperationTrait, dict]:
    """OperationTrait serialization empty."""
    trait = OperationTrait()
    expected: dict[str, Any] = {}
    return trait, expected


# Operation Validation Test Cases
def case_operation_basic() -> str:
    """Operation with required fields only."""
    return """
    action: send
    channel:
      $ref: '#/channels/userSignup'
    """


def case_operation_full() -> str:
    """Operation with all fields."""
    return """
    title: User sign up
    summary: Action to sign a user up.
    description: A longer description
    channel:
      $ref: '#/channels/userSignup'
    action: send
    tags:
      - name: user
      - name: signup
    bindings:
      amqp:
        ack: false
    traits:
      - $ref: '#/components/operationTraits/kafka'
    messages:
      - $ref: '#/channels/userSignup/messages/userSignedUp'
    reply:
      address:
        location: '$message.header#/replyTo'
      channel:
        $ref: '#/channels/userSignupReply'
    """


# Operation Serialization Test Cases
def case_operation_serialization_basic() -> tuple[Operation, dict]:
    """Operation serialization with required fields only."""
    operation = Operation(
        action="send",
        channel=Reference(ref="#/channels/userSignup"),
    )
    expected: dict[str, Any] = {
        "action": "send",
        "channel": {
            "$ref": "#/channels/userSignup",
        },
    }
    return operation, expected


def case_operation_serialization_with_reply() -> tuple[Operation, dict]:
    """Operation serialization with reply."""
    operation = Operation(
        action="send",
        channel=Reference(ref="#/channels/userSignup"),
        reply=OperationReply(
            address=OperationReplyAddress(location="$message.header#/replyTo"),
            channel=Reference(ref="#/channels/userSignupReply"),
        ),
    )
    expected: dict[str, Any] = {
        "action": "send",
        "channel": {
            "$ref": "#/channels/userSignup",
        },
        "reply": {
            "address": {
                "location": "$message.header#/replyTo",
            },
            "channel": {
                "$ref": "#/channels/userSignupReply",
            },
        },
    }
    return operation, expected


def case_operation_serialization_with_messages() -> tuple[Operation, dict]:
    """Operation serialization with messages."""
    operation = Operation(
        action="send",
        channel=Reference(ref="#/channels/userSignup"),
        messages=[
            Reference(ref="#/channels/userSignup/messages/userSignedUp"),
        ],
    )
    expected: dict[str, Any] = {
        "action": "send",
        "channel": {
            "$ref": "#/channels/userSignup",
        },
        "messages": [
            {
                "$ref": "#/channels/userSignup/messages/userSignedUp",
            },
        ],
    }
    return operation, expected


def case_operation_serialization_with_traits() -> tuple[Operation, dict]:
    """Operation serialization with traits."""
    operation = Operation(
        action="send",
        channel=Reference(ref="#/channels/userSignup"),
        traits=[
            Reference(ref="#/components/operationTraits/kafka"),
        ],
    )
    expected: dict[str, Any] = {
        "action": "send",
        "channel": {
            "$ref": "#/channels/userSignup",
        },
        "traits": [
            {
                "$ref": "#/components/operationTraits/kafka",
            },
        ],
    }
    return operation, expected


class TestOperationReplyAddress:
    """Tests for OperationReplyAddress model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_operation_reply_address_basic, case_operation_reply_address_full],
    )
    def test_operation_reply_address_validation(self, yaml_data: str) -> None:
        """Test OperationReplyAddress model validation."""
        data = yaml.safe_load(yaml_data)
        reply_address = OperationReplyAddress.model_validate(data)
        assert reply_address is not None
        assert reply_address.location == "$message.header#/replyTo"

    @parametrize_with_cases(
        "reply_address,expected",
        cases=[
            case_operation_reply_address_serialization_basic,
            case_operation_reply_address_serialization_full,
        ],
    )
    def test_operation_reply_address_serialization(
        self,
        reply_address: OperationReplyAddress,
        expected: dict,
    ) -> None:
        """Test OperationReplyAddress serialization."""
        dumped = reply_address.model_dump()
        assert dumped == expected


class TestOperationReply:
    """Tests for OperationReply model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_operation_reply_basic, case_operation_reply_full],
    )
    def test_operation_reply_validation(self, yaml_data: str) -> None:
        """Test OperationReply model validation."""
        data = yaml.safe_load(yaml_data)
        reply = OperationReply.model_validate(data)
        assert reply is not None
        assert reply.address is not None

    @parametrize_with_cases(
        "reply,expected",
        cases=[
            case_operation_reply_serialization_basic,
            case_operation_reply_serialization_with_reference_channel,
            case_operation_reply_serialization_full,
        ],
    )
    def test_operation_reply_serialization(
        self,
        reply: OperationReply,
        expected: dict,
    ) -> None:
        """Test OperationReply serialization."""
        dumped = reply.model_dump()
        assert dumped == expected

    def test_operation_reply_with_reference_channel_validation(self) -> None:
        """Test OperationReply with channel as Reference validation."""
        yaml_data = """
        address:
          location: '$message.header#/replyTo'
        channel:
          $ref: '#/channels/userSignupReply'
        """
        data = yaml.safe_load(yaml_data)
        reply = OperationReply.model_validate(data)

        assert reply.channel is not None
        assert isinstance(reply.channel, Reference)
        assert reply.channel.ref == "#/channels/userSignupReply"


class TestOperationTrait:
    """Tests for OperationTrait model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_operation_trait_basic, case_operation_trait_full],
    )
    def test_operation_trait_validation(self, yaml_data: str) -> None:
        """Test OperationTrait model validation."""
        data = yaml.safe_load(yaml_data)
        trait = OperationTrait.model_validate(data)
        assert trait is not None

    @parametrize_with_cases(
        "trait,expected",
        cases=[case_operation_trait_serialization_empty],
    )
    def test_operation_trait_serialization(
        self,
        trait: OperationTrait,
        expected: dict,
    ) -> None:
        """Test OperationTrait serialization."""
        dumped = trait.model_dump()
        assert dumped == expected


class TestOperation:
    """Tests for Operation model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_operation_basic, case_operation_full],
    )
    def test_operation_validation(self, yaml_data: str) -> None:
        """Test Operation model validation."""
        data = yaml.safe_load(yaml_data)
        operation = Operation.model_validate(data)
        assert operation is not None
        assert operation.action in ["send", "receive"]
        assert operation.channel is not None

    @parametrize_with_cases(
        "operation,expected",
        cases=[
            case_operation_serialization_basic,
            case_operation_serialization_with_reply,
            case_operation_serialization_with_messages,
            case_operation_serialization_with_traits,
        ],
    )
    def test_operation_serialization(
        self, operation: Operation, expected: dict
    ) -> None:
        """Test Operation serialization."""
        dumped = operation.model_dump()
        assert dumped == expected

    def test_operation_with_reply_validation(self) -> None:
        """Test Operation with reply validation."""
        yaml_data = """
        action: send
        channel:
          $ref: '#/channels/userSignup'
        reply:
          address:
            location: '$message.header#/replyTo'
          channel:
            $ref: '#/channels/userSignupReply'
        """
        data = yaml.safe_load(yaml_data)
        operation = Operation.model_validate(data)

        assert operation.reply is not None
        assert isinstance(operation.reply, OperationReply)
        assert operation.reply.address is not None
        assert operation.reply.address.location == "$message.header#/replyTo"

    def test_operation_with_messages_validation(self) -> None:
        """Test Operation with messages validation."""
        yaml_data = """
        action: send
        channel:
          $ref: '#/channels/userSignup'
        messages:
          - $ref: '#/channels/userSignup/messages/userSignedUp'
        """
        data = yaml.safe_load(yaml_data)
        operation = Operation.model_validate(data)

        assert operation.messages is not None
        assert len(operation.messages) == 1
        assert isinstance(operation.messages[0], Reference)
        assert (
            operation.messages[0].ref == "#/channels/userSignup/messages/userSignedUp"
        )

    def test_operation_with_traits_validation(self) -> None:
        """Test Operation with traits validation."""
        yaml_data = """
        action: send
        channel:
          $ref: '#/channels/userSignup'
        traits:
          - $ref: '#/components/operationTraits/kafka'
        """
        data = yaml.safe_load(yaml_data)
        operation = Operation.model_validate(data)

        assert operation.traits is not None
        assert len(operation.traits) == 1
        assert isinstance(operation.traits[0], Reference)
        assert operation.traits[0].ref == "#/components/operationTraits/kafka"
