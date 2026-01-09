"""Pulsar bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "PulsarChannelBindings",
    "PulsarMessageBindings",
    "PulsarOperationBindings",
    "PulsarRetention",
    "PulsarServerBindings",
]

from typing import Literal

from pydantic import Field

from asyncapi3.models.base_models import NonExtendableBaseModel
from asyncapi3.models.helpers import is_null


class PulsarServerBindings(NonExtendableBaseModel):
    """
    Pulsar Server Binding Object.

    This object contains information about the server representation in Pulsar.
    """

    tenant: str = Field(
        default="public",
        description="The pulsar tenant. If omitted, 'public' MUST be assumed.",
    )
    binding_version: str = Field(
        default="0.1.0",
        alias="bindingVersion",
        description="The version of this binding. If omitted, 'latest' MUST be assumed",
    )


class PulsarRetention(NonExtendableBaseModel):
    """
    Retention Definition Object.

    The Retention Definition Object is used to describe the Pulsar Retention policy.
    """

    time: int | None = Field(
        default=0,
        exclude_if=is_null,
        description="Time given in Minutes.",
    )
    size: int | None = Field(
        default=0,
        exclude_if=is_null,
        description="Size given in MegaBytes.",
    )


class PulsarChannelBindings(NonExtendableBaseModel):
    """
    Pulsar Channel Binding Object.

    This object contains information about the channel representation in Pulsar.
    """

    namespace: str = Field(
        ...,
        description="The namespace the channel is associated with.",
    )
    persistence: Literal["persistent", "non-persistent"] = Field(
        ...,
        description=(
            "Persistence of the topic in Pulsar. It MUST be either persistent or "
            "non-persistent."
        ),
    )
    compaction: int | None = Field(
        default=None,
        exclude_if=is_null,
        description="Topic compaction threshold given in Megabytes.",
    )
    geo_replication: list[str] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="geo-replication",
        description="A list of clusters the topic is replicated to.",
    )
    retention: PulsarRetention | None = Field(
        default=None,
        exclude_if=is_null,
        description="Topic retention policy.",
    )
    ttl: int | None = Field(
        default=None,
        exclude_if=is_null,
        description="Message time-to-live in seconds.",
    )
    deduplication: bool | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Message deduplication. When true, it ensures that each message produced "
            "on Pulsar topics is persisted to disk only once."
        ),
    )
    binding_version: str = Field(
        default="0.1.0",
        alias="bindingVersion",
        description="The version of this binding. If omitted, 'latest' MUST be assumed",
    )


class PulsarOperationBindings(NonExtendableBaseModel):
    """
    Pulsar Operation Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class PulsarMessageBindings(NonExtendableBaseModel):
    """
    Pulsar Message Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """
