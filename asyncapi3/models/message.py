"""Message models for AsyncAPI 3.0 specification."""

__all__ = [
    "Message",
    "MessageExample",
    "MessageTrait",
    "Messages",
]

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from asyncapi3.models.base import ExternalDocumentation, Reference, Tags
from asyncapi3.models.bindings import MessageBindingsObject
from asyncapi3.models.helpers import is_null
from asyncapi3.models.schema import MultiFormatSchema, Schema
from asyncapi3.models.security import CorrelationID


class MessageExample(BaseModel):
    """
    Message Example Object.

    Message Example Object represents an example of a Message Object and MUST contain
    either headers and/or payload fields.

    This object MAY be extended with Specification Extensions.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
    )

    headers: dict[str, Any] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "The value of this field MUST validate against the Message Object's "
            "headers field."
        ),
    )
    payload: Any | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "The value of this field MUST validate against the Message Object's "
            "payload field."
        ),
    )
    name: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="A machine-friendly name.",
    )
    summary: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="A short summary of what the example is about.",
    )


class MessageTrait(BaseModel):
    """
    Message Trait Object.

    Describes a trait that MAY be applied to a Message Object. This object MAY contain
    any property from the Message Object, except payload and traits.

    If you're looking to apply traits to an operation, see the Operation Trait Object.

    This object MAY be extended with Specification Extensions.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
    )

    headers: MultiFormatSchema | Schema | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Schema definition of the application headers. Schema MUST be a map of "
            "key-value pairs. It MUST NOT define the protocol headers. If this is a "
            "Schema Object, then the schemaFormat will be assumed to be "
            "'application/vnd.aai.asyncapi+json;version=asyncapi' where the version "
            "is equal to the AsyncAPI Version String."
        ),
    )
    correlation_id: CorrelationID | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="correlationId",
        description=(
            "Definition of the correlation ID used for message tracing or matching."
        ),
    )
    content_type: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="contentType",
        description=(
            "The content type to use when encoding/decoding a message's payload. "
            "The value MUST be a specific media type (e.g. application/json). "
            "When omitted, the value MUST be the one specified on the "
            "defaultContentType field."
        ),
    )
    name: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="A machine-friendly name for the message.",
    )
    title: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="A human-friendly title for the message.",
    )
    summary: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="A short summary of what the message is about.",
    )
    description: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A verbose explanation of the message. CommonMark syntax can be used for "
            "rich text representation."
        ),
    )
    tags: Tags | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A list of tags for logical grouping and categorization of messages."
        ),
    )
    external_docs: ExternalDocumentation | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="externalDocs",
        description="Additional external documentation for this message.",
    )
    bindings: MessageBindingsObject | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A map where the keys describe the name of the protocol and the values "
            "describe protocol-specific definitions for the message."
        ),
    )
    examples: list[MessageExample] | None = Field(
        default=None,
        exclude_if=is_null,
        description="List of examples.",
    )


class Message(BaseModel):
    """
    Message Object.

    Describes a message received on a given channel and operation.

    This object MAY be extended with Specification Extensions.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
    )

    headers: MultiFormatSchema | Schema | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Schema definition of the application headers. Schema MUST be a map of "
            "key-value pairs. It MUST NOT define the protocol headers. If this is a "
            "Schema Object, then the schemaFormat will be assumed to be "
            "'application/vnd.aai.asyncapi+json;version=asyncapi' where the version "
            "is equal to the AsyncAPI Version String."
        ),
    )
    payload: MultiFormatSchema | Schema | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Definition of the message payload. If this is a Schema Object, then the "
            "schemaFormat will be assumed to be "
            "'application/vnd.aai.asyncapi+json;version=asyncapi' where the version "
            "is equal to the AsyncAPI Version String."
        ),
    )
    correlation_id: CorrelationID | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="correlationId",
        description=(
            "Definition of the correlation ID used for message tracing or matching."
        ),
    )
    content_type: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="contentType",
        description=(
            "The content type to use when encoding/decoding a message's payload. "
            "The value MUST be a specific media type (e.g. application/json). "
            "When omitted, the value MUST be the one specified on the "
            "defaultContentType field."
        ),
    )
    name: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="A machine-friendly name for the message.",
    )
    title: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="A human-friendly title for the message.",
    )
    summary: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="A short summary of what the message is about.",
    )
    description: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A verbose explanation of the message. CommonMark syntax can be used for "
            "rich text representation."
        ),
    )
    tags: Tags | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A list of tags for logical grouping and categorization of messages."
        ),
    )
    external_docs: ExternalDocumentation | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="externalDocs",
        description="Additional external documentation for this message.",
    )
    bindings: MessageBindingsObject | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A map where the keys describe the name of the protocol and the values "
            "describe protocol-specific definitions for the message."
        ),
    )
    examples: list[MessageExample] | None = Field(
        default=None,
        exclude_if=is_null,
        description="List of examples.",
    )
    # TODO: Traits MUST be merged using traits merge mechanism?
    traits: list[MessageTrait | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A list of traits to apply to the message object. Traits MUST be merged "
            "using traits merge mechanism. The resulting object MUST be a valid "
            "Message Object."
        ),
    )


# Messages is a type alias for a dictionary of Message objects
Messages = dict[str, Message | Reference]
