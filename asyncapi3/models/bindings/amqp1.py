"""AMQP 1.0 bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "AMQP1ChannelBindings",
    "AMQP1MessageBindings",
    "AMQP1OperationBindings",
    "AMQP1ServerBindings",
]

from asyncapi3.models.base_models import NonExtendableBaseModel


class AMQP1ServerBindings(NonExtendableBaseModel):
    """
    AMQP 1.0 Server Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class AMQP1ChannelBindings(NonExtendableBaseModel):
    """
    AMQP 1.0 Channel Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class AMQP1OperationBindings(NonExtendableBaseModel):
    """
    AMQP 1.0 Operation Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class AMQP1MessageBindings(NonExtendableBaseModel):
    """
    AMQP 1.0 Message Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """
