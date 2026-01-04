"""STOMP bindings models for AsyncAPI 3.0 specification."""

__all__ = [
    "STOMPChannelBindings",
    "STOMPMessageBindings",
    "STOMPOperationBindings",
    "STOMPServerBindings",
]

from pydantic import BaseModel, ConfigDict


class STOMPServerBindings(BaseModel):
    """
    STOMP Server Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(
        extra="forbid",
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )


class STOMPChannelBindings(BaseModel):
    """
    STOMP Channel Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(
        extra="forbid",
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )


class STOMPOperationBindings(BaseModel):
    """
    STOMP Operation Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(
        extra="forbid",
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )


class STOMPMessageBindings(BaseModel):
    """
    STOMP Message Binding Object.

    This object MUST NOT contain any properties. Its name is reserved for future use.
    """

    model_config = ConfigDict(
        extra="forbid",
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )
