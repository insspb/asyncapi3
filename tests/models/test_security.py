"""Tests for security models."""

from typing import Any

import pytest
import yaml

from pydantic import AnyUrl
from pytest_cases import parametrize_with_cases

from asyncapi3.models.security import (
    CorrelationID,
    OAuthFlow,
    OAuthFlows,
    SecurityScheme,
)


# CorrelationID Validation Test Cases
def case_correlation_id_basic() -> str:
    """CorrelationID with location only."""
    return """
    location: $message.header#/correlationId
    """


def case_correlation_id_full() -> str:
    """CorrelationID with location and description."""
    return """
    description: Default Correlation ID
    location: $message.header#/correlationId
    """


# CorrelationID Serialization Test Cases
def case_correlation_id_serialization_basic() -> tuple[CorrelationID, dict]:
    """CorrelationID serialization with location only."""
    correlation_id = CorrelationID(location="$message.header#/correlationId")
    expected: dict[str, Any] = {"location": "$message.header#/correlationId"}
    return correlation_id, expected


def case_correlation_id_serialization_full() -> tuple[CorrelationID, dict]:
    """CorrelationID serialization with location and description."""
    correlation_id = CorrelationID(
        location="$message.header#/correlationId",
        description="Default Correlation ID",
    )
    expected: dict[str, Any] = {
        "location": "$message.header#/correlationId",
        "description": "Default Correlation ID",
    }
    return correlation_id, expected


# OAuthFlow Validation Test Cases
def case_oauth_flow_implicit() -> str:
    """OAuthFlow implicit flow."""
    return """
    authorizationUrl: 'https://authserver.example/auth'
    availableScopes:
      'streetlights:on': Ability to switch lights on
      'streetlights:off': Ability to switch lights off
    """


def case_oauth_flow_client_credentials() -> str:
    """OAuthFlow clientCredentials flow."""
    return """
    tokenUrl: 'https://authserver.example/token'
    availableScopes:
      'streetlights:on': Ability to switch lights on
      'streetlights:off': Ability to switch lights off
    """


def case_oauth_flow_authorization_code() -> str:
    """OAuthFlow authorizationCode flow."""
    return """
    authorizationUrl: 'https://authserver.example/auth'
    tokenUrl: 'https://authserver.example/token'
    refreshUrl: 'https://authserver.example/refresh'
    availableScopes:
      'streetlights:on': Ability to switch lights on
      'streetlights:off': Ability to switch lights off
    """


# OAuthFlow Serialization Test Cases
def case_oauth_flow_serialization_implicit() -> tuple[OAuthFlow, dict]:
    """OAuthFlow serialization implicit flow."""
    oauth_flow = OAuthFlow(
        authorization_url="https://authserver.example/auth",
        available_scopes={
            "streetlights:on": "Ability to switch lights on",
            "streetlights:off": "Ability to switch lights off",
        },
    )
    expected: dict[str, Any] = {
        "authorizationUrl": AnyUrl("https://authserver.example/auth"),
        "availableScopes": {
            "streetlights:on": "Ability to switch lights on",
            "streetlights:off": "Ability to switch lights off",
        },
    }
    return oauth_flow, expected


def case_oauth_flow_serialization_client_credentials() -> tuple[OAuthFlow, dict]:
    """OAuthFlow serialization clientCredentials flow."""
    oauth_flow = OAuthFlow(
        token_url="https://authserver.example/token",
        available_scopes={
            "streetlights:on": "Ability to switch lights on",
            "streetlights:off": "Ability to switch lights off",
        },
    )
    expected: dict[str, Any] = {
        "tokenUrl": AnyUrl("https://authserver.example/token"),
        "availableScopes": {
            "streetlights:on": "Ability to switch lights on",
            "streetlights:off": "Ability to switch lights off",
        },
    }
    return oauth_flow, expected


def case_oauth_flow_serialization_authorization_code() -> tuple[OAuthFlow, dict]:
    """OAuthFlow serialization authorizationCode flow."""
    oauth_flow = OAuthFlow(
        authorization_url="https://authserver.example/auth",
        token_url="https://authserver.example/token",
        refresh_url="https://authserver.example/refresh",
        available_scopes={
            "streetlights:on": "Ability to switch lights on",
            "streetlights:off": "Ability to switch lights off",
        },
    )
    expected: dict[str, Any] = {
        "authorizationUrl": AnyUrl("https://authserver.example/auth"),
        "tokenUrl": AnyUrl("https://authserver.example/token"),
        "refreshUrl": AnyUrl("https://authserver.example/refresh"),
        "availableScopes": {
            "streetlights:on": "Ability to switch lights on",
            "streetlights:off": "Ability to switch lights off",
        },
    }
    return oauth_flow, expected


# OAuthFlows Validation Test Cases
def case_oauth_flows_basic() -> str:
    """OAuthFlows with implicit flow only."""
    return """
    implicit:
      authorizationUrl: 'https://authserver.example/auth'
      availableScopes:
        'streetlights:on': Ability to switch lights on
    """


def case_oauth_flows_full() -> str:
    """OAuthFlows with all flows."""
    return """
    implicit:
      authorizationUrl: 'https://authserver.example/auth'
      availableScopes:
        'streetlights:on': Ability to switch lights on
    password:
      tokenUrl: 'https://authserver.example/token'
      availableScopes:
        'streetlights:on': Ability to switch lights on
    clientCredentials:
      tokenUrl: 'https://authserver.example/token'
      availableScopes:
        'streetlights:on': Ability to switch lights on
    authorizationCode:
      authorizationUrl: 'https://authserver.example/auth'
      tokenUrl: 'https://authserver.example/token'
      availableScopes:
        'streetlights:on': Ability to switch lights on
    """


# OAuthFlows Serialization Test Cases
def case_oauth_flows_serialization_empty() -> tuple[OAuthFlows, dict]:
    """OAuthFlows serialization empty."""
    oauth_flows = OAuthFlows()
    expected: dict[str, Any] = {}
    return oauth_flows, expected


def case_oauth_flows_serialization_basic() -> tuple[OAuthFlows, dict]:
    """OAuthFlows serialization with implicit flow only."""
    oauth_flows = OAuthFlows(
        implicit=OAuthFlow(
            authorization_url="https://authserver.example/auth",
            available_scopes={"streetlights:on": "Ability to switch lights on"},
        ),
    )
    expected: dict[str, Any] = {
        "implicit": {
            "authorizationUrl": AnyUrl("https://authserver.example/auth"),
            "availableScopes": {
                "streetlights:on": "Ability to switch lights on",
            },
        },
    }
    return oauth_flows, expected


def case_oauth_flows_serialization_full() -> tuple[OAuthFlows, dict]:
    """OAuthFlows serialization with all flows."""
    oauth_flows = OAuthFlows(
        implicit=OAuthFlow(
            authorization_url="https://authserver.example/auth",
            available_scopes={"streetlights:on": "Ability to switch lights on"},
        ),
        password=OAuthFlow(
            token_url="https://authserver.example/token",
            available_scopes={"streetlights:on": "Ability to switch lights on"},
        ),
        client_credentials=OAuthFlow(
            token_url="https://authserver.example/token",
            available_scopes={"streetlights:on": "Ability to switch lights on"},
        ),
        authorization_code=OAuthFlow(
            authorization_url="https://authserver.example/auth",
            token_url="https://authserver.example/token",
            available_scopes={"streetlights:on": "Ability to switch lights on"},
        ),
    )
    expected: dict[str, Any] = {
        "implicit": {
            "authorizationUrl": AnyUrl("https://authserver.example/auth"),
            "availableScopes": {
                "streetlights:on": "Ability to switch lights on",
            },
        },
        "password": {
            "tokenUrl": AnyUrl("https://authserver.example/token"),
            "availableScopes": {
                "streetlights:on": "Ability to switch lights on",
            },
        },
        "clientCredentials": {
            "tokenUrl": AnyUrl("https://authserver.example/token"),
            "availableScopes": {
                "streetlights:on": "Ability to switch lights on",
            },
        },
        "authorizationCode": {
            "authorizationUrl": AnyUrl("https://authserver.example/auth"),
            "tokenUrl": AnyUrl("https://authserver.example/token"),
            "availableScopes": {
                "streetlights:on": "Ability to switch lights on",
            },
        },
    }
    return oauth_flows, expected


# SecurityScheme Validation Test Cases
def case_security_scheme_http() -> str:
    """SecurityScheme http type."""
    return """
    type: http
    scheme: bearer
    bearerFormat: JWT
    """


def case_security_scheme_oauth2() -> str:
    """SecurityScheme oauth2 type."""
    return """
    type: oauth2
    description: Flows to support OAuth 2.0
    flows:
      implicit:
        authorizationUrl: 'https://authserver.example/auth'
        availableScopes:
          'streetlights:on': Ability to switch lights on
    scopes:
      - 'streetlights:on'
    """


def case_security_scheme_api_key() -> str:
    """SecurityScheme apiKey type."""
    return """
    type: apiKey
    in: user
    name: api_key
    """


# SecurityScheme Serialization Test Cases
def case_security_scheme_serialization_http() -> tuple[SecurityScheme, dict]:
    """SecurityScheme serialization http type."""
    security_scheme = SecurityScheme(
        type_="http",
        scheme="bearer",
        bearer_format="JWT",
    )
    expected: dict[str, Any] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    return security_scheme, expected


def case_security_scheme_serialization_api_key() -> tuple[SecurityScheme, dict]:
    """SecurityScheme serialization apiKey type."""
    security_scheme = SecurityScheme(
        type_="apiKey",
        in_="user",
        name="api_key",
    )
    expected: dict[str, Any] = {
        "type": "apiKey",
        "in": "user",
        "name": "api_key",
    }
    return security_scheme, expected


def case_security_scheme_serialization_oauth2() -> tuple[SecurityScheme, dict]:
    """SecurityScheme serialization oauth2 type."""
    security_scheme = SecurityScheme(
        type_="oauth2",
        description="Flows to support OAuth 2.0",
        flows=OAuthFlows(
            implicit=OAuthFlow(
                authorization_url="https://authserver.example/auth",
                available_scopes={"streetlights:on": "Ability to switch lights on"},
            ),
        ),
        scopes=["streetlights:on"],
    )
    expected: dict[str, Any] = {
        "type": "oauth2",
        "description": "Flows to support OAuth 2.0",
        "flows": {
            "implicit": {
                "authorizationUrl": AnyUrl("https://authserver.example/auth"),
                "availableScopes": {
                    "streetlights:on": "Ability to switch lights on",
                },
            },
        },
        "scopes": ["streetlights:on"],
    }
    return security_scheme, expected


# SecurityScheme Validation Error Test Cases
def case_security_scheme_http_api_key_missing_name() -> tuple[str, str]:
    """SecurityScheme httpApiKey missing name - should fail validation."""
    yaml_data = """
    type: httpApiKey
    in: header
    """
    expected_error = "name is required for httpApiKey type"
    return yaml_data, expected_error


def case_security_scheme_api_key_missing_in() -> tuple[str, str]:
    """SecurityScheme apiKey missing in - should fail validation."""
    yaml_data = """
    type: apiKey
    name: api_key
    """
    expected_error = "in is required for apiKey type"
    return yaml_data, expected_error


def case_security_scheme_http_api_key_missing_in() -> tuple[str, str]:
    """SecurityScheme httpApiKey missing in - should fail validation."""
    yaml_data = """
    type: httpApiKey
    name: api_key
    """
    expected_error = "in is required for httpApiKey type"
    return yaml_data, expected_error


def case_security_scheme_http_missing_scheme() -> tuple[str, str]:
    """SecurityScheme http missing scheme - should fail validation."""
    yaml_data = """
    type: http
    """
    expected_error = "scheme is required for http type"
    return yaml_data, expected_error


def case_security_scheme_api_key_invalid_in() -> tuple[str, str]:
    """SecurityScheme apiKey with invalid in value - should fail validation."""
    yaml_data = """
    type: apiKey
    in: header
    name: api_key
    """
    expected_error = "in must be 'user' or 'password' for apiKey type"
    return yaml_data, expected_error


def case_security_scheme_http_api_key_invalid_in() -> tuple[str, str]:
    """SecurityScheme httpApiKey with invalid in value - should fail validation."""
    yaml_data = """
    type: httpApiKey
    in: user
    name: api_key
    """
    expected_error = "in must be 'query', 'header', or 'cookie' for httpApiKey type"
    return yaml_data, expected_error


def case_security_scheme_bearer_format_without_bearer_scheme() -> tuple[str, str]:
    """SecurityScheme with bearerFormat but not bearer scheme - should fail validation."""
    yaml_data = """
    type: http
    scheme: basic
    bearerFormat: JWT
    """
    expected_error = "bearerFormat can only be used with http type and bearer scheme"
    return yaml_data, expected_error


def case_security_scheme_bearer_format_without_http_type() -> tuple[str, str]:
    """SecurityScheme with bearerFormat but not http type - should fail validation."""
    yaml_data = """
    type: apiKey
    in: user
    name: api_key
    bearerFormat: JWT
    """
    expected_error = "bearerFormat can only be used with http type and bearer scheme"
    return yaml_data, expected_error


def case_security_scheme_oauth2_missing_flows() -> tuple[str, str]:
    """SecurityScheme oauth2 missing flows - should fail validation."""
    yaml_data = """
    type: oauth2
    """
    expected_error = "flows is required for oauth2 type"
    return yaml_data, expected_error


def case_security_scheme_openid_connect_missing_url() -> tuple[str, str]:
    """SecurityScheme openIdConnect missing openIdConnectUrl - should fail validation."""
    yaml_data = """
    type: openIdConnect
    """
    expected_error = "openIdConnectUrl is required for openIdConnect type"
    return yaml_data, expected_error


def case_security_scheme_scopes_with_wrong_type() -> tuple[str, str]:
    """SecurityScheme with scopes but wrong type - should fail validation."""
    yaml_data = """
    type: http
    scheme: basic
    scopes:
      - read
    """
    expected_error = "scopes can only be used with oauth2 or openIdConnect type"
    return yaml_data, expected_error


# OAuthFlows Validation Error Test Cases
def case_oauth_flows_implicit_missing_authorization_url() -> tuple[str, str]:
    """OAuthFlows implicit flow missing authorizationUrl - should fail validation."""
    yaml_data = """
    implicit:
      availableScopes:
        'read': Read access
    """
    expected_error = "authorizationUrl is required for implicit flow"
    return yaml_data, expected_error


def case_oauth_flows_password_missing_token_url() -> tuple[str, str]:
    """OAuthFlows password flow missing tokenUrl - should fail validation."""
    yaml_data = """
    password:
      availableScopes:
        'read': Read access
    """
    expected_error = "tokenUrl is required for password flow"
    return yaml_data, expected_error


def case_oauth_flows_client_credentials_missing_token_url() -> tuple[str, str]:
    """OAuthFlows clientCredentials flow missing tokenUrl - should fail validation."""
    yaml_data = """
    clientCredentials:
      availableScopes:
        'read': Read access
    """
    expected_error = "tokenUrl is required for clientCredentials flow"
    return yaml_data, expected_error


def case_oauth_flows_authorization_code_missing_authorization_url() -> tuple[str, str]:
    """OAuthFlows authorizationCode flow missing authorizationUrl - should fail validation."""
    yaml_data = """
    authorizationCode:
      tokenUrl: 'https://authserver.example/token'
      availableScopes:
        'read': Read access
    """
    expected_error = "authorizationUrl is required for authorizationCode flow"
    return yaml_data, expected_error


def case_oauth_flows_authorization_code_missing_token_url() -> tuple[str, str]:
    """OAuthFlows authorizationCode flow missing tokenUrl - should fail validation."""
    yaml_data = """
    authorizationCode:
      authorizationUrl: 'https://authserver.example/auth'
      availableScopes:
        'read': Read access
    """
    expected_error = "tokenUrl is required for authorizationCode flow"
    return yaml_data, expected_error


# CorrelationID Validation Error Test Cases
def case_correlation_id_invalid_location() -> tuple[str, str]:
    """CorrelationID with invalid location - should fail validation."""
    yaml_data = """
    location: invalid_location
    """
    expected_error = "location must be a runtime expression starting with '\\$message.'"
    return yaml_data, expected_error


def case_correlation_id_empty_location() -> tuple[str, str]:
    """CorrelationID with empty location - should fail validation."""
    yaml_data = """
    location: ""
    """
    expected_error = "location must be a runtime expression starting with '\\$message.'"
    return yaml_data, expected_error


class TestCorrelationID:
    """Tests for CorrelationID model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_correlation_id_basic, case_correlation_id_full],
    )
    def test_correlation_id_validation(self, yaml_data: str) -> None:
        """Test CorrelationID model validation."""
        data = yaml.safe_load(yaml_data)
        correlation_id = CorrelationID.model_validate(data)
        assert correlation_id is not None
        assert correlation_id.location == "$message.header#/correlationId"

    @parametrize_with_cases(
        "correlation_id,expected",
        cases=[
            case_correlation_id_serialization_basic,
            case_correlation_id_serialization_full,
        ],
    )
    def test_correlation_id_serialization(
        self,
        correlation_id: CorrelationID,
        expected: dict,
    ) -> None:
        """Test CorrelationID serialization."""
        dumped = correlation_id.model_dump()
        assert dumped == expected

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_correlation_id_invalid_location,
            case_correlation_id_empty_location,
        ],
    )
    def test_correlation_id_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test CorrelationID validation errors for invalid runtime expressions."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValueError, match=expected_error):
            CorrelationID.model_validate(data)


class TestSecuritySchemeValidationErrors:
    """Tests for SecurityScheme validation errors."""

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_security_scheme_http_api_key_missing_name,
            case_security_scheme_api_key_missing_in,
            case_security_scheme_http_api_key_missing_in,
            case_security_scheme_http_missing_scheme,
            case_security_scheme_api_key_invalid_in,
            case_security_scheme_http_api_key_invalid_in,
            case_security_scheme_bearer_format_without_bearer_scheme,
            case_security_scheme_bearer_format_without_http_type,
            case_security_scheme_oauth2_missing_flows,
            case_security_scheme_openid_connect_missing_url,
            case_security_scheme_scopes_with_wrong_type,
        ],
    )
    def test_security_scheme_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test SecurityScheme validation errors for invalid field combinations."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValueError, match=expected_error):
            SecurityScheme.model_validate(data)


class TestOAuthFlowsValidationErrors:
    """Tests for OAuthFlows validation errors."""

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_oauth_flows_implicit_missing_authorization_url,
            case_oauth_flows_password_missing_token_url,
            case_oauth_flows_client_credentials_missing_token_url,
            case_oauth_flows_authorization_code_missing_authorization_url,
            case_oauth_flows_authorization_code_missing_token_url,
        ],
    )
    def test_oauth_flows_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test OAuthFlows validation errors for invalid flow configurations."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValueError, match=expected_error):
            OAuthFlows.model_validate(data)


class TestOAuthFlow:
    """Tests for OAuthFlow model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[
            case_oauth_flow_implicit,
            case_oauth_flow_client_credentials,
            case_oauth_flow_authorization_code,
        ],
    )
    def test_oauth_flow_validation(self, yaml_data: str) -> None:
        """Test OAuthFlow model validation."""
        data = yaml.safe_load(yaml_data)
        oauth_flow = OAuthFlow.model_validate(data)
        assert oauth_flow is not None
        assert oauth_flow.available_scopes is not None

    @parametrize_with_cases(
        "oauth_flow,expected",
        cases=[
            case_oauth_flow_serialization_implicit,
            case_oauth_flow_serialization_client_credentials,
            case_oauth_flow_serialization_authorization_code,
        ],
    )
    def test_oauth_flow_serialization(
        self,
        oauth_flow: OAuthFlow,
        expected: dict,
    ) -> None:
        """Test OAuthFlow serialization."""
        dumped = oauth_flow.model_dump()
        assert dumped == expected


class TestOAuthFlows:
    """Tests for OAuthFlows model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_oauth_flows_basic, case_oauth_flows_full],
    )
    def test_oauth_flows_validation(self, yaml_data: str) -> None:
        """Test OAuthFlows model validation."""
        data = yaml.safe_load(yaml_data)
        oauth_flows = OAuthFlows.model_validate(data)
        assert oauth_flows is not None
        if "implicit" in data:
            assert oauth_flows.implicit is not None

    @parametrize_with_cases(
        "oauth_flows,expected",
        cases=[
            case_oauth_flows_serialization_empty,
            case_oauth_flows_serialization_basic,
            case_oauth_flows_serialization_full,
        ],
    )
    def test_oauth_flows_serialization(
        self,
        oauth_flows: OAuthFlows,
        expected: dict,
    ) -> None:
        """Test OAuthFlows serialization."""
        dumped = oauth_flows.model_dump()
        assert dumped == expected


class TestSecurityScheme:
    """Tests for SecurityScheme model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[
            case_security_scheme_http,
            case_security_scheme_oauth2,
            case_security_scheme_api_key,
        ],
    )
    def test_security_scheme_validation(self, yaml_data: str) -> None:
        """Test SecurityScheme model validation."""
        data = yaml.safe_load(yaml_data)
        security_scheme = SecurityScheme.model_validate(data)
        assert security_scheme is not None
        assert security_scheme.type_ == data["type"]

    @parametrize_with_cases(
        "security_scheme,expected",
        cases=[
            case_security_scheme_serialization_http,
            case_security_scheme_serialization_api_key,
            case_security_scheme_serialization_oauth2,
        ],
    )
    def test_security_scheme_serialization(
        self,
        security_scheme: SecurityScheme,
        expected: dict,
    ) -> None:
        """Test SecurityScheme serialization."""
        dumped = security_scheme.model_dump()
        assert dumped == expected

    def test_security_scheme_oauth2_with_flows_validation(self) -> None:
        """Test SecurityScheme oauth2 with flows validation."""
        yaml_data = """
        type: oauth2
        description: Flows to support OAuth 2.0
        flows:
          implicit:
            authorizationUrl: 'https://authserver.example/auth'
            availableScopes:
              'streetlights:on': Ability to switch lights on
        scopes:
          - 'streetlights:on'
        """
        data = yaml.safe_load(yaml_data)
        security_scheme = SecurityScheme.model_validate(data)

        assert security_scheme.type_ == "oauth2"
        assert security_scheme.flows is not None
        assert isinstance(security_scheme.flows, OAuthFlows)
        assert security_scheme.flows.implicit is not None
        assert isinstance(security_scheme.flows.implicit.authorization_url, AnyUrl)
