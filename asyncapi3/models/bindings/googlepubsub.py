"""Google Cloud Pub/Sub bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "GooglePubSubChannelBindings",
    "GooglePubSubMessageBindings",
    "GooglePubSubMessageStoragePolicy",
    "GooglePubSubOperationBindings",
    "GooglePubSubSchemaDefinition",
    "GooglePubSubSchemaSettings",
    "GooglePubSubServerBindings",
]

from typing import Any, Literal

from pydantic import Field

from asyncapi3.models.base_models import NonExtendableBaseModel
from asyncapi3.models.helpers import is_null


class GooglePubSubServerBindings(NonExtendableBaseModel):
    """
    Google Cloud Pub/Sub Server Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class GooglePubSubMessageStoragePolicy(NonExtendableBaseModel):
    """
    Google Cloud Pub/Sub Message Storage Policy Object.

    Policy constraining the set of Google Cloud Platform regions where messages
    published to the topic may be stored.
    """

    allowed_persistence_regions: list[str] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="allowedPersistenceRegions",
        description=(
            "A list of IDs of GCP regions where messages that are published to the "
            "topic may be persisted in storage."
        ),
    )


class GooglePubSubSchemaSettings(NonExtendableBaseModel):
    """
    Google Cloud Pub/Sub Schema Settings Object.

    Settings for validating messages published against a schema.
    """

    encoding: (
        Literal[
            "ENCODING_UNSPECIFIED",
            "JSON",
            "BINARY",
        ]
        | None
    ) = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "The encoding of the message. Must be one of the possible Encoding values."
        ),
    )
    first_revision_id: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="firstRevisionId",
        description=(
            "The minimum (inclusive) revision allowed for validating messages."
        ),
    )
    last_revision_id: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="lastRevisionId",
        description=(
            "The maximum (inclusive) revision allowed for validating messages."
        ),
    )
    name: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "The name of the schema that messages published should be validated "
            "against. The format is projects/{project}/schemas/{schema}."
        ),
    )


class GooglePubSubChannelBindings(NonExtendableBaseModel):
    """
    Google Cloud Pub/Sub Channel Binding Object.

    The Channel Bindings Object is used to describe the Google Cloud Pub/Sub specific
    Topic details with AsyncAPI.
    """

    binding_version: str = Field(
        default="0.2.0",
        alias="bindingVersion",
        description="The current version is 0.2.0.",
    )
    labels: dict[str, Any] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "An object of key-value pairs. These are used to categorize Cloud "
            "Resources like Cloud Pub/Sub Topics."
        ),
    )
    message_retention_duration: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="messageRetentionDuration",
        description=(
            "Indicates the minimum duration to retain a message after it is published "
            "to the topic. Must be a valid Duration."
        ),
    )
    message_storage_policy: GooglePubSubMessageStoragePolicy | None = Field(
        default=None,
        exclude_if=is_null,
        alias="messageStoragePolicy",
        description=(
            "Policy constraining the set of Google Cloud Platform regions where "
            "messages published to the topic may be stored."
        ),
    )
    schema_settings: GooglePubSubSchemaSettings | None = Field(
        default=None,
        exclude_if=is_null,
        alias="schemaSettings",
        description="Settings for validating messages published against a schema.",
    )


class GooglePubSubOperationBindings(NonExtendableBaseModel):
    """
    Google Cloud Pub/Sub Operation Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class GooglePubSubSchemaDefinition(NonExtendableBaseModel):
    """
    Google Cloud Pub/Sub Schema Definition Object.

    Describes the schema used to validate the payload of this message.
    """

    name: str | None = Field(
        default=None,
        exclude_if=is_null,
        description="The name of the schema.",
    )


class GooglePubSubMessageBindings(NonExtendableBaseModel):
    """
    Google Cloud Pub/Sub Message Binding Object.

    The Message Binding Object is used to describe the Google Cloud Pub/Sub specific
    PubsubMessage details, alongside with pertinent parts of the Google Cloud Pub/Sub
    Schema Object, with AsyncAPI.
    """

    binding_version: str = Field(
        default="0.2.0",
        alias="bindingVersion",
        description="The current version is 0.2.0.",
    )
    attributes: dict[str, Any] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Attributes for this message. If this field is empty, the message must "
            "contain non-empty data. This can be used to filter messages on the "
            "subscription."
        ),
    )
    ordering_key: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="orderingKey",
        description=(
            "If non-empty, identifies related messages for which publish order should "
            "be respected. For more information, see ordering messages."
        ),
    )
    schema: GooglePubSubSchemaDefinition | None = Field(  # type: ignore[assignment]
        default=None,
        exclude_if=is_null,
        description=(
            "Describes the schema used to validate the payload of this message."
        ),
    )
