"""Tests for helper functions."""

from typing import Any

import pytest

from pydantic import BaseModel, TypeAdapter, ValidationError

from asyncapi3.models.helpers import (
    UNSET,
    EmailStr,
    is_null,
    update_object_attributes,
    validate_patterned_key,
)


class TestIsNull:
    """Tests for is_null function."""

    def test_is_null_with_none(self) -> None:
        """Test is_null returns True for None."""
        assert is_null(None) is True

    @pytest.mark.parametrize(
        "value",
        [
            "",
            0,
            False,
            [],
            {},
            "test",
            42,
        ],
        ids=[
            "empty_string",
            "zero",
            "false_bool",
            "empty_list",
            "empty_dict",
            "string",
            "integer",
        ],
    )
    def test_is_null_with_non_none_values(self, value: Any) -> None:
        """Test is_null returns False for non-None values."""
        assert is_null(value) is False


class TestEmailStr:
    """Tests for EmailStr custom type."""

    def test_emailstr_valid(self) -> None:
        """Test EmailStr accepts valid email addresses."""
        adapter = TypeAdapter(EmailStr)

        valid_emails = [
            "test@example.com",
            "user.name+tag@example.co.uk",
            "test.email@subdomain.example.org",
        ]
        for email in valid_emails:
            result = adapter.validate_python(email)
            assert result == email
            assert isinstance(result, str)

    @pytest.mark.parametrize(
        "invalid_email",
        [
            "invalid-email",
            "test@",
            "@example.com",
            "test@.com",
            "test..email@example.com",
            "test@example",
            "",
        ],
        ids=[
            "no_at_symbol",
            "missing_domain",
            "missing_local_part",
            "dot_after_at",
            "double_dot",
            "no_tld",
            "empty_string",
        ],
    )
    def test_emailstr_invalid(self, invalid_email: str) -> None:
        """Test EmailStr rejects invalid email addresses."""
        adapter = TypeAdapter(EmailStr)

        with pytest.raises(ValidationError, match="Invalid email format"):
            adapter.validate_python(invalid_email)

    def test_emailstr_json_schema(self) -> None:
        """Test EmailStr generates correct JSON schema with email format."""
        # Test direct TypeAdapter schema
        adapter = TypeAdapter(EmailStr)
        schema = adapter.json_schema()
        assert schema == {"type": "string", "format": "email"}

        # Test schema in Pydantic model
        class TestModel(BaseModel):
            email: EmailStr
            optional_email: EmailStr | None = None

        model_schema = TestModel.model_json_schema()

        # Check required email field
        email_property = model_schema["properties"]["email"]
        assert email_property["type"] == "string"
        assert email_property["format"] == "email"

        # Check optional email field
        optional_email_property = model_schema["properties"]["optional_email"]
        assert "anyOf" in optional_email_property
        assert len(optional_email_property["anyOf"]) == 2

        # Find the string schema in anyOf
        string_schema = None
        for item in optional_email_property["anyOf"]:
            if item.get("type") == "string":
                string_schema = item
                break

        assert string_schema is not None
        assert string_schema["type"] == "string"
        assert string_schema["format"] == "email"


class TestValidatePatternedKey:
    """Tests for validate_patterned_key function."""

    @pytest.mark.parametrize(
        "key",
        [
            "valid_key",
            "valid-key",
            "valid123",
            "valid_key_123",
            "a",
            "A",
            "Test123",
            "test_123-456",
        ],
    )
    def test_validate_patterned_key_accepts_valid_keys(self, key: str) -> None:
        """Test validate_patterned_key accepts valid patterned keys."""
        # Should not raise any exception
        validate_patterned_key(key, "test")

    @pytest.mark.parametrize(
        ("key", "expected_error"),
        [
            (
                "invalid@key",
                "Field 'invalid@key' does not match patterned object key pattern. Keys must contain letters, digits, hyphens, and underscores.",
            ),
            (
                "invalid key",
                "Field 'invalid key' does not match patterned object key pattern. Keys must contain letters, digits, hyphens, and underscores.",
            ),
            (
                "invalid.key",
                "Field 'invalid.key' does not match patterned object key pattern. Keys must contain letters, digits, hyphens, and underscores.",
            ),
            (
                "invalid/key",
                "Field 'invalid/key' does not match patterned object key pattern. Keys must contain letters, digits, hyphens, and underscores.",
            ),
            (
                "invalid#key",
                "Field 'invalid#key' does not match patterned object key pattern. Keys must contain letters, digits, hyphens, and underscores.",
            ),
            (
                "invalid?key",
                "Field 'invalid?key' does not match patterned object key pattern. Keys must contain letters, digits, hyphens, and underscores.",
            ),
            (
                "invalid:key",
                "Field 'invalid:key' does not match patterned object key pattern. Keys must contain letters, digits, hyphens, and underscores.",
            ),
            (
                "",
                "Field '' does not match patterned object key pattern. Keys must contain letters, digits, hyphens, and underscores.",
            ),
        ],
    )
    def test_validate_patterned_key_rejects_invalid_keys(
        self, key: str, expected_error: str
    ) -> None:
        """Test validate_patterned_key rejects invalid patterned keys."""
        with pytest.raises(ValueError) as exc_info:  # noqa: PT011
            validate_patterned_key(key, "test")
        assert str(exc_info.value) == expected_error

    @pytest.mark.parametrize(
        ("key", "expected_error"),
        [
            (
                123,
                "Key '123' must be a string, got int",
            ),
            (
                42.5,
                "Key '42.5' must be a string, got float",
            ),
            (
                True,
                "Key 'True' must be a string, got bool",
            ),
            (
                False,
                "Key 'False' must be a string, got bool",
            ),
            (
                ["list"],
                "Key '['list']' must be a string, got list",
            ),
            (
                {"dict": "value"},
                "Key '{'dict': 'value'}' must be a string, got dict",
            ),
            (
                None,
                "Key 'None' must be a string, got NoneType",
            ),
        ],
    )
    def test_validate_patterned_key_rejects_non_string_types(
        self, key: Any, expected_error: str
    ) -> None:
        """Test validate_patterned_key rejects non-string key types with TypeError."""
        with pytest.raises(TypeError) as exc_info:
            validate_patterned_key(key, "test")

        assert str(exc_info.value) == expected_error


class TestUpdateObjectAttributes:
    """Tests for update_object_attributes function."""

    def test_update_object_attributes_updates_provided_values(self) -> None:
        """Test update_object_attributes updates attributes with provided values."""

        class TestModel(BaseModel):
            name: str | None = None
            age: int | None = None
            active: bool | None = None

        obj = TestModel(name="John", age=25)

        result = update_object_attributes(obj, name="Jane", age=30, active=True)

        # Should return the same object
        assert result is obj
        assert result.name == "Jane"
        assert result.age == 30
        assert result.active is True

    def test_update_object_attributes_skips_unset_values(self) -> None:
        """Test update_object_attributes skips UNSET values."""

        class TestModel(BaseModel):
            name: str | None = None
            age: int | None = None
            active: bool | None = None

        obj = TestModel(name="John", age=25, active=False)

        result = update_object_attributes(
            obj,
            name="Jane",
            age=UNSET,  # Should be skipped
            active=UNSET,  # Should be skipped
        )

        # Should return the same object
        assert result is obj
        assert result.name == "Jane"
        assert result.age == 25  # Unchanged
        assert result.active is False  # Unchanged

    def test_update_object_attributes_handles_none_values(self) -> None:
        """Test update_object_attributes handles None values correctly."""

        class TestModel(BaseModel):
            name: str | None = None
            description: str | None = None

        obj = TestModel(name="John", description="Developer")

        result = update_object_attributes(
            obj,
            name=None,  # Explicitly set to None
            description=UNSET,  # Should be skipped
        )

        # Should return the same object
        assert result is obj
        assert result.name is None  # Explicitly set to None
        assert result.description == "Developer"  # Unchanged

    def test_update_object_attributes_with_empty_kwargs(self) -> None:
        """Test update_object_attributes with no arguments."""

        class TestModel(BaseModel):
            name: str = "John"

        obj = TestModel()

        result = update_object_attributes(obj)

        # Should return the same object unchanged
        assert result is obj
        assert result.name == "John"

    def test_update_object_attributes_type_preservation(self) -> None:
        """Test update_object_attributes preserves object type."""

        class TestModel(BaseModel):
            value: str

        obj = TestModel(value="test")
        result = update_object_attributes(obj, value="updated")

        # Should return the same type
        assert isinstance(result, TestModel)
        assert result.value == "updated"
