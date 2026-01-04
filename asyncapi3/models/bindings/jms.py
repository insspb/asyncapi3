"""JMS bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "JMSChannelBindings",
    "JMSMessageBindings",
    "JMSOperationBindings",
    "JMSServerBindings",
]

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from asyncapi3.models.base import Reference
from asyncapi3.models.helpers import is_null
from asyncapi3.models.schema import Schema


class JMSServerBindings(BaseModel):
    """
    JMS Server Binding Object.

    The JMS Server Binding Object is defined by a JSON Schema, which defines these
    fields.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
    )

    jms_connection_factory: str = Field(
        alias="jmsConnectionFactory",
        description=(
            "REQUIRED. The classname of the ConnectionFactory implementation for "
            "the JMS Provider."
        ),
    )
    properties: list[Schema] | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "Additional properties to set on the JMS ConnectionFactory implementation "
            "for the JMS Provider."
        ),
    )
    client_id: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="clientID",
        description=(
            "A client identifier for applications that use this JMS connection factory "
            "If the Client ID Policy is set to 'Restricted' (the default), then "
            "configuring a Client ID on the ConnectionFactory prevents more than one "
            "JMS client from using a connection from this factory."
        ),
    )
    binding_version: str = Field(
        default="0.0.1",
        alias="bindingVersion",
        description="The version of this binding. Optional, defaults to latest.",
    )


class JMSChannelBindings(BaseModel):
    """
    JMS Channel Binding Object.

    The JMS Channel Binding Object is defined by a JSON Schema, which defines these
    fields.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
    )

    destination: str | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "The destination (queue) name for this channel. SHOULD only be specified "
            "if the channel name differs from the actual destination name, such as "
            "when the channel name is not a valid destination name according to the "
            "JMS Provider. Optional, defaults to the channel name."
        ),
    )
    destination_type: Literal["queue", "fifo-queue"] | None = Field(
        default=None,
        exclude_if=is_null,
        alias="destinationType",
        description=(
            "The type of destination, which MUST be either queue, or fifo-queue. "
            "SHOULD be specified to document the messaging model (point-to-point, "
            "or strict message ordering) supported by this channel. Optional, defaults "
            "to queue."
        ),
    )
    binding_version: str = Field(
        default="0.0.1",
        alias="bindingVersion",
        description="The version of this binding. Optional, defaults to latest.",
    )


class JMSOperationBindings(BaseModel):
    """
    JMS Operation Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(extra="forbid")


class JMSMessageBindings(BaseModel):
    """
    JMS Message Binding Object.

    The JMS Message Binding Object is defined by a JSON Schema, which defines these
    fields.
    """

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
    )

    headers: Schema | Reference | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "A Schema object containing the definitions for JMS specific headers "
            "(so-called protocol headers). This schema MUST be of type object and "
            "have a properties key. Examples of JMS protocol headers are JMSMessageID, "
            "JMSTimestamp, and JMSCorrelationID."
        ),
    )
    binding_version: str = Field(
        default="0.0.1",
        alias="bindingVersion",
        description="The version of this binding. Optional, defaults to latest.",
    )
