"""Tests for helper functions."""

from typing import Any

import pytest

from asyncapi3.models.helpers import EmailStr, is_null


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
        from pydantic import TypeAdapter

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
        from pydantic import TypeAdapter, ValidationError

        adapter = TypeAdapter(EmailStr)

        with pytest.raises(ValidationError, match="Invalid email format"):
            adapter.validate_python(invalid_email)

    def test_emailstr_json_schema(self) -> None:
        """Test EmailStr generates correct JSON schema with email format."""

        from pydantic import BaseModel, TypeAdapter

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
