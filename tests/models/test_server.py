"""Tests for server models."""

from typing import Any

import pytest
import yaml

from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.base import Reference
from asyncapi3.models.server import Server, Servers, ServerVariable


# ServerVariable Validation Test Cases
def case_server_variable_basic() -> str:
    """ServerVariable with default only."""
    return """
    default: '1883'
    """


def case_server_variable_full() -> str:
    """ServerVariable with all fields."""
    return """
    description: Environment to connect to. It can be either `production` or `staging`.
    enum:
      - production
      - staging
    default: production
    examples:
      - production
      - staging
    """


# ServerVariable Serialization Test Cases
def case_server_variable_serialization_empty() -> tuple[ServerVariable, dict]:
    """ServerVariable serialization empty."""
    server_variable = ServerVariable()
    expected: dict[str, Any] = {}
    return server_variable, expected


def case_server_variable_serialization_basic() -> tuple[ServerVariable, dict]:
    """ServerVariable serialization with default only."""
    server_variable = ServerVariable(default="1883")
    expected: dict[str, Any] = {"default": "1883"}
    return server_variable, expected


def case_server_variable_serialization_with_enum() -> tuple[ServerVariable, dict]:
    """ServerVariable serialization with enum."""
    server_variable = ServerVariable(
        description="Environment to connect to.",
        enum=["production", "staging"],
        default="production",
    )
    expected: dict[str, Any] = {
        "description": "Environment to connect to.",
        "enum": ["production", "staging"],
        "default": "production",
    }
    return server_variable, expected


def case_server_variable_serialization_full() -> tuple[ServerVariable, dict]:
    """ServerVariable serialization with all fields."""
    server_variable = ServerVariable(
        description="Environment to connect to. It can be either `production` or `staging`.",
        enum=["production", "staging"],
        default="production",
        examples=["production", "staging"],
    )
    expected: dict[str, Any] = {
        "description": "Environment to connect to. It can be either `production` or `staging`.",
        "enum": ["production", "staging"],
        "default": "production",
        "examples": ["production", "staging"],
    }
    return server_variable, expected


# Server Validation Test Cases
def case_server_basic() -> str:
    """Server with required fields only."""
    return """
    host: kafka.in.mycompany.com:9092
    protocol: kafka
    """


def case_server_full() -> str:
    """Server with all fields."""
    return """
    host: kafka.in.mycompany.com:9092
    description: Production Kafka broker.
    protocol: kafka
    protocolVersion: '3.2'
    """


def case_server_with_pathname() -> str:
    """Server with pathname."""
    return """
    host: rabbitmq.in.mycompany.com:5672
    pathname: /production
    protocol: amqp
    description: Production RabbitMQ broker (uses the `production` vhost).
    """


def case_server_with_variables() -> str:
    """Server with variables."""
    return """
    host: 'rabbitmq.in.mycompany.com:5672'
    pathname: '/{env}'
    protocol: amqp
    description: RabbitMQ broker. Use the `env` variable to point to either `production` or `staging`.
    variables:
      env:
        description: Environment to connect to. It can be either `production` or `staging`.
        enum:
          - production
          - staging
    """


# Server Serialization Test Cases
def case_server_serialization_basic() -> tuple[Server, dict]:
    """Server serialization with required fields only."""
    server = Server(
        host="kafka.in.mycompany.com:9092",
        protocol="kafka",
    )
    expected: dict[str, Any] = {
        "host": "kafka.in.mycompany.com:9092",
        "protocol": "kafka",
    }
    return server, expected


def case_server_serialization_with_pathname() -> tuple[Server, dict]:
    """Server serialization with pathname."""
    server = Server(
        host="rabbitmq.in.mycompany.com:5672",
        pathname="/production",
        protocol="amqp",
    )
    expected: dict[str, Any] = {
        "host": "rabbitmq.in.mycompany.com:5672",
        "pathname": "/production",
        "protocol": "amqp",
    }
    return server, expected


def case_server_serialization_with_protocol_version() -> tuple[Server, dict]:
    """Server serialization with protocolVersion."""
    server = Server(
        host="kafka.in.mycompany.com:9092",
        protocol="kafka",
        protocol_version="3.2",
    )
    expected: dict[str, Any] = {
        "host": "kafka.in.mycompany.com:9092",
        "protocol": "kafka",
        "protocolVersion": "3.2",
    }
    return server, expected


def case_server_serialization_with_variables() -> tuple[Server, dict]:
    """Server serialization with variables."""
    server = Server(
        host="rabbitmq.in.mycompany.com:5672",
        pathname="/{env}",
        protocol="amqp",
        variables={
            "env": ServerVariable(
                description="Environment to connect to.",
                enum=["production", "staging"],
                default="production",
            ),
        },
    )
    expected: dict[str, Any] = {
        "host": "rabbitmq.in.mycompany.com:5672",
        "pathname": "/{env}",
        "protocol": "amqp",
        "variables": {
            "env": {
                "description": "Environment to connect to.",
                "enum": ["production", "staging"],
                "default": "production",
            },
        },
    }
    return server, expected


def case_server_serialization_with_reference_variable() -> tuple[Server, dict]:
    """Server serialization with variable as Reference."""
    server = Server(
        host="rabbitmq.in.mycompany.com:5672",
        protocol="amqp",
        variables={"env": Reference(ref="#/components/serverVariables/env")},
    )
    expected: dict[str, Any] = {
        "host": "rabbitmq.in.mycompany.com:5672",
        "protocol": "amqp",
        "variables": {
            "env": {
                "$ref": "#/components/serverVariables/env",
            },
        },
    }
    return server, expected


# Servers Validation Test Cases
def case_servers_basic() -> str:
    """Servers with basic valid keys."""
    return """
    production:
      host: kafka.in.mycompany.com:9092
      protocol: kafka
    staging:
      host: kafka-staging.in.mycompany.com:9092
      protocol: kafka
    """


def case_servers_with_underscores_and_hyphens() -> str:
    """Servers with keys containing underscores and hyphens."""
    return """
    production_server_1:
      host: kafka.in.mycompany.com:9092
      protocol: kafka
    staging-server-2:
      host: kafka-staging.in.mycompany.com:9092
      protocol: kafka
    server_3:
      host: kafka-dev.in.mycompany.com:9092
      protocol: kafka
    """


def case_servers_with_references() -> str:
    """Servers with Reference objects."""
    return """
    production:
      $ref: '#/components/servers/production'
    staging:
      host: kafka-staging.in.mycompany.com:9092
      protocol: kafka
    """


# Servers Validation Error Test Cases
def case_servers_invalid_key_spaces() -> tuple[str, str]:
    """Servers with key containing spaces - should fail validation."""
    yaml_data = """
    production server:
      host: kafka.in.mycompany.com:9092
      protocol: kafka
    """
    expected_error = "Field 'production server' does not match patterned object key pattern. Keys must contain letters, digits, hyphens, and underscores."
    return yaml_data, expected_error


def case_servers_invalid_key_special_chars() -> tuple[str, str]:
    """Servers with key containing special characters - should fail validation."""
    yaml_data = """
    production@server:
      host: kafka.in.mycompany.com:9092
      protocol: kafka
    """
    expected_error = "Field 'production@server' does not match patterned object key pattern. Keys must contain letters, digits, hyphens, and underscores."
    return yaml_data, expected_error


def case_servers_invalid_key_dots() -> tuple[str, str]:
    """Servers with key containing dots - should fail validation."""
    yaml_data = """
    production.server:
      host: kafka.in.mycompany.com:9092
      protocol: kafka
    """
    expected_error = "Field 'production.server' does not match patterned object key pattern. Keys must contain letters, digits, hyphens, and underscores."
    return yaml_data, expected_error


def case_servers_invalid_key_empty() -> tuple[str, str]:
    """Servers with empty key - should fail validation."""
    yaml_data = """
    "":
      host: kafka.in.mycompany.com:9092
      protocol: kafka
    """
    expected_error = "Field '' does not match patterned object key pattern. Keys must contain letters, digits, hyphens, and underscores."
    return yaml_data, expected_error


class TestServerVariable:
    """Tests for ServerVariable model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_server_variable_basic, case_server_variable_full],
    )
    def test_server_variable_validation(self, yaml_data: str) -> None:
        """Test ServerVariable model validation."""
        data = yaml.safe_load(yaml_data)
        server_variable = ServerVariable.model_validate(data)
        assert server_variable is not None
        if "default" in data:
            assert server_variable.default == data["default"]

    @parametrize_with_cases(
        "server_variable,expected",
        cases=[
            case_server_variable_serialization_empty,
            case_server_variable_serialization_basic,
            case_server_variable_serialization_with_enum,
            case_server_variable_serialization_full,
        ],
    )
    def test_server_variable_serialization(
        self,
        server_variable: ServerVariable,
        expected: dict,
    ) -> None:
        """Test ServerVariable serialization."""
        dumped = server_variable.model_dump()
        assert dumped == expected

    def test_server_variable_with_enum_validation(self) -> None:
        """Test ServerVariable with enum validation."""
        yaml_data = """
        description: Environment to connect to.
        enum:
          - production
          - staging
        default: production
        """
        data = yaml.safe_load(yaml_data)
        server_variable = ServerVariable.model_validate(data)

        assert server_variable.enum == ["production", "staging"]
        assert server_variable.default == "production"
        assert server_variable.description == "Environment to connect to."

    def test_server_variable_empty_enum_validation(self) -> None:
        """Test ServerVariable with empty enum list."""
        yaml_data = """
        enum: []
        default: production
        """
        data = yaml.safe_load(yaml_data)
        server_variable = ServerVariable.model_validate(data)

        assert server_variable.enum == []
        assert server_variable.default == "production"


class TestServer:
    """Tests for Server model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[
            case_server_basic,
            case_server_full,
            case_server_with_pathname,
            case_server_with_variables,
        ],
    )
    def test_server_validation(self, yaml_data: str) -> None:
        """Test Server model validation."""
        data = yaml.safe_load(yaml_data)
        server = Server.model_validate(data)
        assert server is not None
        assert server.host == data["host"]
        assert server.protocol == data["protocol"]

    @parametrize_with_cases(
        "server,expected",
        cases=[
            case_server_serialization_basic,
            case_server_serialization_with_pathname,
            case_server_serialization_with_protocol_version,
            case_server_serialization_with_variables,
            case_server_serialization_with_reference_variable,
        ],
    )
    def test_server_serialization(self, server: Server, expected: dict) -> None:
        """Test Server serialization."""
        dumped = server.model_dump()
        assert dumped == expected

    def test_server_with_variables_validation(self) -> None:
        """Test Server with variables validation."""
        yaml_data = """
        host: 'rabbitmq.in.mycompany.com:5672'
        pathname: '/{env}'
        protocol: amqp
        variables:
          env:
            description: Environment to connect to.
            enum:
              - production
              - staging
            default: production
        """
        data = yaml.safe_load(yaml_data)
        server = Server.model_validate(data)

        assert server.variables is not None
        assert "env" in server.variables
        assert isinstance(server.variables["env"], ServerVariable)
        assert server.variables["env"].default == "production"
        assert server.variables["env"].enum == ["production", "staging"]

    def test_server_with_reference_variable_validation(self) -> None:
        """Test Server with variable as Reference validation."""
        yaml_data = """
        host: 'rabbitmq.in.mycompany.com:5672'
        protocol: amqp
        variables:
          env:
            $ref: '#/components/serverVariables/env'
        """
        data = yaml.safe_load(yaml_data)
        server = Server.model_validate(data)

        assert server.variables is not None
        assert "env" in server.variables
        assert isinstance(server.variables["env"], Reference)
        assert server.variables["env"].ref == "#/components/serverVariables/env"

    def test_server_with_protocol_version_validation(self) -> None:
        """Test Server with protocolVersion validation."""
        yaml_data = """
        host: kafka.in.mycompany.com:9092
        protocol: kafka
        protocolVersion: '3.2'
        """
        data = yaml.safe_load(yaml_data)
        server = Server.model_validate(data)

        assert server.protocol_version == "3.2"

    def test_server_with_pathname_validation(self) -> None:
        """Test Server with pathname validation."""
        yaml_data = """
        host: rabbitmq.in.mycompany.com:5672
        pathname: /production
        protocol: amqp
        """
        data = yaml.safe_load(yaml_data)
        server = Server.model_validate(data)

        assert server.pathname == "/production"

    def test_server_missing_host_validation_error(self) -> None:
        """Test Server validation error when host is missing."""
        yaml_data = """
        protocol: kafka
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            Server.model_validate(data)

    def test_server_missing_protocol_validation_error(self) -> None:
        """Test Server validation error when protocol is missing."""
        yaml_data = """
        host: kafka.in.mycompany.com:9092
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            Server.model_validate(data)

    def test_server_missing_required_fields_validation_error(self) -> None:
        """Test Server validation error when both host and protocol are missing."""
        yaml_data = """
        description: Test server
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            Server.model_validate(data)


class TestServers:
    """Tests for Servers model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[
            case_servers_basic,
            case_servers_with_underscores_and_hyphens,
            case_servers_with_references,
        ],
    )
    def test_servers_validation(self, yaml_data: str) -> None:
        """Test Servers model validation."""
        data = yaml.safe_load(yaml_data)
        servers = Servers.model_validate(data)
        assert servers is not None
        assert isinstance(servers.root, dict)
        assert len(servers.root) > 0

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_servers_invalid_key_spaces,
            case_servers_invalid_key_special_chars,
            case_servers_invalid_key_dots,
            case_servers_invalid_key_empty,
        ],
    )
    def test_servers_validation_errors(
        self, yaml_data: str, expected_error: str
    ) -> None:
        """Test Servers validation errors for invalid field names."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValueError, match=expected_error):
            Servers.model_validate(data)

    def test_servers_empty_dict_validation(self) -> None:
        """Test Servers with empty dict validation."""
        servers = Servers.model_validate({})
        assert servers is not None
        assert servers.root == {}
        assert len(servers.root) == 0

    def test_servers_iteration(self) -> None:
        """Test Servers __iter__ method."""
        data: dict[str, Server | Reference] = {
            "production": Server(host="kafka.in.mycompany.com:9092", protocol="kafka"),
            "staging": Server(
                host="kafka-staging.in.mycompany.com:9092", protocol="kafka"
            ),
        }
        servers = Servers(root=data)

        keys = list(servers)
        assert len(keys) == 2
        assert "production" in keys
        assert "staging" in keys

    def test_servers_getitem(self) -> None:
        """Test Servers __getitem__ method."""
        production_server = Server(host="kafka.in.mycompany.com:9092", protocol="kafka")
        staging_server = Server(
            host="kafka-staging.in.mycompany.com:9092", protocol="kafka"
        )

        data: dict[str, Server | Reference] = {
            "production": production_server,
            "staging": staging_server,
        }
        servers = Servers(root=data)

        assert servers["production"] == production_server
        assert servers["staging"] == staging_server

        # Test with Reference
        ref = Reference(ref="#/components/servers/dev")
        data_with_ref: dict[str, Server | Reference] = {"dev": ref}
        servers_with_ref = Servers(root=data_with_ref)
        assert servers_with_ref["dev"] == ref

    def test_servers_getattr(self) -> None:
        """Test Servers __getattr__ method."""
        production_server = Server(host="kafka.in.mycompany.com:9092", protocol="kafka")
        staging_server = Server(
            host="kafka-staging.in.mycompany.com:9092", protocol="kafka"
        )

        data: dict[str, Server | Reference] = {
            "production": production_server,
            "staging": staging_server,
        }
        servers = Servers(root=data)

        assert servers.production == production_server
        assert servers.staging == staging_server

        # Test with Reference
        ref = Reference(ref="#/components/servers/dev")
        data_with_ref: dict[str, Server | Reference] = {"dev": ref}
        servers_with_ref = Servers(root=data_with_ref)
        assert servers_with_ref.dev == ref
