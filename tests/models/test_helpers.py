"""Tests for helper functions."""

from typing import Any

import pytest

from asyncapi3.models.helpers import is_null


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
