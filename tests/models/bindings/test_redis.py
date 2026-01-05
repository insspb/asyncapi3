"""Tests for Redis bindings models."""

import pytest
import yaml

from pydantic import ValidationError

from asyncapi3.models.bindings.redis import (
    RedisChannelBindings,
    RedisMessageBindings,
    RedisOperationBindings,
    RedisServerBindings,
)


class TestRedisServerBindings:
    """Tests for RedisServerBindings model."""

    def test_redis_server_bindings_serialization(self) -> None:
        """Test RedisServerBindings serialization."""
        redis_binding = RedisServerBindings()
        dumped = redis_binding.model_dump()
        assert dumped == {}

    def test_redis_server_bindings_python_validation_error(self) -> None:
        """Test RedisServerBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            RedisServerBindings(some_field="value")

    def test_redis_server_bindings_yaml_validation_error(self) -> None:
        """Test RedisServerBindings YAML validation error with any fields."""
        yaml_data = """
        redis:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            RedisServerBindings.model_validate(data["redis"])

    def test_redis_server_bindings_yaml_empty_validation(self) -> None:
        """Test RedisServerBindings YAML validation with no fields."""
        yaml_data = """
        redis: {}
        """
        data = yaml.safe_load(yaml_data)
        redis_binding = RedisServerBindings.model_validate(data["redis"])
        assert redis_binding is not None


class TestRedisChannelBindings:
    """Tests for RedisChannelBindings model."""

    def test_redis_channel_bindings_serialization(self) -> None:
        """Test RedisChannelBindings serialization."""
        redis_binding = RedisChannelBindings()
        dumped = redis_binding.model_dump()
        assert dumped == {}

    def test_redis_channel_bindings_python_validation_error(self) -> None:
        """Test RedisChannelBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            RedisChannelBindings(some_field="value")

    def test_redis_channel_bindings_yaml_validation_error(self) -> None:
        """Test RedisChannelBindings YAML validation error with any fields."""
        yaml_data = """
        redis:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            RedisChannelBindings.model_validate(data["redis"])

    def test_redis_channel_bindings_yaml_empty_validation(self) -> None:
        """Test RedisChannelBindings YAML validation with no fields."""
        yaml_data = """
        redis: {}
        """
        data = yaml.safe_load(yaml_data)
        redis_binding = RedisChannelBindings.model_validate(data["redis"])
        assert redis_binding is not None


class TestRedisOperationBindings:
    """Tests for RedisOperationBindings model."""

    def test_redis_operation_bindings_serialization(self) -> None:
        """Test RedisOperationBindings serialization."""
        redis_binding = RedisOperationBindings()
        dumped = redis_binding.model_dump()
        assert dumped == {}

    def test_redis_operation_bindings_python_validation_error(self) -> None:
        """Test RedisOperationBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            RedisOperationBindings(some_field="value")

    def test_redis_operation_bindings_yaml_validation_error(self) -> None:
        """Test RedisOperationBindings YAML validation error with any fields."""
        yaml_data = """
        redis:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            RedisOperationBindings.model_validate(data["redis"])

    def test_redis_operation_bindings_yaml_empty_validation(self) -> None:
        """Test RedisOperationBindings YAML validation with no fields."""
        yaml_data = """
        redis: {}
        """
        data = yaml.safe_load(yaml_data)
        redis_binding = RedisOperationBindings.model_validate(data["redis"])
        assert redis_binding is not None


class TestRedisMessageBindings:
    """Tests for RedisMessageBindings model."""

    def test_redis_message_bindings_serialization(self) -> None:
        """Test RedisMessageBindings serialization."""
        redis_binding = RedisMessageBindings()
        dumped = redis_binding.model_dump()
        assert dumped == {}

    def test_redis_message_bindings_python_validation_error(self) -> None:
        """Test RedisMessageBindings Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            RedisMessageBindings(some_field="value")

    def test_redis_message_bindings_yaml_validation_error(self) -> None:
        """Test RedisMessageBindings YAML validation error with any fields."""
        yaml_data = """
        redis:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            RedisMessageBindings.model_validate(data["redis"])

    def test_redis_message_bindings_yaml_empty_validation(self) -> None:
        """Test RedisMessageBindings YAML validation with no fields."""
        yaml_data = """
        redis: {}
        """
        data = yaml.safe_load(yaml_data)
        redis_binding = RedisMessageBindings.model_validate(data["redis"])
        assert redis_binding is not None
