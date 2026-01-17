"""Channel models for AsyncAPI 3.0 specification."""

__all__ = [
    "Channel",
    "Channels",
    "Parameter",
    "Parameters",
]

import re

from pydantic import Field, model_validator

from asyncapi3.models.base import ExternalDocumentation, Reference, Tags
from asyncapi3.models.base_models import ExtendableBaseModel, PatternedRootModel
from asyncapi3.models.bindings import ChannelBindingsObject
from asyncapi3.models.helpers import is_null
from asyncapi3.models.message import Messages


class Parameter(ExtendableBaseModel):
    """
    Parameter Object.

    Describes a parameter included in a channel address.

    This object MAY be extended with Specification Extensions.
    """

    enum: list[str] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "An enumeration of string values to be used if the substitution options "
            "are from a limited set."
        ),
    )
    default: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "The default value to use for substitution, and to send, if an alternate "
            "value is not supplied."
        ),
    )
    description: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "An optional description for the parameter. CommonMark syntax MAY be used "
            "for rich text representation."
        ),
    )
    examples: list[str] | None = Field(
        default=None,
        exclude_if=is_null,
        description="An array of examples of the parameter value.",
    )
    location: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A runtime expression that specifies the location of the parameter value."
        ),
    )


class Parameters(PatternedRootModel[Parameter | Reference]):
    """
    Parameters Object.

    This model validates that all keys match the AsyncAPI patterned object key pattern
    ^[A-Za-z0-9\\.\\-_]+$, values match Reference or Parameter objects.
    """


class Channel(ExtendableBaseModel):
    """
    Channel Object.

    Describes a shared communication channel.

    This object MAY be extended with Specification Extensions.
    """

    address: str | None = Field(
        default=None,
        description=(
            "An optional string representation of this channel's address. The address "
            "is typically the 'topic name', 'routing key', 'event type', or 'path'. "
            "When null or absent, it MUST be interpreted as unknown. This is useful "
            "when the address is generated dynamically at runtime or can't be known "
            "upfront. It MAY contain Channel Address Expressions. Query parameters "
            "and fragments SHALL NOT be used, instead use bindings to define them."
        ),
    )
    messages: Messages | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A map of the messages that will be sent to this channel by any "
            "application at any time. Every message sent to this channel MUST be "
            "valid against one, and only one, of the message objects defined in this "
            "map."
        ),
    )
    title: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="A human-friendly title for the channel.",
    )
    summary: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="A short summary of the channel.",
    )
    description: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "An optional description of this channel. CommonMark syntax can be used "
            "for rich text representation."
        ),
    )
    # TODO: How to deal with deref recommendation?
    servers: list[Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "An array of $ref pointers to the definition of the servers in which "
            "this channel is available. If the channel is located in the root "
            "Channels Object, it MUST point to a subset of server definitions located "
            "in the root Servers Object, and MUST NOT point to a subset of server "
            "definitions located in the Components Object or anywhere else. "
            "If the channel is located in the Components Object, it MAY point to a "
            "Server Objects in any location. If servers is absent or empty, this "
            "channel MUST be available on all the servers defined in the Servers "
            "Object. Please note the servers property value MUST be an array of "
            "Reference Objects and, therefore, MUST NOT contain an array of "
            "Server Objects. However, it is RECOMMENDED that parsers "
            "(or other software) dereference this property for a better development "
            "experience."
        ),
    )
    parameters: Parameters | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A map of the parameters included in the channel address. It MUST be "
            "present only when the address contains Channel Address Expressions."
        ),
    )
    tags: Tags | None = Field(
        default=None,
        exclude_if=is_null,
        description="A list of tags for logical grouping of channels.",
    )
    external_docs: ExternalDocumentation | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="externalDocs",
        description="Additional external documentation for this channel.",
    )
    bindings: ChannelBindingsObject | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A map where the keys describe the name of the protocol and the values "
            "describe protocol-specific definitions for the channel."
        ),
    )

    @model_validator(mode="after")
    def validate_parameters(self) -> "Channel":
        """
        Validate that parameters are present only when address contains
        Channel Address Expressions.

        Channel Address Expressions are expressions enclosed in curly braces
        like {userId}.
        """
        if self.parameters is None:
            return self

        if self.address is None:
            raise ValueError(
                "parameters must not be provided when address is null or absent"
            )

        # Check if address contains channel address expressions (curly braces)
        expression_pattern = re.compile(r"\{[^}]+\}")
        if not expression_pattern.search(self.address):
            raise ValueError(
                "parameters must not be provided when address does not contain "
                "Channel Address Expressions"
            )

        return self


class Channels(PatternedRootModel[Channel | Reference]):
    """
    Channels Object.

    This model validates that all keys match the AsyncAPI patterned object key pattern
    ^[A-Za-z0-9\\.\\-_]+$, values match Reference or Channel objects.
    """
