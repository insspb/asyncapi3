"""Tests for AsyncAPI3Builder class."""

from typing import Any

import pytest
import yaml

from pydantic import AnyUrl, HttpUrl
from pytest_mock import MockerFixture

from asyncapi3.builder import AsyncAPI3Builder
from asyncapi3.models.info import Contact, Info, License


class TestAsyncAPI3Builder:
    """Tests for AsyncAPI3Builder class."""

    def test_init_initializes_empty_builder(self) -> None:
        """Test that __init__ initializes all attributes to None/empty."""
        builder = AsyncAPI3Builder()

        assert builder._id is None
        # Info is now initialized with default values
        assert builder._info.title == "Sample APP"
        assert builder._info.version == "0.0.1"
        assert builder._info.description is None
        assert builder._info.terms_of_service is None
        assert builder._info.contact is None
        assert builder._info.license is None
        assert builder._info.tags is None
        assert builder._info.external_docs is None
        # Servers, Channels, Operations are now initialized as empty objects
        assert len(builder._servers.root) == 0
        assert builder._default_content_type is None
        assert len(builder._channels.root) == 0
        assert len(builder._operations.root) == 0
        # Components is now initialized with default values
        assert builder._components.schemas is None

    def test_init_with_info_parameters(self) -> None:
        """Test that __init__ accepts and sets Info parameters."""
        contact = Contact(name="Test Contact", email="test@example.com")
        license_obj = License(name="MIT")

        builder = AsyncAPI3Builder(
            title="Custom Title",
            version="2.0.0",
            description="Custom description",
            terms_of_service="https://example.com/tos",
            contact=contact,
            license=license_obj,
        )

        assert builder._info.title == "Custom Title"
        assert builder._info.version == "2.0.0"
        assert builder._info.description == "Custom description"
        assert builder._info.terms_of_service == HttpUrl("https://example.com/tos")
        assert str(builder._info.terms_of_service) == "https://example.com/tos"
        assert builder._info.contact == contact
        assert builder._info.license == license_obj
        assert builder._info.tags is None
        assert builder._info.external_docs is None

    def test_spec_setter_raises_attribute_error(self) -> None:
        """Test that spec setter raises AttributeError."""
        builder = AsyncAPI3Builder()

        with pytest.raises(AttributeError, match="Cannot set spec directly"):
            builder.spec = None  # type: ignore[assignment]

    @pytest.mark.parametrize("ensure_ascii", [True, False])
    @pytest.mark.parametrize("indent", [None, 2])
    def test_get_json_with_ensure_ascii_parameter(
        self, mocker: MockerFixture, ensure_ascii: bool, indent: int | None
    ) -> None:
        """Test get_json method passes ensure_ascii parameter correctly."""
        builder = AsyncAPI3Builder()
        builder.update_info(title="Test API", version="1.0.0")

        # Mock the spec property to return a mock object
        mock_spec = mocker.Mock()
        mock_spec.model_dump_json.return_value = '{"test": "data"}'
        mocker.patch.object(
            type(builder),
            "spec",
            new_callable=mocker.PropertyMock,
            return_value=mock_spec,
        )

        builder.get_json(ensure_ascii=ensure_ascii, indent=indent)
        mock_spec.model_dump_json.assert_called_with(
            indent=indent, ensure_ascii=ensure_ascii
        )

    def test_get_yaml_uses_safe_dumper(self, mocker: MockerFixture) -> None:
        """Test get_yaml method uses SafeDumper and proper settings."""
        builder = AsyncAPI3Builder()
        builder.update_info(title="Test API", version="1.0.0")

        # Mock yaml.dump to control its return value and check arguments
        mock_yaml_dump = mocker.patch("asyncapi3.builder.yaml.dump")
        mock_yaml_dump.return_value = (
            "asyncapi: 3.0.0\ntitle: Test API\nversion: 1.0.0\n"
        )

        yaml_output = builder.get_yaml()

        # Verify yaml.dump was called with correct arguments
        mock_yaml_dump.assert_called_once()
        args, kwargs = mock_yaml_dump.call_args

        # Check positional arguments
        assert len(args) == 1  # data dict
        assert isinstance(args[0], dict)  # should be the dumped spec data

        # Check keyword arguments
        assert kwargs == {
            "default_flow_style": False,
            "sort_keys": False,
            "allow_unicode": True,
            "Dumper": yaml.SafeDumper,
        }

        # Verify return value
        assert yaml_output == "asyncapi: 3.0.0\ntitle: Test API\nversion: 1.0.0\n"

    def test_replace_info_obj_sets_info_attribute(self) -> None:
        """Test replace_info_obj method sets _info attribute."""
        builder = AsyncAPI3Builder()
        info = Info(title="Test API", version="1.0.0")

        assert builder._info is not info
        result = builder.replace_info_obj(info)

        assert result is builder  # Should return self for chaining
        assert builder._info is info

    def test_replace_info_obj_raises_value_error_for_none(self) -> None:
        """Test replace_info_obj method raises ValueError for None input."""
        builder = AsyncAPI3Builder()

        with pytest.raises(ValueError, match="Info object cannot be None"):
            builder.replace_info_obj(None)  # type: ignore[arg-type]

    def test_replace_info_obj_raises_type_error_for_wrong_type(self) -> None:
        """Test replace_info_obj method raises TypeError for wrong input type."""
        builder = AsyncAPI3Builder()

        with pytest.raises(
            TypeError, match="Info object must be an instance of Info class"
        ):
            builder.replace_info_obj("not an info object")  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        (
            "update_kwargs",
            "expected_title",
            "expected_version",
            "expected_description",
        ),
        [
            ({"title": "Updated Title"}, "Updated Title", "0.0.1", None),
            ({"version": "2.0.0"}, "Sample APP", "2.0.0", None),
            (
                {"description": "New description"},
                "Sample APP",
                "0.0.1",
                "New description",
            ),
            ({"description": None}, "Sample APP", "0.0.1", None),
        ],
    )
    def test_update_info_updates_provided_fields(
        self,
        update_kwargs: dict[str, Any],
        expected_title: str,
        expected_version: str,
        expected_description: str | None,
    ) -> None:
        """Test update_info method updates only provided fields."""
        builder = AsyncAPI3Builder()

        result = builder.update_info(**update_kwargs)

        assert result is builder  # Should return self for chaining
        assert builder._info.title == expected_title
        assert builder._info.version == expected_version
        assert builder._info.description == expected_description

    def test_update_info_leaves_unchanged_fields_unchanged(self) -> None:
        """Test that update_info doesn't change fields that are not provided."""
        builder = AsyncAPI3Builder()

        # Set initial description
        builder.update_info(description="Initial description")
        assert builder._info.description == "Initial description"

        # Update only title, description should remain unchanged
        builder.update_info(title="New Title")
        assert builder._info.title == "New Title"
        assert (
            builder._info.description == "Initial description"
        )  # Should remain unchanged

    def test_update_default_content_type_sets_value(self) -> None:
        """Test update_default_content_type method sets a content type."""
        builder = AsyncAPI3Builder()

        result = builder.update_default_content_type("application/json")

        assert result is builder  # Should return self for chaining
        assert builder._default_content_type == "application/json"

    def test_update_default_content_type_clears_value(self) -> None:
        """Test update_default_content_type method clears default content type with None."""
        builder = AsyncAPI3Builder()

        # First set a value
        builder.update_default_content_type("application/json")
        assert builder._default_content_type == "application/json"

        # Then clear it
        result = builder.update_default_content_type(None)

        assert result is builder  # Should return self for chaining
        assert builder._default_content_type is None

    def test_update_id_sets_id_attribute(self) -> None:
        """Test update_id method sets an ID."""
        builder = AsyncAPI3Builder()
        id_value = "urn:ietf:rfc:3986"

        result = builder.update_id(id_value)

        assert result is builder  # Should return self for chaining
        assert str(builder._id) == id_value
        assert builder._id == AnyUrl(id_value)

    def test_update_id_clears_id_attribute(self) -> None:
        """Test update_id method clears _id attribute with None."""
        builder = AsyncAPI3Builder()
        id_value = "urn:ietf:rfc:3986"

        # First set a value
        builder.update_id(id_value)
        assert builder._id == AnyUrl(id_value)

        # Then clear it
        result = builder.update_id(None)

        assert result is builder  # Should return self for chaining
        assert builder._id is None

    @pytest.mark.parametrize(
        "valid_id",
        [
            "urn:ietf:rfc:3986",
            "https://example.com/api",
            "http://localhost:8080/api",
        ],
        ids=["Valid URN", "Valid URL", "Valid localhost URL"],
    )
    def test_update_id_validates_uri_format(self, valid_id: str) -> None:
        """Test update_id method validates that ID conforms to URI format."""
        builder = AsyncAPI3Builder()

        result = builder.update_id(valid_id)

        assert result is builder
        assert str(builder._id) == valid_id

    @pytest.mark.parametrize(
        "invalid_id",
        [
            "invalid uri with spaces",
            "",
            "not-a-uri",
            "://missing-scheme",
            "http://",
        ],
        ids=["spaces", "empty", "no_scheme", "invalid_scheme", "incomplete_url"],
    )
    def test_update_id_raises_validation_error_for_invalid_uri(
        self, invalid_id: str
    ) -> None:
        """Test update_id method raises ValueError for invalid URI format."""
        builder = AsyncAPI3Builder()

        with pytest.raises(
            ValueError, match=r"Invalid ID format.*must conform to URI format"
        ):
            builder.update_id(invalid_id)

    def test_validate_accepts_valid_info(self) -> None:
        """Test validate method accepts valid Info instance."""
        builder = AsyncAPI3Builder()

        # Should not raise for valid Info
        builder.validate()

    def test_validate_raises_value_error_for_none_info(self) -> None:
        """Test validate method raises ValueError when _info is None."""
        builder = AsyncAPI3Builder()

        # Set _info to None
        builder._info = None  # type: ignore[assignment]

        with pytest.raises(
            ValueError,
            match=(
                r"Info object is required but not provided, use `.update_info` "
                r"or `.replace_info_obj` methods to fix it."
            ),
        ):
            builder.validate()

    def test_validate_raises_type_error_for_invalid_info_type(self) -> None:
        """Test validate method raises TypeError for invalid _info type."""
        builder = AsyncAPI3Builder()

        # Set _info to wrong type
        builder._info = "not an info object"  # type: ignore[assignment]

        with pytest.raises(
            TypeError, match="Info object must be an instance of Info class"
        ):
            builder.validate()

    def test_update_info_calls_validation(self, mocker: MockerFixture) -> None:
        """Test that update_info calls _validate_info method."""
        builder = AsyncAPI3Builder()

        # Mock the _validate_info method to track calls
        mock_validate_info = mocker.patch.object(builder, "_validate_info")

        # Call update_info
        result = builder.update_info(title="Updated Title")

        # Verify _validate_info was called
        mock_validate_info.assert_called_once()

        # Verify return value and update
        assert result is builder
        assert builder._info.title == "Updated Title"

    def test_update_info_explicit_ellipsis_leaves_fields_unchanged(self) -> None:
        """Test that explicitly passing EllipsisType leaves fields unchanged."""
        builder = AsyncAPI3Builder()

        # Set initial values
        builder.update_info(
            title="Initial Title",
            description="Initial Description",
            version="1.0.0",
        )

        # Update with explicit EllipsisType for some fields
        builder.update_info(
            title=...,  # EllipsisType, should not change
            description="Updated Description",  # Should change
            version=...,  # EllipsisType, should not change
        )

        # Verify only description was updated
        assert builder._info.title == "Initial Title"
        assert builder._info.description == "Updated Description"
        assert builder._info.version == "1.0.0"
