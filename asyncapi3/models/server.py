"""Server models for AsyncAPI 3.0 specification."""

__all__ = [
    "Server",
    "ServerVariable",
    "Servers",
]

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from asyncapi3.models.base import ExternalDocumentation, Reference, Tags
from asyncapi3.models.bindings import ServerBindingsObject
from asyncapi3.models.helpers import is_null
from asyncapi3.models.security import SecurityScheme


class ServerVariable(BaseModel):
    """
    Server Variable Object.

    An object representing a Server Variable for server URL template substitution.

    This object MAY be extended with Specification Extensions.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
    )

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
            "An optional description for the server variable. CommonMark syntax MAY "
            "be used for rich text representation."
        ),
    )
    # TODO: Find a spec with examples
    examples: list[Any] | None = Field(
        default=None,
        exclude_if=is_null,
        description="An array of examples of the server variable.",
    )


class Server(BaseModel):
    """
    Server Object.

    An object representing a message broker, a server or any other kind of computer
    program capable of sending and/or receiving data. This object is used to capture
    details such as URIs, protocols and security configuration. Variable substitution
    can be used so that some details, for example usernames and passwords, can be
    injected by code generation tools.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
    )

    # TODO: Supports Server Variables?!
    host: str = Field(
        description=(
            "REQUIRED. The server host name. It MAY include the port. This field "
            "supports Server Variables. Variable substitutions will be made when a "
            "variable is named in {braces}."
        ),
    )
    protocol: str = Field(
        description="REQUIRED. The protocol this server supports for connection.",
    )
    protocol_version: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="protocolVersion",
        description=(
            "The version of the protocol used for connection. For instance: "
            "AMQP 0.9.1, HTTP 2.0, Kafka 1.0.0, etc."
        ),
    )
    # TODO: Supports Server Variables?!
    pathname: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "The path to a resource in the host. This field supports Server Variables. "
            "Variable substitutions will be made when a variable is named in {braces}."
        ),
    )
    description: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "An optional string describing the server. CommonMark syntax MAY be used "
            "for rich text representation."
        ),
    )
    title: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="A human-friendly title for the server.",
    )
    summary: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="A short summary of the server.",
    )
    variables: dict[str, ServerVariable | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A map between a variable name and its value. The value is used for "
            "substitution in the server's host and pathname template."
        ),
    )
    security: list[SecurityScheme | Reference] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A declaration of which security schemes can be used with this server. "
            "The list of values includes alternative security scheme objects that "
            "can be used. Only one of the security scheme objects need to be "
            "satisfied to authorize a connection or operation."
        ),
    )
    tags: Tags | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A list of tags for logical grouping and categorization of servers."
        ),
    )
    external_docs: ExternalDocumentation | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="externalDocs",
        description="Additional external documentation for this server.",
    )
    bindings: ServerBindingsObject | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A map where the keys describe the name of the protocol and the values "
            "describe protocol-specific definitions for the server."
        ),
    )


# Servers is a type alias for a dictionary of Server objects
Servers = dict[str, Server | Reference]
