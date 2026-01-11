"""Operation models for AsyncAPI 3.0 specification."""

__all__ = [
    "Operation",
    "OperationReply",
    "OperationReplyAddress",
    "OperationTrait",
    "Operations",
]

from typing import Literal

from pydantic import Field

from asyncapi3.models.base import ExternalDocumentation, Reference, Tags
from asyncapi3.models.base_models import ExtendableBaseModel
from asyncapi3.models.bindings import OperationBindingsObject
from asyncapi3.models.helpers import is_null
from asyncapi3.models.security import SecurityScheme


class OperationReplyAddress(ExtendableBaseModel):
    """
    Operation Reply Address Object.

    An object that specifies where an operation has to send the reply.

    For specifying and computing the location of a reply address, a runtime expression
    is used.

    This object MAY be extended with Specification Extensions.
    """

    location: str = Field(
        description=(
            "REQUIRED. A runtime expression that specifies the location of the reply "
            "address."
        ),
    )
    description: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "An optional description of the address. CommonMark syntax can be used "
            "for rich text representation."
        ),
    )


class OperationReply(ExtendableBaseModel):
    """
    Operation Reply Object.

    Describes the reply part that MAY be applied to an Operation Object. If an
    operation implements the request/reply pattern, the reply object represents the
    response message.

    This object MAY be extended with Specification Extensions.
    """

    address: OperationReplyAddress | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Definition of the address that implementations MUST use for the reply."
        ),
    )
    # TODO: How to deal with deref recommendation?
    channel: Reference | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A $ref pointer to the definition of the channel in which this "
            "operation is performed. When address is specified, the address property "
            "of the channel referenced by this property MUST be either null or not "
            "defined. If the operation reply is located inside a root Operation "
            "Object, it MUST point to a channel definition located in the root "
            "Channels Object, and MUST NOT point to a channel definition located in "
            "the Components Object or anywhere else. If the operation reply is "
            "located inside an Operation Object in the Components Object or in the "
            "Replies Object in the Components Object, it MAY point to a Channel "
            "Object in any location. Please note the channel property value MUST be "
            "a Reference Object and, therefore, MUST NOT contain a Channel Object. "
            "However, it is RECOMMENDED that parsers (or other software) dereference "
            "this property for a better development experience."
        ),
    )
    # TODO: How to deal with deref recommendation?
    messages: list[Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A list of $ref pointers pointing to the supported Message Objects that "
            "can be processed by this operation as reply. It MUST contain a subset of "
            "the messages defined in the channel referenced in this operation reply, "
            "and MUST NOT point to a subset of message definitions located in the "
            "Components Object or anywhere else. Every message processed by this "
            "operation MUST be valid against one, and only one, of the message "
            "objects referenced in this list. Please note the messages property "
            "value MUST be a list of Reference Objects and, therefore, MUST NOT "
            "contain Message Objects. However, it is RECOMMENDED that parsers (or "
            "other software) dereference this property for a better development "
            "experience."
        ),
    )


class OperationTrait(ExtendableBaseModel):
    """
    Operation Trait Object.

    Describes a trait that MAY be applied to an Operation Object. This object MAY
    contain any property from the Operation Object, except the action, channel,
    messages and traits ones.

    If you're looking to apply traits to a message, see the Message Trait Object.

    This object MAY be extended with Specification Extensions.
    """

    title: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="A human-friendly title for the operation.",
    )
    summary: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="A short summary of what the operation is about.",
    )
    description: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A verbose explanation of the operation. CommonMark syntax can be used "
            "for rich text representation."
        ),
    )
    security: list[SecurityScheme | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A declaration of which security schemes are associated with this "
            "operation. Only one of the security scheme objects MUST be satisfied to "
            "authorize an operation. In cases where Server Security also applies, "
            "it MUST also be satisfied."
        ),
    )
    tags: Tags | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A list of tags for logical grouping and categorization of operations."
        ),
    )
    external_docs: ExternalDocumentation | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="externalDocs",
        description="Additional external documentation for this operation.",
    )
    bindings: OperationBindingsObject | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A map where the keys describe the name of the protocol and the values "
            "describe protocol-specific definitions for the operation."
        ),
    )


class Operation(ExtendableBaseModel):
    """
    Operation Object.

    Describes a specific operation.

    This object MAY be extended with Specification Extensions.
    """

    action: Literal["send", "receive"] = Field(
        description=(
            "Use send when it's expected that the application will send a message "
            "to the given channel, and receive when the application should expect "
            "receiving messages from the given channel."
        ),
    )
    # TODO: How to deal with deref recommendation?
    channel: Reference = Field(
        description=(
            "REQUIRED. A $ref pointer to the definition of the channel in which this "
            "operation is performed. If the operation is located in the root "
            "Operations Object, it MUST point to a channel definition located in the "
            "root Channels Object, and MUST NOT point to a channel definition located "
            "in the Components Object or anywhere else. If the operation is located "
            "in the Components Object, it MAY point to a Channel Object in any "
            "location. Please note the channel property value MUST be a Reference "
            "Object and, therefore, MUST NOT contain a Channel Object. However, "
            "it is RECOMMENDED that parsers (or other software) dereference this "
            "property for a better development experience."
        ),
    )
    title: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="A human-friendly title for the operation.",
    )
    summary: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="A short summary of what the operation is about.",
    )
    description: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A verbose explanation of the operation. CommonMark syntax can be used "
            "for rich text representation."
        ),
    )
    security: list[SecurityScheme | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A declaration of which security schemes are associated with this "
            "operation. Only one of the security scheme objects MUST be satisfied to "
            "authorize an operation. In cases where Server Security also applies, "
            "it MUST also be satisfied."
        ),
    )
    tags: Tags | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A list of tags for logical grouping and categorization of operations."
        ),
    )
    external_docs: ExternalDocumentation | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="externalDocs",
        description="Additional external documentation for this operation.",
    )
    bindings: OperationBindingsObject | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A map where the keys describe the name of the protocol and the values "
            "describe protocol-specific definitions for the operation."
        ),
    )
    # TODO: Traits MUST be merged using traits merge mechanism?
    traits: list[OperationTrait | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A list of traits to apply to the operation object. Traits MUST be merged "
            "using traits merge mechanism. The resulting object MUST be a valid "
            "Operation Object."
        ),
    )
    # TODO: How to deal with deref recommendation?
    messages: list[Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A list of $ref pointers pointing to the supported Message Objects that "
            "can be processed by this operation. It MUST contain a subset of the "
            "messages defined in the channel referenced in this operation, and "
            "MUST NOT point to a subset of message definitions located in the "
            "Messages Object in the Components Object or anywhere else. Every message "
            "processed by this operation MUST be valid against one, and only one, of "
            "the message objects referenced in this list. Please note the messages "
            "property value MUST be a list of Reference Objects and, therefore, "
            "MUST NOT contain Message Objects. However, it is RECOMMENDED that parsers "
            "(or other software) dereference this property for a better development "
            "experience. Note: excluding this property from the Operation implies "
            "that all messages from the channel will be included. Explicitly set the "
            "messages property to [] if this operation should contain no messages."
        ),
    )
    reply: OperationReply | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        description="The definition of the reply in a request-reply operation.",
    )


# Operations is a type alias for a dictionary of Operation objects
Operations = dict[str, Operation | Reference]
