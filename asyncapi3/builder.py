"""AsyncAPI 3.0 specification builder.

This module provides a fluent builder pattern for constructing AsyncAPI 3.0
specifications. The AsyncAPI3Builder allows step-by-step construction of AsyncAPI
documents with validation, type safety and simplified usage.
"""

__all__ = ["AsyncAPI3Builder"]


from types import EllipsisType
from typing import Any, NoReturn

import yaml

from pydantic import AnyUrl, HttpUrl, ValidationError

from asyncapi3.models.asyncapi import AsyncAPI3
from asyncapi3.models.base import ExternalDocumentation, Reference, Tags
from asyncapi3.models.bindings import (
    ChannelBindingsObject,
    ServerBindingsObject,
)
from asyncapi3.models.channel import Channel, Channels, Parameters
from asyncapi3.models.components import (
    Components,
)
from asyncapi3.models.helpers import (
    UNSET,
    update_object_attributes,
    validate_patterned_key,
)
from asyncapi3.models.info import Contact, Info, License
from asyncapi3.models.message import Messages
from asyncapi3.models.operation import (
    Operations,
)
from asyncapi3.models.security import SecurityScheme
from asyncapi3.models.server import Server, Servers, ServerVariable


class AsyncAPI3Builder:
    """Builder class for constructing AsyncAPI 3.0 specifications step by step."""

    def __init__(
        self,
        title: str = "Sample APP",
        version: str = "0.0.1",
        description: str | None = None,
        terms_of_service: HttpUrl | str | None = None,
        contact: Contact | None = None,
        license: License | None = None,  # noqa: A002
        tags: Tags | None = None,
        external_docs: ExternalDocumentation | Reference | None = None,
    ) -> None:
        """Initialize the AsyncAPI specification builder with Info parameters.

        Args:
            title: The title of the application.
            version: Provides the version of the application API (not to be confused
                with the specification version).
            description: A short description of the application. CommonMark syntax can
                be used for rich text representation.
            terms_of_service: A URL to the Terms of Service for the API. This MUST be
                in the form of an absolute URL.
            contact: The contact information for the exposed API.
            license: The license information for the exposed API.
            tags: A list of tags for application API documentation control. Tags can be
                used for logical grouping of applications.
            external_docs: Additional external documentation of the exposed API.
        """
        self._id: AnyUrl | None = None
        self._info: Info = Info(
            title=title,
            version=version,
            description=description,
            terms_of_service=terms_of_service,
            contact=contact,
            license=license,
            tags=tags,
            external_docs=external_docs,
        )
        self._servers: Servers = Servers({})
        self._default_content_type: str | None = None
        self._channels: Channels = Channels({})
        self._operations: Operations = Operations({})
        self._components: Components = Components()

    @property
    def spec(self) -> AsyncAPI3:
        """Return the constructed AsyncAPI 3.0 specification object."""
        self.validate()

        return AsyncAPI3(
            id=self._id,
            info=self._info,
            servers=self._servers,
            default_content_type=self._default_content_type,
            channels=self._channels,
            operations=self._operations,
            components=self._components,
        )

    @spec.setter
    def spec(self, value: Any) -> NoReturn:
        """
        Prevent direct setting of spec.

        The AsyncAPI specification object should be constructed step by step
        using the builder methods, not set directly.
        """
        raise AttributeError(
            "Cannot set spec directly. Use builder methods to construct "
            "the AsyncAPI specification step by step."
        )

    def validate(self) -> "AsyncAPI3Builder":
        """Ensure that all required objects are present and valid."""
        # Check that info is provided and is a valid Info object (required field)
        self._validate_info()

        return self

    def _validate_info(self) -> None:
        """Validate that _info is a valid Info object."""
        if self._info is None:
            raise ValueError(
                "Info object is required but not provided, use `.update_info` or "
                "`.replace_info_obj` methods to fix it."
            )
        if not isinstance(self._info, Info):
            raise TypeError(
                f"Info object must be an instance of Info class, got "
                f"{type(self._info).__name__}. Use `.update_info` or "
                f"`.replace_info_obj` methods to set a valid Info object."
            )

    def get_json(self, indent: int | None = None, ensure_ascii: bool = False) -> str:
        """
        Return JSON representation of AsyncAPI 3.0 specification.

        Args:
            indent: Number of spaces for indentation. If None, no indentation is used.
            ensure_ascii: If True, all non-ASCII characters are escaped.

        Returns:
            JSON string representation of the specification.
        """
        return self.spec.model_dump_json(indent=indent, ensure_ascii=ensure_ascii)

    def get_yaml(self) -> str:
        """Return YAML representation of AsyncAPI 3.0 specification."""
        # Convert to dict first, then to YAML
        data = self.spec.model_dump()
        return yaml.dump(
            data,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            Dumper=yaml.SafeDumper,
        )

    # Set/Update/Replace methods for AsyncAPI3 specification components/fields
    def update_default_content_type(
        self, content_type: str | None
    ) -> "AsyncAPI3Builder":
        """
        Update the default content type for the specification.

        Args:
            content_type: The default content type for message payloads. Pass None to
                remove the default content type.

        Returns:
            The builder instance for method chaining.
        """
        self._default_content_type = content_type
        return self

    def update_id(self, id_value: str | None) -> "AsyncAPI3Builder":
        """
        Update the identifier for the AsyncAPI document.

        The identifier must conform to the URI format, according to RFC3986.
        It is RECOMMENDED to use a URN to globally and uniquely identify
        the application during long periods of time.

        Args:
            id_value: The identifier value. Must be a valid URI/URN. Pass None to
                remove the identifier.

        Raises:
            ValidationError: If the id_value is not a valid URI.
        """
        if id_value is None:
            self._id = None
            return self

        try:
            # Validate that id_value is a valid URI
            validated_id = AnyUrl(id_value)
        except ValidationError as e:
            # Re-raise with a more user-friendly message
            raise ValueError(
                f"Invalid ID format: '{id_value}'. ID must conform to URI format "
                f"(RFC3986). "
                f"It is RECOMMENDED to use a URN for global uniqueness. "
                f"Examples: 'urn:ietf:rfc:3986', 'https://example.com/api'"
            ) from e

        self._id = validated_id
        return self

    def update_info(
        self,
        title: str | EllipsisType = UNSET,
        version: str | EllipsisType = UNSET,
        description: str | EllipsisType | None = UNSET,
        terms_of_service: HttpUrl | str | EllipsisType | None = UNSET,
        contact: Contact | EllipsisType | None = UNSET,
        license: License | EllipsisType | None = UNSET,  # noqa: A002
        tags: Tags | EllipsisType | None = UNSET,
        external_docs: ExternalDocumentation | Reference | EllipsisType | None = UNSET,
    ) -> "AsyncAPI3Builder":
        """
        Update the Info object with provided parameters.

        Only the parameters that are explicitly provided (not UNSET) will be updated
        in the existing Info object. To explicitly set a field to None, pass None
        as the value. To leave a field unchanged, omit the parameter or pass UNSET.

        The Info object is initialized with default values in the constructor.

        Args:
            title: The title of the application.
            version: Provides the version of the application API, not to be confused
                with the specification version.
            description: A short description of the application.
                CommonMark syntax can be used for rich text representation.
                Pass None to explicitly remove the description.
            terms_of_service: A URL to the Terms of Service for the API.
                This MUST be in the form of an absolute URL.
                Pass None to explicitly remove the terms of service.
            contact: The contact information for the exposed API.
                Pass None to explicitly remove contact information.
            license: The license information for the exposed API.
                Pass None to explicitly remove license information.
            tags: A list of tags for application API documentation control.
                Tags can be used for logical grouping of applications.
                Pass None to explicitly remove all tags.
            external_docs: Additional external documentation of the exposed API.
                Pass None to explicitly remove external documentation.
        """
        # Validate an info object before attempting to update it
        self._validate_info()

        update_object_attributes(
            self._info,
            title=title,
            version=version,
            description=description,
            terms_of_service=terms_of_service,
            contact=contact,
            license=license,
            tags=tags,
            external_docs=external_docs,
        )

        return self

    def replace_info_obj(self, info: Info) -> "AsyncAPI3Builder":
        """
        Replace the Info object directly.

        Args:
            info: The Info object to set.

        Returns:
            The builder instance for method chaining.

        Raises:
            ValueError: If info is None.
            TypeError: If info is not an instance of an Info class.
        """
        if info is None:
            raise ValueError("Info object cannot be None.")
        if not isinstance(info, Info):
            raise TypeError(
                f"Info object must be an instance of Info class, got "
                f"{type(info).__name__}."
            )
        self._info = info
        return self

    # Server methods
    def update_or_create_server(
        self,
        name: str,
        host: str | EllipsisType = UNSET,
        protocol: str | EllipsisType = UNSET,
        protocol_version: str | EllipsisType | None = UNSET,
        pathname: str | EllipsisType | None = UNSET,
        description: str | EllipsisType | None = UNSET,
        title: str | EllipsisType | None = UNSET,
        summary: str | EllipsisType | None = UNSET,
        variables: dict[str, ServerVariable | Reference] | EllipsisType | None = UNSET,
        security: list[SecurityScheme | Reference] | EllipsisType | None = UNSET,
        tags: Tags | EllipsisType | None = UNSET,
        external_docs: ExternalDocumentation | Reference | EllipsisType | None = UNSET,
        bindings: ServerBindingsObject | Reference | EllipsisType | None = UNSET,
        is_root_server: bool = True,
    ) -> "AsyncAPI3Builder":
        """
        Add a server to the specification or update an existing server.

        If the server doesn't exist in components.servers, it will be created.
        The server is always stored in components.servers as a Server object.
        If is_root_server=True, a Reference to the server will be added to root servers.

        Args:
            name: Server name identifier (key in components.servers and potentially
                servers).
            host: The server host name. Required when creating a new server.
            protocol: The protocol this server supports. Required when creating a new
                server.
            protocol_version: The version of the protocol used for connection.
            pathname: The path to a resource in the host.
            description: An optional string describing the server.
            title: A human-friendly title for the server.
            summary: A short summary of the server.
            variables: A map between a variable name and its value.
            security: A declaration of which security schemes can be used with this
                server.
            tags: A list of tags for logical grouping and categorization of servers.
            external_docs: Additional external documentation for this server.
            bindings: Protocol-specific definitions for the server.
            is_root_server: Whether to add a reference to this server in root servers.

        Raises:
            ValueError: If the server name does not match the required pattern, or if
                host and protocol are not provided when creating a new server.
            TypeError: If attempting to update a server that is stored as a Reference
                object instead of a Server object, or if server name is not a string.
        """
        # Validate name format
        validate_patterned_key(name, "server")

        # Initialize components.servers if not exists
        if self._components.servers is None:
            self._components.servers = Servers({})

        # Check if a server exists in components
        server = self._components.servers.root.get(name)

        # For new servers, require host and protocol
        if server is None:
            if host is UNSET or protocol is UNSET:
                raise ValueError(
                    f"Cannot create new server '{name}': both 'host' and 'protocol' "
                    "are required when creating a server for the first time."
                )
            # Create a new server
            server = Server(host=host, protocol=protocol)

        if isinstance(server, Reference):
            raise TypeError(
                f"The server with name '{name}' is stored as reference. "
                "Cannot update a server reference, delete reference first."
            )

        # Update provided fields
        update_object_attributes(
            server,
            host=host,
            protocol=protocol,
            protocol_version=protocol_version,
            pathname=pathname,
            description=description,
            title=title,
            summary=summary,
            variables=variables,
            security=security,
            tags=tags,
            external_docs=external_docs,
            bindings=bindings,
        )

        # Always store/update in components.servers
        self._components.servers[name] = server

        # Add/remove reference in root servers
        if is_root_server:
            self.add_root_server_as_ref(name)
        else:
            self.remove_root_server(name)

        return self

    def add_root_server_as_ref(self, name: str) -> "AsyncAPI3Builder":
        """
        Add reference to components server to root servers.

        The server must already exist in components.servers. This method only adds
        a reference to it in the root servers section.

        Args:
            name: Server name to add to root servers. Must exist in components.servers.

        Raises:
            ValueError: If the server name does not match the required pattern, or if
                the server does not exist in components.servers.
            TypeError: If server name is not a string.
        """
        # Validate name format
        validate_patterned_key(name, "server")

        # Check if server exists in components
        if self._components.servers is None or name not in self._components.servers:
            raise ValueError(
                f"Cannot add server '{name}' to root servers: "
                "server does not exist in components.servers. "
                "Add the server first using update_or_create_server()."
            )

        # Add reference to root servers
        self._servers[name] = Reference.to_component_server_name(name)

        return self

    def remove_root_server(
        self,
        name: str,
        cascade: bool = False,
    ) -> "AsyncAPI3Builder":
        """
        Remove a server reference from root servers.

        Args:
            name: Server name to remove from root servers.
            cascade: If True, also remove the server from components.servers.

        Raises:
            ValueError: If the server name does not match the required pattern.
            TypeError: If server name is not a string.
        """
        # Validate name format
        validate_patterned_key(name, "server")

        if name in self._servers:
            del self._servers[name]

        if (
            cascade
            and self._components.servers is not None
            and name in self._components.servers
        ):
            del self._components.servers[name]

        return self

    # Channel methods
    def update_or_create_channel(
        self,
        name: str,
        address: str | EllipsisType | None = UNSET,
        title: str | EllipsisType | None = UNSET,
        summary: str | EllipsisType | None = UNSET,
        description: str | EllipsisType | None = UNSET,
        servers: list[Reference] | EllipsisType | None = UNSET,
        parameters: Parameters | EllipsisType | None = UNSET,
        tags: Tags | EllipsisType | None = UNSET,
        external_docs: ExternalDocumentation | Reference | EllipsisType | None = UNSET,
        bindings: ChannelBindingsObject | Reference | EllipsisType | None = UNSET,
        messages: Messages | EllipsisType | None = UNSET,
        is_root_channel: bool = True,
    ) -> "AsyncAPI3Builder":
        """
        Add a channel to the specification or update an existing channel.

        If the channel doesn't exist in components.channels, it will be created.
        The channel is always stored in components.channels as a Channel object.
        If is_root_channel=True, a Reference to the channel will be added to root
        channels.

        Args:
            name: Channel name identifier (key in components.channels and potentially
                channels).
            address: An optional string representation of this channel's address.
                The address is typically the 'topic name', 'routing key', 'event type',
                or 'path'.
            title: A human-friendly title for the channel.
            summary: A short summary of the channel.
            description: An optional description of this channel. CommonMark syntax
                can be used for rich text representation.
            servers: An array of $ref pointers to the definition of the servers in which
                this channel is available. If the channel is located in the root
                Channels Object, it MUST point to a subset of server definitions
                located in the root Servers Object, and MUST NOT point to a subset of
                server definitions located in the Components Object or anywhere else.
                If the channel is located in the Components Object, it MAY point to
                Server Objects in any location.
            parameters: A map of the parameters included in the channel address. It
                MUST be present only when the address contains Channel Address
                Expressions.
            tags: A list of tags for logical grouping of channels.
            external_docs: Additional external documentation for this channel.
            bindings: A map where the keys describe the name of the protocol and the
                values describe protocol-specific definitions for the channel.
            messages: A map of the messages that will be sent to this channel by any
                application at any time.
            is_root_channel: Whether to add a reference to this channel in root
                channels.

        Raises:
            ValueError: If the channel name does not match the required pattern, or if
                address is not provided when creating a new channel.
            TypeError: If attempting to update a channel that is stored as a Reference
                object instead of a Channel object, or if channel name is not a string.
        """
        # Validate name format
        validate_patterned_key(name, "channel")

        # Initialize components.channels if not exists
        if self._components.channels is None:
            self._components.channels = Channels({})

        # Check if a channel exists in components
        channel = self._components.channels.root.get(name)

        # New channel
        if channel is None:
            channel = Channel()

        if isinstance(channel, Reference):
            raise TypeError(
                f"The channel with name '{name}' is stored as reference. "
                "Cannot update a channel reference, delete reference first."
            )

        # Update provided fields
        update_object_attributes(
            channel,
            address=address,
            title=title,
            summary=summary,
            description=description,
            servers=servers,
            parameters=parameters,
            tags=tags,
            external_docs=external_docs,
            bindings=bindings,
            messages=messages,
        )

        # Always store/update in components.channels
        self._components.channels[name] = channel

        # Add/remove reference in root channels
        if is_root_channel:
            self.add_root_channel_as_ref(name)
        else:
            self.remove_root_channel(name)

        return self

    def add_root_channel_as_ref(self, name: str) -> "AsyncAPI3Builder":
        """
        Add reference to components channel to root channels.

        The channel must already exist in components.channels. This method only adds
        a reference to it in the root channels section.

        Args:
            name: Channel name to add to root channels. Must exist in
                components.channels.

        Raises:
            ValueError: If the channel name does not match the required pattern, or if
                the channel does not exist in components.channels.
            TypeError: If channel name is not a string.
        """
        # Validate name format
        validate_patterned_key(name, "channel")

        # Check if channel exists in components
        if self._components.channels is None or name not in self._components.channels:
            raise ValueError(
                f"Cannot add channel '{name}' to root channels: "
                "channel does not exist in components.channels. "
                "Add the channel first using update_or_create_channel()."
            )

        # Add reference to root channels
        self._channels[name] = Reference.to_root_channel_name(name)

        return self

    def remove_root_channel(
        self,
        name: str,
        cascade: bool = False,
    ) -> "AsyncAPI3Builder":
        """
        Remove a channel reference from root channels.

        Args:
            name: Channel name to remove from root channels.
            cascade: If True, also remove the channel from components.channels.

        Raises:
            ValueError: If the channel name does not match the required pattern.
            TypeError: If channel name is not a string.
        """
        # Validate name format
        validate_patterned_key(name, "channel")

        if name in self._channels:
            del self._channels[name]

        if (
            cascade
            and self._components.channels is not None
            and name in self._components.channels
        ):
            del self._components.channels[name]

        return self
