"""Base models for AsyncAPI 3.0 specification."""

__all__ = ["ExternalDocumentation", "Reference", "Tag", "Tags"]

from pydantic import AnyUrl, Field

from asyncapi3.models.base_models import ExtendableBaseModel, NonExtendableBaseModel
from asyncapi3.models.helpers import is_null


class Reference(NonExtendableBaseModel):
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

    ref: str = Field(
        alias="$ref",
        description="The reference string.",
    )

    # Reference factory methods - single source of truth for AsyncAPI 3.0 paths
    # All reference creation should go through these methods for consistency

    @classmethod
    def to_root_server_name(cls, server_name: str) -> "Reference":
        return cls(ref=f"#/servers/{server_name}")

    @classmethod
    def to_root_channel_name(cls, channel_name: str) -> "Reference":
        return cls(ref=f"#/channels/{channel_name}")

    @classmethod
    def to_root_operation_name(cls, operation_name: str) -> "Reference":
        return cls(ref=f"#/operations/{operation_name}")

    @classmethod
    def to_component_schema_name(cls, schema_name: str) -> "Reference":
        return cls(ref=f"#/components/schemas/{schema_name}")

    @classmethod
    def to_component_server_name(cls, server_name: str) -> "Reference":
        return cls(ref=f"#/components/servers/{server_name}")

    @classmethod
    def to_component_channel_name(cls, channel_name: str) -> "Reference":
        return cls(ref=f"#/components/channels/{channel_name}")

    @classmethod
    def to_component_operation_name(cls, operation_name: str) -> "Reference":
        return cls(ref=f"#/components/operations/{operation_name}")

    @classmethod
    def to_component_message_name(cls, message_name: str) -> "Reference":
        return cls(ref=f"#/components/messages/{message_name}")

    @classmethod
    def to_component_security_scheme_name(
        cls, security_scheme_name: str
    ) -> "Reference":
        return cls(ref=f"#/components/securitySchemes/{security_scheme_name}")

    @classmethod
    def to_component_server_variable_name(
        cls, server_variable_name: str
    ) -> "Reference":
        return cls(ref=f"#/components/serverVariables/{server_variable_name}")

    @classmethod
    def to_component_parameter_name(cls, parameter_name: str) -> "Reference":
        return cls(ref=f"#/components/parameters/{parameter_name}")

    @classmethod
    def to_component_correlation_id_name(cls, correlation_id_name: str) -> "Reference":
        return cls(ref=f"#/components/correlationIds/{correlation_id_name}")

    @classmethod
    def to_component_reply_name(cls, reply_name: str) -> "Reference":
        return cls(ref=f"#/components/replies/{reply_name}")

    @classmethod
    def to_component_reply_address_name(cls, reply_address_name: str) -> "Reference":
        return cls(ref=f"#/components/replyAddresses/{reply_address_name}")

    @classmethod
    def to_component_external_doc_name(cls, external_doc_name: str) -> "Reference":
        return cls(ref=f"#/components/externalDocs/{external_doc_name}")

    @classmethod
    def to_component_tag_name(cls, tag_name: str) -> "Reference":
        return cls(ref=f"#/components/tags/{tag_name}")

    @classmethod
    def to_component_operation_trait_name(
        cls, operation_trait_name: str
    ) -> "Reference":
        return cls(ref=f"#/components/operationTraits/{operation_trait_name}")

    @classmethod
    def to_component_message_trait_name(cls, message_trait_name: str) -> "Reference":
        return cls(ref=f"#/components/messageTraits/{message_trait_name}")

    @classmethod
    def to_component_server_binding_name(cls, server_binding_name: str) -> "Reference":
        return cls(ref=f"#/components/serverBindings/{server_binding_name}")

    @classmethod
    def to_component_channel_binding_name(
        cls, channel_binding_name: str
    ) -> "Reference":
        return cls(ref=f"#/components/channelBindings/{channel_binding_name}")

    @classmethod
    def to_component_operation_binding_name(
        cls,
        operation_binding_name: str,
    ) -> "Reference":
        return cls(ref=f"#/components/operationBindings/{operation_binding_name}")

    @classmethod
    def to_component_message_binding_name(
        cls, message_binding_name: str
    ) -> "Reference":
        return cls(ref=f"#/components/messageBindings/{message_binding_name}")


class ExternalDocumentation(ExtendableBaseModel):
    """
    External Documentation Object.

    Allows referencing an external resource for extended documentation.
    """

    url: AnyUrl = Field(
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


class Tag(ExtendableBaseModel):
    """
    Tag Object.

    Allows adding meta data to a single tag.
    """

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
