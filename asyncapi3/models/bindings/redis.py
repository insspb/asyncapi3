"""Redis bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "RedisChannelBindings",
    "RedisMessageBindings",
    "RedisOperationBindings",
    "RedisServerBindings",
]

from pydantic import BaseModel, ConfigDict


class RedisServerBindings(BaseModel):
    """
    Redis Server Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(extra="forbid")


class RedisChannelBindings(BaseModel):
    """
    Redis Channel Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(extra="forbid")


class RedisOperationBindings(BaseModel):
    """
    Redis Operation Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(extra="forbid")


class RedisMessageBindings(BaseModel):
    """
    Redis Message Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(extra="forbid")
