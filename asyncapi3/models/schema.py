"""Schema models for AsyncAPI 3.0 specification."""

__all__ = [
    "MultiFormatSchema",
    "Schema",
]
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from asyncapi3.models.base import ExternalDocumentation, Reference
from asyncapi3.models.helpers import is_null


# TODO: Not full at this point. Should go to dict instead?
# TODO: MAY be represented by the boolean value true
class Schema(BaseModel):
    """
    Schema Object.

    The Schema Object allows the definition of input and output data types.
    These types can be objects, but also primitives and arrays. This object is a
    superset of the JSON Schema Specification Draft 07. The empty schema (which allows
    any instance to validate) MAY be represented by the boolean value true and a schema
    which allows no instance to validate MAY be represented by the boolean value false.

    Further information about the properties can be found in JSON Schema Core and JSON
    Schema Validation. Unless stated otherwise, the property definitions follow the
    JSON Schema specification as referenced here. For other formats (e.g., Avro, RAML,
    etc) see Multi Format Schema Object.

    The AsyncAPI Schema Object is a JSON Schema vocabulary which extends JSON Schema
    Core and Validation vocabularies. As such, any keyword available for those
    vocabularies is by definition available in AsyncAPI, and will work the exact same
    way, including but not limited to: title, type, required, multipleOf, maximum,
    exclusiveMaximum, minimum, exclusiveMinimum, maxLength, minLength, pattern,
    maxItems, minItems, uniqueItems, maxProperties, minProperties, enum, const,
    examples, if/then/else, readOnly, writeOnly, properties, patternProperties,
    additionalProperties, additionalItems, items, propertyNames, contains, allOf,
    oneOf, anyOf, not.

    The following properties are taken from the JSON Schema definition but their
    definitions were adjusted to the AsyncAPI Specification:

    - description - CommonMark syntax can be used for rich text representation.
    - format - See Data Type Formats for further details. While relying on JSON
      Schema's defined formats, the AsyncAPI Specification offers a few additional
      predefined formats.
    - default - Use it to specify that property has a predefined value if no other
      value is present. Unlike JSON Schema, the value MUST conform to the defined type
      for the Schema Object defined at the same level. For example, of type is string,
      then default can be "foo" but cannot be 1.

    Alternatively, any time a Schema Object can be used, a Reference Object can be
    used in its place. This allows referencing definitions in place of defining them
    inline. It is appropriate to clarify that the $ref keyword MUST follow the behavior
    described by Reference Object instead of the one in JSON Schema definition.

    In addition to the JSON Schema fields, the following AsyncAPI vocabulary fields
    MAY be used for further schema documentation:

    This object MAY be extended with Specification Extensions.
    """

    # JSON Schema fields - these are dynamic and can be any JSON Schema properties
    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    discriminator: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Adds support for polymorphism. The discriminator is the schema property "
            "name that is used to differentiate between other schema that inherit this "
            "schema. The property name used MUST be defined at this schema and it MUST "
            "be in the required property list. When used, the value MUST be the name "
            "of this schema or any schema that inherits it. See Composition and "
            "Inheritance for more details."
        ),
    )
    external_docs: ExternalDocumentation | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="externalDocs",
        description=("Additional external documentation for this schema."),
    )
    deprecated: bool | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Specifies that a schema is deprecated and SHOULD be transitioned out of "
            "usage. Default value is false."
        ),
    )


class MultiFormatSchema(BaseModel):
    """
    Multi Format Schema Object.

    The Multi Format Schema Object represents a schema definition. It differs from the
    Schema Object in that it supports multiple schema formats or languages (e.g., JSON
    Schema, Avro, etc.).

    This object MAY be extended with Specification Extensions.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    schema_format: str = Field(
        alias="schemaFormat",
        default="application/vnd.aai.asyncapi;version=3.0.0",
        description=(
            "REQUIRED. A string containing the name of the schema format that is "
            "used to define the information. If schemaFormat is missing, it MUST "
            "default to application/vnd.aai.asyncapi+json;version={{asyncapi}} where "
            "{{asyncapi}} matches the AsyncAPI Version String. In such a case, this "
            "would make the Multi Format Schema Object equivalent to the Schema "
            "Object. When using Reference Object within the schema, the schemaFormat "
            "of the resource being referenced MUST match the schemaFormat of the "
            "schema that contains the initial reference. For example, if you "
            "reference Avro schema, then schemaFormat of referencing resource and "
            "the resource being reference MUST match. Check out the supported "
            "schema formats table for more information. Custom values are allowed "
            "but their implementation is OPTIONAL. A custom value MUST NOT refer "
            "to one of the schema formats listed in the table. When using Reference "
            "Objects within the schema, the schemaFormat of the referenced resource "
            "MUST match the schemaFormat of the schema containing the reference."
        ),
    )
    # TODO: So either Schema, dict or string?
    schema: Any = Field(
        description=(
            "REQUIRED. Definition of the message payload. It can be of any type but "
            "defaults to Schema Object. It MUST match the schema format defined in "
            "schemaFormat, including the encoding type. E.g., Avro should be inlined "
            "as either a YAML or JSON object instead of as a string to be parsed as "
            "YAML or JSON. Non-JSON-based schemas (e.g., Protobuf or XSD) MUST be "
            "inlined as a string."
        ),
    )
