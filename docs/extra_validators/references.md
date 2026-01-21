# Reference Objects extra validators

AsyncAPI 3 specification has a lot of `Reference` objects. If such object points to
non-existent target, it is considered invalid.

We implement extra validators for `Reference` objects to ensure that they point to
valid targets. Each validator is designed to handle specific original object types, as
some of them has specific reference rules.

This document provides detailed information about each specification field that can
be in form of `Reference` object, as well as the validation rules for each field and
related validator class.

## Document Structure

### Per model section

Describes validators related to model.

- **Model file name** (H2 header)
- **Model Class name** (H3 header)
- **Model field name**: declared field types
- Validated by: `validator class name`; Allows the following values:
- Allowed reference values list

All lines should have checkbox marks for use as a TODO list.

Example:

```markdown
## `asyncapi3/models/info.py`

### Info

- [ ] `tags`: Tags | None (list[Tag | Reference])
  - [ ] Validated by `TagsRefValidator`; Allows the following values:
    - [ ] External values with warning
    - [ ] `#/components/tags/{key}`
- [ ] `external_docs`: ExternalDocumentation | Reference | None
  - [ ] Not validated yet
```

### Per validator sections

Shortly describes validator behavior and a list of checked fields location.

- Validator file name (H2)
- Validator class name (H3)
- List of allowed ref values
- List of verified fields
- List of not verified fields

Example:

```markdown
## `asyncapi3/validators/tags_ref_validator.py)`

### TagsRefValidator

- [ ] Allowed values:
  - [ ] `#/components/tags/{tag_name}`
- [ ] Verified fields:
  - [ ] `root.info.tags`
  - [ ] `root.servers.tags`
  - [ ] `root.channels.tags`
  - [ ] `root.operations.tags`
  - [ ] `components.messages.tags`
  - [ ] `components.channels.tags`
  - [ ] `components.operations.tags`
- [ ] Not verified fields:
  - `field.name`
```

### Statistics section

- **Total fields with Reference**: int
- **Validated fields**: int
- **Non-validated fields**: int

## `asyncapi3/models/asyncapi.py`

### AsyncAPI3

- [ ] `servers`: `Servers | None` (dict[str, Server | Reference])
  - [ ] `Reference` values: `ServersRefValidator`
  - [ ] `Server` values:
    - [ ] `variables`: `ServerVariablesRefValidator`
    - [ ] `security`: `SecuritySchemesRefValidator`
    - [x] `tags`: `TagsRefValidator`
    - [ ] `external_docs`: `ExternalDocsRefValidator`
    - [ ] `bindings`: `ServerBindingsRefValidator`
- [ ] `channels`: `Channels | None` (dict[str, Channel | Reference])
  - [ ] `Reference` values: `ChannelsRefValidator`
  - [ ] `Channel` values:
    - [ ] `messages`: `MessagesRefValidator`
    - [ ] `servers`: `ServersRefValidator`
    - [ ] `parameters`: `ParametersRefValidator`
    - [x] `tags`: `TagsRefValidator`
    - [ ] `external_docs`: `ExternalDocsRefValidator`
    - [ ] `bindings`: `ChannelBindingsRefValidator`
- [ ] `operations`: `Operations | None` (dict[str, Operation | Reference])
  - [ ] `Reference` values: `OperationsRefValidator`
  - [ ] `Operation` values:
    - [ ] `channel`: `ChannelsRefValidator`
    - [ ] `security`: `SecuritySchemesRefValidator`
    - [x] `tags`: `TagsRefValidator`
    - [ ] `external_docs`: `ExternalDocsRefValidator`
    - [ ] `bindings`: `OperationBindingsRefValidator`
    - [ ] `traits`: `OperationTraitsRefValidator`
    - [ ] `messages`: `MessagesRefValidator`
    - [ ] `reply`: `RepliesRefValidator`

## `asyncapi3/models/base.py`

### Tag

- [ ] `external_docs`: `ExternalDocumentation | Reference | None`
  - [ ] Validated by `ExternalDocsRefValidator`

## `asyncapi3/models/info.py`

### Info

- [x] `tags`: `Tags | None` (`list[Tag | Reference]`)
  - [x] Validated by `TagsRefValidator`; Allows the following values:
    - [x] External values with warning
    - [x] `#/components/tags/{key}`
- [ ] `external_docs`: `ExternalDocumentation | Reference | None`
  - [ ] Validated by `ExternalDocsRefValidator`

## `asyncapi3/models/server.py`

### Server

- [ ] `variables`: `dict[str, ServerVariable | Reference] | None`
  - [ ] Validated by `ServerVariablesRefValidator`
- [ ] `security`: `list[SecurityScheme | Reference] | None`
  - [ ] Validated by `SecuritySchemesRefValidator`
- [x] `tags`: `Tags | None` (`list[Tag | Reference]`)
  - [x] Validated by `TagsRefValidator` (when in `root.servers`)
- [ ] `external_docs`: `ExternalDocumentation | Reference | None`
  - [ ] Validated by `ExternalDocsRefValidator`
- [ ] `bindings`: `ServerBindingsObject | Reference | None`
  - [ ] Validated by `ServerBindingsRefValidator`

## `asyncapi3/models/channel.py`

### Channel

- [ ] `messages`: `Messages | None` (dict[str, Message | Reference])
  - [ ] Validated by `MessagesRefValidator`
- [ ] `servers`: `list[Reference] | None`
  - [ ] Validated by `ServersRefValidator`
- [ ] `parameters`: `Parameters | None` (dict[str, Parameter | Reference])
  - [ ] Validated by `ParametersRefValidator`
- [x] `tags`: `Tags | None` (`list[Tag | Reference]`)
  - [x] Validated by `TagsRefValidator`
- [ ] `external_docs`: `ExternalDocumentation | Reference | None`
  - [ ] Validated by `ExternalDocsRefValidator`
- [ ] `bindings`: `ChannelBindingsObject | Reference | None`
  - [ ] Validated by `ChannelBindingsRefValidator`

## `asyncapi3/models/operation.py`

### OperationReply

- [ ] `address`: `OperationReplyAddress | Reference | None`
  - [ ] Validated by `ReplyAddressesRefValidator`
- [ ] `channel`: `Reference | None`
  - [ ] Validated by `ChannelsRefValidator`
- [ ] `messages`: `list[Reference] | None`
  - [ ] Validated by `MessagesRefValidator`
  - [x] `tags` validated by `TagsRefValidator` (indirectly via referenced channel)

### OperationTrait

- [ ] `security`: `list[SecurityScheme | Reference] | None`
  - [ ] Validated by `SecuritySchemesRefValidator`
- [x] `tags`: `Tags | None` (`list[Tag | Reference]`)
  - [x] Validated by `TagsRefValidator`
- [ ] `external_docs`: `ExternalDocumentation | Reference | None`
  - [ ] Validated by `ExternalDocsRefValidator`
- [ ] `bindings`: `OperationBindingsObject | Reference | None`
  - [ ] Validated by `OperationBindingsRefValidator`

### Operation

- [ ] `channel`: `Reference`
  - [ ] Validated by `ChannelsRefValidator`
- [ ] `security`: `list[SecurityScheme | Reference] | None`
  - [ ] Validated by `SecuritySchemesRefValidator`
- [x] `tags`: `Tags | None` (`list[Tag | Reference]`)
  - [x] Validated by `TagsRefValidator`
- [ ] `external_docs`: `ExternalDocumentation | Reference | None`
  - [ ] Validated by `ExternalDocsRefValidator`
- [ ] `bindings`: `OperationBindingsObject | Reference | None`
  - [ ] Validated by `OperationBindingsRefValidator`
- [ ] `traits`: `list[OperationTrait | Reference] | None`
  - [ ] Validated by `OperationTraitsRefValidator`
- [ ] `messages`: `list[Reference] | None`
  - [ ] Validated by `MessagesRefValidator`
- [ ] `reply`: `OperationReply | Reference | None`
  - [ ] Validated by `RepliesRefValidator`

## `asyncapi3/models/message.py`

### MessageTrait

- [ ] `headers`: `MultiFormatSchema | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `correlation_id`: `CorrelationID | Reference | None`
  - [ ] Validated by `CorrelationIdsRefValidator`
- [x] `tags`: `Tags | None` (`list[Tag | Reference]`)
  - [x] Validated by `TagsRefValidator`
- [ ] `external_docs`: `ExternalDocumentation | Reference | None`
  - [ ] Validated by `ExternalDocsRefValidator`
- [ ] `bindings`: `MessageBindingsObject | Reference | None`
  - [ ] Validated by `MessageBindingsRefValidator`

### Message

- [ ] `headers`: `MultiFormatSchema | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `payload`: `MultiFormatSchema | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `correlation_id`: `CorrelationID | Reference | None`
  - [ ] Validated by `CorrelationIdsRefValidator`
- [x] `tags`: `Tags | None` (`list[Tag | Reference]`)
  - [x] Validated by `TagsRefValidator`
- [ ] `external_docs`: `ExternalDocumentation | Reference | None`
  - [ ] Validated by `ExternalDocsRefValidator`
- [ ] `bindings`: `MessageBindingsObject | Reference | None`
  - [ ] Validated by `MessageBindingsRefValidator`
- [ ] `traits`: `list[MessageTrait | Reference] | None`
  - [ ] Validated by `MessageTraitsRefValidator`

## `asyncapi3/models/components.py`

### Components

- [ ] `schemas`: `Schemas | None` (dict[str, MultiFormatSchema | Schema | Reference])
  - [ ] `Reference` values: `SchemasRefValidator`
  - [ ] `Schema` values:
    - [ ] `external_docs`: `ExternalDocsRefValidator`
- [ ] `servers`: `Servers | None` (dict[str, Server | Reference])
  - [ ] `Reference` values: `ServersRefValidator`
  - [ ] `Server` values:
    - [ ] `variables`: `ServerVariablesRefValidator`
    - [ ] `security`: `SecuritySchemesRefValidator`
    - [x] `tags`: `TagsRefValidator`
    - [ ] `external_docs`: `ExternalDocsRefValidator`
    - [ ] `bindings`: `ServerBindingsRefValidator`
- [ ] `channels`: `Channels | None` (dict[str, Channel | Reference])
  - [ ] `Reference` values: `ChannelsRefValidator`
  - [ ] `Channel` values:
    - [ ] `messages`: `MessagesRefValidator`
    - [ ] `servers`: `ServersRefValidator`
    - [ ] `parameters`: `ParametersRefValidator`
    - [x] `tags`: `TagsRefValidator`
    - [ ] `external_docs`: `ExternalDocsRefValidator`
    - [ ] `bindings`: `ChannelBindingsRefValidator`
- [ ] `operations`: `Operations | None` (dict[str, Operation | Reference])
  - [ ] `Reference` values: `OperationsRefValidator`
  - [ ] `Operation` values:
    - [ ] `channel`: `ChannelsRefValidator`
    - [ ] `security`: `SecuritySchemesRefValidator`
    - [x] `tags`: `TagsRefValidator`
    - [ ] `external_docs`: `ExternalDocsRefValidator`
    - [ ] `bindings`: `OperationBindingsRefValidator`
    - [ ] `traits`: `OperationTraitsRefValidator`
    - [ ] `messages`: `MessagesRefValidator`
    - [ ] `reply`: `RepliesRefValidator`
- [ ] `messages`: `Messages | None` (dict[str, Message | Reference])
  - [ ] `Reference` values: `MessagesRefValidator`
  - [ ] `Message` values:
    - [ ] `headers`: `SchemasRefValidator`
    - [ ] `payload`: `SchemasRefValidator`
    - [ ] `correlation_id`: `CorrelationIdsRefValidator`
    - [x] `tags`: `TagsRefValidator`
    - [ ] `external_docs`: `ExternalDocsRefValidator`
    - [ ] `bindings`: `MessageBindingsRefValidator`
    - [ ] `traits`: `MessageTraitsRefValidator`
- [ ] `security_schemes`: `SecuritySchemes | None` (dict[str, SecurityScheme | Reference])
- [ ] `server_variables`: `ServerVariables | None` (dict[str, ServerVariable | Reference])
- [ ] `parameters`: `Parameters | None` (dict[str, Parameter | Reference])
- [ ] `correlation_ids`: `CorrelationIDs | None` (dict[str, CorrelationID | Reference])
- [ ] `replies`: `Replies | None` (dict[str, OperationReply | Reference])
  - [ ] `Reference` values: `RepliesRefValidator`
  - [ ] `OperationReply` values:
    - [ ] `address`: `ReplyAddressesRefValidator`
    - [ ] `channel`: `ChannelsRefValidator`
    - [ ] `messages`: `MessagesRefValidator`
- [ ] `reply_addresses`: `ReplyAddresses | None` (dict[str, OperationReplyAddress | Reference])
- [ ] `external_docs`: `ExternalDocs | None` (dict[str, ExternalDocumentation | Reference])
- [ ] `tags`: `TagsDict | None` (dict[str, Tag | Reference])
  - [x] `Reference` values: `TagsRefValidator`
  - [ ] `Tag` values:
    - [ ] `external_docs`: `ExternalDocsRefValidator`
- [ ] `operation_traits`: `OperationTraits | None` (dict[str, OperationTrait | Reference])
  - [ ] `Reference` values: `OperationTraitsRefValidator`
  - [ ] `OperationTrait` values:
    - [ ] `security`: `SecuritySchemesRefValidator`
    - [x] `tags`: `TagsRefValidator`
    - [ ] `external_docs`: `ExternalDocsRefValidator`
    - [ ] `bindings`: `OperationBindingsRefValidator`
- [ ] `message_traits`: `MessageTraits | None` (dict[str, MessageTrait | Reference])
  - [ ] `Reference` values: `MessageTraitsRefValidator`
  - [ ] `MessageTrait` values:
    - [ ] `headers`: `SchemasRefValidator`
    - [ ] `correlation_id`: `CorrelationIdsRefValidator`
    - [x] `tags`: `TagsRefValidator`
    - [ ] `external_docs`: `ExternalDocsRefValidator`
    - [ ] `bindings`: `MessageBindingsRefValidator`
- [ ] `server_bindings`: `ServerBindings | None`
  (dict[str, ServerBindingsObject | Reference])
- [ ] `channel_bindings`: `ChannelBindings | None`
  (dict[str, ChannelBindingsObject | Reference])
- [ ] `operation_bindings`: `OperationBindings | None`
  (dict[str, OperationBindingsObject | Reference])
- [ ] `message_bindings`: `MessageBindings | None`
  (dict[str, MessageBindingsObject | Reference])

## `asyncapi3/models/schema.py`

### Schema

- [ ] `external_docs`: `ExternalDocumentation | Reference | None`
  - [ ] Validated by `ExternalDocsRefValidator`

## `asyncapi3/models/bindings/http.py`

### HTTPOperationBindings

- [ ] `query`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

### HTTPMessageBindings

- [ ] `headers`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

## `asyncapi3/models/bindings/mqtt.py`

### MQTTServerBindings

- [ ] `session_expiry_interval`: `int | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `maximum_packet_size`: `int | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

### MQTTOperationBindings

- [ ] `message_expiry_interval`: `int | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

### MQTTMessageBindings

- [ ] `correlation_data`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `response_topic`: `str | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

## `asyncapi3/models/bindings/kafka.py`

### KafkaOperationBindings

- [ ] `group_id`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `client_id`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

### KafkaMessageBindings

- [ ] `key`: `Schema | Reference | dict[str, Any] | None`
  - [ ] Validated by `SchemasRefValidator`

## `asyncapi3/models/bindings/websockets.py`

### WebSocketsChannelBindings

- [ ] `query`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `headers`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

## `asyncapi3/models/bindings/mqtt5.py`

### MQTT5ServerBindings

- [ ] `session_expiry_interval`: `int | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

## `asyncapi3/models/bindings/jms.py`

### JMSMessageBindings

- [ ] `headers`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

## `asyncapi3/models/bindings/anypointmq.py`

### AnypointMQMessageBindings

- [ ] `headers`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

## `asyncapi3/models/bindings/solace.py`

### SolaceOperationBindings

- [ ] `time_to_live`: `int | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `priority`: `int | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

## `asyncapi3/validators/channel_bindings_ref_validator.py`

### ChannelBindingsRefValidator

- [ ] Verified fields:
  - [ ] `root.channels[].bindings`
  - [ ] `root.components.channels[].bindings`
  - [ ] `root.components.channelBindings`

## `asyncapi3/validators/channels_ref_validator.py`

### ChannelsRefValidator

- [ ] Verified fields:
  - [ ] `root.channels`
  - [ ] `root.operations[].channel`
  - [ ] `root.operations[].reply.channel`
  - [ ] `root.components.channels`

## `asyncapi3/validators/correlation_ids_ref_validator.py`

### CorrelationIdsRefValidator

- [ ] Verified fields:
  - [ ] `root.messages[].correlation_id`
  - [ ] `root.messageTraits[].correlation_id`
  - [ ] `root.components.correlationIds`

## `asyncapi3/validators/external_docs_ref_validator.py`

### ExternalDocsRefValidator

- [ ] Allowed values:
  - [ ] External values with warning
  - [ ] `#/components/externalDocs/{external_doc_name}`
- [ ] Verified fields:
  - [ ] `root.info.external_docs`
  - [ ] `root.servers[].external_docs`
  - [ ] `root.channels[].external_docs`
  - [ ] `root.operations[].external_docs`
  - [ ] `root.messages[].external_docs`
  - [ ] `root.operationTraits[].external_docs`
  - [ ] `root.messageTraits[].external_docs`
  - [ ] `root.tags[].external_docs`
  - [ ] `root.components.externalDocs`
  - [ ] `root.schemas[].external_docs`

## `asyncapi3/validators/message_bindings_ref_validator.py`

### MessageBindingsRefValidator

- [ ] Verified fields:
  - [ ] `root.messages[].bindings`
  - [ ] `root.messageTraits[].bindings`
  - [ ] `root.components.messageBindings`

## `asyncapi3/validators/message_traits_ref_validator.py`

### MessageTraitsRefValidator

- [ ] Verified fields:
  - [ ] `root.messages[].traits`
  - [ ] `root.components.messageTraits`

## `asyncapi3/validators/messages_ref_validator.py`

### MessagesRefValidator

- [ ] Verified fields:
  - [ ] `root.channels[].messages`
  - [ ] `root.operations[].messages`
  - [ ] `root.operations[].reply.messages`
  - [ ] `root.components.messages`

## `asyncapi3/validators/operation_bindings_ref_validator.py`

### OperationBindingsRefValidator

- [ ] Verified fields:
  - [ ] `root.operations[].bindings`
  - [ ] `root.operationTraits[].bindings`
  - [ ] `root.components.operationBindings`

## `asyncapi3/validators/operation_traits_ref_validator.py`

### OperationTraitsRefValidator

- [ ] Verified fields:
  - [ ] `root.operations[].traits`
  - [ ] `root.components.operationTraits`

## `asyncapi3/validators/operations_ref_validator.py`

### OperationsRefValidator

- [ ] Verified fields:
  - [ ] `root.operations`
  - [ ] `root.components.operations`

## `asyncapi3/validators/parameters_ref_validator.py`

### ParametersRefValidator

- [ ] Verified fields:
  - [ ] `root.channels[].parameters`
  - [ ] `root.components.parameters`

## `asyncapi3/validators/replies_ref_validator.py`

### RepliesRefValidator

- [ ] Verified fields:
  - [ ] `root.operations[].reply`
  - [ ] `root.components.replies`

## `asyncapi3/validators/reply_addresses_ref_validator.py`

### ReplyAddressesRefValidator

- [ ] Verified fields:
  - [ ] `root.operations[].reply.address`
  - [ ] `root.components.replyAddresses`

## `asyncapi3/validators/schemas_ref_validator.py`

### SchemasRefValidator

- [ ] Verified fields:
  - [ ] `root.messages[].headers`
  - [ ] `root.messages[].payload`
  - [ ] `root.messageTraits[].headers`
  - [ ] `root.components.schemas`
  - [ ] `bindings.http.operation.query`
  - [ ] `bindings.http.message.headers`
  - [ ] `bindings.mqtt.server.session_expiry_interval`
  - [ ] `bindings.mqtt.server.maximum_packet_size`
  - [ ] `bindings.mqtt.operation.message_expiry_interval`
  - [ ] `bindings.mqtt.message.correlation_data`
  - [ ] `bindings.mqtt.message.response_topic`
  - [ ] `bindings.kafka.operation.group_id`
  - [ ] `bindings.kafka.operation.client_id`
  - [ ] `bindings.kafka.message.key`
  - [ ] `bindings.websockets.channel.query`
  - [ ] `bindings.websockets.channel.headers`
  - [ ] `bindings.mqtt5.server.session_expiry_interval`
  - [ ] `bindings.jms.message.headers`
  - [ ] `bindings.anypointmq.message.headers`
  - [ ] `bindings.solace.operation.time_to_live`
  - [ ] `bindings.solace.operation.priority`

## `asyncapi3/validators/security_schemes_ref_validator.py`

### SecuritySchemesRefValidator

- [ ] Verified fields:
  - [ ] `root.servers[].security`
  - [ ] `root.operations[].security`
  - [ ] `root.operationTraits[].security`
  - [ ] `root.components.securitySchemes`

## `asyncapi3/validators/server_bindings_ref_validator.py`

### ServerBindingsRefValidator

- [ ] Verified fields:
  - [ ] `root.servers[].bindings`
  - [ ] `root.components.serverBindings`

## `asyncapi3/validators/server_variables_ref_validator.py`

### ServerVariablesRefValidator

- [ ] Verified fields:
  - [ ] `root.servers[].variables`
  - [ ] `root.components.serverVariables`

## `asyncapi3/validators/servers_ref_validator.py`

### ServersRefValidator

- [ ] Verified fields:
  - [ ] `root.servers`
  - [ ] `root.channels[].servers`
  - [ ] `root.components.servers`

## `asyncapi3/validators/tags_ref_validator.py`

### TagsRefValidator

- [x] Allowed values:
  - [x] External values with warning
  - [x] `#/components/tags/{tag_name}`
- [x] Verified fields:
  - [x] `AsyncAPI3.info.tags`
  - [x] `AsyncAPI3.servers[].tags`
  - [x] `AsyncAPI3.channels[].tags`
  - [x] `AsyncAPI3.channels[].messages[].tags`
  - [x] `AsyncAPI3.operations[].tags`
  - [x] `AsyncAPI3.operations[].reply.messages[].tags` (indirectly via referenced
    channel)
  - [x] `AsyncAPI3.components.messages[].tags`
  - [x] `AsyncAPI3.components.channels[].tags`
  - [x] `AsyncAPI3.components.operations[].tags`
  - [x] `AsyncAPI3.components.servers[].tags`
  - [x] `AsyncAPI3.components.operationTraits[].tags`
  - [x] `AsyncAPI3.components.messageTraits[].tags`
  - [x] `AsyncAPI3.components.channels[].messages[].tags`
  - [ ] `AsyncAPI3.components.tags[].tags
