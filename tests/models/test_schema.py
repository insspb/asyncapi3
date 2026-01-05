"""Tests for schema models."""

from typing import Any

import yaml

from pydantic import AnyUrl
from pytest_cases import parametrize_with_cases

from asyncapi3.models.base import ExternalDocumentation, Reference
from asyncapi3.models.schema import MultiFormatSchema, Schema


# Schema Validation Test Cases
def case_schema_basic() -> str:
    """Schema with type only."""
    return """
    type: object
    """


def case_schema_full() -> str:
    """Schema with multiple fields."""
    return """
    type: object
    properties:
      displayName:
        type: string
        description: Name of the user
      email:
        type: string
        format: email
        description: Email of the user
    required:
      - displayName
      - email
    discriminator: userType
    deprecated: false
    externalDocs:
      description: Find more info here
      url: https://example.com
    """


# Schema Serialization Test Cases
def case_schema_serialization_basic() -> tuple[Schema, dict]:
    """Schema serialization with type only."""
    schema = Schema(type="object")
    expected: dict[str, Any] = {"type": "object"}
    return schema, expected


def case_schema_serialization_with_discriminator() -> tuple[Schema, dict]:
    """Schema serialization with discriminator."""
    schema = Schema(
        type="object",
        discriminator="userType",
        properties={"name": Schema(type="string")},
    )
    expected: dict[str, Any] = {
        "type": "object",
        "discriminator": "userType",
        "properties": {
            "name": {
                "type": "string",
            },
        },
    }
    return schema, expected


def case_schema_serialization_with_external_docs() -> tuple[Schema, dict]:
    """Schema serialization with externalDocs."""
    schema = Schema(
        type="object",
        external_docs=ExternalDocumentation(
            url="https://example.com",
            description="Find more info here",
        ),
    )
    expected: dict[str, Any] = {
        "type": "object",
        "externalDocs": {
            "url": AnyUrl("https://example.com/"),
            "description": "Find more info here",
        },
    }
    return schema, expected


def case_schema_serialization_with_reference_external_docs() -> tuple[Schema, dict]:
    """Schema serialization with externalDocs as Reference."""
    schema = Schema(
        type="object",
        external_docs=Reference(ref="#/components/externalDocs/infoDocs"),
    )
    expected: dict[str, Any] = {
        "type": "object",
        "externalDocs": {
            "$ref": "#/components/externalDocs/infoDocs",
        },
    }
    return schema, expected


# MultiFormatSchema Validation Test Cases
def case_multi_format_schema_basic() -> str:
    """MultiFormatSchema with default schemaFormat."""
    return """
    schema:
      type: object
      properties:
        name:
          type: string
    """


def case_multi_format_schema_avro() -> str:
    """MultiFormatSchema with Avro format."""
    return """
    schemaFormat: 'application/vnd.apache.avro+yaml;version=1.9.0'
    schema:
      $ref: './user-create.avsc'
    """


# MultiFormatSchema Serialization Test Cases
def case_multi_format_schema_serialization_default() -> tuple[MultiFormatSchema, dict]:
    """MultiFormatSchema serialization with default schemaFormat."""
    multi_schema = MultiFormatSchema(
        schema=Schema(
            type="object",
            properties={"name": Schema(type="string")},
        ),
    )
    expected: dict[str, Any] = {
        "schemaFormat": "application/vnd.aai.asyncapi;version=3.0.0",
        "schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                },
            },
        },
    }
    return multi_schema, expected


def case_multi_format_schema_serialization_avro() -> tuple[MultiFormatSchema, dict]:
    """MultiFormatSchema serialization with Avro format."""
    multi_schema = MultiFormatSchema(
        schema_format="application/vnd.apache.avro+yaml;version=1.9.0",
        schema=Reference(ref="./user-create.avsc"),
    )
    expected: dict[str, Any] = {
        "schemaFormat": "application/vnd.apache.avro+yaml;version=1.9.0",
        "schema": {
            "$ref": "./user-create.avsc",
        },
    }
    return multi_schema, expected


class TestSchema:
    """Tests for Schema model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_schema_basic, case_schema_full],
    )
    def test_schema_validation(self, yaml_data: str) -> None:
        """Test Schema model validation."""
        data = yaml.safe_load(yaml_data)
        schema = Schema.model_validate(data)
        assert schema is not None
        if "type" in data:
            assert schema.type == data["type"]

    @parametrize_with_cases(
        "schema,expected",
        cases=[
            case_schema_serialization_basic,
            case_schema_serialization_with_discriminator,
            case_schema_serialization_with_external_docs,
            case_schema_serialization_with_reference_external_docs,
        ],
    )
    def test_schema_serialization(self, schema: Schema, expected: dict) -> None:
        """Test Schema serialization."""
        dumped = schema.model_dump()
        assert dumped == expected

    def test_schema_with_discriminator_validation(self) -> None:
        """Test Schema with discriminator validation."""
        yaml_data = """
        type: object
        discriminator: userType
        properties:
          name:
            type: string
        """
        data = yaml.safe_load(yaml_data)
        schema = Schema.model_validate(data)

        assert schema.discriminator == "userType"

    def test_schema_with_external_docs_validation(self) -> None:
        """Test Schema with externalDocs validation."""
        yaml_data = """
        type: object
        externalDocs:
          description: Find more info here
          url: https://example.com
        """
        data = yaml.safe_load(yaml_data)
        schema = Schema.model_validate(data)

        assert schema.external_docs is not None
        assert str(schema.external_docs.url) == "https://example.com/"

    def test_schema_with_reference_external_docs_validation(self) -> None:
        """Test Schema with externalDocs as Reference validation."""
        yaml_data = """
        type: object
        externalDocs:
          $ref: '#/components/externalDocs/infoDocs'
        """
        data = yaml.safe_load(yaml_data)
        schema = Schema.model_validate(data)

        assert schema.external_docs is not None
        assert isinstance(schema.external_docs, Reference)
        assert schema.external_docs.ref == "#/components/externalDocs/infoDocs"


class TestMultiFormatSchema:
    """Tests for MultiFormatSchema model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_multi_format_schema_basic, case_multi_format_schema_avro],
    )
    def test_multi_format_schema_validation(self, yaml_data: str) -> None:
        """Test MultiFormatSchema model validation."""
        data = yaml.safe_load(yaml_data)
        multi_schema = MultiFormatSchema.model_validate(data)
        assert multi_schema is not None
        assert multi_schema.schema is not None

    @parametrize_with_cases(
        "multi_schema,expected",
        cases=[
            case_multi_format_schema_serialization_default,
            case_multi_format_schema_serialization_avro,
        ],
    )
    def test_multi_format_schema_serialization(
        self,
        multi_schema: MultiFormatSchema,
        expected: dict,
    ) -> None:
        """Test MultiFormatSchema serialization."""
        dumped = multi_schema.model_dump()
        assert dumped == expected

    def test_multi_format_schema_default_format_validation(self) -> None:
        """Test MultiFormatSchema with default schemaFormat validation."""
        yaml_data = """
        schema:
          type: object
          properties:
            name:
              type: string
        """
        data = yaml.safe_load(yaml_data)
        multi_schema = MultiFormatSchema.model_validate(data)

        assert (
            multi_schema.schema_format == "application/vnd.aai.asyncapi;version=3.0.0"
        )
