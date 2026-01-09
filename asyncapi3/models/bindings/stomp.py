"""STOMP bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "STOMPChannelBindings",
    "STOMPMessageBindings",
    "STOMPOperationBindings",
    "STOMPServerBindings",
]

from asyncapi3.models.base_models import NonExtendableBaseModel


class STOMPServerBindings(NonExtendableBaseModel):
    """
    STOMP Server Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class STOMPChannelBindings(NonExtendableBaseModel):
    """
    STOMP Channel Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class STOMPOperationBindings(NonExtendableBaseModel):
    """
    STOMP Operation Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class STOMPMessageBindings(NonExtendableBaseModel):
    """
    STOMP Message Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """
