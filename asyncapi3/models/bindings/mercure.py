"""Mercure bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "MercureChannelBindings",
    "MercureMessageBindings",
    "MercureOperationBindings",
    "MercureServerBindings",
]

from pydantic import BaseModel, ConfigDict


class MercureServerBindings(BaseModel):
    """
    Mercure Server Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(extra="forbid")


class MercureChannelBindings(BaseModel):
    """
    Mercure Channel Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(extra="forbid")


class MercureOperationBindings(BaseModel):
    """
    Mercure Operation Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(extra="forbid")


class MercureMessageBindings(BaseModel):
    """
    Mercure Message Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(extra="forbid")
