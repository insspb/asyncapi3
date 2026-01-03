"""AMQP 1.0 bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "AMQP1ChannelBindings",
    "AMQP1MessageBindings",
    "AMQP1OperationBindings",
    "AMQP1ServerBindings",
]

from pydantic import BaseModel, ConfigDict


class AMQP1ServerBindings(BaseModel):
    """
    AMQP 1.0 Server Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(extra="forbid")


class AMQP1ChannelBindings(BaseModel):
    """
    AMQP 1.0 Channel Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(extra="forbid")


class AMQP1OperationBindings(BaseModel):
    """
    AMQP 1.0 Operation Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(extra="forbid")


class AMQP1MessageBindings(BaseModel):
    """
    AMQP 1.0 Message Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(extra="forbid")
