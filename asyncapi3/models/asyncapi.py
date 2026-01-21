"""AsyncAPI root model for AsyncAPI 3.0 specification."""

__all__ = ["AsyncAPI3"]

import re

from typing import Any

from pydantic import (
    AnyUrl,
    Field,
    HttpUrl,
    field_validator,
    model_validator,
)
from pydantic.json_schema import SkipJsonSchema

from asyncapi3.managers import (
    ChannelMessagesManager,
    ChannelParametersManager,
    ChannelsManager,
    OperationsManager,
    ServersManager,
    TagsManager,
)
from asyncapi3.models.base import ExternalDocumentation, Reference, Tags
from asyncapi3.models.base_models import ExtendableBaseModel
from asyncapi3.models.channel import Channels, Parameters
from asyncapi3.models.components import (
    ChannelBindings,
    Components,
    CorrelationIDs,
    ExternalDocs,
    MessageBindings,
    MessageTraits,
    OperationBindings,
    OperationTraits,
    Replies,
    ReplyAddresses,
    Schemas,
    SecuritySchemes,
    ServerBindings,
    ServerVariables,
)
from asyncapi3.models.components import (
    Tags as TagsDict,
)
from asyncapi3.models.helpers import is_null
from asyncapi3.models.info import Contact, Info, License
from asyncapi3.models.message import Messages
from asyncapi3.models.operation import (
    Operations,
)
from asyncapi3.models.server import Servers
from asyncapi3.protocols import ProcessorProtocol
from asyncapi3.validators import (
    ChannelBindingsRefValidator,
    ChannelsRefValidator,
    CorrelationIdsRefValidator,
    ExternalDocsRefValidator,
    MessageBindingsRefValidator,
    MessagesRefValidator,
    MessageTraitsRefValidator,
    OperationBindingsRefValidator,
    OperationsRefValidator,
    OperationTraitsRefValidator,
    ParametersRefValidator,
    RepliesRefValidator,
    ReplyAddressesRefValidator,
    SchemasRefValidator,
    SecuritySchemesRefValidator,
    ServerBindingsRefValidator,
    ServersRefValidator,
    ServerVariablesRefValidator,
    TagsRefValidator,
)


class AsyncAPI3(ExtendableBaseModel):
    """
    AsyncAPI Object.

    This is the root document object for the AsyncAPI 3.0 specification.
    It combines resource listing and API declaration into one document.

    This object MAY be extended with Specification Extensions.
    """

    asyncapi: str = Field(
        default="3.0.0",
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
    id: AnyUrl | None = Field(
        default=None,
        exclude_if=is_null,
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
    servers: Servers | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "The Servers Object is a map of Server Objects. Provides connection "
            "details of servers."
        ),
    )
    default_content_type: str | None = Field(
        default=None,
        exclude_if=is_null,
        alias="defaultContentType",
        description=(
            "Default content type to use when encoding/decoding a message's payload."
        ),
    )
    channels: Channels | None = Field(
        default=None,
        exclude_if=is_null,
        description="The channels used by this application.",
    )
    operations: Operations | None = Field(
        default=None,
        exclude_if=is_null,
        description="The operations this application MUST implement.",
    )
    components: Components | None = Field(
        default=None,
        exclude_if=is_null,
        description=(
            "An element to hold various reusable objects for the specification. "
            "Everything that is defined inside this object represents a resource "
            "that MAY or MAY NOT be used in the rest of the document and MAY or "
            "MAY NOT be used by the implemented Application."
        ),
    )
    extra_converters: SkipJsonSchema[list[type[ProcessorProtocol]] | None] = Field(
        default=None,
        exclude=True,
        description=(
            "List of managers that can be used to convert specific fields in the "
            "AsyncAPI model. Usually such converters require cross-model references. "
            "Applied after basic types validation, but before `extra_validators`."
        ),
    )
    extra_validators: SkipJsonSchema[list[type[ProcessorProtocol]] | None] = Field(
        default=None,
        exclude=True,
        description=(
            "List of processors that can be used to validate specific fields in the "
            "AsyncAPI model. Usually such processors require cross-model references. "
            "Applied after model validation and `extra_converters`."
        ),
    )

    @classmethod
    def as_builder(
        cls,
        /,
        title: str = "Sample APP",
        version: str = "0.0.1",
        description: str | None = None,
        terms_of_service: HttpUrl | str | None = None,
        contact: Contact | None = None,
        license: License | None = None,  # noqa: A002
        tags: Tags | None = None,
        external_docs: ExternalDocumentation | Reference | None = None,
        **kwargs: Any,
    ) -> "AsyncAPI3":
        """
        Create an AsyncAPI3 instance with default parameters for simplified object
        building.

        This method provides a convenient way to create an AsyncAPI specification with
        default values for common fields, while allowing customization of key metadata.
        All collection fields (servers, channels, operations, components) are
        initialized as empty collections, providing a clean starting point for
        specification building.

        Args:
            title: The title of the application (defaults to "Sample APP")
            version: The version of the API (defaults to "0.0.1")
            description: A description of the application
            terms_of_service: A URL to the Terms of Service for the API
            contact: Contact information for the API
            license: License information for the API
            tags: A list of tags for API documentation
            external_docs: External documentation references
            **kwargs: Additional keyword arguments passed to AsyncAPI3 constructor

        Returns:
            AsyncAPI3: A new AsyncAPI3 instance with default parameters set
        """
        info = Info(
            title=title,
            version=version,
            description=description,
            terms_of_service=terms_of_service,
            contact=contact,
            license=license,
            tags=tags,
            external_docs=external_docs,
        )

        components = Components(
            schemas=Schemas({}),
            servers=Servers({}),
            channels=Channels({}),
            operations=Operations({}),
            messages=Messages({}),
            security_schemes=SecuritySchemes({}),
            server_variables=ServerVariables({}),
            parameters=Parameters({}),
            correlation_ids=CorrelationIDs({}),
            replies=Replies({}),
            reply_addresses=ReplyAddresses({}),
            external_docs=ExternalDocs({}),
            tags=TagsDict({}),
            operation_traits=OperationTraits({}),
            message_traits=MessageTraits({}),
            server_bindings=ServerBindings({}),
            channel_bindings=ChannelBindings({}),
            operation_bindings=OperationBindings({}),
            message_bindings=MessageBindings({}),
        )

        init_params = {
            "info": info,
            "servers": Servers({}),
            "channels": Channels({}),  # list[Reference] -> root.servers
            # operations Reference -> root.channel(condition);
            # operations list[Reference] -> channel.messages(condition)
            "operations": Operations({}),
            "components": components,
            "extra_converters": [
                # Safe to merge values
                TagsManager,  # Only name has meaning
                # Values defined with names (core objects (L1))
                ServersManager,
                ChannelsManager,
                OperationsManager,
                ChannelMessagesManager,
                ChannelParametersManager,
            ],
            "extra_validators": [
                ChannelBindingsRefValidator,
                ChannelsRefValidator,
                CorrelationIdsRefValidator,
                ExternalDocsRefValidator,
                MessageBindingsRefValidator,
                MessagesRefValidator,
                MessageTraitsRefValidator,
                OperationBindingsRefValidator,
                OperationsRefValidator,
                OperationTraitsRefValidator,
                ParametersRefValidator,
                RepliesRefValidator,
                ReplyAddressesRefValidator,
                SchemasRefValidator,
                SecuritySchemesRefValidator,
                ServerBindingsRefValidator,
                ServersRefValidator,
                ServerVariablesRefValidator,
                TagsRefValidator,
            ],
            **kwargs,
        }
        spec = cls(**init_params)

        return spec

    @field_validator("asyncapi")
    @classmethod
    def validate_asyncapi_version(cls, version: str) -> str:
        """Validate AsyncAPI version format (semantic versioning) and compatibility."""
        # Pattern for semantic versioning: major.minor.patch[-suffix]
        pattern = r"^\d+\.\d+\.\d+(-[\w\.\-]+)?$"
        if not re.match(pattern, version):
            raise ValueError(
                "asyncapi must be in semantic versioning format: "
                "major.minor.patch[-suffix]"
            )

        # Check that major version is 3 (this application only supports AsyncAPI 3.x.x)
        major_version = int(version.split(".")[0])
        if major_version != 3:
            raise ValueError(
                f"asyncapi version {version} is not supported. "
                "This application only supports AsyncAPI 3.x.x versions"
            )

        return version

    @model_validator(mode="after")
    def run_extra_processors(self) -> "AsyncAPI3":
        """Run all extra processors after model validation."""
        self._run_extra_converters()
        self._run_extra_validators()
        return self

    def _run_extra_converters(self) -> None:
        """Run extra converters for cross-model optimizations."""
        if self.extra_converters:
            for converter_cls in self.extra_converters:
                processor = converter_cls()
                processor(self)

    def _run_extra_validators(self) -> None:
        """Run extra validators after converters."""
        if self.extra_validators:
            for validator_cls in self.extra_validators:
                processor = validator_cls()
                processor(self)
