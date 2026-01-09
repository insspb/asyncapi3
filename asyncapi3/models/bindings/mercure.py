"""Mercure bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "MercureChannelBindings",
    "MercureMessageBindings",
    "MercureOperationBindings",
    "MercureServerBindings",
]

from asyncapi3.models.base_models import NonExtendableBaseModel


class MercureServerBindings(NonExtendableBaseModel):
    """
    Mercure Server Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class MercureChannelBindings(NonExtendableBaseModel):
    """
    Mercure Channel Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class MercureOperationBindings(NonExtendableBaseModel):
    """
    Mercure Operation Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class MercureMessageBindings(NonExtendableBaseModel):
    """
    Mercure Message Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """
