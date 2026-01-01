"""Security models for AsyncAPI 3.0 specification."""

__all__ = [
    "CorrelationID",
    "OAuthFlow",
    "OAuthFlows",
    "SecurityScheme",
]

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from asyncapi3.models.helpers import is_null


# TODO: Support Runtime expressions
class CorrelationID(BaseModel):
    """
    Correlation ID Object.

    An object that specifies an identifier at design time that can used for message
    tracing and correlation.

    For specifying and computing the location of a Correlation ID, a runtime
    expression is used.

    This object MAY be extended with Specification Extensions.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
    )

    description: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "An optional description of the identifier. CommonMark syntax can be used "
            "for rich text representation."
        ),
    )
    location: str = Field(
        description=(
            "REQUIRED. A runtime expression that specifies the location of the "
            "correlation ID."
        ),
    )


class OAuthFlow(BaseModel):
    """
    OAuth Flow Object.

    Configuration details for a supported OAuth Flow.

    This object MAY be extended with Specification Extensions.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
    )

    # TODO: Make complete validation for spec rules (required for dependency)
    authorization_url: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="authorizationUrl",
        description=(
            "REQUIRED for: oauth2 ('implicit', 'authorizationCode'). The "
            "authorization URL to be used for this flow. This MUST be in the form "
            "of an absolute URL."
        ),
    )
    # TODO: Make complete validation for spec rules (required for dependency)
    token_url: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="tokenUrl",
        description=(
            "REQUIRED for: oauth2 ('password', 'clientCredentials', "
            "'authorizationCode'). The token URL to be used for this flow. This MUST "
            "be in the form of an absolute URL."
        ),
    )
    refresh_url: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="refreshUrl",
        description=(
            "Applied to oauth2 type. The URL to be used for obtaining refresh tokens. "
            "This MUST be in the form of an absolute URL."
        ),
    )
    # TODO: Make complete validation for spec rules (required for dependency)
    available_scopes: dict[str, str] = Field(
        alias="availableScopes",
        description=(
            "REQUIRED for oauth2 type. The available scopes for the OAuth2 security "
            "scheme. A map between the scope name and a short description for it."
        ),
    )


class OAuthFlows(BaseModel):
    """
    OAuth Flows Object.

    Allows configuration of the supported OAuth Flows.

    This object MAY be extended with Specification Extensions.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
    )

    implicit: OAuthFlow | None = Field(
        default=None,
        exclude_if=is_null,
        description="Configuration for the OAuth Implicit flow.",
    )
    password: OAuthFlow | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Configuration for the OAuth Resource Owner Protected Credentials flow."
        ),
    )
    client_credentials: OAuthFlow | None = Field(
        default=None,
        exclude_if=is_null,
        alias="clientCredentials",
        description="Configuration for the OAuth Client Credentials flow.",
    )
    authorization_code: OAuthFlow | None = Field(
        default=None,
        exclude_if=is_null,
        alias="authorizationCode",
        description="Configuration for the OAuth Authorization Code flow.",
    )


class SecurityScheme(BaseModel):
    """
    Security Scheme Object.

    Defines a security scheme that can be used by the operations. Supported schemes
    are:

    - User/Password.
    - API key (either as user or as password).
    - X.509 certificate.
    - End-to-end encryption (either symmetric or asymmetric).
    - HTTP authentication.
    - HTTP API key.
    - OAuth2's common flows (Implicit, Resource Owner Protected Credentials, Client
      Credentials and Authorization Code) as defined in RFC6749.
    - OpenID Connect Discovery.
    - SASL (Simple Authentication and Security Layer) as defined in RFC4422.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
    )

    type_: Literal[
        "apiKey",
        "asymmetricEncryption",
        "gssapi",
        "http",
        "httpApiKey",
        "oauth2",
        "openIdConnect",
        "plain",
        "scramSha256",
        "scramSha512",
        "symmetricEncryption",
        "userPassword",
        "X509",
    ] = Field(
        alias="type",
        description=(
            "REQUIRED for any type. The type of the security scheme. Valid values "
            "are 'userPassword', 'apiKey', 'X509', 'symmetricEncryption', "
            "'asymmetricEncryption', 'httpApiKey', 'http', 'oauth2', 'openIdConnect', "
            "'plain', 'scramSha256', 'scramSha512', and 'gssapi'."
        ),
    )
    description: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A short description for security type. CommonMark syntax MAY be used "
            "for rich text representation."
        ),
    )
    # TODO: Make complete validation for spec rules (required for dependency)
    name: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "REQUIRED for httpApiKey scheme. The name of the header, query or cookie "
            "parameter to be used."
        ),
    )
    # TODO: Make complete validation for spec rules (required for dependency)
    in_: (
        Literal[
            "user",
            "password",
            "query",
            "header",
            "cookie",
        ]
        | None
    ) = Field(
        default=None,
        exclude_if=is_null,
        alias="in",
        description=(
            "REQUIRED for apiKey or httpApiKey type. The location of the API key. "
            "Valid values are 'user' and 'password' for apiKey and 'query', 'header' "
            "or 'cookie' for httpApiKey."
        ),
    )
    # TODO: Make complete validation for spec rules (required for dependency)
    scheme: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "REQUIRED for http type. The name of the HTTP Authorization scheme to be "
            "used in the Authorization header as defined in RFC7235."
        ),
    )
    bearer_format: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="bearerFormat",
        description=(
            "Used with http ('bearer') type. A hint to the client to identify how the "
            "bearer token is formatted. Bearer tokens are usually generated by an "
            "authorization server, so this information is primarily for documentation "
            "purposes."
        ),
    )
    # TODO: Make complete validation for spec rules (required for dependency)
    flows: OAuthFlows | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "REQUIRED for oauth2 type. An object containing configuration information "
            "for the flow types supported."
        ),
    )
    # TODO: Make complete validation for spec rules (required for dependency)
    open_id_connect_url: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="openIdConnectUrl",
        description=(
            "REQUIRED for openIdConnect type. OpenId Connect URL to discover OAuth2 "
            "configuration values. This MUST be in the form of an absolute URL."
        ),
    )
    scopes: list[str] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Used with oauth2 or openIdConnect type. List of the needed scope names. "
            "An empty array means no scopes are needed."
        ),
    )
