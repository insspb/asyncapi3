"""WebSockets bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "WebSocketsChannelBindings",
    "WebSocketsMessageBindings",
    "WebSocketsOperationBindings",
    "WebSocketsServerBindings",
]

from typing import Literal

from pydantic import Field

from asyncapi3.models.base import Reference
from asyncapi3.models.base_models import NonExtendableBaseModel
from asyncapi3.models.helpers import is_null
from asyncapi3.models.schema import Schema


class WebSocketsServerBindings(NonExtendableBaseModel):
    """
    WebSockets Server Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class WebSocketsChannelBindings(NonExtendableBaseModel):
    """
    WebSockets Channel Binding Object.

    When using WebSockets, the channel represents the connection. Unlike other protocols
    that support multiple virtual channels (topics, routing keys, etc.) per connection,
    WebSockets doesn't support virtual channels or, put it another way, there's only
    one channel and its characteristics are strongly related to the protocol used for
    the handshake, i.e., HTTP.

    This object MUST contain only the properties defined below.
    """

    method: Literal["GET", "POST"] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "The HTTP method to use when establishing the connection. Its value "
            "MUST be either GET or POST."
        ),
    )
    query: Schema | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A Schema object containing the definitions for each query parameter. This "
            "schema MUST be of type object and have a properties key."
        ),
    )
    headers: Schema | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A Schema object containing the definitions of the HTTP headers to use "
            "when establishing the connection. This schema MUST be of type object and "
            "have a properties key."
        ),
    )
    binding_version: str = Field(
        default="0.1.0",
        alias="bindingVersion",
        description="The version of this binding. If omitted, 'latest' MUST be assumed",
    )


class WebSocketsOperationBindings(NonExtendableBaseModel):
    """
    WebSockets Operation Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class WebSocketsMessageBindings(NonExtendableBaseModel):
    """
    WebSockets Message Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """
