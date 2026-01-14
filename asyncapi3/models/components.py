"""Components model for AsyncAPI 3.0 specification."""

__all__ = [
    "ChannelBindings",
    "Components",
    "CorrelationIDs",
    "ExternalDocs",
    "MessageBindings",
    "Messages",
    "OperationBindings",
    "OperationTraits",
    "Parameters",
    "Replies",
    "ReplyAddresses",
    "Schemas",
    "SecuritySchemes",
    "ServerBindings",
    "ServerVariables",
    "Tags",
]


from pydantic import Field

from asyncapi3.models.base import ExternalDocumentation, Reference, Tag
from asyncapi3.models.base_models import ExtendableBaseModel, PatternedRootModel
from asyncapi3.models.bindings import (
    ChannelBindingsObject,
    MessageBindingsObject,
    OperationBindingsObject,
    ServerBindingsObject,
)
from asyncapi3.models.channel import Channels, Parameter
from asyncapi3.models.helpers import is_null
from asyncapi3.models.message import Message, MessageTrait
from asyncapi3.models.operation import (
    OperationReply,
    OperationReplyAddress,
    Operations,
    OperationTrait,
)
from asyncapi3.models.schema import MultiFormatSchema, Schema
from asyncapi3.models.security import CorrelationID, SecurityScheme
from asyncapi3.models.server import Servers, ServerVariable


class Schemas(PatternedRootModel[MultiFormatSchema | Schema | Reference]):
    """
    Schemas Object.

    This model validates that all keys match the AsyncAPI patterned object key pattern
    ^[A-Za-z0-9\\.\\-_]+$, values match Reference or Schema objects.
    """


class Messages(PatternedRootModel[Message | Reference]):
    """
    Messages Object.

    This model validates that all keys match the AsyncAPI patterned object key pattern
    ^[A-Za-z0-9\\.\\-_]+$, values match Reference or Message objects.
    """


class SecuritySchemes(PatternedRootModel[SecurityScheme | Reference]):
    """
    SecuritySchemes Object.

    This model validates that all keys match the AsyncAPI patterned object key pattern
    ^[A-Za-z0-9\\.\\-_]+$, values match Reference or SecurityScheme objects.
    """


class ServerVariables(PatternedRootModel[ServerVariable | Reference]):
    """
    ServerVariable Object.

    This model validates that all keys match the AsyncAPI patterned object key pattern
    ^[A-Za-z0-9\\.\\-_]+$, values match Reference or ServerVariable objects.
    """


class Parameters(PatternedRootModel[Parameter | Reference]):
    """
    Parameter Object.

    This model validates that all keys match the AsyncAPI patterned object key pattern
    ^[A-Za-z0-9\\.\\-_]+$, values match Reference or Parameter objects.
    """


class CorrelationIDs(PatternedRootModel[CorrelationID | Reference]):
    """
    CorrelationID Object.

    This model validates that all keys match the AsyncAPI patterned object key pattern
    ^[A-Za-z0-9\\.\\-_]+$, values match Reference or CorrelationID objects.
    """


class Replies(PatternedRootModel[OperationReply | Reference]):
    """
    OperationReply Object.

    This model validates that all keys match the AsyncAPI patterned object key pattern
    ^[A-Za-z0-9\\.\\-_]+$, values match Reference or OperationReply objects.
    """


class ReplyAddresses(PatternedRootModel[OperationReplyAddress | Reference]):
    """
    OperationReplyAddress Object.

    This model validates that all keys match the AsyncAPI patterned object key pattern
    ^[A-Za-z0-9\\.\\-_]+$, values match Reference or OperationReplyAddress objects.
    """


class ExternalDocs(PatternedRootModel[ExternalDocumentation | Reference]):
    """
    ExternalDocumentation Object.

    This model validates that all keys match the AsyncAPI patterned object key pattern
    ^[A-Za-z0-9\\.\\-_]+$, values match Reference or ExternalDocumentation objects.
    """


class Tags(PatternedRootModel[Tag | Reference]):
    """
    Tag Object.

    This model validates that all keys match the AsyncAPI patterned object key pattern
    ^[A-Za-z0-9\\.\\-_]+$, values match Reference or Tag objects.
    """


class OperationTraits(PatternedRootModel[OperationTrait | Reference]):
    """
    OperationTrait Object.

    This model validates that all keys match the AsyncAPI patterned object key pattern
    ^[A-Za-z0-9\\.\\-_]+$, values match Reference or OperationTrait objects.
    """


class MessageTraits(PatternedRootModel[MessageTrait | Reference]):
    """
    MessageTrait Object.

    This model validates that all keys match the AsyncAPI patterned object key pattern
    ^[A-Za-z0-9\\.\\-_]+$, values match Reference or MessageTrait objects.
    """


class ServerBindings(PatternedRootModel[ServerBindingsObject | Reference]):
    """
    ServerBindingsObject Object.

    This model validates that all keys match the AsyncAPI patterned object key pattern
    ^[A-Za-z0-9\\.\\-_]+$, values match Reference or ServerBindingsObject objects.
    """


class ChannelBindings(PatternedRootModel[ChannelBindingsObject | Reference]):
    """
    ChannelBindingsObject Object.

    This model validates that all keys match the AsyncAPI patterned object key pattern
    ^[A-Za-z0-9\\.\\-_]+$, values match Reference or ChannelBindingsObject objects.
    """


class OperationBindings(PatternedRootModel[OperationBindingsObject | Reference]):
    """
    OperationBindingsObject Object.

    This model validates that all keys match the AsyncAPI patterned object key pattern
    ^[A-Za-z0-9\\.\\-_]+$, values match Reference or OperationBindingsObject objects.
    """


class MessageBindings(PatternedRootModel[MessageBindingsObject | Reference]):
    """
    MessageBindingsObject Object.

    This model validates that all keys match the AsyncAPI patterned object key pattern
    ^[A-Za-z0-9\\.\\-_]+$, values match Reference or MessageBindingsObject objects.
    """


class Components(ExtendableBaseModel):
    """
    Components Object.

    Holds a set of reusable objects for different aspects of the AsyncAPI specification.
    All objects defined within the components object will have no effect on the API
    unless they are explicitly referenced from properties outside the components object.

    This object MAY be extended with Specification Extensions.
    """

    schemas: Schemas | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "An object to hold reusable Schema Object. If this is a Schema Object, "
            "then the schemaFormat will be assumed to be "
            "'application/vnd.aai.asyncapi+json;version=asyncapi' where the version "
            "is equal to the AsyncAPI Version String."
        ),
    )
    servers: Servers | None = Field(
        default=None,
        exclude_if=is_null,
        description="An object to hold reusable Server Objects.",
    )
    channels: Channels | None = Field(
        default=None,
        exclude_if=is_null,
        description="An object to hold reusable Channel Objects.",
    )
    operations: Operations | None = Field(
        default=None,
        exclude_if=is_null,
        description="An object to hold reusable Operation Objects.",
    )
    messages: Messages | None = Field(
        default=None,
        exclude_if=is_null,
        description="An object to hold reusable Message Objects.",
    )
    security_schemes: SecuritySchemes | None = Field(
        default=None,
        exclude_if=is_null,
        alias="securitySchemes",
        description="An object to hold reusable Security Scheme Objects.",
    )
    server_variables: ServerVariables | None = Field(
        default=None,
        exclude_if=is_null,
        alias="serverVariables",
        description="An object to hold reusable Server Variable Objects.",
    )
    parameters: Parameters | None = Field(
        default=None,
        exclude_if=is_null,
        description="An object to hold reusable Parameter Objects.",
    )
    correlation_ids: CorrelationIDs | None = Field(
        default=None,
        exclude_if=is_null,
        alias="correlationIds",
        description="An object to hold reusable Correlation ID Objects.",
    )
    replies: Replies | None = Field(
        default=None,
        exclude_if=is_null,
        description="An object to hold reusable Operation Reply Objects.",
    )
    reply_addresses: ReplyAddresses | None = Field(
        default=None,
        exclude_if=is_null,
        alias="replyAddresses",
        description="An object to hold reusable Operation Reply Address Objects.",
    )
    external_docs: ExternalDocs | None = Field(
        default=None,
        exclude_if=is_null,
        alias="externalDocs",
        description="An object to hold reusable External Documentation Objects.",
    )
    tags: Tags | None = Field(
        default=None,
        exclude_if=is_null,
        description="An object to hold reusable Tag Objects.",
    )
    operation_traits: OperationTraits | None = Field(
        default=None,
        exclude_if=is_null,
        alias="operationTraits",
        description="An object to hold reusable Operation Trait Objects.",
    )
    message_traits: MessageTraits | None = Field(
        default=None,
        exclude_if=is_null,
        alias="messageTraits",
        description="An object to hold reusable Message Trait Objects.",
    )
    server_bindings: ServerBindings | None = Field(
        default=None,
        exclude_if=is_null,
        alias="serverBindings",
        description="An object to hold reusable Server Bindings Objects.",
    )
    channel_bindings: ChannelBindings | None = Field(
        default=None,
        exclude_if=is_null,
        alias="channelBindings",
        description="An object to hold reusable Channel Bindings Objects.",
    )
    operation_bindings: OperationBindings | None = Field(
        default=None,
        exclude_if=is_null,
        alias="operationBindings",
        description="An object to hold reusable Operation Bindings Objects.",
    )
    message_bindings: MessageBindings | None = Field(
        default=None,
        exclude_if=is_null,
        alias="messageBindings",
        description="An object to hold reusable Message Bindings Objects.",
    )
