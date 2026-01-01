"""AsyncAPI root model for AsyncAPI 3.0 specification."""

__all__ = ["AsyncAPI3"]

from pydantic import BaseModel, Field

from asyncapi3.models.info import Info


class AsyncAPI3(BaseModel):
    """
    AsyncAPI Object.

    This is the root document object for the AsyncAPI 3.0 specification.
    It combines resource listing and API declaration into one document.

    This object MAY be extended with Specification Extensions.
    """

    model_config = {"extra": "allow"}

    asyncapi: str = Field(
        description=(
            "Specifies the AsyncAPI Specification version being used. It can be used "
            "by tooling Specifications and clients to interpret the version. "
            "The structure shall be major.minor.patch, where patch versions must be "
            "compatible with the existing major.minor tooling. Typically patch "
            "versions will be introduced to address errors in the documentation, "
            "and tooling should typically be compatible with the corresponding "
            "major.minor (1.0.*). Patch versions will correspond to patches of this "
            "document."
        ),
    )
    id: str | None = Field(
        default=None,
        description=(
            "Identifier of the application the AsyncAPI document is defining. "
            "This field represents a unique universal identifier of the application "
            "the AsyncAPI document is defining. It must conform to the URI format, "
            "according to RFC3986. It is RECOMMENDED to use a URN to globally and "
            "uniquely identify the application during long periods of time, even "
            "after it becomes unavailable or ceases to exist."
        ),
    )
    info: Info = Field(
        description=(
            "Provides metadata about the API. The metadata can be used by the clients "
            "if needed."
        ),
    )
    # servers: Servers | None = Field(
    #     default=None,
    #     description="Provides connection details of servers.",
    # )
    # default_content_type: str | None = Field(
    #     default=None,
    #     alias="defaultContentType",
    #     description=(
    #         "Default content type to use when encoding/decoding a message's payload."
    #     ),
    # )
    # channels: Channels | None = Field(
    #     default=None,
    #     description="The channels used by this application.",
    # )
    # operations: Operations | None = Field(
    #     default=None,
    #     description="The operations this application MUST implement.",
    # )
    # components: Components | None = Field(
    #     default=None,
    #     description=(
    #         "An element to hold various reusable objects for the specification. "
    #         "Everything that is defined inside this object represents a resource "
    #         "that MAY or MAY NOT be used in the rest of the document and MAY or "
    #         "MAY NOT be used by the implemented Application."
    #     ),
    # )
