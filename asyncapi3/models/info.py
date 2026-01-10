"""Info models for AsyncAPI 3.0 specification."""

__all__ = ["Contact", "Info", "License"]

from pydantic import Field, HttpUrl

from asyncapi3.models.base import ExternalDocumentation, Reference, Tags
from asyncapi3.models.base_models import ExtendableBaseModel
from asyncapi3.models.helpers import EmailStr, is_null


class Contact(ExtendableBaseModel):
    """
    Contact Object.

    Contact information for the exposed API.
    """

    name: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="The identifying name of the contact person/organization.",
    )
    url: HttpUrl | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "The URL pointing to the contact information. This MUST be in the form "
            "of an absolute URL."
        ),
    )
    email: EmailStr | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "The email address of the contact person/organization. MUST be in the "
            "format of an email address."
        ),
    )


class License(ExtendableBaseModel):
    """
    License Object.

    License information for the exposed API.
    """

    name: str = Field(
        description="The license name used for the API.",
    )
    url: HttpUrl | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A URL to the license used for the API. This MUST be in the form of an "
            "absolute URL."
        ),
    )


class Info(ExtendableBaseModel):
    """
    Info Object.

    The object provides metadata about the API.
    The metadata can be used by the clients if needed.
    """

    title: str = Field(
        description="The title of the application.",
    )
    version: str = Field(
        description=(
            "Provides the version of the application API (not to be confused with "
            "the specification version)."
        ),
    )
    description: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A short description of the application. CommonMark syntax can be used "
            "for rich text representation."
        ),
    )
    terms_of_service: HttpUrl | None = Field(
        default=None,
        exclude_if=is_null,
        alias="termsOfService",
        description=(
            "A URL to the Terms of Service for the API. This MUST be in the form "
            "of an absolute URL."
        ),
    )
    contact: Contact | None = Field(
        default=None,
        exclude_if=is_null,
        description="The contact information for the exposed API.",
    )
    license: License | None = Field(
        default=None,
        exclude_if=is_null,
        description="The license information for the exposed API.",
    )
    tags: Tags | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A list of tags for application API documentation control. Tags can be "
            "used for logical grouping of applications."
        ),
    )
    external_docs: ExternalDocumentation | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="externalDocs",
        description="Additional external documentation of the exposed API.",
    )
