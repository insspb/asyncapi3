"""Tests for base models."""

from typing import Any

import pytest
import yaml

from pydantic import AnyUrl, ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.base import ExternalDocumentation, Reference, Tag
from asyncapi3.models.base_models import ExtendableBaseModel


# Reference Validation Test Cases
def case_reference_basic() -> str:
    """Reference with basic $ref."""
    return """
    $ref: '#/components/schemas/Pet'
    """


def case_reference_components() -> str:
    """Reference to components."""
    return """
    $ref: '#/components/messages/userSignUp'
    """


# Reference Serialization Test Cases
def case_reference_serialization_basic() -> tuple[Reference, dict]:
    """Reference serialization with basic $ref."""
    reference = Reference(ref="#/components/schemas/Pet")
    expected: dict[str, Any] = {"$ref": "#/components/schemas/Pet"}
    return reference, expected


def case_reference_serialization_components() -> tuple[Reference, dict]:
    """Reference serialization to components."""
    reference = Reference(ref="#/components/messages/userSignUp")
    expected: dict[str, Any] = {"$ref": "#/components/messages/userSignUp"}
    return reference, expected


# ExternalDocumentation Validation Test Cases
def case_external_docs_basic() -> str:
    """ExternalDocumentation with url only."""
    return """
    url: https://example.com
    """


def case_external_docs_full() -> str:
    """ExternalDocumentation with url and description."""
    return """
    description: Find more info here
    url: https://example.com
    """


# ExternalDocumentation Serialization Test Cases
def case_external_docs_serialization_basic() -> tuple[ExternalDocumentation, dict]:
    """ExternalDocumentation serialization with url only."""
    external_docs = ExternalDocumentation(url="https://example.com")
    expected: dict[str, Any] = {"url": AnyUrl("https://example.com/")}
    return external_docs, expected


def case_external_docs_serialization_full() -> tuple[ExternalDocumentation, dict]:
    """ExternalDocumentation serialization with url and description."""
    external_docs = ExternalDocumentation(
        url="https://example.com",
        description="Find more info here",
    )
    expected: dict[str, Any] = {
        "url": AnyUrl("https://example.com/"),
        "description": "Find more info here",
    }
    return external_docs, expected


# Tag Validation Test Cases
def case_tag_basic() -> str:
    """Tag with name only."""
    return """
    name: user
    """


def case_tag_full() -> str:
    """Tag with name and description."""
    return """
    name: user
    description: User-related messages
    """


def case_tag_with_external_docs() -> str:
    """Tag with name, description and externalDocs."""
    return """
    name: e-commerce
    description: E-commerce related messages
    externalDocs:
      description: Find more info here
      url: https://example.com
    """


# Tag Serialization Test Cases
def case_tag_serialization_basic() -> tuple[Tag, dict]:
    """Tag serialization with name only."""
    tag = Tag(name="user")
    expected: dict[str, Any] = {"name": "user"}
    return tag, expected


def case_tag_serialization_full() -> tuple[Tag, dict]:
    """Tag serialization with name and description."""
    tag = Tag(name="user", description="User-related messages")
    expected: dict[str, Any] = {
        "name": "user",
        "description": "User-related messages",
    }
    return tag, expected


def case_tag_serialization_with_external_docs() -> tuple[Tag, dict]:
    """Tag serialization with externalDocs object."""
    tag = Tag(
        name="e-commerce",
        description="E-commerce related messages",
        external_docs=ExternalDocumentation(
            url="https://example.com",
            description="Find more info here",
        ),
    )
    expected: dict[str, Any] = {
        "name": "e-commerce",
        "description": "E-commerce related messages",
        "externalDocs": {
            "url": AnyUrl("https://example.com/"),
            "description": "Find more info here",
        },
    }
    return tag, expected


def case_tag_serialization_with_reference_external_docs() -> tuple[Tag, dict]:
    """Tag serialization with externalDocs as Reference."""
    tag = Tag(
        name="user",
        external_docs=Reference(ref="#/components/externalDocs/infoDocs"),
    )
    expected: dict[str, Any] = {
        "name": "user",
        "externalDocs": {
            "$ref": "#/components/externalDocs/infoDocs",
        },
    }
    return tag, expected


class TestReference:
    """Tests for Reference model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_reference_basic, case_reference_components],
    )
    def test_reference_validation(self, yaml_data: str) -> None:
        """Test Reference model validation."""
        data = yaml.safe_load(yaml_data)
        reference = Reference.model_validate(data)
        assert reference is not None
        assert reference.ref.startswith("#/")

    @parametrize_with_cases(
        "reference,expected",
        cases=[
            case_reference_serialization_basic,
            case_reference_serialization_components,
        ],
    )
    def test_reference_serialization(
        self, reference: Reference, expected: dict
    ) -> None:
        """Test Reference serialization."""
        dumped = reference.model_dump()
        assert dumped == expected

    def test_reference_forbids_extra_fields(self) -> None:
        """Test that Reference forbids extra fields (inherits from NonExtendableBaseModel)."""
        yaml_data = """
        $ref: '#/components/schemas/Pet'
        extra_field: should_fail
        """
        data = yaml.safe_load(yaml_data)

        with pytest.raises(ValidationError) as exc_info:
            Reference.model_validate(data)

        error_msg = str(exc_info.value)
        assert (
            "Extra inputs are not permitted" in error_msg
            or "extra_forbidden" in error_msg
        )

    def test_to_root_server_name(self) -> None:
        """Test to_root_server_name factory method."""
        reference = Reference.to_root_server_name("production")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/servers/production"

    def test_to_root_channel_name(self) -> None:
        """Test to_root_channel_name factory method."""
        reference = Reference.to_root_channel_name("userSignup")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/channels/userSignup"

    def test_to_root_operation_name(self) -> None:
        """Test to_root_operation_name factory method."""
        reference = Reference.to_root_operation_name("sendMessage")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/operations/sendMessage"

    def test_to_component_schema_name(self) -> None:
        """Test to_component_schema_name factory method."""
        reference = Reference.to_component_schema_name("Pet")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/components/schemas/Pet"

    def test_to_component_server_name(self) -> None:
        """Test to_component_server_name factory method."""
        reference = Reference.to_component_server_name("production")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/components/servers/production"

    def test_to_component_channel_name(self) -> None:
        """Test to_component_channel_name factory method."""
        reference = Reference.to_component_channel_name("userSignup")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/components/channels/userSignup"

    def test_to_component_operation_name(self) -> None:
        """Test to_component_operation_name factory method."""
        reference = Reference.to_component_operation_name("sendMessage")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/components/operations/sendMessage"

    def test_to_component_message_name(self) -> None:
        """Test to_component_message_name factory method."""
        reference = Reference.to_component_message_name("userSignUp")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/components/messages/userSignUp"

    def test_to_component_security_scheme_name(self) -> None:
        """Test to_component_security_scheme_name factory method."""
        reference = Reference.to_component_security_scheme_name("oauth2")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/components/securitySchemes/oauth2"

    def test_to_component_server_variable_name(self) -> None:
        """Test to_component_server_variable_name factory method."""
        reference = Reference.to_component_server_variable_name("port")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/components/serverVariables/port"

    def test_to_component_parameter_name(self) -> None:
        """Test to_component_parameter_name factory method."""
        reference = Reference.to_component_parameter_name("userId")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/components/parameters/userId"

    def test_to_component_correlation_id_name(self) -> None:
        """Test to_component_correlation_id_name factory method."""
        reference = Reference.to_component_correlation_id_name("defaultCorrelationId")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/components/correlationIds/defaultCorrelationId"

    def test_to_component_reply_name(self) -> None:
        """Test to_component_reply_name factory method."""
        reference = Reference.to_component_reply_name("successReply")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/components/replies/successReply"

    def test_to_component_reply_address_name(self) -> None:
        """Test to_component_reply_address_name factory method."""
        reference = Reference.to_component_reply_address_name("responseAddress")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/components/replyAddresses/responseAddress"

    def test_to_component_external_doc_name(self) -> None:
        """Test to_component_external_doc_name factory method."""
        reference = Reference.to_component_external_doc_name("apiDocs")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/components/externalDocs/apiDocs"

    def test_to_component_tag_name(self) -> None:
        """Test to_component_tag_name factory method."""
        reference = Reference.to_component_tag_name("deprecated")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/components/tags/deprecated"

    def test_to_component_operation_trait_name(self) -> None:
        """Test to_component_operation_trait_name factory method."""
        reference = Reference.to_component_operation_trait_name(
            "authenticatedOperation"
        )
        assert isinstance(reference, Reference)
        assert reference.ref == "#/components/operationTraits/authenticatedOperation"

    def test_to_component_message_trait_name(self) -> None:
        """Test to_component_message_trait_name factory method."""
        reference = Reference.to_component_message_trait_name("envelopedMessage")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/components/messageTraits/envelopedMessage"

    def test_to_component_server_binding_name(self) -> None:
        """Test to_component_server_binding_name factory method."""
        reference = Reference.to_component_server_binding_name("mqttBinding")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/components/serverBindings/mqttBinding"

    def test_to_component_channel_binding_name(self) -> None:
        """Test to_component_channel_binding_name factory method."""
        reference = Reference.to_component_channel_binding_name("kafkaBinding")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/components/channelBindings/kafkaBinding"

    def test_to_component_operation_binding_name(self) -> None:
        """Test to_component_operation_binding_name factory method."""
        reference = Reference.to_component_operation_binding_name("httpBinding")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/components/operationBindings/httpBinding"

    def test_to_component_message_binding_name(self) -> None:
        """Test to_component_message_binding_name factory method."""
        reference = Reference.to_component_message_binding_name("amqpBinding")
        assert isinstance(reference, Reference)
        assert reference.ref == "#/components/messageBindings/amqpBinding"


class TestExternalDocumentation:
    """Tests for ExternalDocumentation model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_external_docs_basic, case_external_docs_full],
    )
    def test_external_documentation_validation(self, yaml_data: str) -> None:
        """Test ExternalDocumentation model validation."""
        data = yaml.safe_load(yaml_data)
        external_docs = ExternalDocumentation.model_validate(data)
        assert external_docs is not None
        assert str(external_docs.url) == "https://example.com/"

    @parametrize_with_cases(
        "external_docs,expected",
        cases=[
            case_external_docs_serialization_basic,
            case_external_docs_serialization_full,
        ],
    )
    def test_external_documentation_serialization(
        self,
        external_docs: ExternalDocumentation,
        expected: dict,
    ) -> None:
        """Test ExternalDocumentation serialization."""
        dumped = external_docs.model_dump()
        assert dumped == expected

    def test_external_documentation_inherit_from_extendable_base_model(self) -> None:
        """Test that ExternalDocumentation inherits from ExtendableBaseModel."""
        # Check inheritance
        assert issubclass(ExternalDocumentation, ExtendableBaseModel)
        assert isinstance(
            ExternalDocumentation(url="https://example.com"), ExtendableBaseModel
        )

    def test_external_documentation_valid_extensions(self) -> None:
        """Test ExternalDocumentation with valid x- extensions."""
        yaml_data = """
        url: https://example.com
        description: Test documentation
        x-custom-extension: "custom value"
        x-vendor-specific: 123
        x-detailed.info: true
        """
        data = yaml.safe_load(yaml_data)
        external_docs = ExternalDocumentation.model_validate(data)

        # Check that extensions are stored
        assert external_docs.model_extra is not None
        assert external_docs.model_extra["x-custom-extension"] == "custom value"
        assert external_docs.model_extra["x-vendor-specific"] == 123
        assert external_docs.model_extra["x-detailed.info"] is True

        # Check serialization includes extensions
        dumped = external_docs.model_dump()
        assert "x-custom-extension" in dumped
        assert "x-vendor-specific" in dumped
        assert "x-detailed.info" in dumped

    def test_external_documentation_invalid_extensions(self) -> None:
        """Test ExternalDocumentation with invalid extensions."""
        yaml_data = """
        url: https://example.com
        invalid-extension: "should fail"
        x-invalid_extension: "underscore not allowed"
        """
        data = yaml.safe_load(yaml_data)

        with pytest.raises(ValidationError) as exc_info:
            ExternalDocumentation.model_validate(data)

        error_msg = str(exc_info.value)
        assert "does not match specification extension pattern" in error_msg


class TestTag:
    """Tests for Tag model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_tag_basic, case_tag_full, case_tag_with_external_docs],
    )
    def test_tag_validation(self, yaml_data: str) -> None:
        """Test Tag model validation."""
        data = yaml.safe_load(yaml_data)
        tag = Tag.model_validate(data)
        assert tag is not None
        assert tag.name in ("user", "e-commerce")

    @parametrize_with_cases(
        "tag,expected",
        cases=[
            case_tag_serialization_basic,
            case_tag_serialization_full,
            case_tag_serialization_with_external_docs,
            case_tag_serialization_with_reference_external_docs,
        ],
    )
    def test_tag_serialization(self, tag: Tag, expected: dict) -> None:
        """Test Tag serialization."""
        dumped = tag.model_dump()
        assert dumped == expected

    def test_tag_with_external_docs_validation(self) -> None:
        """Test Tag with externalDocs validation."""
        yaml_data = """
        name: e-commerce
        description: E-commerce related messages
        externalDocs:
          description: Find more info here
          url: https://example.com
        """
        data = yaml.safe_load(yaml_data)
        tag = Tag.model_validate(data)

        assert tag.name == "e-commerce"
        assert tag.description == "E-commerce related messages"
        assert tag.external_docs is not None
        assert isinstance(tag.external_docs, ExternalDocumentation)
        assert str(tag.external_docs.url) == "https://example.com/"
        assert tag.external_docs.description == "Find more info here"

    def test_tag_with_reference_external_docs_validation(self) -> None:
        """Test Tag with externalDocs as Reference validation."""
        yaml_data = """
        name: user
        externalDocs:
          $ref: '#/components/externalDocs/infoDocs'
        """
        data = yaml.safe_load(yaml_data)
        tag = Tag.model_validate(data)

        assert tag.name == "user"
        assert tag.external_docs is not None
        assert isinstance(tag.external_docs, Reference)
        assert tag.external_docs.ref == "#/components/externalDocs/infoDocs"

    def test_tag_inherit_from_extendable_base_model(self) -> None:
        """Test that Tag inherits from ExtendableBaseModel."""
        # Check inheritance
        assert issubclass(Tag, ExtendableBaseModel)
        assert isinstance(Tag(name="test"), ExtendableBaseModel)

    def test_tag_valid_extensions(self) -> None:
        """Test Tag with valid x- extensions."""
        yaml_data = """
        name: user
        description: User-related messages
        x-workflow-id: "wf-123"
        x-metadata: {"key": "value"}
        x-category: "events"
        """
        data = yaml.safe_load(yaml_data)
        tag = Tag.model_validate(data)

        # Check extensions
        assert tag.model_extra is not None
        assert tag.model_extra["x-workflow-id"] == "wf-123"
        assert tag.model_extra["x-metadata"] == {"key": "value"}
        assert tag.model_extra["x-category"] == "events"

    def test_tag_invalid_extensions(self) -> None:
        """Test Tag with invalid extensions."""
        yaml_data = """
        name: user
        not-x-prefix: "invalid"
        x-invalid@symbol: "invalid char"
        """
        data = yaml.safe_load(yaml_data)

        with pytest.raises(ValidationError) as exc_info:
            Tag.model_validate(data)

        error_msg = str(exc_info.value)
        assert "does not match specification extension pattern" in error_msg
