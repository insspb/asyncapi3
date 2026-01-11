"""Security models for AsyncAPI 3.0 specification."""

__all__ = [
    "CorrelationID",
    "OAuthFlow",
    "OAuthFlows",
    "SecurityScheme",
]

from typing import Literal

from pydantic import AnyUrl, Field, field_validator, model_validator

from asyncapi3.models.base_models import ExtendableBaseModel
from asyncapi3.models.helpers import is_null


class CorrelationID(ExtendableBaseModel):
    """
    Correlation ID Object.

    An object that specifies an identifier at design time that can used for message
    tracing and correlation.

    For specifying and computing the location of a Correlation ID, a runtime
    expression is used.

    This object MAY be extended with Specification Extensions.
    """

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

    @field_validator("location")
    @classmethod
    def validate_runtime_expression(cls, location: str) -> str:
        """
        Validate that location contains a valid runtime expression.

        Runtime expressions must start with '$message.' according to
        AsyncAPI 3.0 specification.
        """
        if not location.startswith("$message."):
            raise ValueError(
                "location must be a runtime expression starting with '$message.'"
            )
        return location


class OAuthFlow(ExtendableBaseModel):
    """
    OAuth Flow Object.

    Configuration details for a supported OAuth Flow.

    This object MAY be extended with Specification Extensions.
    """

    authorization_url: AnyUrl | None = Field(
        default=None,
        exclude_if=is_null,
        alias="authorizationUrl",
        description=(
            "REQUIRED for: oauth2 ('implicit', 'authorizationCode'). The "
            "authorization URL to be used for this flow. This MUST be in the form "
            "of an absolute URL."
        ),
    )
    token_url: AnyUrl | None = Field(
        default=None,
        exclude_if=is_null,
        alias="tokenUrl",
        description=(
            "REQUIRED for: oauth2 ('password', 'clientCredentials', "
            "'authorizationCode'). The token URL to be used for this flow. This MUST "
            "be in the form of an absolute URL."
        ),
    )
    refresh_url: AnyUrl | None = Field(
        default=None,
        exclude_if=is_null,
        alias="refreshUrl",
        description=(
            "Applied to oauth2 type. The URL to be used for obtaining refresh tokens. "
            "This MUST be in the form of an absolute URL."
        ),
    )
    available_scopes: dict[str, str] = Field(
        alias="availableScopes",
        description=(
            "REQUIRED for oauth2 type. The available scopes for the OAuth2 security "
            "scheme. A map between the scope name and a short description for it."
        ),
    )


class OAuthFlows(ExtendableBaseModel):
    """
    OAuth Flows Object.

    Allows configuration of the supported OAuth Flows.

    This object MAY be extended with Specification Extensions.
    """

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

    @model_validator(mode="after")
    def validate_oauth_flows_requirements(self) -> "OAuthFlows":
        """
        Validate OAuthFlows field requirements based on flow types.

        Performs validation according to AsyncAPI 3.0 specification requirements
        for different OAuth flow types.
        """
        self._validate_implicit_flow()
        self._validate_password_flow()
        self._validate_client_credentials_flow()
        self._validate_authorization_code_flow()
        return self

    def _validate_implicit_flow(self) -> None:
        """Validate implicit flow requirements."""
        if self.implicit is not None and self.implicit.authorization_url is None:
            raise ValueError("authorizationUrl is required for implicit flow")

    def _validate_password_flow(self) -> None:
        """Validate password flow requirements."""
        if self.password is not None and self.password.token_url is None:
            raise ValueError("tokenUrl is required for password flow")

    def _validate_client_credentials_flow(self) -> None:
        """Validate clientCredentials flow requirements."""
        if (
            self.client_credentials is not None
            and self.client_credentials.token_url is None
        ):
            raise ValueError("tokenUrl is required for clientCredentials flow")

    def _validate_authorization_code_flow(self) -> None:
        """Validate authorizationCode flow requirements."""
        if self.authorization_code is not None:
            if self.authorization_code.authorization_url is None:
                raise ValueError(
                    "authorizationUrl is required for authorizationCode flow"
                )
            if self.authorization_code.token_url is None:
                raise ValueError("tokenUrl is required for authorizationCode flow")


class SecurityScheme(ExtendableBaseModel):
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
    name: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "REQUIRED for httpApiKey scheme. The name of the header, query or cookie "
            "parameter to be used."
        ),
    )
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
    flows: OAuthFlows | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "REQUIRED for oauth2 type. An object containing configuration information "
            "for the flow types supported."
        ),
    )
    open_id_connect_url: AnyUrl | None = Field(
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

    @model_validator(mode="after")
    def validate_security_scheme_dependencies(self) -> "SecurityScheme":
        """
        Validate SecurityScheme field dependencies based on type.

        Performs validation according to AsyncAPI 3.0 specification requirements
        for different security scheme types.
        """
        self._validate_api_key_requirements()
        self._validate_bearer_format_requirements()
        self._validate_http_api_key_requirements()
        self._validate_http_requirements()
        self._validate_oauth2_requirements()
        self._validate_openid_connect_requirements()
        self._validate_scopes_requirements()

        return self

    def _validate_api_key_requirements(self) -> None:
        """Validate apiKey type requirements."""
        if self.type_ == "apiKey":
            if self.in_ is None:
                raise ValueError("in is required for apiKey type")
            if self.in_ not in ("user", "password"):
                raise ValueError("in must be 'user' or 'password' for apiKey type")

    def _validate_http_api_key_requirements(self) -> None:
        """Validate httpApiKey type requirements."""
        if self.type_ == "httpApiKey":
            if self.name is None:
                raise ValueError("name is required for httpApiKey type")
            if self.in_ is None:
                raise ValueError("in is required for httpApiKey type")
            if self.in_ not in ("query", "header", "cookie"):
                raise ValueError(
                    "in must be 'query', 'header', or 'cookie' for httpApiKey type"
                )

    def _validate_http_requirements(self) -> None:
        """Validate http type requirements."""
        if self.type_ == "http" and self.scheme is None:
            raise ValueError("scheme is required for http type")

    def _validate_bearer_format_requirements(self) -> None:
        """Validate bearerFormat requirements."""
        if self.bearer_format is not None and (
            self.type_ != "http" or self.scheme != "bearer"
        ):
            raise ValueError(
                "bearerFormat can only be used with http type and bearer scheme"
            )

    def _validate_oauth2_requirements(self) -> None:
        """Validate oauth2 type requirements."""
        if self.type_ == "oauth2" and self.flows is None:
            raise ValueError("flows is required for oauth2 type")

    def _validate_openid_connect_requirements(self) -> None:
        """Validate openIdConnect type requirements."""
        if self.type_ == "openIdConnect" and self.open_id_connect_url is None:
            raise ValueError("openIdConnectUrl is required for openIdConnect type")

    def _validate_scopes_requirements(self) -> None:
        """Validate scopes requirements."""
        if self.scopes is not None and self.type_ not in ("oauth2", "openIdConnect"):
            raise ValueError(
                "scopes can only be used with oauth2 or openIdConnect type"
            )
