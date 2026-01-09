"""MQTT 5 bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "MQTT5ChannelBindings",
    "MQTT5MessageBindings",
    "MQTT5OperationBindings",
    "MQTT5ServerBindings",
]

from pydantic import Field

from asyncapi3.models.base import Reference
from asyncapi3.models.base_models import NonExtendableBaseModel
from asyncapi3.models.helpers import is_null
from asyncapi3.models.schema import Schema


class MQTT5ServerBindings(NonExtendableBaseModel):
    """
    MQTT 5 Server Binding Object.

    This object contains information about the server representation in MQTT5.

    This object MUST contain only the properties defined below.
    """

    session_expiry_interval: int | Schema | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        alias="sessionExpiryInterval",
        description=(
            "Session Expiry Interval in seconds or a Schema Object containing the "
            "definition of the interval."
        ),
    )
    binding_version: str = Field(
        default="0.2.0",
        alias="bindingVersion",
        description="The version of this binding. If omitted, 'latest' MUST be assumed",
    )


class MQTT5ChannelBindings(NonExtendableBaseModel):
    """
    MQTT 5 Channel Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class MQTT5OperationBindings(NonExtendableBaseModel):
    """
    MQTT 5 Operation Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class MQTT5MessageBindings(NonExtendableBaseModel):
    """
    MQTT 5 Message Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """
