"""Tests for info models."""

from typing import Any

import pytest
import yaml

from pydantic import ValidationError
from pytest_cases import parametrize_with_cases

from asyncapi3.models.base import ExternalDocumentation, Reference, Tag
from asyncapi3.models.info import Contact, Info, License


# Contact Validation Test Cases
def case_contact_full() -> str:
    """Contact with all fields."""
    return """
    name: API Support
    url: https://www.example.com/support
    email: support@example.com
    """


def case_contact_partial() -> str:
    """Contact with partial fields."""
    return """
    name: API Support
    email: support@example.com
    """


# Contact Serialization Test Cases
def case_contact_serialization_empty() -> tuple[Contact, dict]:
    """Contact serialization empty."""
    contact = Contact()
    expected: dict[str, Any] = {}
    return contact, expected


def case_contact_serialization_full() -> tuple[Contact, dict]:
    """Contact serialization with all fields."""
    contact = Contact(
        name="API Support",
        url="https://www.example.com/support",
        email="support@example.com",
    )
    expected: dict[str, Any] = {
        "name": "API Support",
        "url": "https://www.example.com/support",
        "email": "support@example.com",
    }
    return contact, expected


def case_contact_serialization_partial() -> tuple[Contact, dict]:
    """Contact serialization with partial fields."""
    contact = Contact(
        name="API Support",
        email="support@example.com",
    )
    expected: dict[str, Any] = {
        "name": "API Support",
        "email": "support@example.com",
    }
    return contact, expected


# License Validation Test Cases
def case_license_name_only() -> str:
    """License with name only."""
    return """
    name: Apache 2.0
    """


def case_license_full() -> str:
    """License with name and url."""
    return """
    name: Apache 2.0
    url: https://www.apache.org/licenses/LICENSE-2.0.html
    """


# License Serialization Test Cases
def case_license_serialization_name_only() -> tuple[License, dict]:
    """License serialization with name only."""
    license_obj = License(name="Apache 2.0")
    expected: dict[str, Any] = {"name": "Apache 2.0"}
    return license_obj, expected


def case_license_serialization_full() -> tuple[License, dict]:
    """License serialization with name and url."""
    license_obj = License(
        name="Apache 2.0",
        url="https://www.apache.org/licenses/LICENSE-2.0.html",
    )
    expected: dict[str, Any] = {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
    return license_obj, expected


# Info Validation Test Cases
def case_info_minimal() -> str:
    """Info with required fields only."""
    return """
    title: AsyncAPI Sample App
    version: 1.0.1
    """


def case_info_full() -> str:
    """Info with all fields."""
    return """
    title: AsyncAPI Sample App
    version: 1.0.1
    description: This is a sample app.
    termsOfService: https://asyncapi.org/terms/
    contact:
      name: API Support
      url: https://www.asyncapi.org/support
      email: support@asyncapi.org
    license:
      name: Apache 2.0
      url: https://www.apache.org/licenses/LICENSE-2.0.html
    externalDocs:
      description: Find more info here
      url: https://www.asyncapi.org
    tags:
      - name: e-commerce
    """


def case_info_with_defaults() -> str:
    """Info with default values."""
    return """
    title: My App
    version: 2.0.0
    """


# Info Serialization Test Cases
def case_info_serialization_minimal_required() -> tuple[Info, dict]:
    """Info serialization with required fields only."""
    info = Info(title="AsyncAPI Sample App", version="1.0.1")
    expected: dict[str, Any] = {
        "title": "AsyncAPI Sample App",
        "version": "1.0.1",
    }
    return info, expected


def case_info_serialization_minimal() -> tuple[Info, dict]:
    """Info serialization with required fields only."""
    info = Info(title="AsyncAPI Sample App", version="1.0.1")
    expected: dict[str, Any] = {
        "title": "AsyncAPI Sample App",
        "version": "1.0.1",
    }
    return info, expected


def case_info_serialization_with_contact() -> tuple[Info, dict]:
    """Info serialization with contact."""
    info = Info(
        title="My App",
        version="1.0.0",
        contact=Contact(
            name="API Support",
            url="https://www.example.com/support",
            email="support@example.com",
        ),
    )
    expected: dict[str, Any] = {
        "title": "My App",
        "version": "1.0.0",
        "contact": {
            "name": "API Support",
            "url": "https://www.example.com/support",
            "email": "support@example.com",
        },
    }
    return info, expected


def case_info_serialization_with_license() -> tuple[Info, dict]:
    """Info serialization with license."""
    info = Info(
        title="My App",
        version="1.0.0",
        license=License(
            name="Apache 2.0",
            url="https://www.apache.org/licenses/LICENSE-2.0.html",
        ),
    )
    expected: dict[str, Any] = {
        "title": "My App",
        "version": "1.0.0",
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
    }
    return info, expected


def case_info_serialization_with_external_docs() -> tuple[Info, dict]:
    """Info serialization with externalDocs."""
    info = Info(
        title="My App",
        version="1.0.0",
        external_docs=ExternalDocumentation(
            url="https://www.asyncapi.org",
            description="Find more info here",
        ),
    )
    expected: dict[str, Any] = {
        "title": "My App",
        "version": "1.0.0",
        "externalDocs": {
            "url": "https://www.asyncapi.org/",
            "description": "Find more info here",
        },
    }
    return info, expected


def case_info_serialization_with_reference_external_docs() -> tuple[Info, dict]:
    """Info serialization with externalDocs as Reference."""
    info = Info(
        title="My App",
        version="1.0.0",
        external_docs=Reference(ref="#/components/externalDocs/infoDocs"),
    )
    expected: dict[str, Any] = {
        "title": "My App",
        "version": "1.0.0",
        "externalDocs": {
            "$ref": "#/components/externalDocs/infoDocs",
        },
    }
    return info, expected


def case_info_serialization_with_tags() -> tuple[Info, dict]:
    """Info serialization with tags."""
    info = Info(
        title="My App",
        version="1.0.0",
        tags=[
            Tag(name="e-commerce"),
            Tag(name="user", description="User-related messages"),
        ],
    )
    expected: dict[str, Any] = {
        "title": "My App",
        "version": "1.0.0",
        "tags": [
            {"name": "e-commerce"},
            {"name": "user", "description": "User-related messages"},
        ],
    }
    return info, expected


class TestContact:
    """Tests for Contact model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_contact_full, case_contact_partial],
    )
    def test_contact_validation(self, yaml_data: str) -> None:
        """Test Contact model validation."""
        data = yaml.safe_load(yaml_data)
        contact = Contact.model_validate(data)
        assert contact is not None
        assert contact.name == "API Support"

    @parametrize_with_cases(
        "contact,expected",
        cases=[
            case_contact_serialization_empty,
            case_contact_serialization_full,
            case_contact_serialization_partial,
        ],
    )
    def test_contact_serialization(self, contact: Contact, expected: dict) -> None:
        """Test Contact serialization."""
        dumped = contact.model_dump(mode="json")
        assert dumped == expected

    def test_contact_extensions_validation(self) -> None:
        """Test Contact extensions validation."""
        yaml_data = """
        name: API Support
        x-contact-extension: extended info
        """
        data = yaml.safe_load(yaml_data)
        contact = Contact.model_validate(data)

        assert contact.name == "API Support"
        assert contact.model_extra == {"x-contact-extension": "extended info"}

        # Test invalid extension
        yaml_data_invalid = """
        name: API Support
        invalid-extension: value
        """
        data_invalid = yaml.safe_load(yaml_data_invalid)
        with pytest.raises(
            ValueError, match="does not match specification extension pattern"
        ):
            Contact.model_validate(data_invalid)


class TestLicense:
    """Tests for License model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_license_name_only, case_license_full],
    )
    def test_license_validation(self, yaml_data: str) -> None:
        """Test License model validation."""
        data = yaml.safe_load(yaml_data)
        license_obj = License.model_validate(data)
        assert license_obj is not None
        assert license_obj.name == "Apache 2.0"

    @parametrize_with_cases(
        "license_obj,expected",
        cases=[
            case_license_serialization_name_only,
            case_license_serialization_full,
        ],
    )
    def test_license_serialization(self, license_obj: License, expected: dict) -> None:
        """Test License serialization."""
        dumped = license_obj.model_dump(mode="json")
        assert dumped == expected

    def test_license_extensions_validation(self) -> None:
        """Test License extensions validation."""
        yaml_data = """
        name: Apache 2.0
        x-license-extension: extended info
        """
        data = yaml.safe_load(yaml_data)
        license_obj = License.model_validate(data)

        assert license_obj.name == "Apache 2.0"
        assert license_obj.model_extra == {"x-license-extension": "extended info"}

        # Test invalid extension
        yaml_data_invalid = """
        name: Apache 2.0
        invalid-extension: value
        """
        data_invalid = yaml.safe_load(yaml_data_invalid)
        with pytest.raises(
            ValueError, match="does not match specification extension pattern"
        ):
            License.model_validate(data_invalid)


class TestInfo:
    """Tests for Info model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_info_minimal, case_info_full, case_info_with_defaults],
    )
    def test_info_validation(self, yaml_data: str) -> None:
        """Test Info model validation."""
        data = yaml.safe_load(yaml_data)
        info = Info.model_validate(data)
        assert info is not None
        assert info.title == data["title"]
        assert info.version == data["version"]

    @parametrize_with_cases(
        "info,expected",
        cases=[
            case_info_serialization_minimal_required,
            case_info_serialization_minimal,
            case_info_serialization_with_contact,
            case_info_serialization_with_license,
            case_info_serialization_with_external_docs,
            case_info_serialization_with_reference_external_docs,
            case_info_serialization_with_tags,
        ],
    )
    def test_info_serialization(self, info: Info, expected: dict) -> None:
        """Test Info serialization."""
        dumped = info.model_dump(mode="json")
        assert dumped == expected

    def test_info_with_contact_validation(self) -> None:
        """Test Info with contact validation."""
        yaml_data = """
        title: My App
        version: 1.0.0
        contact:
          name: API Support
          url: https://www.example.com/support
          email: support@example.com
        """
        data = yaml.safe_load(yaml_data)
        info = Info.model_validate(data)

        assert info.contact is not None
        assert isinstance(info.contact, Contact)
        assert info.contact.name == "API Support"
        assert str(info.contact.url) == "https://www.example.com/support"
        assert info.contact.email == "support@example.com"

    def test_info_with_license_validation(self) -> None:
        """Test Info with license validation."""
        yaml_data = """
        title: My App
        version: 1.0.0
        license:
          name: Apache 2.0
          url: https://www.apache.org/licenses/LICENSE-2.0.html
        """
        data = yaml.safe_load(yaml_data)
        info = Info.model_validate(data)

        assert info.license is not None
        assert isinstance(info.license, License)
        assert info.license.name == "Apache 2.0"
        assert (
            str(info.license.url) == "https://www.apache.org/licenses/LICENSE-2.0.html"
        )

    def test_info_with_external_docs_validation(self) -> None:
        """Test Info with externalDocs validation."""
        yaml_data = """
        title: My App
        version: 1.0.0
        externalDocs:
          description: Find more info here
          url: https://www.asyncapi.org
        """
        data = yaml.safe_load(yaml_data)
        info = Info.model_validate(data)

        assert info.external_docs is not None
        assert isinstance(info.external_docs, ExternalDocumentation)
        assert str(info.external_docs.url) == "https://www.asyncapi.org/"
        assert info.external_docs.description == "Find more info here"

    def test_info_with_reference_external_docs_validation(self) -> None:
        """Test Info with externalDocs as Reference validation."""
        yaml_data = """
        title: My App
        version: 1.0.0
        externalDocs:
          $ref: '#/components/externalDocs/infoDocs'
        """
        data = yaml.safe_load(yaml_data)
        info = Info.model_validate(data)

        assert info.external_docs is not None
        assert isinstance(info.external_docs, Reference)
        assert info.external_docs.ref == "#/components/externalDocs/infoDocs"

    def test_info_with_tags_validation(self) -> None:
        """Test Info with tags validation."""
        yaml_data = """
        title: My App
        version: 1.0.0
        tags:
          - name: e-commerce
          - name: user
            description: User-related messages
        """
        data = yaml.safe_load(yaml_data)
        info = Info.model_validate(data)

        assert info.tags is not None
        assert len(info.tags) == 2
        assert info.tags[0].name == "e-commerce"
        assert info.tags[1].name == "user"
        assert info.tags[1].description == "User-related messages"

    def test_info_required_fields_validation_error(self) -> None:
        """Test Info validation error when required fields are missing."""
        # Test missing title
        with pytest.raises(ValidationError):
            Info(version="1.0.0")

        # Test missing version
        with pytest.raises(ValidationError):
            Info(title="Test App")

        # Test empty object
        with pytest.raises(ValidationError):
            Info()

    def test_info_extensions_validation(self) -> None:
        """Test Info extensions validation."""
        yaml_data = """
        title: My App
        version: 1.0.0
        x-custom-extension: custom value
        x-another-extension:
          key: value
        """
        data = yaml.safe_load(yaml_data)
        info = Info.model_validate(data)

        assert info.title == "My App"
        assert info.version == "1.0.0"
        assert info.model_extra == {
            "x-custom-extension": "custom value",
            "x-another-extension": {"key": "value"},
        }

        # Test invalid extension name
        yaml_data_invalid = """
        title: My App
        version: 1.0.0
        invalid-extension: value
        """
        data_invalid = yaml.safe_load(yaml_data_invalid)
        with pytest.raises(
            ValueError, match="does not match specification extension pattern"
        ):
            Info.model_validate(data_invalid)

    def test_contact_url_validation(self) -> None:
        """Test Contact URL validation."""
        # Test valid URL
        contact = Contact(name="Test", url="https://example.com")
        assert str(contact.url) == "https://example.com/"

        # Test invalid URL
        with pytest.raises(ValidationError):
            Contact(name="Test", url="not-a-url")

    def test_contact_email_validation(self) -> None:
        """Test Contact email validation."""
        # Test valid email
        contact = Contact(name="Test", email="test@example.com")
        assert contact.email == "test@example.com"

        # Test invalid email
        with pytest.raises(ValidationError, match="Invalid email format"):
            Contact(name="Test", email="not-an-email")

    def test_license_url_validation(self) -> None:
        """Test License URL validation."""
        # Test valid URL
        license_obj = License(name="MIT", url="https://opensource.org/licenses/MIT")
        assert str(license_obj.url) == "https://opensource.org/licenses/MIT"

        # Test invalid URL
        with pytest.raises(ValidationError):
            License(name="MIT", url="not-a-url")

    def test_info_terms_of_service_url_validation(self) -> None:
        """Test Info termsOfService URL validation."""
        # Test valid URL
        info = Info(
            title="Test", version="1.0.0", terms_of_service="https://example.com/terms"
        )
        assert str(info.terms_of_service) == "https://example.com/terms"

        # Test invalid URL
        with pytest.raises(ValidationError):
            Info(title="Test", version="1.0.0", terms_of_service="not-a-url")
