"""Tests for AsyncAPI3Builder class."""

from typing import Any

import pytest
import yaml

from pydantic import AnyUrl, HttpUrl
from pytest_mock import MockerFixture

from asyncapi3.builder import AsyncAPI3Builder
from asyncapi3.models.base import Reference
from asyncapi3.models.info import Contact, Info, License
from asyncapi3.models.server import Servers


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

    # Server method tests
    def test_update_or_create_server_creates_new_server(self) -> None:
        """Test update_or_create_server creates a new server when it doesn't exist."""
        builder = AsyncAPI3Builder()

        result = builder.update_or_create_server(
            "test-server",
            host="localhost:5672",
            protocol="amqp",
        )

        assert result is builder  # Should return self for chaining
        # Check server was added to components
        assert "test-server" in builder._components.servers.root
        server = builder._components.servers.root["test-server"]
        assert server.host == "localhost:5672"
        assert server.protocol == "amqp"
        # Check reference was added to root servers
        assert "test-server" in builder._servers.root
        ref = builder._servers.root["test-server"]
        assert ref.ref == "#/components/servers/test-server"

    def test_update_or_create_server_updates_existing_server(self) -> None:
        """Test update_or_create_server updates an existing server."""
        builder = AsyncAPI3Builder()

        # Create initial server
        builder.update_or_create_server(
            "test-server", host="localhost:5672", protocol="amqp"
        )

        # Update some fields
        result = builder.update_or_create_server(
            "test-server", description="Updated description"
        )

        assert result is builder
        server = builder._components.servers.root["test-server"]
        assert server.host == "localhost:5672"  # Should remain unchanged
        assert server.protocol == "amqp"  # Should remain unchanged
        assert server.description == "Updated description"  # Should be updated

    def test_update_or_create_server_requires_host_and_protocol_for_new_server(
        self,
    ) -> None:
        """Test update_or_create_server requires host and protocol for new servers."""
        builder = AsyncAPI3Builder()

        with pytest.raises(ValueError, match="Cannot create new server 'test-server'"):
            builder.update_or_create_server(
                "test-server", description="Test description"
            )

    def test_update_or_create_server_validates_name_pattern(self) -> None:
        """Test update_or_create_server validates server name pattern."""
        builder = AsyncAPI3Builder()

        with pytest.raises(
            ValueError,
            match="Field 'invalid@name' does not match patterned object key pattern",
        ):
            builder.update_or_create_server(
                "invalid@name", host="localhost:5672", protocol="amqp"
            )

    def test_update_or_create_server_with_is_root_server_false(self) -> None:
        """Test update_or_create_server with is_root_server=False doesn't add to root servers."""
        builder = AsyncAPI3Builder()

        builder.update_or_create_server(
            "test-server", host="localhost:5672", protocol="amqp", is_root_server=False
        )

        # Server should be in components
        assert "test-server" in builder._components.servers.root
        # But not in root servers
        assert "test-server" not in builder._servers.root

    def test_update_or_create_server_fails_if_server_stored_as_reference(self) -> None:
        """Test update_or_create_server raises TypeError if server is stored as Reference."""

        # Manually put a Reference in components.servers (simulating edge case)
        builder = AsyncAPI3Builder()
        builder._components.servers = Servers({})
        builder._components.servers["bad-server"] = Reference.to_component_server_name(
            "some-other-server"
        )

        # Try to update - should raise TypeError
        with pytest.raises(
            TypeError, match="The server with name 'bad-server' is stored as reference"
        ):
            builder.update_or_create_server(
                "bad-server", host="localhost:5672", protocol="amqp"
            )

    def test_remove_root_server_removes_reference(self) -> None:
        """Test remove_root_server removes server reference from root servers."""
        builder = AsyncAPI3Builder()

        # Add server
        builder.update_or_create_server(
            "test-server", host="localhost:5672", protocol="amqp"
        )

        # Remove from root servers
        result = builder.remove_root_server("test-server")

        assert result is builder
        # Reference should be removed from root servers
        assert "test-server" not in builder._servers.root
        # But server should remain in components
        assert "test-server" in builder._components.servers.root

    def test_remove_root_server_validates_name_pattern(self) -> None:
        """Test remove_root_server validates server name pattern."""
        builder = AsyncAPI3Builder()

        with pytest.raises(
            ValueError,
            match="Field 'invalid@name' does not match patterned object key pattern",
        ):
            builder.remove_root_server("invalid@name")

    def test_remove_root_server_with_cascade_removes_from_components(self) -> None:
        """Test remove_root_server with cascade=True removes from both places."""
        builder = AsyncAPI3Builder()

        # Add server
        builder.update_or_create_server(
            "test-server", host="localhost:5672", protocol="amqp"
        )

        # Remove with cascade
        result = builder.remove_root_server("test-server", cascade=True)

        assert result is builder
        # Should be removed from both places
        assert "test-server" not in builder._servers.root
        assert "test-server" not in builder._components.servers.root

    def test_add_root_server_as_ref_success(self) -> None:
        """Test add_root_server_as_ref successfully adds reference when server exists."""
        builder = AsyncAPI3Builder()

        # Add server to components only (without adding to root servers)
        builder.update_or_create_server(
            "test-server", host="localhost:5672", protocol="amqp", is_root_server=False
        )

        # Add reference to root servers
        result = builder.add_root_server_as_ref("test-server")

        assert result is builder  # Should return self for chaining
        # Server should be in components
        assert "test-server" in builder._components.servers.root
        # Reference should be added to root servers
        assert "test-server" in builder._servers.root
        ref = builder._servers.root["test-server"]
        assert ref.ref == "#/components/servers/test-server"

    def test_add_root_server_as_ref_server_not_exists(self) -> None:
        """Test add_root_server_as_ref raises ValueError when server doesn't exist in components."""
        builder = AsyncAPI3Builder()

        with pytest.raises(
            ValueError,
            match=(
                r"Cannot add server 'nonexistent-server' to root servers: "
                r"server does not exist in components\.servers\. "
                r"Add the server first using update_or_create_server\(\)\."
            ),
        ):
            builder.add_root_server_as_ref("nonexistent-server")

    def test_add_root_server_as_ref_invalid_name_pattern(self) -> None:
        """Test add_root_server_as_ref validates server name pattern."""
        builder = AsyncAPI3Builder()

        with pytest.raises(
            ValueError,
            match="Field 'invalid@name' does not match patterned object key pattern",
        ):
            builder.add_root_server_as_ref("invalid@name")
