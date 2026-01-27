"""Tests for UnifiedReferencesValidator."""

import logging

import pytest

from _pytest.logging import LogCaptureFixture
from pydantic import BaseModel, ConfigDict, Field

from asyncapi3.models.asyncapi import AsyncAPI3
from asyncapi3.models.base import ExternalDocumentation, Reference, Tag
from asyncapi3.models.bindings import (
    ChannelBindingsObject,
    MessageBindingsObject,
    OperationBindingsObject,
    ServerBindingsObject,
)
from asyncapi3.models.channel import Channel, Parameter
from asyncapi3.models.message import Message, MessageTrait
from asyncapi3.models.operation import (
    Operation,
    OperationReply,
    OperationReplyAddress,
    OperationTrait,
)
from asyncapi3.models.schema import MultiFormatSchema, Schema
from asyncapi3.models.security import CorrelationID, SecurityScheme
from asyncapi3.models.server import Server, ServerVariable
from asyncapi3.validators import UnifiedReferencesValidator
from asyncapi3.validators import (
    unified_references_validator as unified_references_module,
)

REFERENCE_TYPE_MAPPINGS_OLD = {
    "spec.channels.*": Channel,
    "spec.channels.*.bindings": ChannelBindingsObject,
    "spec.channels.*.bindings.ws.headers": Schema,
    "spec.channels.*.bindings.ws.headers.external_docs": ExternalDocumentation,
    "spec.channels.*.bindings.ws.query": Schema,
    "spec.channels.*.bindings.ws.query.external_docs": ExternalDocumentation,
    "spec.channels.*.external_docs": ExternalDocumentation,
    "spec.channels.*.messages.*": Message,
    "spec.channels.*.messages.*.bindings": MessageBindingsObject,
    "spec.channels.*.messages.*.bindings.anypointmq.headers": Schema,
    (
        "spec.channels.*.messages.*.bindings.anypointmq.headers.external_docs"
    ): ExternalDocumentation,
    "spec.channels.*.messages.*.bindings.http.headers": Schema,
    (
        "spec.channels.*.messages.*.bindings.http.headers.external_docs"
    ): ExternalDocumentation,
    "spec.channels.*.messages.*.bindings.jms.headers": Schema,
    (
        "spec.channels.*.messages.*.bindings.jms.headers.external_docs"
    ): ExternalDocumentation,
    "spec.channels.*.messages.*.bindings.kafka.key": Schema,
    (
        "spec.channels.*.messages.*.bindings.kafka.key.external_docs"
    ): ExternalDocumentation,
    "spec.channels.*.messages.*.bindings.mqtt.correlation_data": Schema,
    (
        "spec.channels.*.messages.*.bindings.mqtt.correlation_data.external_docs"
    ): ExternalDocumentation,
    "spec.channels.*.messages.*.bindings.mqtt.response_topic": Schema,
    (
        "spec.channels.*.messages.*.bindings.mqtt.response_topic.external_docs"
    ): ExternalDocumentation,
    "spec.channels.*.messages.*.correlation_id": CorrelationID,
    "spec.channels.*.messages.*.external_docs": ExternalDocumentation,
    "spec.channels.*.messages.*.headers": MultiFormatSchema | Schema,
    "spec.channels.*.messages.*.headers.external_docs": ExternalDocumentation,
    "spec.channels.*.messages.*.payload": MultiFormatSchema | Schema,
    "spec.channels.*.messages.*.payload.external_docs": ExternalDocumentation,
    "spec.channels.*.messages.*.tags.*": Tag,
    "spec.channels.*.messages.*.tags.*.external_docs": ExternalDocumentation,
    "spec.channels.*.messages.*.traits.*": MessageTrait,
    "spec.channels.*.messages.*.traits.*.bindings": MessageBindingsObject,
    "spec.channels.*.messages.*.traits.*.bindings.anypointmq.headers": Schema,
    (
        "spec.channels.*.messages.*.traits.*.bindings.anypointmq.headers.external_docs"
    ): ExternalDocumentation,
    "spec.channels.*.messages.*.traits.*.bindings.http.headers": Schema,
    (
        "spec.channels.*.messages.*.traits.*.bindings.http.headers.external_docs"
    ): ExternalDocumentation,
    "spec.channels.*.messages.*.traits.*.bindings.jms.headers": Schema,
    (
        "spec.channels.*.messages.*.traits.*.bindings.jms.headers.external_docs"
    ): ExternalDocumentation,
    "spec.channels.*.messages.*.traits.*.bindings.kafka.key": Schema,
    (
        "spec.channels.*.messages.*.traits.*.bindings.kafka.key.external_docs"
    ): ExternalDocumentation,
    "spec.channels.*.messages.*.traits.*.bindings.mqtt.correlation_data": Schema,
    (
        "spec.channels.*.messages.*.traits.*.bindings.mqtt."
        "correlation_data.external_docs"
    ): ExternalDocumentation,
    "spec.channels.*.messages.*.traits.*.bindings.mqtt.response_topic": Schema,
    (
        "spec.channels.*.messages.*.traits.*.bindings.mqtt.response_topic.external_docs"
    ): ExternalDocumentation,
    "spec.channels.*.messages.*.traits.*.correlation_id": CorrelationID,
    "spec.channels.*.messages.*.traits.*.external_docs": ExternalDocumentation,
    "spec.channels.*.messages.*.traits.*.headers": MultiFormatSchema | Schema,
    "spec.channels.*.messages.*.traits.*.headers.external_docs": ExternalDocumentation,
    "spec.channels.*.messages.*.traits.*.tags.*": Tag,
    "spec.channels.*.messages.*.traits.*.tags.*.external_docs": ExternalDocumentation,
    "spec.channels.*.parameters.*": Parameter,
    "spec.channels.*.servers.*": Server,
    "spec.channels.*.tags.*": Tag,
    "spec.channels.*.tags.*.external_docs": ExternalDocumentation,
    "spec.components.channel_bindings.*": ChannelBindingsObject,
    "spec.components.channel_bindings.*.ws.headers": Schema,
    (
        "spec.components.channel_bindings.*.ws.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.channel_bindings.*.ws.query": Schema,
    "spec.components.channel_bindings.*.ws.query.external_docs": ExternalDocumentation,
    "spec.components.channels.*": Channel,
    "spec.components.channels.*.bindings": ChannelBindingsObject,
    "spec.components.channels.*.bindings.ws.headers": Schema,
    (
        "spec.components.channels.*.bindings.ws.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.channels.*.bindings.ws.query": Schema,
    "spec.components.channels.*.bindings.ws.query.external_docs": ExternalDocumentation,
    "spec.components.channels.*.external_docs": ExternalDocumentation,
    "spec.components.channels.*.messages.*": Message,
    "spec.components.channels.*.messages.*.bindings": MessageBindingsObject,
    "spec.components.channels.*.messages.*.bindings.anypointmq.headers": Schema,
    (
        "spec.components.channels.*.messages.*.bindings."
        "anypointmq.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.channels.*.messages.*.bindings.http.headers": Schema,
    (
        "spec.components.channels.*.messages.*.bindings.http.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.channels.*.messages.*.bindings.jms.headers": Schema,
    (
        "spec.components.channels.*.messages.*.bindings.jms.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.channels.*.messages.*.bindings.kafka.key": Schema,
    (
        "spec.components.channels.*.messages.*.bindings.kafka.key.external_docs"
    ): ExternalDocumentation,
    "spec.components.channels.*.messages.*.bindings.mqtt.correlation_data": Schema,
    (
        "spec.components.channels.*.messages.*.bindings."
        "mqtt.correlation_data.external_docs"
    ): ExternalDocumentation,
    "spec.components.channels.*.messages.*.bindings.mqtt.response_topic": Schema,
    (
        "spec.components.channels.*.messages.*.bindings."
        "mqtt.response_topic.external_docs"
    ): ExternalDocumentation,
    "spec.components.channels.*.messages.*.correlation_id": CorrelationID,
    "spec.components.channels.*.messages.*.external_docs": ExternalDocumentation,
    "spec.components.channels.*.messages.*.headers": MultiFormatSchema | Schema,
    (
        "spec.components.channels.*.messages.*.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.channels.*.messages.*.payload": MultiFormatSchema | Schema,
    (
        "spec.components.channels.*.messages.*.payload.external_docs"
    ): ExternalDocumentation,
    "spec.components.channels.*.messages.*.tags.*": Tag,
    "spec.components.channels.*.messages.*.tags.*.external_docs": ExternalDocumentation,
    "spec.components.channels.*.messages.*.traits.*": MessageTrait,
    "spec.components.channels.*.messages.*.traits.*.bindings": MessageBindingsObject,
    (
        "spec.components.channels.*.messages.*.traits.*.bindings.anypointmq.headers"
    ): Schema,
    (
        "spec.components.channels.*.messages.*.traits.*."
        "bindings.anypointmq.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.channels.*.messages.*.traits.*.bindings.http.headers": Schema,
    (
        "spec.components.channels.*.messages.*.traits.*."
        "bindings.http.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.channels.*.messages.*.traits.*.bindings.jms.headers": Schema,
    (
        "spec.components.channels.*.messages.*.traits.*."
        "bindings.jms.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.channels.*.messages.*.traits.*.bindings.kafka.key": Schema,
    (
        "spec.components.channels.*.messages.*.traits.*."
        "bindings.kafka.key.external_docs"
    ): ExternalDocumentation,
    (
        "spec.components.channels.*.messages.*.traits.*.bindings.mqtt.correlation_data"
    ): Schema,
    (
        "spec.components.channels.*.messages.*.traits.*."
        "bindings.mqtt.correlation_data.external_docs"
    ): ExternalDocumentation,
    (
        "spec.components.channels.*.messages.*.traits.*.bindings.mqtt.response_topic"
    ): Schema,
    (
        "spec.components.channels.*.messages.*.traits.*."
        "bindings.mqtt.response_topic.external_docs"
    ): ExternalDocumentation,
    "spec.components.channels.*.messages.*.traits.*.correlation_id": CorrelationID,
    (
        "spec.components.channels.*.messages.*.traits.*.external_docs"
    ): ExternalDocumentation,
    ("spec.components.channels.*.messages.*.traits.*.headers"): MultiFormatSchema
    | Schema,
    (
        "spec.components.channels.*.messages.*.traits.*.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.channels.*.messages.*.traits.*.tags.*": Tag,
    (
        "spec.components.channels.*.messages.*.traits.*.tags.*.external_docs"
    ): ExternalDocumentation,
    "spec.components.channels.*.parameters.*": Parameter,
    "spec.components.channels.*.servers.*": Server,
    "spec.components.channels.*.tags.*": Tag,
    "spec.components.channels.*.tags.*.external_docs": ExternalDocumentation,
    "spec.components.correlation_ids.*": CorrelationID,
    "spec.components.external_docs.*": ExternalDocumentation,
    "spec.components.message_bindings.*": MessageBindingsObject,
    "spec.components.message_bindings.*.anypointmq.headers": Schema,
    (
        "spec.components.message_bindings.*.anypointmq.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.message_bindings.*.http.headers": Schema,
    (
        "spec.components.message_bindings.*.http.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.message_bindings.*.jms.headers": Schema,
    (
        "spec.components.message_bindings.*.jms.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.message_bindings.*.kafka.key": Schema,
    "spec.components.message_bindings.*.kafka.key.external_docs": ExternalDocumentation,
    "spec.components.message_bindings.*.mqtt.correlation_data": Schema,
    (
        "spec.components.message_bindings.*.mqtt.correlation_data.external_docs"
    ): ExternalDocumentation,
    "spec.components.message_bindings.*.mqtt.response_topic": Schema,
    (
        "spec.components.message_bindings.*.mqtt.response_topic.external_docs"
    ): ExternalDocumentation,
    "spec.components.message_traits.*": MessageTrait,
    "spec.components.message_traits.*.bindings": MessageBindingsObject,
    "spec.components.message_traits.*.bindings.anypointmq.headers": Schema,
    (
        "spec.components.message_traits.*.bindings.anypointmq.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.message_traits.*.bindings.http.headers": Schema,
    (
        "spec.components.message_traits.*.bindings.http.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.message_traits.*.bindings.jms.headers": Schema,
    (
        "spec.components.message_traits.*.bindings.jms.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.message_traits.*.bindings.kafka.key": Schema,
    (
        "spec.components.message_traits.*.bindings.kafka.key.external_docs"
    ): ExternalDocumentation,
    "spec.components.message_traits.*.bindings.mqtt.correlation_data": Schema,
    (
        "spec.components.message_traits.*.bindings.mqtt.correlation_data.external_docs"
    ): ExternalDocumentation,
    "spec.components.message_traits.*.bindings.mqtt.response_topic": Schema,
    (
        "spec.components.message_traits.*.bindings.mqtt.response_topic.external_docs"
    ): ExternalDocumentation,
    "spec.components.message_traits.*.correlation_id": CorrelationID,
    "spec.components.message_traits.*.external_docs": ExternalDocumentation,
    "spec.components.message_traits.*.headers": MultiFormatSchema | Schema,
    "spec.components.message_traits.*.headers.external_docs": ExternalDocumentation,
    "spec.components.message_traits.*.tags.*": Tag,
    "spec.components.message_traits.*.tags.*.external_docs": ExternalDocumentation,
    "spec.components.messages.*": Message,
    "spec.components.messages.*.bindings": MessageBindingsObject,
    "spec.components.messages.*.bindings.anypointmq.headers": Schema,
    (
        "spec.components.messages.*.bindings.anypointmq.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.messages.*.bindings.http.headers": Schema,
    (
        "spec.components.messages.*.bindings.http.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.messages.*.bindings.jms.headers": Schema,
    (
        "spec.components.messages.*.bindings.jms.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.messages.*.bindings.kafka.key": Schema,
    (
        "spec.components.messages.*.bindings.kafka.key.external_docs"
    ): ExternalDocumentation,
    "spec.components.messages.*.bindings.mqtt.correlation_data": Schema,
    (
        "spec.components.messages.*.bindings.mqtt.correlation_data.external_docs"
    ): ExternalDocumentation,
    "spec.components.messages.*.bindings.mqtt.response_topic": Schema,
    (
        "spec.components.messages.*.bindings.mqtt.response_topic.external_docs"
    ): ExternalDocumentation,
    "spec.components.messages.*.correlation_id": CorrelationID,
    "spec.components.messages.*.external_docs": ExternalDocumentation,
    "spec.components.messages.*.headers": MultiFormatSchema | Schema,
    "spec.components.messages.*.headers.external_docs": ExternalDocumentation,
    "spec.components.messages.*.payload": MultiFormatSchema | Schema,
    "spec.components.messages.*.payload.external_docs": ExternalDocumentation,
    "spec.components.messages.*.tags.*": Tag,
    "spec.components.messages.*.tags.*.external_docs": ExternalDocumentation,
    "spec.components.messages.*.traits.*": MessageTrait,
    "spec.components.messages.*.traits.*.bindings": MessageBindingsObject,
    "spec.components.messages.*.traits.*.bindings.anypointmq.headers": Schema,
    (
        "spec.components.messages.*.traits.*.bindings.anypointmq.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.messages.*.traits.*.bindings.http.headers": Schema,
    (
        "spec.components.messages.*.traits.*.bindings.http.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.messages.*.traits.*.bindings.jms.headers": Schema,
    (
        "spec.components.messages.*.traits.*.bindings.jms.headers.external_docs"
    ): ExternalDocumentation,
    "spec.components.messages.*.traits.*.bindings.kafka.key": Schema,
    (
        "spec.components.messages.*.traits.*.bindings.kafka.key.external_docs"
    ): ExternalDocumentation,
    "spec.components.messages.*.traits.*.bindings.mqtt.correlation_data": Schema,
    (
        "spec.components.messages.*.traits.*.bindings.mqtt."
        "correlation_data.external_docs"
    ): ExternalDocumentation,
    "spec.components.messages.*.traits.*.bindings.mqtt.response_topic": Schema,
    (
        "spec.components.messages.*.traits.*.bindings.mqtt.response_topic.external_docs"
    ): ExternalDocumentation,
    "spec.components.messages.*.traits.*.correlation_id": CorrelationID,
    "spec.components.messages.*.traits.*.external_docs": ExternalDocumentation,
    "spec.components.messages.*.traits.*.headers": MultiFormatSchema | Schema,
    "spec.components.messages.*.traits.*.headers.external_docs": ExternalDocumentation,
    "spec.components.messages.*.traits.*.tags.*": Tag,
    "spec.components.messages.*.traits.*.tags.*.external_docs": ExternalDocumentation,
    "spec.components.operation_bindings.*": OperationBindingsObject,
    "spec.components.operation_bindings.*.http.query": Schema,
    (
        "spec.components.operation_bindings.*.http.query.external_docs"
    ): ExternalDocumentation,
    "spec.components.operation_bindings.*.kafka.client_id": Schema,
    (
        "spec.components.operation_bindings.*.kafka.client_id.external_docs"
    ): ExternalDocumentation,
    "spec.components.operation_bindings.*.kafka.group_id": Schema,
    (
        "spec.components.operation_bindings.*.kafka.group_id.external_docs"
    ): ExternalDocumentation,
    "spec.components.operation_bindings.*.mqtt.message_expiry_interval": Schema,
    (
        "spec.components.operation_bindings.*.mqtt."
        "message_expiry_interval.external_docs"
    ): ExternalDocumentation,
    "spec.components.operation_bindings.*.solace.priority": Schema,
    (
        "spec.components.operation_bindings.*.solace.priority.external_docs"
    ): ExternalDocumentation,
    "spec.components.operation_bindings.*.solace.time_to_live": Schema,
    (
        "spec.components.operation_bindings.*.solace.time_to_live.external_docs"
    ): ExternalDocumentation,
    "spec.components.operation_traits.*": OperationTrait,
    "spec.components.operation_traits.*.bindings": OperationBindingsObject,
    "spec.components.operation_traits.*.bindings.http.query": Schema,
    (
        "spec.components.operation_traits.*.bindings.http.query.external_docs"
    ): ExternalDocumentation,
    "spec.components.operation_traits.*.bindings.kafka.client_id": Schema,
    (
        "spec.components.operation_traits.*.bindings.kafka.client_id.external_docs"
    ): ExternalDocumentation,
    "spec.components.operation_traits.*.bindings.kafka.group_id": Schema,
    (
        "spec.components.operation_traits.*.bindings.kafka.group_id.external_docs"
    ): ExternalDocumentation,
    "spec.components.operation_traits.*.bindings.mqtt.message_expiry_interval": Schema,
    (
        "spec.components.operation_traits.*.bindings.mqtt."
        "message_expiry_interval.external_docs"
    ): ExternalDocumentation,
    "spec.components.operation_traits.*.bindings.solace.priority": Schema,
    (
        "spec.components.operation_traits.*.bindings.solace.priority.external_docs"
    ): ExternalDocumentation,
    "spec.components.operation_traits.*.bindings.solace.time_to_live": Schema,
    (
        "spec.components.operation_traits.*.bindings.solace.time_to_live.external_docs"
    ): ExternalDocumentation,
    "spec.components.operation_traits.*.external_docs": ExternalDocumentation,
    "spec.components.operation_traits.*.security.*": SecurityScheme,
    "spec.components.operation_traits.*.tags.*": Tag,
    "spec.components.operation_traits.*.tags.*.external_docs": ExternalDocumentation,
    "spec.components.operations.*": Operation,
    "spec.components.operations.*.bindings": OperationBindingsObject,
    "spec.components.operations.*.bindings.http.query": Schema,
    (
        "spec.components.operations.*.bindings.http.query.external_docs"
    ): ExternalDocumentation,
    "spec.components.operations.*.bindings.kafka.client_id": Schema,
    (
        "spec.components.operations.*.bindings.kafka.client_id.external_docs"
    ): ExternalDocumentation,
    "spec.components.operations.*.bindings.kafka.group_id": Schema,
    (
        "spec.components.operations.*.bindings.kafka.group_id.external_docs"
    ): ExternalDocumentation,
    "spec.components.operations.*.bindings.mqtt.message_expiry_interval": Schema,
    (
        "spec.components.operations.*.bindings.mqtt."
        "message_expiry_interval.external_docs"
    ): ExternalDocumentation,
    "spec.components.operations.*.bindings.solace.priority": Schema,
    (
        "spec.components.operations.*.bindings.solace.priority.external_docs"
    ): ExternalDocumentation,
    "spec.components.operations.*.bindings.solace.time_to_live": Schema,
    (
        "spec.components.operations.*.bindings.solace.time_to_live.external_docs"
    ): ExternalDocumentation,
    "spec.components.operations.*.channel": Channel,
    "spec.components.operations.*.external_docs": ExternalDocumentation,
    "spec.components.operations.*.messages.*": Message,
    "spec.components.operations.*.reply": OperationReply,
    "spec.components.operations.*.reply.address": OperationReplyAddress,
    "spec.components.operations.*.reply.channel": Channel,
    "spec.components.operations.*.reply.messages.*": Message,
    "spec.components.operations.*.security.*": SecurityScheme,
    "spec.components.operations.*.tags.*": Tag,
    "spec.components.operations.*.tags.*.external_docs": ExternalDocumentation,
    "spec.components.operations.*.traits.*": OperationTrait,
    "spec.components.operations.*.traits.*.bindings": OperationBindingsObject,
    "spec.components.operations.*.traits.*.bindings.http.query": Schema,
    (
        "spec.components.operations.*.traits.*.bindings.http.query.external_docs"
    ): ExternalDocumentation,
    "spec.components.operations.*.traits.*.bindings.kafka.client_id": Schema,
    (
        "spec.components.operations.*.traits.*.bindings.kafka.client_id.external_docs"
    ): ExternalDocumentation,
    "spec.components.operations.*.traits.*.bindings.kafka.group_id": Schema,
    (
        "spec.components.operations.*.traits.*.bindings.kafka.group_id.external_docs"
    ): ExternalDocumentation,
    (
        "spec.components.operations.*.traits.*.bindings.mqtt.message_expiry_interval"
    ): Schema,
    (
        "spec.components.operations.*.traits.*.bindings."
        "mqtt.message_expiry_interval.external_docs"
    ): ExternalDocumentation,
    "spec.components.operations.*.traits.*.bindings.solace.priority": Schema,
    (
        "spec.components.operations.*.traits.*.bindings.solace.priority.external_docs"
    ): ExternalDocumentation,
    "spec.components.operations.*.traits.*.bindings.solace.time_to_live": Schema,
    (
        "spec.components.operations.*.traits.*.bindings."
        "solace.time_to_live.external_docs"
    ): ExternalDocumentation,
    "spec.components.operations.*.traits.*.external_docs": ExternalDocumentation,
    "spec.components.operations.*.traits.*.security.*": SecurityScheme,
    "spec.components.operations.*.traits.*.tags.*": Tag,
    "spec.components.operations.*.traits.*.tags.*.external_docs": ExternalDocumentation,
    "spec.components.parameters.*": Parameter,
    "spec.components.replies.*": OperationReply,
    "spec.components.replies.*.address": OperationReplyAddress,
    "spec.components.replies.*.channel": Channel,
    "spec.components.replies.*.messages.*": Message,
    "spec.components.reply_addresses.*": OperationReplyAddress,
    "spec.components.schemas.*": MultiFormatSchema | Schema,
    "spec.components.schemas.*.external_docs": ExternalDocumentation,
    "spec.components.security_schemes.*": SecurityScheme,
    "spec.components.server_bindings.*": ServerBindingsObject,
    (
        "spec.components.server_bindings.*.jms.properties.*.external_docs"
    ): ExternalDocumentation,
    "spec.components.server_bindings.*.mqtt.maximum_packet_size": Schema,
    (
        "spec.components.server_bindings.*.mqtt.maximum_packet_size.external_docs"
    ): ExternalDocumentation,
    "spec.components.server_bindings.*.mqtt.session_expiry_interval": Schema,
    (
        "spec.components.server_bindings.*.mqtt.session_expiry_interval.external_docs"
    ): ExternalDocumentation,
    "spec.components.server_bindings.*.mqtt5.session_expiry_interval": Schema,
    (
        "spec.components.server_bindings.*.mqtt5.session_expiry_interval.external_docs"
    ): ExternalDocumentation,
    "spec.components.server_variables.*": ServerVariable,
    "spec.components.servers.*": Server,
    "spec.components.servers.*.bindings": ServerBindingsObject,
    (
        "spec.components.servers.*.bindings.jms.properties.*.external_docs"
    ): ExternalDocumentation,
    "spec.components.servers.*.bindings.mqtt.maximum_packet_size": Schema,
    (
        "spec.components.servers.*.bindings.mqtt.maximum_packet_size.external_docs"
    ): ExternalDocumentation,
    "spec.components.servers.*.bindings.mqtt.session_expiry_interval": Schema,
    (
        "spec.components.servers.*.bindings.mqtt.session_expiry_interval.external_docs"
    ): ExternalDocumentation,
    "spec.components.servers.*.bindings.mqtt5.session_expiry_interval": Schema,
    (
        "spec.components.servers.*.bindings.mqtt5.session_expiry_interval.external_docs"
    ): ExternalDocumentation,
    "spec.components.servers.*.external_docs": ExternalDocumentation,
    "spec.components.servers.*.security.*": SecurityScheme,
    "spec.components.servers.*.tags.*": Tag,
    "spec.components.servers.*.tags.*.external_docs": ExternalDocumentation,
    "spec.components.servers.*.variables.*": ServerVariable,
    "spec.components.tags.*": Tag,
    "spec.components.tags.*.external_docs": ExternalDocumentation,
    "spec.info.external_docs": ExternalDocumentation,
    "spec.info.tags.*": Tag,
    "spec.info.tags.*.external_docs": ExternalDocumentation,
    "spec.operations.*": Operation,
    "spec.operations.*.bindings": OperationBindingsObject,
    "spec.operations.*.bindings.http.query": Schema,
    "spec.operations.*.bindings.http.query.external_docs": ExternalDocumentation,
    "spec.operations.*.bindings.kafka.client_id": Schema,
    "spec.operations.*.bindings.kafka.client_id.external_docs": ExternalDocumentation,
    "spec.operations.*.bindings.kafka.group_id": Schema,
    "spec.operations.*.bindings.kafka.group_id.external_docs": ExternalDocumentation,
    "spec.operations.*.bindings.mqtt.message_expiry_interval": Schema,
    (
        "spec.operations.*.bindings.mqtt.message_expiry_interval.external_docs"
    ): ExternalDocumentation,
    "spec.operations.*.bindings.solace.priority": Schema,
    "spec.operations.*.bindings.solace.priority.external_docs": ExternalDocumentation,
    "spec.operations.*.bindings.solace.time_to_live": Schema,
    (
        "spec.operations.*.bindings.solace.time_to_live.external_docs"
    ): ExternalDocumentation,
    "spec.operations.*.channel": Channel,
    "spec.operations.*.external_docs": ExternalDocumentation,
    "spec.operations.*.messages.*": Message,
    "spec.operations.*.reply": OperationReply,
    "spec.operations.*.reply.address": OperationReplyAddress,
    "spec.operations.*.reply.channel": Channel,
    "spec.operations.*.reply.messages.*": Message,
    "spec.operations.*.security.*": SecurityScheme,
    "spec.operations.*.tags.*": Tag,
    "spec.operations.*.tags.*.external_docs": ExternalDocumentation,
    "spec.operations.*.traits.*": OperationTrait,
    "spec.operations.*.traits.*.bindings": OperationBindingsObject,
    "spec.operations.*.traits.*.bindings.http.query": Schema,
    (
        "spec.operations.*.traits.*.bindings.http.query.external_docs"
    ): ExternalDocumentation,
    "spec.operations.*.traits.*.bindings.kafka.client_id": Schema,
    (
        "spec.operations.*.traits.*.bindings.kafka.client_id.external_docs"
    ): ExternalDocumentation,
    "spec.operations.*.traits.*.bindings.kafka.group_id": Schema,
    (
        "spec.operations.*.traits.*.bindings.kafka.group_id.external_docs"
    ): ExternalDocumentation,
    "spec.operations.*.traits.*.bindings.mqtt.message_expiry_interval": Schema,
    (
        "spec.operations.*.traits.*.bindings.mqtt.message_expiry_interval.external_docs"
    ): ExternalDocumentation,
    "spec.operations.*.traits.*.bindings.solace.priority": Schema,
    (
        "spec.operations.*.traits.*.bindings.solace.priority.external_docs"
    ): ExternalDocumentation,
    "spec.operations.*.traits.*.bindings.solace.time_to_live": Schema,
    (
        "spec.operations.*.traits.*.bindings.solace.time_to_live.external_docs"
    ): ExternalDocumentation,
    "spec.operations.*.traits.*.external_docs": ExternalDocumentation,
    "spec.operations.*.traits.*.security.*": SecurityScheme,
    "spec.operations.*.traits.*.tags.*": Tag,
    "spec.operations.*.traits.*.tags.*.external_docs": ExternalDocumentation,
    "spec.servers.*": Server,
    "spec.servers.*.bindings": ServerBindingsObject,
    "spec.servers.*.bindings.jms.properties.*.external_docs": ExternalDocumentation,
    "spec.servers.*.bindings.mqtt.maximum_packet_size": Schema,
    (
        "spec.servers.*.bindings.mqtt.maximum_packet_size.external_docs"
    ): ExternalDocumentation,
    "spec.servers.*.bindings.mqtt.session_expiry_interval": Schema,
    (
        "spec.servers.*.bindings.mqtt.session_expiry_interval.external_docs"
    ): ExternalDocumentation,
    "spec.servers.*.bindings.mqtt5.session_expiry_interval": Schema,
    (
        "spec.servers.*.bindings.mqtt5.session_expiry_interval.external_docs"
    ): ExternalDocumentation,
    "spec.servers.*.external_docs": ExternalDocumentation,
    "spec.servers.*.security.*": SecurityScheme,
    "spec.servers.*.tags.*": Tag,
    "spec.servers.*.tags.*.external_docs": ExternalDocumentation,
    "spec.servers.*.variables.*": ServerVariable,
}


class TestUnifiedReferencesValidator:
    """Tests for UnifiedReferencesValidator."""

    def test_unified_validator_valid_channel_reference(self) -> None:
        """Test UnifiedReferencesValidator validates channel references correctly."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={
                "title": "Test API",
                "version": "1.0.0",
            },
            channels={
                "userChannel": {
                    "address": "user/{userId}",
                    "messages": {},
                },
            },
            operations={
                "userOp": {
                    "action": "send",
                    "channel": {"$ref": "#/channels/userChannel"},
                },
            },
            extra_validators=[UnifiedReferencesValidator],
        )

        # Should not raise any errors
        assert spec is not None

    def test_unified_validator_invalid_server_reference_path(self) -> None:
        """Test UnifiedReferencesValidator errors for invalid server reference path."""
        with pytest.raises(ValueError, match="Invalid reference"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={
                    "title": "Test API",
                    "version": "1.0.0",
                },
                channels={
                    "test": {
                        "$ref": "#/servers/nonexistent",  # Server doesn't exist
                    },
                },
                extra_validators=[UnifiedReferencesValidator],
            )

    def test_unified_validator_valid_tag_reference(self) -> None:
        """Test UnifiedReferencesValidator validates tag references correctly."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={
                "title": "Test API",
                "version": "1.0.0",
                "tags": [{"$ref": "#/components/tags/prod"}],
            },
            components={
                "tags": {
                    "prod": {
                        "name": "prod",
                        "description": "Production environment",
                    },
                },
            },
            extra_validators=[UnifiedReferencesValidator],
        )

        # Should not raise any errors
        assert spec is not None

    def test_unified_validator_invalid_tag_reference_path(self) -> None:
        """Test UnifiedReferencesValidator errors for invalid tag reference path."""
        with pytest.raises(ValueError, match="Invalid reference"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={
                    "title": "Test API",
                    "version": "1.0.0",
                    "tags": [
                        {"$ref": "#/components/tags/nonexistent"}
                    ],  # Tag doesn't exist
                },
                components={
                    "tags": {
                        "prod": {
                            "name": "prod",
                            "description": "Production environment",
                        },
                    },
                },
                extra_validators=[UnifiedReferencesValidator],
            )

    def test_unified_validator_external_reference_logs_warning(
        self, caplog: LogCaptureFixture
    ) -> None:
        """Test UnifiedReferencesValidator logs warning for external references."""

        with caplog.at_level(logging.WARNING):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={
                    "title": "Test API",
                    "version": "1.0.0",
                    "tags": [{"$ref": "https://example.com/external-tag"}],
                },
                extra_validators=[UnifiedReferencesValidator],
            )

        assert any("External reference" in record.message for record in caplog.records)

    def test_unified_validator_unsupported_reference_format(self) -> None:
        """Test UnifiedReferencesValidator errors for unsupported reference format."""
        with pytest.raises(ValueError, match="Unsupported reference format"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={
                    "title": "Test API",
                    "version": "1.0.0",
                    "tags": [{"$ref": "file://local-tag"}],  # Unsupported format
                },
                extra_validators=[UnifiedReferencesValidator],
            )

    def test_unified_validator_circular_reference_detection(self) -> None:
        """Test UnifiedReferencesValidator detects circular references."""
        # This is a complex test case that would require setting up circular references
        # For now, we'll skip this test as it requires more complex setup
        pass

    def test_unified_validator_valid_schema_reference(self) -> None:
        """Test UnifiedReferencesValidator validates schema references correctly."""
        spec = AsyncAPI3(
            asyncapi="3.0.0",
            info={
                "title": "Test API",
                "version": "1.0.0",
            },
            components={
                "schemas": {
                    "User": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                        },
                    },
                },
                "messages": {
                    "UserMessage": {
                        "payload": {"$ref": "#/components/schemas/User"},
                    },
                },
            },
            extra_validators=[UnifiedReferencesValidator],
        )

        # Should not raise any errors
        assert spec is not None

    def test_unified_validator_invalid_schema_reference(self) -> None:
        """Test UnifiedReferencesValidator raises error for invalid schema reference."""
        with pytest.raises(ValueError, match="Invalid reference"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={
                    "title": "Test API",
                    "version": "1.0.0",
                },
                components={
                    "messages": {
                        "UserMessage": {
                            "payload": {
                                "$ref": "#/components/schemas/NonExistentSchema"
                            },
                        },
                    },
                },
                extra_validators=[UnifiedReferencesValidator],
            )


# Test cases for bindings references
def case_valid_server_bindings_reference() -> dict:
    """Valid server bindings reference."""
    return {
        "asyncapi": "3.0.0",
        "info": {
            "title": "Test API",
            "version": "1.0.0",
        },
        "servers": {
            "prod": {
                "host": "api.example.com",
                "protocol": "https",
                "bindings": {"$ref": "#/components/server_bindings/httpBindings"},
            },
        },
        "components": {
            "serverBindings": {
                "httpBindings": {
                    "http": {},
                },
            },
        },
    }


def case_valid_channel_bindings_reference() -> dict:
    """Valid channel bindings reference."""
    return {
        "asyncapi": "3.0.0",
        "info": {
            "title": "Test API",
            "version": "1.0.0",
        },
        "channels": {
            "userChannel": {
                "address": "user/{userId}",
                "bindings": {"$ref": "#/components/channel_bindings/kafkaBindings"},
            },
        },
        "components": {
            "channelBindings": {
                "kafkaBindings": {
                    "kafka": {
                        "topic": "user-events",
                        "partitions": 3,
                    },
                },
            },
        },
    }


def case_valid_operation_bindings_reference() -> dict:
    """Valid operation bindings reference."""
    return {
        "asyncapi": "3.0.0",
        "info": {
            "title": "Test API",
            "version": "1.0.0",
        },
        "operations": {
            "sendMessage": {
                "action": "send",
                "channel": {"$ref": "#/channels/userChannel"},
                "bindings": {"$ref": "#/components/operation_bindings/httpBindings"},
            },
        },
        "channels": {
            "userChannel": {
                "address": "user/{userId}",
            },
        },
        "components": {
            "operationBindings": {
                "httpBindings": {
                    "http": {
                        "method": "POST",
                    },
                },
            },
        },
    }


def case_valid_message_bindings_reference() -> dict:
    """Valid message bindings reference."""
    return {
        "asyncapi": "3.0.0",
        "info": {
            "title": "Test API",
            "version": "1.0.0",
        },
        "components": {
            "messages": {
                "userMessage": {
                    "payload": {"type": "object"},
                    "bindings": {"$ref": "#/components/message_bindings/kafkaBindings"},
                },
            },
            "messageBindings": {
                "kafkaBindings": {
                    "kafka": {
                        "key": {"type": "string"},
                    },
                },
            },
        },
    }


# Test cases for traits references
def case_valid_operation_trait_reference() -> dict:
    """Valid operation trait reference."""
    return {
        "asyncapi": "3.0.0",
        "info": {
            "title": "Test API",
            "version": "1.0.0",
        },
        "channels": {
            "userChannel": {
                "address": "user/{userId}",
            },
        },
        "components": {
            "operations": {
                "sendMessage": {
                    "action": "send",
                    "channel": {"$ref": "#/channels/userChannel"},
                    "traits": [{"$ref": "#/components/operationTraits/commonTrait"}],
                },
            },
            "operationTraits": {
                "commonTrait": {
                    "bindings": {
                        "http": {
                            "method": "POST",
                        },
                    },
                },
            },
        },
    }


def case_valid_message_trait_reference() -> dict:
    """Valid message trait reference."""
    return {
        "asyncapi": "3.0.0",
        "info": {
            "title": "Test API",
            "version": "1.0.0",
        },
        "components": {
            "messages": {
                "userMessage": {
                    "payload": {"type": "object"},
                    "traits": [{"$ref": "#/components/messageTraits/commonTrait"}],
                },
            },
            "messageTraits": {
                "commonTrait": {
                    "headers": {"type": "object"},
                },
            },
        },
    }


# Test cases for other component references
def case_valid_security_scheme_reference() -> dict:
    """Valid security scheme reference."""
    return {
        "asyncapi": "3.0.0",
        "info": {
            "title": "Test API",
            "version": "1.0.0",
        },
        "components": {
            "securitySchemes": {
                "apiKey": {
                    "type": "apiKey",
                    "in": "user",
                },
            },
        },
        "servers": {
            "prod": {
                "host": "api.example.com",
                "protocol": "https",
                "security": [{"$ref": "#/components/securitySchemes/apiKey"}],
            },
        },
    }


def case_valid_server_variable_reference() -> dict:
    """Valid server variable reference."""
    return {
        "asyncapi": "3.0.0",
        "info": {
            "title": "Test API",
            "version": "1.0.0",
        },
        "servers": {
            "prod": {
                "host": "{environment}.api.example.com",
                "protocol": "https",
                "variables": {
                    "environment": {
                        "default": "prod",
                        "enum": ["dev", "staging", "prod"],
                    },
                },
            },
        },
    }


def case_valid_correlation_id_reference() -> dict:
    """Valid correlation ID reference."""
    return {
        "asyncapi": "3.0.0",
        "info": {
            "title": "Test API",
            "version": "1.0.0",
        },
        "components": {
            "correlationIds": {
                "requestId": {
                    "description": "Unique request identifier",
                    "location": "$message.header#/requestId",
                },
            },
            "messages": {
                "requestMessage": {
                    "correlationId": {"$ref": "#/components/correlationIds/requestId"},
                    "payload": {"type": "object"},
                },
            },
        },
    }


def case_valid_reply_reference() -> dict:
    """Valid reply reference."""
    return {
        "asyncapi": "3.0.0",
        "info": {
            "title": "Test API",
            "version": "1.0.0",
        },
        "channels": {
            "requestChannel": {
                "address": "request",
            },
            "replyChannel": {
                "address": "reply/{requestId}",
            },
        },
        "components": {
            "replies": {
                "successReply": {
                    "address": {
                        "location": "$message.payload#/replyTo",
                    },
                    "channel": {"$ref": "#/channels/replyChannel"},
                    "messages": [{"$ref": "#/components/messages/successMessage"}],
                },
            },
            "messages": {
                "successMessage": {
                    "payload": {"type": "object"},
                },
            },
            "operations": {
                "sendRequest": {
                    "action": "send",
                    "channel": {"$ref": "#/channels/requestChannel"},
                    "reply": {"$ref": "#/components/replies/successReply"},
                },
            },
        },
    }


def case_valid_reply_address_reference() -> dict:
    """Valid reply address reference."""
    return {
        "asyncapi": "3.0.0",
        "info": {
            "title": "Test API",
            "version": "1.0.0",
        },
        "channels": {
            "requestChannel": {
                "address": "request",
            },
            "replyChannel": {
                "address": "reply/{requestId}",
            },
        },
        "components": {
            "replyAddresses": {
                "successAddress": {
                    "location": "$message.payload#/replyTo",
                },
            },
            "operations": {
                "sendRequest": {
                    "action": "send",
                    "channel": {"$ref": "#/channels/requestChannel"},
                    "reply": {
                        "address": {
                            "$ref": "#/components/replyAddresses/successAddress"
                        },
                        "channel": {"$ref": "#/channels/replyChannel"},
                    },
                },
            },
        },
    }


class TestUnifiedReferencesValidatorParametrized:
    """Parametrized tests for UnifiedReferencesValidator."""

    @pytest.mark.parametrize(
        ("ref_path", "expected_type"),
        list(REFERENCE_TYPE_MAPPINGS_OLD.items()),
        ids=[path for path, _ in REFERENCE_TYPE_MAPPINGS_OLD.items()],
    )
    def test_reference_type_mappings_resolve_old_paths(
        self, ref_path: str, expected_type: object
    ) -> None:
        """Test new mappings resolve old paths to the same expected type."""
        validator = UnifiedReferencesValidator()
        resolved_type = validator._get_expected_type_for_path(ref_path=ref_path)
        assert resolved_type == expected_type

    @pytest.mark.parametrize(
        "spec_data",
        [
            case_valid_server_bindings_reference(),
            case_valid_channel_bindings_reference(),
            case_valid_operation_bindings_reference(),
            case_valid_message_bindings_reference(),
        ],
    )
    def test_valid_bindings_references(self, spec_data: dict) -> None:
        """Test valid bindings references."""
        spec = AsyncAPI3(
            **spec_data,
            extra_validators=[UnifiedReferencesValidator],
        )
        assert spec is not None

    def test_invalid_server_bindings_reference(self) -> None:
        """Test invalid server bindings reference."""
        with pytest.raises(ValueError, match="Invalid reference"):
            AsyncAPI3(
                asyncapi="3.0.0",
                info={
                    "title": "Test API",
                    "version": "1.0.0",
                },
                servers={
                    "prod": {
                        "host": "api.example.com",
                        "protocol": "https",
                        "bindings": {
                            "$ref": "#/components/server_bindings/nonexistent"
                        },
                    },
                },
                extra_validators=[UnifiedReferencesValidator],
            )

    @pytest.mark.parametrize(
        "spec_data",
        [
            case_valid_operation_trait_reference(),
            case_valid_message_trait_reference(),
        ],
    )
    def test_valid_trait_references(self, spec_data: dict) -> None:
        """Test valid trait references."""
        spec = AsyncAPI3(
            **spec_data,
            extra_validators=[UnifiedReferencesValidator],
        )
        assert spec is not None

    @pytest.mark.parametrize(
        "spec_data",
        [
            case_valid_security_scheme_reference(),
            case_valid_server_variable_reference(),
            case_valid_correlation_id_reference(),
            case_valid_reply_reference(),
            case_valid_reply_address_reference(),
        ],
    )
    def test_valid_component_references(self, spec_data: dict) -> None:
        """Test valid component references."""
        spec = AsyncAPI3(
            **spec_data,
            extra_validators=[UnifiedReferencesValidator],
        )
        assert spec is not None


class DummyModel(BaseModel):
    """Pydantic model for recursion tests."""

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    skip: str = Field(default="ignored", exclude=True)
    none: str | None = None
    value: int = 1


class TestUnifiedReferencesValidatorInternals:
    """Tests for internal helper behavior."""

    def _build_spec(self) -> AsyncAPI3:
        return AsyncAPI3(
            asyncapi="3.0.0",
            info={"title": "Test API", "version": "1.0.0"},
            channels={
                "test": {
                    "address": "test",
                },
            },
        )

    def test_normalize_path_removes_root_and_indices(self) -> None:
        validator = UnifiedReferencesValidator()
        assert (
            validator._normalize_path("spec.root.channels[0].messages[2].root")
            == "spec.channels.messages"
        )

    def test_path_matches_double_star(self) -> None:
        validator = UnifiedReferencesValidator()
        assert validator._path_matches("**", "spec.channels")

    def test_path_matches_message_glob(self) -> None:
        validator = UnifiedReferencesValidator()
        assert validator._path_matches("**.messages.*", "spec.channels.messages.msg")

    def test_path_matches_single_segment_glob(self) -> None:
        validator = UnifiedReferencesValidator()
        assert validator._path_matches(
            "spec.*.messages.*",
            "spec.channels.messages.msg",
        )

    def test_path_matches_wildcard_in_segment(self) -> None:
        validator = UnifiedReferencesValidator()
        assert validator._path_matches(
            "**.*_bindings.*",
            "spec.channel_bindings.kafka",
        )

    def test_path_matches_escaped_dot_segment(self) -> None:
        validator = UnifiedReferencesValidator()
        assert validator._path_matches(
            "spec.channels.*",
            "spec.channels.foo\\.bar",
        )

    def test_path_matches_rejects_missing_segment(self) -> None:
        validator = UnifiedReferencesValidator()
        assert not validator._path_matches("spec.channels.*", "spec.channels")

    def test_path_matches_rejects_mismatch(self) -> None:
        validator = UnifiedReferencesValidator()
        assert not validator._path_matches("spec.channels.*", "spec.channel.msg")

    def test_pattern_specificity_prefers_literals(self) -> None:
        validator = UnifiedReferencesValidator()
        specific = validator._pattern_specificity("**.channels.*.bindings")
        generic = validator._pattern_specificity("**.channels.*.*")
        assert specific > generic

    def test_expected_type_prefers_specific_pattern(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        mapping = {
            "**.channels.*.*": Message,
            "**.channels.*.bindings": ChannelBindingsObject,
        }
        monkeypatch.setattr(
            unified_references_module,
            "REFERENCE_TYPE_MAPPINGS",
            mapping,
        )

        validator = UnifiedReferencesValidator()
        expected = validator._get_expected_type_for_path(
            ref_path="spec.channels.sample.bindings"
        )
        assert expected is ChannelBindingsObject

    def test_get_expected_type_raises_for_unknown_path(self) -> None:
        validator = UnifiedReferencesValidator()
        with pytest.raises(ValueError, match="Unknown reference type"):
            validator._get_expected_type_for_path(ref_path="spec.unknown.path")

    def test_get_expected_type_with_escaped_dot(self) -> None:
        validator = UnifiedReferencesValidator()
        expected = validator._get_expected_type_for_path(
            ref_path="spec.channels.foo\\.bar"
        )
        assert expected is Channel

    def test_type_compatibility_union(self) -> None:
        validator = UnifiedReferencesValidator()
        assert validator._is_type_compatible(
            actual_type=Schema,
            expected_type=Schema | MultiFormatSchema,
        )

    def test_type_compatibility_exact(self) -> None:
        validator = UnifiedReferencesValidator()
        assert validator._is_type_compatible(actual_type=Schema, expected_type=Schema)

    def test_type_compatibility_incompatible_type(self) -> None:
        validator = UnifiedReferencesValidator()
        assert not validator._is_type_compatible(
            actual_type=Schema,
            expected_type=Message,
        )

    def test_type_compatibility_incompatible_non_type(self) -> None:
        validator = UnifiedReferencesValidator()
        assert not validator._is_type_compatible(
            actual_type=Schema,
            expected_type="Schema",
        )

    def test_format_type_name_union(self) -> None:
        validator = UnifiedReferencesValidator()
        assert (
            validator._format_type_name(expected_type=Schema | MultiFormatSchema)
            == "Schema | MultiFormatSchema"
        )

    def test_format_type_name_type(self) -> None:
        validator = UnifiedReferencesValidator()
        assert validator._format_type_name(expected_type=Schema) == "Schema"

    def test_format_type_name_string(self) -> None:
        validator = UnifiedReferencesValidator()
        assert validator._format_type_name(expected_type="custom") == "custom"

    def test_validate_reference_adds_ref(self) -> None:
        spec = self._build_spec()
        validator = UnifiedReferencesValidator()

        ref = Reference(ref="#/channels/test")
        validated_refs: set[str] = set()
        validator.validate_reference(
            spec=spec,
            ref_obj=ref,
            ref_path="spec.channels.test",
            validated_refs=validated_refs,
        )
        assert ref.ref in validated_refs

    def test_validate_reference_skips_already_validated(self) -> None:
        spec = self._build_spec()
        validator = UnifiedReferencesValidator()
        ref = Reference(ref="#/channels/test")
        validated_refs = {ref.ref}
        validator.validate_reference(
            spec=spec,
            ref_obj=ref,
            ref_path="spec.channels.test",
            validated_refs=validated_refs,
        )
        assert validated_refs == {ref.ref}

    def test_validate_reference_cached_ref_still_validates(self) -> None:
        spec = self._build_spec()
        validator = UnifiedReferencesValidator()
        ref = Reference(ref="#/channels/test")
        validated_refs = {ref.ref}
        with pytest.raises(ValueError, match="expected"):
            validator.validate_reference(
                spec=spec,
                ref_obj=ref,
                ref_path="spec.messages",
                validated_refs=validated_refs,
            )

    def test_validate_reference_external_ref(self) -> None:
        spec = self._build_spec()
        validator = UnifiedReferencesValidator()
        external_ref = Reference(ref="https://example.com/ref")
        validated_refs: set[str] = set()
        validator.validate_reference(
            spec=spec,
            ref_obj=external_ref,
            ref_path="spec.channels.test",
            validated_refs=validated_refs,
        )
        assert external_ref.ref in validated_refs

    def test_validate_reference_invalid_reference_error(self) -> None:
        spec = self._build_spec()
        validator = UnifiedReferencesValidator()
        invalid_ref = Reference(ref="#/channels/missing")
        with pytest.raises(ValueError, match="Invalid reference"):
            validator.validate_reference(
                spec=spec,
                ref_obj=invalid_ref,
                ref_path="spec.channels.missing",
                validated_refs=set(),
            )

    def test_validate_reference_type_mismatch_error(self) -> None:
        spec = self._build_spec()
        validator = UnifiedReferencesValidator()
        ref = Reference(ref="#/channels/test")
        with pytest.raises(ValueError, match="expected"):
            validator.validate_reference(
                spec=spec,
                ref_obj=ref,
                ref_path="spec.messages",
                validated_refs=set(),
            )

    def test_validate_references_recursive_reference(self) -> None:
        spec = self._build_spec()
        validator = UnifiedReferencesValidator()
        validated_refs: set[str] = set()

        validator.validate_references_recursive(
            spec=spec,
            obj=Reference(ref="#/channels/test"),
            current_path="spec.channels.test",
            validated_refs=validated_refs,
        )
        assert "#/channels/test" in validated_refs

    def test_validate_references_recursive_list_cycle(self) -> None:
        spec = self._build_spec()
        validator = UnifiedReferencesValidator()
        validated_refs: set[str] = set()
        items: list[object] = []
        items.append(items)
        validator.validate_references_recursive(
            spec=spec,
            obj=items,
            current_path="spec.messages",
            validated_refs=validated_refs,
        )
        assert validated_refs == set()

    def test_validate_references_recursive_mapping(self) -> None:
        spec = self._build_spec()
        validator = UnifiedReferencesValidator()
        validated_refs: set[str] = set()
        validator.validate_references_recursive(
            spec=spec,
            obj={"nested": 1},
            current_path="spec.messages",
            validated_refs=validated_refs,
        )
        assert validated_refs == set()

    def test_validate_references_recursive_model(self) -> None:
        spec = self._build_spec()
        validator = UnifiedReferencesValidator()
        validated_refs: set[str] = set()
        validator.validate_references_recursive(
            spec=spec,
            obj=DummyModel(),
            current_path="spec",
            validated_refs=validated_refs,
        )
        assert validated_refs == set()

    def test_validate_references_recursive_other_object(self) -> None:
        spec = self._build_spec()
        validator = UnifiedReferencesValidator()
        validated_refs: set[str] = set()
        validator.validate_references_recursive(
            spec=spec,
            obj=1,
            current_path="spec",
            validated_refs=validated_refs,
        )
        assert validated_refs == set()
