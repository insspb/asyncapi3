"""AsyncAPI 3.0 specification builder.

This module provides a fluent builder pattern for constructing AsyncAPI 3.0
specifications. The AsyncAPI3Builder allows step-by-step construction of AsyncAPI
documents with validation, type safety and simplified usage.
"""

__all__ = ["AsyncAPI3Builder"]

from types import EllipsisType
from typing import Any, NoReturn

import yaml

from pydantic import AnyUrl, HttpUrl, ValidationError

from asyncapi3.models.asyncapi import AsyncAPI3
from asyncapi3.models.base import ExternalDocumentation, Reference, Tags
from asyncapi3.models.channel import Channels
from asyncapi3.models.components import (
    Components,
)
from asyncapi3.models.helpers import UNSET, update_object_attributes
from asyncapi3.models.info import Contact, Info, License
from asyncapi3.models.operation import (
    Operations,
)
from asyncapi3.models.server import Servers


class AsyncAPI3Builder:
    """Builder class for constructing AsyncAPI 3.0 specifications step by step."""

    def __init__(
        self,
        title: str = "Sample APP",
        version: str = "0.0.1",
        description: str | None = None,
        terms_of_service: HttpUrl | str | None = None,
        contact: Contact | None = None,
        license: License | None = None,  # noqa: A002
        tags: Tags | None = None,
        external_docs: ExternalDocumentation | Reference | None = None,
    ) -> None:
        """Initialize the AsyncAPI specification builder with Info parameters.

        Args:
            title: The title of the application.
            version: Provides the version of the application API (not to be confused
                with the specification version).
            description: A short description of the application. CommonMark syntax can
                be used for rich text representation.
            terms_of_service: A URL to the Terms of Service for the API. This MUST be
                in the form of an absolute URL.
            contact: The contact information for the exposed API.
            license: The license information for the exposed API.
            tags: A list of tags for application API documentation control. Tags can be
                used for logical grouping of applications.
            external_docs: Additional external documentation of the exposed API.
        """
        self._id: AnyUrl | None = None
        self._info: Info = Info(
            title=title,
            version=version,
            description=description,
            terms_of_service=terms_of_service,
            contact=contact,
            license=license,
            tags=tags,
            external_docs=external_docs,
        )
        self._servers: Servers = Servers({})
        self._default_content_type: str | None = None
        self._channels: Channels = Channels({})
        self._operations: Operations = Operations({})
        self._components: Components = Components()

    @property
    def spec(self) -> AsyncAPI3:
        """Return the constructed AsyncAPI 3.0 specification object."""
        self.validate()

        return AsyncAPI3(
            id=self._id,
            info=self._info,
            servers=self._servers,
            default_content_type=self._default_content_type,
            channels=self._channels,
            operations=self._operations,
            components=self._components,
        )

    @spec.setter
    def spec(self, value: Any) -> NoReturn:
        """
        Prevent direct setting of spec.

        The AsyncAPI specification object should be constructed step by step
        using the builder methods, not set directly.
        """
        raise AttributeError(
            "Cannot set spec directly. Use builder methods to construct "
            "the AsyncAPI specification step by step."
        )

    def validate(self) -> "AsyncAPI3Builder":
        """Ensure that all required objects are present and valid."""
        # Check that info is provided and is a valid Info object (required field)
        self._validate_info()

        return self

    def _validate_info(self) -> None:
        """Validate that _info is a valid Info object."""
        if self._info is None:
            raise ValueError(
                "Info object is required but not provided, use `.update_info` or "
                "`.replace_info_obj` methods to fix it."
            )
        if not isinstance(self._info, Info):
            raise TypeError(
                f"Info object must be an instance of Info class, got "
                f"{type(self._info).__name__}. Use `.update_info` or "
                f"`.replace_info_obj` methods to set a valid Info object."
            )

    def get_json(self, indent: int | None = None, ensure_ascii: bool = False) -> str:
        """
        Return JSON representation of AsyncAPI 3.0 specification.

        Args:
            indent: Number of spaces for indentation. If None, no indentation is used.
            ensure_ascii: If True, all non-ASCII characters are escaped.

        Returns:
            JSON string representation of the specification.
        """
        return self.spec.model_dump_json(indent=indent, ensure_ascii=ensure_ascii)

    def get_yaml(self) -> str:
        """Return YAML representation of AsyncAPI 3.0 specification."""
        # Convert to dict first, then to YAML
        data = self.spec.model_dump()
        return yaml.dump(
            data,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            Dumper=yaml.SafeDumper,
        )

    # Set/Update/Replace methods for AsyncAPI3 specification components/fields
    def update_default_content_type(
        self, content_type: str | None
    ) -> "AsyncAPI3Builder":
        """
        Update the default content type for the specification.

        Args:
            content_type: The default content type for message payloads. Pass None to
                remove the default content type.

        Returns:
            The builder instance for method chaining.
        """
        self._default_content_type = content_type
        return self

    def update_id(self, id_value: str | None) -> "AsyncAPI3Builder":
        """
        Update the identifier for the AsyncAPI document.

        The identifier must conform to the URI format, according to RFC3986.
        It is RECOMMENDED to use a URN to globally and uniquely identify
        the application during long periods of time.

        Args:
            id_value: The identifier value. Must be a valid URI/URN. Pass None to
                remove the identifier.

        Raises:
            ValidationError: If the id_value is not a valid URI.
        """
        if id_value is None:
            self._id = None
            return self

        try:
            # Validate that id_value is a valid URI
            validated_id = AnyUrl(id_value)
        except ValidationError as e:
            # Re-raise with a more user-friendly message
            raise ValueError(
                f"Invalid ID format: '{id_value}'. ID must conform to URI format "
                f"(RFC3986). "
                f"It is RECOMMENDED to use a URN for global uniqueness. "
                f"Examples: 'urn:ietf:rfc:3986', 'https://example.com/api'"
            ) from e

        self._id = validated_id
        return self

    def update_info(
        self,
        title: str | EllipsisType = UNSET,
        version: str | EllipsisType = UNSET,
        description: str | EllipsisType | None = UNSET,
        terms_of_service: HttpUrl | str | EllipsisType | None = UNSET,
        contact: Contact | EllipsisType | None = UNSET,
        license: License | EllipsisType | None = UNSET,  # noqa: A002
        tags: Tags | EllipsisType | None = UNSET,
        external_docs: ExternalDocumentation | Reference | EllipsisType | None = UNSET,
    ) -> "AsyncAPI3Builder":
        """
        Update the Info object with provided parameters.

        Only the parameters that are explicitly provided (not UNSET) will be updated
        in the existing Info object. To explicitly set a field to None, pass None
        as the value. To leave a field unchanged, omit the parameter or pass UNSET.

        The Info object is initialized with default values in the constructor.

        Args:
            title: The title of the application.
            version: Provides the version of the application API, not to be confused
                with the specification version.
            description: A short description of the application.
                CommonMark syntax can be used for rich text representation.
                Pass None to explicitly remove the description.
            terms_of_service: A URL to the Terms of Service for the API.
                This MUST be in the form of an absolute URL.
                Pass None to explicitly remove the terms of service.
            contact: The contact information for the exposed API.
                Pass None to explicitly remove contact information.
            license: The license information for the exposed API.
                Pass None to explicitly remove license information.
            tags: A list of tags for application API documentation control.
                Tags can be used for logical grouping of applications.
                Pass None to explicitly remove all tags.
            external_docs: Additional external documentation of the exposed API.
                Pass None to explicitly remove external documentation.
        """
        # Validate an info object before attempting to update it
        self._validate_info()

        update_object_attributes(
            self._info,
            title=title,
            version=version,
            description=description,
            terms_of_service=terms_of_service,
            contact=contact,
            license=license,
            tags=tags,
            external_docs=external_docs,
        )

        return self

    def replace_info_obj(self, info: Info) -> "AsyncAPI3Builder":
        """
        Replace the Info object directly.

        Args:
            info: The Info object to set.

        Returns:
            The builder instance for method chaining.

        Raises:
            ValueError: If info is None.
            TypeError: If info is not an instance of an Info class.
        """
        if info is None:
            raise ValueError("Info object cannot be None.")
        if not isinstance(info, Info):
            raise TypeError(
                f"Info object must be an instance of Info class, got "
                f"{type(info).__name__}."
            )
        self._info = info
        return self
