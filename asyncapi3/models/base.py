"""Base models for AsyncAPI 3.0 specification."""

__all__ = ["ExternalDocumentation", "Reference", "Tag", "Tags"]

from pydantic import BaseModel, ConfigDict, Field

from asyncapi3.models.helpers import is_null


class Reference(BaseModel):
    """
    Reference Object.

    A simple object to allow referencing other components in the specification,
    internally and externally.

    The Reference Object is defined by JSON Reference and follows the same structure,
    behavior and rules. A JSON Reference SHALL only be used to refer to a schema that
    is formatted in either JSON or YAML. In the case of a YAML-formatted Schema, the
    JSON Reference SHALL be applied to the JSON representation of that schema. The
    JSON representation SHALL be made by applying the conversion described in the Format
    section.

    For this specification, reference resolution is done as defined by the JSON
    Reference specification and not by the JSON Schema specification.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    ref: str = Field(
        alias="$ref",
        description="The reference string.",
    )


class ExternalDocumentation(BaseModel):
    """
    External Documentation Object.

    Allows referencing an external resource for extended documentation.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    url: str = Field(
        description=(
            "The URL for the target documentation. This MUST be in the form of an "
            "absolute URL."
        ),
    )
    description: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A short description of the target documentation. CommonMark syntax can "
            "be used for rich text representation."
        ),
    )


class Tag(BaseModel):
    """
    Tag Object.

    Allows adding meta data to a single tag.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    name: str = Field(
        description="The name of the tag.",
    )
    description: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A short description for the tag. CommonMark syntax can be used for rich "
            "text representation."
        ),
    )
    external_docs: ExternalDocumentation | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="externalDocs",
        description="Additional external documentation for this tag.",
    )


# Tags is a type alias for a list of Tag objects
Tags = list[Tag | Reference]
