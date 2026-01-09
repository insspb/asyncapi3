"""Redis bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "RedisChannelBindings",
    "RedisMessageBindings",
    "RedisOperationBindings",
    "RedisServerBindings",
]

from asyncapi3.models.base_models import NonExtendableBaseModel


class RedisServerBindings(NonExtendableBaseModel):
    """
    Redis Server Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class RedisChannelBindings(NonExtendableBaseModel):
    """
    Redis Channel Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class RedisOperationBindings(NonExtendableBaseModel):
    """
    Redis Operation Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """


class RedisMessageBindings(NonExtendableBaseModel):
    """
    Redis Message Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """
