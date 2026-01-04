"""Components model for AsyncAPI 3.0 specification."""

__all__ = ["Components"]

from pydantic import BaseModel, ConfigDict, Field

from asyncapi3.models.base import ExternalDocumentation, Reference, Tag
from asyncapi3.models.bindings import (
    ChannelBindingsObject,
    MessageBindingsObject,
    OperationBindingsObject,
    ServerBindingsObject,
)
from asyncapi3.models.channel import Channel, Parameter
from asyncapi3.models.helpers import is_null
from asyncapi3.models.message import Message, MessageTrait
from asyncapi3.models.operation import (
    Operation,
    OperationReply,
    OperationReplyAddress,
    OperationTrait,
)
from asyncapi3.models.schema import MultiFormatSchema, Schema
from asyncapi3.models.security import CorrelationID, SecurityScheme
from asyncapi3.models.server import Server, ServerVariable


# TODO: Regex dict names validation
class Components(BaseModel):
    """
    Components Object.

    Holds a set of reusable objects for different aspects of the AsyncAPI specification.
    All objects defined within the components object will have no effect on the API
    unless they are explicitly referenced from properties outside the components object.

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

    schemas: dict[str, MultiFormatSchema | Schema | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "An object to hold reusable Schema Object. If this is a Schema Object, "
            "then the schemaFormat will be assumed to be "
            "'application/vnd.aai.asyncapi+json;version=asyncapi' where the version "
            "is equal to the AsyncAPI Version String."
        ),
    )
    servers: dict[str, Server | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        description="An object to hold reusable Server Objects.",
    )
    channels: dict[str, Channel | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        description="An object to hold reusable Channel Objects.",
    )
    operations: dict[str, Operation | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        description="An object to hold reusable Operation Objects.",
    )
    messages: dict[str, Message | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        description="An object to hold reusable Message Objects.",
    )
    security_schemes: dict[str, SecurityScheme | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="securitySchemes",
        description="An object to hold reusable Security Scheme Objects.",
    )
    server_variables: dict[str, ServerVariable | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="serverVariables",
        description="An object to hold reusable Server Variable Objects.",
    )
    parameters: dict[str, Parameter | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        description="An object to hold reusable Parameter Objects.",
    )
    correlation_ids: dict[str, CorrelationID | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="correlationIds",
        description="An object to hold reusable Correlation ID Objects.",
    )
    replies: dict[str, OperationReply | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        description="An object to hold reusable Operation Reply Objects.",
    )
    reply_addresses: dict[str, OperationReplyAddress | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="replyAddresses",
        description="An object to hold reusable Operation Reply Address Objects.",
    )
    external_docs: dict[str, ExternalDocumentation | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="externalDocs",
        description="An object to hold reusable External Documentation Objects.",
    )
    tags: dict[str, Tag | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        description="An object to hold reusable Tag Objects.",
    )
    operation_traits: dict[str, OperationTrait | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="operationTraits",
        description="An object to hold reusable Operation Trait Objects.",
    )
    message_traits: dict[str, MessageTrait | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="messageTraits",
        description="An object to hold reusable Message Trait Objects.",
    )
    server_bindings: dict[str, ServerBindingsObject | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="serverBindings",
        description="An object to hold reusable Server Bindings Objects.",
    )
    channel_bindings: dict[str, ChannelBindingsObject | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="channelBindings",
        description="An object to hold reusable Channel Bindings Objects.",
    )
    operation_bindings: dict[str, OperationBindingsObject | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="operationBindings",
        description="An object to hold reusable Operation Bindings Objects.",
    )
    message_bindings: dict[str, MessageBindingsObject | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="messageBindings",
        description="An object to hold reusable Message Bindings Objects.",
    )
