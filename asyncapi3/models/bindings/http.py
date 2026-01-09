"""HTTP bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "HTTPChannelBindings",
    "HTTPMessageBindings",
    "HTTPOperationBindings",
    "HTTPServerBindings",
]

from typing import Literal

from pydantic import Field

from asyncapi3.models.base import Reference
from asyncapi3.models.base_models import NonExtendableBaseModel
from asyncapi3.models.helpers import is_null
from asyncapi3.models.schema import Schema


class HTTPServerBindings(NonExtendableBaseModel):
    """
    HTTP Server Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class HTTPChannelBindings(NonExtendableBaseModel):
    """
    HTTP Channel Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class HTTPOperationBindings(NonExtendableBaseModel):
    """
    HTTP Operation Binding Object.

    This object contains information about the operation representation in HTTP.

    This object MUST contain only the properties defined below.
    """

    method: Literal[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "HEAD",
        "OPTIONS",
        "CONNECT",
        "TRACE",
    ] = Field(
        description=(
            "The HTTP method for the request. Its value MUST be one of GET, POST, PUT, "
            "PATCH, DELETE, HEAD, OPTIONS, CONNECT, and TRACE."
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
    binding_version: str = Field(
        default="0.3.0",
        alias="bindingVersion",
        description="The version of this binding. If omitted, 'latest' MUST be assumed",
    )


class HTTPMessageBindings(NonExtendableBaseModel):
    """
    HTTP Message Binding Object.

    This object contains information about the message representation in HTTP.

    This object MUST contain only the properties defined below.
    """

    headers: Schema | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A Schema object containing the definitions for HTTP-specific headers. "
            "This schema MUST be of type object and have a properties key."
        ),
    )
    status_code: int | None = Field(
        default=None,
        exclude_if=is_null,
        alias="statusCode",
        description=(
            "The HTTP response status code according to RFC 9110. statusCode is only "
            "relevant for messages referenced by the Operation Reply Object, as it "
            "defines the status code for the response. In all other cases, this value "
            "can be safely ignored."
        ),
    )
    binding_version: str = Field(
        default="0.3.0",
        alias="bindingVersion",
        description="The version of this binding. If omitted, 'latest' MUST be assumed",
    )
