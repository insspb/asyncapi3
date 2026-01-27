# Reference Objects extra validators

AsyncAPI 3 specification has a lot of `Reference` objects. If such object points to
non-existent target, it is considered invalid.

We implement extra validators for `Reference` objects to ensure that they point to
valid targets. Each validator is designed to handle specific original object types, as
some of them has specific reference rules.

This document provides detailed information about each specification field that can
contain `Reference` objects, organized by logical structure rather than by files.
It shows validation status, responsible validators, and allowed reference patterns
for each field that can contain references.

## Document Structure

### Per Field data

This section organizes all fields that can contain `Reference` objects by their logical
location in the AsyncAPI specification structure.

**Structure:**

- **Logical Section** (H2 header) - Groups fields by AsyncAPI specification areas (Root
  Level, Components, Bindings)
- **Field Path**: `field.path` (with type annotation)
- **Validator**: `ValidatorClass` - Which validator handles this field
- **Status**: `[x]` for implemented, `[ ]` for not implemented
- **Allowed References**: List of reference patterns this field accepts

All lines should have checkbox marks for use as a TODO list.

Example:

```markdown
### Root Level Objects

#### AsyncAPI3 (Root Document)

- [x] `servers`: `Servers | None` (dict[str, Server | Reference])
  - [ ] `Reference` values: `ServersRefValidator`
  - [ ] `Server` values: (nested validation)
    - [ ] `variables`: `ServerVariablesRefValidator`
    - [ ] `security`: `SecuritySchemesRefValidator`
    - [x] `tags`: `TagsRefValidator`
    - [x] `external_docs`: `ExternalDocsRefValidator`
```

### Per Validator data

This section describes each validator's behavior and lists all fields it validates.

**Structure:**

- **Validator File** (H2 header)
- **Validator Class** (H3 header)
- **Allowed Values**: Reference patterns this validator accepts
- **Verified Fields**: Complete list of all fields this validator checks
- **Not Verified Fields**: Fields that should be validated but aren't yet

Example:

```markdown
### `asyncapi3/validators/tags_ref_validator.py`

#### TagsRefValidator

- [x] Allowed values:
  - [x] External values with warning
  - [x] `#/components/tags/{tag_name}`
- [x] Verified fields:
  - [x] `AsyncAPI3.info.tags`
  - [x] `AsyncAPI3.servers[].tags`
  - [x] `AsyncAPI3.channels[].tags`
  - [x] `AsyncAPI3.channels[].messages[].tags`
  - [x] `AsyncAPI3.operations[].tags`
  - [x] `AsyncAPI3.components.messages[].tags`
  - [x] `AsyncAPI3.components.channels[].tags`
  - [x] `AsyncAPI3.components.channels[].messages[].tags`
  - [x] `AsyncAPI3.components.operations[].tags`
  - [x] `AsyncAPI3.components.servers[].tags`
  - [x] `AsyncAPI3.components.operationTraits[].tags`
  - [x] `AsyncAPI3.components.messageTraits[].tags`
  - [x] `AsyncAPI3.components.tags[]`
- [ ] Not verified fields:
  - [ ] None (all implemented fields are listed above)
```

## Per Field data

This section organizes all fields that can contain `Reference` objects by their logical
location in the AsyncAPI specification structure.

### Root Level Objects

#### AsyncAPI3 (Root Document)

##### Root Level Collections

- [ ] `servers`: `Servers | None` (dict[str, Server | Reference])
  - [ ] `Reference` values: `ServersRefValidator`
  - [ ] `Server` values:
    - [ ] `variables`: `ServerVariablesRefValidator`
    - [ ] `security`: `SecuritySchemesRefValidator`
    - [x] `tags`: `TagsRefValidator` → `AsyncAPI3.servers[].tags`
    - [x] `external_docs`: `ExternalDocsRefValidator` →
      `AsyncAPI3.servers[].external_docs`
    - [ ] `bindings`: `ServerBindingsRefValidator`

- [ ] `channels`: `Channels | None` (dict[str, Channel | Reference])
  - [ ] `Reference` values: `ChannelsRefValidator`
  - [ ] `Channel` values:
    - [ ] `messages`: `MessagesRefValidator`
    - [ ] `servers`: `ServersRefValidator`
    - [ ] `parameters`: `ParametersRefValidator`
    - [x] `tags`: `TagsRefValidator` → `AsyncAPI3.channels[].tags`
    - [x] `external_docs`: `ExternalDocsRefValidator` →
      `AsyncAPI3.channels[].external_docs`
    - [ ] `bindings`: `ChannelBindingsRefValidator`

- [ ] `operations`: `Operations | None` (dict[str, Operation | Reference])
  - [ ] `Reference` values: `OperationsRefValidator`
  - [ ] `Operation` values:
    - [ ] `channel`: `ChannelsRefValidator`
    - [ ] `security`: `SecuritySchemesRefValidator`
    - [x] `tags`: `TagsRefValidator` → `AsyncAPI3.operations[].tags`
    - [x] `external_docs`: `ExternalDocsRefValidator` →
      `AsyncAPI3.operations[].external_docs`
    - [ ] `bindings`: `OperationBindingsRefValidator`
    - [ ] `traits`: `OperationTraitsRefValidator`
    - [ ] `messages`: `MessagesRefValidator`
    - [ ] `reply`: `RepliesRefValidator`

##### Root Level Objects

- [x] `info.tags`: `TagsRefValidator`
- [x] `info.external_docs`: `ExternalDocsRefValidator`
- [x] `info.tags[].external_docs`: `ExternalDocsRefValidator`

##### Nested Objects in Root Collections

###### Channels[].Messages[]

- [x] `channels[].messages[].tags`: `TagsRefValidator`
- [x] `channels[].messages[].external_docs`: `ExternalDocsRefValidator`
- [ ] `channels[].messages[].headers`: `SchemasRefValidator`
- [ ] `channels[].messages[].payload`: `SchemasRefValidator`
- [ ] `channels[].messages[].correlation_id`: `CorrelationIdsRefValidator`
- [ ] `channels[].messages[].bindings`: `MessageBindingsRefValidator`
- [x] `channels[].messages[].traits[].external_docs`: `ExternalDocsRefValidator`
- [x] `channels[].messages[].traits[].tags[].external_docs`: `ExternalDocsRefValidator`
- [ ] `channels[].messages[].traits[].headers`: `SchemasRefValidator`
- [ ] `channels[].messages[].traits[].correlation_id`: `CorrelationIdsRefValidator`
- [x] `channels[].messages[].traits[].tags`: `TagsRefValidator`
- [ ] `channels[].messages[].traits[].bindings`: `MessageBindingsRefValidator`

###### Operations[].Traits[]

- [x] `operations[].traits[].external_docs`: `ExternalDocsRefValidator`
- [x] `operations[].traits[].tags`: `TagsRefValidator`
- [x] `operations[].traits[].tags[].external_docs`: `ExternalDocsRefValidator`
- [ ] `operations[].traits[].security`: `SecuritySchemesRefValidator`
- [ ] `operations[].traits[].bindings`: `OperationBindingsRefValidator`

### Components Objects

#### Components.schemas

- [ ] `components.schemas[]`: `MultiFormatSchema | Schema | Reference`
  - [ ] `Reference` values: `SchemasRefValidator`
  - [ ] `Schema` values:
    - [x] `external_docs`: `ExternalDocsRefValidator` →
      `AsyncAPI3.components.schemas[].external_docs`

#### Components.servers

- [ ] `components.servers[]`: `Server | Reference`
  - [ ] `Reference` values: `ServersRefValidator`
  - [ ] `Server` values:
    - [ ] `variables[]`: `ServerVariablesRefValidator`
    - [ ] `security[]`: `SecuritySchemesRefValidator`
    - [x] `tags[]`: `TagsRefValidator` → `AsyncAPI3.components.servers[].tags`
    - [x] `external_docs`: `ExternalDocsRefValidator` →
      `AsyncAPI3.components.servers[].external_docs`
    - [ ] `bindings`: `ServerBindingsRefValidator`

#### Components.channels

- [ ] `components.channels[]`: `Channel | Reference`
  - [ ] `Reference` values: `ChannelsRefValidator`
  - [ ] `Channel` values:
    - [ ] `messages[]`: `MessagesRefValidator`
    - [ ] `servers[]`: `ServersRefValidator`
    - [ ] `parameters[]`: `ParametersRefValidator`
    - [x] `tags[]`: `TagsRefValidator` → `AsyncAPI3.components.channels[].tags`
    - [x] `external_docs`: `ExternalDocsRefValidator` →
      `AsyncAPI3.components.channels[].external_docs`
    - [ ] `bindings`: `ChannelBindingsRefValidator`

##### Components.channels[].messages[]

- [x] `components.channels[].messages[].tags[]`: `TagsRefValidator`
- [x] `components.channels[].messages[].external_docs`: `ExternalDocsRefValidator`
- [ ] `components.channels[].messages[].headers`: `SchemasRefValidator`
- [ ] `components.channels[].messages[].payload`: `SchemasRefValidator`
- [ ] `components.channels[].messages[].correlation_id`: `CorrelationIdsRefValidator`
- [ ] `components.channels[].messages[].bindings`: `MessageBindingsRefValidator`

##### Components.channels[].messages[].traits[]

- [x] `components.channels[].messages[].traits[].external_docs`:
  `ExternalDocsRefValidator`
- [x] `components.channels[].messages[].traits[].tags[]`: `TagsRefValidator`
- [x] `components.channels[].messages[].traits[].tags[].external_docs`:
  `ExternalDocsRefValidator`
- [ ] `components.channels[].messages[].traits[].headers`: `SchemasRefValidator`
- [ ] `components.channels[].messages[].traits[].correlation_id`:
  `CorrelationIdsRefValidator`
- [ ] `components.channels[].messages[].traits[].bindings`:
  `MessageBindingsRefValidator`

#### Components.operations

- [ ] `components.operations[]`: `Operation | Reference`
  - [ ] `Reference` values: `OperationsRefValidator`
  - [ ] `Operation` values:
    - [ ] `channel`: `ChannelsRefValidator`
    - [ ] `security[]`: `SecuritySchemesRefValidator`
    - [x] `tags[]`: `TagsRefValidator` → `AsyncAPI3.components.operations[].tags`
    - [x] `external_docs`: `ExternalDocsRefValidator` →
      `AsyncAPI3.components.operations[].external_docs`
    - [ ] `bindings`: `OperationBindingsRefValidator`
    - [ ] `traits[]`: `OperationTraitsRefValidator`
    - [ ] `messages[]`: `MessagesRefValidator`
    - [ ] `reply`: `RepliesRefValidator`

##### Components.operations[].traits[]

- [x] `components.operations[].traits[].external_docs`: `ExternalDocsRefValidator`
- [x] `components.operations[].traits[].tags[]`: `TagsRefValidator`
- [x] `components.operations[].traits[].tags[].external_docs`:
  `ExternalDocsRefValidator`
- [ ] `components.operations[].traits[].security[]`: `SecuritySchemesRefValidator`
- [ ] `components.operations[].traits[].bindings`: `OperationBindingsRefValidator`

#### Components.messages

- [ ] `components.messages[]`: `Message | Reference`
  - [ ] `Reference` values: `MessagesRefValidator`
  - [ ] `Message` values:
    - [x] `external_docs`: `ExternalDocsRefValidator` →
      `AsyncAPI3.components.messages[].external_docs`
    - [ ] `headers`: `SchemasRefValidator` → `AsyncAPI3.components.messages[].headers`
    - [ ] `payload`: `SchemasRefValidator` → `AsyncAPI3.components.messages[].payload`
    - [ ] `correlation_id`: `CorrelationIdsRefValidator`
    - [x] `tags[]`: `TagsRefValidator` → `AsyncAPI3.components.messages[].tags`
    - [ ] `bindings`: `MessageBindingsRefValidator`
    - [ ] `traits[]`: `MessageTraitsRefValidator`

##### Components.messages[].traits[]

- [x] `components.messages[].traits[].external_docs`: `ExternalDocsRefValidator`
- [x] `components.messages[].traits[].tags[]`: `TagsRefValidator`
- [x] `components.messages[].traits[].tags[].external_docs`: `ExternalDocsRefValidator`
- [ ] `components.messages[].traits[].headers`: `SchemasRefValidator`
- [ ] `components.messages[].traits[].correlation_id`: `CorrelationIdsRefValidator`
- [ ] `components.messages[].traits[].bindings`: `MessageBindingsRefValidator`

#### Components.securitySchemes

- [ ] `components.securitySchemes[]`: `SecurityScheme | Reference`
  - [ ] `Reference` values: `SecuritySchemesRefValidator`

#### Components.serverVariables

- [ ] `components.serverVariables[]`: `ServerVariable | Reference`
  - [ ] `Reference` values: `ServerVariablesRefValidator`

#### Components.parameters

- [ ] `components.parameters[]`: `Parameter | Reference`
  - [ ] `Reference` values: `ParametersRefValidator`

#### Components.correlationIds

- [ ] `components.correlationIds[]`: `CorrelationID | Reference`
  - [ ] `Reference` values: `CorrelationIdsRefValidator`

#### Components.replies

- [ ] `components.replies[]`: `OperationReply | Reference`
  - [ ] `Reference` values: `RepliesRefValidator`
  - [ ] `OperationReply` values:
    - [ ] `address`: `ReplyAddressesRefValidator`
    - [ ] `channel`: `ChannelsRefValidator`
    - [ ] `messages[]`: `MessagesRefValidator`

#### Components.replyAddresses

- [ ] `components.replyAddresses[]`: `OperationReplyAddress | Reference`
  - [ ] `Reference` values: `ReplyAddressesRefValidator`

#### Components.externalDocs

- [ ] `components.externalDocs[]`: `ExternalDocumentation | Reference`
  - [ ] `Reference` values: `ExternalDocsRefValidator`
  - [ ] `ExternalDocumentation` values: self-referencing validation

#### Components.tags

- [ ] `components.tags[]`: `Tag | Reference`
  - [x] `Reference` values: `TagsRefValidator`
  - [ ] `Tag` values:
    - [x] `external_docs`: `ExternalDocsRefValidator` →
      `AsyncAPI3.components.tags[].external_docs`

#### Components Traits

- [ ] `components.operationTraits[]`: `OperationTrait | Reference`
  - [ ] `Reference` values: `OperationTraitsRefValidator`
  - [ ] `OperationTrait` values:
    - [x] `external_docs`: `ExternalDocsRefValidator` →
      `AsyncAPI3.components.operationTraits[].external_docs`
    - [x] `tags[]`: `TagsRefValidator` → `AsyncAPI3.components.operationTraits[].tags`
    - [ ] `security[]`: `SecuritySchemesRefValidator`
    - [ ] `bindings`: `OperationBindingsRefValidator`

- [ ] `components.messageTraits[]`: `MessageTrait | Reference`
  - [ ] `Reference` values: `MessageTraitsRefValidator`
  - [ ] `MessageTrait` values:
    - [x] `external_docs`: `ExternalDocsRefValidator` →
      `AsyncAPI3.components.messageTraits[].external_docs`
    - [x] `tags[]`: `TagsRefValidator` → `AsyncAPI3.components.messageTraits[].tags`
    - [ ] `headers`: `SchemasRefValidator` →
      `AsyncAPI3.components.messageTraits[].headers`
    - [ ] `correlation_id`: `CorrelationIdsRefValidator`
    - [ ] `bindings`: `MessageBindingsRefValidator`

#### Components Bindings

- [ ] `components.serverBindings[]`: `ServerBindingsObject | Reference`
  - [ ] `Reference` values: `ServerBindingsRefValidator`

- [ ] `components.channelBindings[]`: `ChannelBindingsObject | Reference`
  - [ ] `Reference` values: `ChannelBindingsRefValidator`

- [ ] `components.operationBindings[]`: `OperationBindingsObject | Reference`
  - [ ] `Reference` values: `OperationBindingsRefValidator`

- [ ] `components.messageBindings[]`: `MessageBindingsObject | Reference`
  - [ ] `Reference` values: `MessageBindingsRefValidator`

### Bindings Objects

#### HTTP Bindings

- [ ] `bindings.http.operation.query`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

- [ ] `bindings.http.message.headers`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

#### MQTT Bindings

- [ ] `bindings.mqtt.server.session_expiry_interval`: `int | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `bindings.mqtt.server.maximum_packet_size`: `int | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `bindings.mqtt.operation.message_expiry_interval`:
  `int | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `bindings.mqtt.message.correlation_data`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `bindings.mqtt.message.response_topic`: `str | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

#### Kafka Bindings

- [ ] `bindings.kafka.operation.group_id`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `bindings.kafka.operation.client_id`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `bindings.kafka.message.key`: `Schema | Reference | dict[str, Any] | None`
  - [ ] Validated by `SchemasRefValidator`

#### WebSockets Bindings

- [ ] `bindings.websockets.channel.query`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `bindings.websockets.channel.headers`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

#### MQTT5 Bindings

- [ ] `bindings.mqtt5.server.session_expiry_interval`: `int | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

#### JMS Bindings

- [ ] `bindings.jms.message.headers`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

#### AnypointMQ Bindings

- [ ] `bindings.anypointmq.message.headers`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

#### Solace Bindings

- [ ] `bindings.solace.operation.time_to_live`: `int | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `bindings.solace.operation.priority`: `int | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

### Other Objects

#### Base Objects

- [x] `*.external_docs`: `ExternalDocumentation | Reference | None` (in various objects)
  - [x] Validated by `ExternalDocsRefValidator`; Allows the following values:
    - [x] External values with warning
    - [x] `#/components/externalDocs/{external_doc_name}`

- [x] `*.tags`: `Tags | None` (list[Tag | Reference]) (in various objects)
  - [x] Validated by `TagsRefValidator`; Allows the following values:
    - [x] External values with warning
    - [x] `#/components/tags/{tag_name}`

## Per Model file data

### `asyncapi3/models/base.py`

#### Tag

- [x] `external_docs`: `ExternalDocumentation | Reference | None`
  - [x] Validated by `ExternalDocsRefValidator`; Allows the following values:
    - [x] External values with warning
    - [x] `#/components/externalDocs/{external_doc_name}`

### `asyncapi3/models/info.py`

#### Info

- [x] `tags`: `Tags | None` (`list[Tag | Reference]`)
  - [x] Validated by `TagsRefValidator`; Allows the following values:
    - [x] External values with warning
    - [x] `#/components/tags/{key}`
- [x] `external_docs`: `ExternalDocumentation | Reference | None`
  - [x] Validated by `ExternalDocsRefValidator`; Allows the following values:
    - [x] External values with warning
    - [x] `#/components/externalDocs/{external_doc_name}`

### `asyncapi3/models/server.py`

#### Server

- [ ] `variables`: `dict[str, ServerVariable | Reference] | None`
  - [ ] Validated by `ServerVariablesRefValidator`
- [ ] `security`: `list[SecurityScheme | Reference] | None`
  - [ ] Validated by `SecuritySchemesRefValidator`
- [x] `tags`: `Tags | None` (`list[Tag | Reference]`)
  - [x] Validated by `TagsRefValidator` (when in `AsyncAPI3.servers`)
- [x] `external_docs`: `ExternalDocumentation | Reference | None`
  - [x] Validated by `ExternalDocsRefValidator`; Allows the following values:
    - [x] External values with warning
    - [x] `#/components/externalDocs/{external_doc_name}`
- [ ] `bindings`: `ServerBindingsObject | Reference | None`
  - [ ] Validated by `ServerBindingsRefValidator`

### `asyncapi3/models/channel.py`

#### Channel

- [ ] `messages`: `Messages | None` (dict[str, Message | Reference])
  - [ ] Validated by `MessagesRefValidator`
- [ ] `servers`: `list[Reference] | None`
  - [ ] Validated by `ServersRefValidator`
- [ ] `parameters`: `Parameters | None` (dict[str, Parameter | Reference])
  - [ ] Validated by `ParametersRefValidator`
- [x] `tags`: `Tags | None` (`list[Tag | Reference]`)
  - [x] Validated by `TagsRefValidator`
- [x] `external_docs`: `ExternalDocumentation | Reference | None`
  - [x] Validated by `ExternalDocsRefValidator`; Allows the following values:
    - [x] External values with warning
    - [x] `#/components/externalDocs/{external_doc_name}`
- [ ] `bindings`: `ChannelBindingsObject | Reference | None`
  - [ ] Validated by `ChannelBindingsRefValidator`

### `asyncapi3/models/operation.py`

#### OperationReply

- [ ] `address`: `OperationReplyAddress | Reference | None`
  - [ ] Validated by `ReplyAddressesRefValidator`
- [ ] `channel`: `Reference | None`
  - [ ] Validated by `ChannelsRefValidator`
- [ ] `messages`: `list[Reference] | None`
  - [ ] Validated by `MessagesRefValidator`
  - [x] `tags` validated by `TagsRefValidator` (indirectly via referenced channel)

#### OperationTrait

- [ ] `security`: `list[SecurityScheme | Reference] | None`
  - [ ] Validated by `SecuritySchemesRefValidator`
- [x] `tags`: `Tags | None` (`list[Tag | Reference]`)
  - [x] Validated by `TagsRefValidator`
- [x] `external_docs`: `ExternalDocumentation | Reference | None`
  - [x] Validated by `ExternalDocsRefValidator`; Allows the following values:
    - [x] External values with warning
    - [x] `#/components/externalDocs/{external_doc_name}`
- [ ] `bindings`: `OperationBindingsObject | Reference | None`
  - [ ] Validated by `OperationBindingsRefValidator`

#### Operation

- [ ] `channel`: `Reference`
  - [ ] Validated by `ChannelsRefValidator`
- [ ] `security`: `list[SecurityScheme | Reference] | None`
  - [ ] Validated by `SecuritySchemesRefValidator`
- [x] `tags`: `Tags | None` (`list[Tag | Reference]`)
  - [x] Validated by `TagsRefValidator`
- [x] `external_docs`: `ExternalDocumentation | Reference | None`
  - [x] Validated by `ExternalDocsRefValidator`; Allows the following values:
    - [x] External values with warning
    - [x] `#/components/externalDocs/{external_doc_name}`
- [ ] `bindings`: `OperationBindingsObject | Reference | None`
  - [ ] Validated by `OperationBindingsRefValidator`
- [ ] `traits`: `list[OperationTrait | Reference] | None`
  - [ ] Validated by `OperationTraitsRefValidator`
- [ ] `messages`: `list[Reference] | None`
  - [ ] Validated by `MessagesRefValidator`
- [ ] `reply`: `OperationReply | Reference | None`
  - [ ] Validated by `RepliesRefValidator`

### `asyncapi3/models/message.py`

#### MessageTrait

- [ ] `headers`: `MultiFormatSchema | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `correlation_id`: `CorrelationID | Reference | None`
  - [ ] Validated by `CorrelationIdsRefValidator`
- [x] `tags`: `Tags | None` (`list[Tag | Reference]`)
  - [x] Validated by `TagsRefValidator`
- [x] `external_docs`: `ExternalDocumentation | Reference | None`
  - [x] Validated by `ExternalDocsRefValidator`; Allows the following values:
    - [x] External values with warning
    - [x] `#/components/externalDocs/{external_doc_name}`
- [ ] `bindings`: `MessageBindingsObject | Reference | None`
  - [ ] Validated by `MessageBindingsRefValidator`

#### Message

- [ ] `headers`: `MultiFormatSchema | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `payload`: `MultiFormatSchema | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `correlation_id`: `CorrelationID | Reference | None`
  - [ ] Validated by `CorrelationIdsRefValidator`
- [x] `tags`: `Tags | None` (`list[Tag | Reference]`)
  - [x] Validated by `TagsRefValidator`
- [x] `external_docs`: `ExternalDocumentation | Reference | None`
  - [x] Validated by `ExternalDocsRefValidator`; Allows the following values:
    - [x] External values with warning
    - [x] `#/components/externalDocs/{external_doc_name}`
- [ ] `bindings`: `MessageBindingsObject | Reference | None`
  - [ ] Validated by `MessageBindingsRefValidator`
- [ ] `traits`: `list[MessageTrait | Reference] | None`
  - [ ] Validated by `MessageTraitsRefValidator`

### `asyncapi3/models/components.py`

#### Components

- [ ] `schemas`: `Schemas | None` (dict[str, MultiFormatSchema | Schema | Reference])
  - [ ] `Reference` values: `SchemasRefValidator`
  - [ ] `Schema` values:
    - [x] `external_docs`: `ExternalDocsRefValidator`
- [ ] `servers`: `Servers | None` (dict[str, Server | Reference])
  - [ ] `Reference` values: `ServersRefValidator`
  - [ ] `Server` values:
    - [ ] `variables`: `ServerVariablesRefValidator`
    - [ ] `security`: `SecuritySchemesRefValidator`
    - [x] `tags`: `TagsRefValidator`
    - [x] `external_docs`: `ExternalDocsRefValidator`
    - [ ] `bindings`: `ServerBindingsRefValidator`
- [ ] `channels`: `Channels | None` (dict[str, Channel | Reference])
  - [ ] `Reference` values: `ChannelsRefValidator`
  - [ ] `Channel` values:
    - [ ] `messages`: `MessagesRefValidator`
    - [ ] `servers`: `ServersRefValidator`
    - [ ] `parameters`: `ParametersRefValidator`
    - [x] `tags`: `TagsRefValidator`
    - [x] `external_docs`: `ExternalDocsRefValidator`
    - [ ] `bindings`: `ChannelBindingsRefValidator`
- [ ] `operations`: `Operations | None` (dict[str, Operation | Reference])
  - [ ] `Reference` values: `OperationsRefValidator`
  - [ ] `Operation` values:
    - [ ] `channel`: `ChannelsRefValidator`
    - [ ] `security`: `SecuritySchemesRefValidator`
    - [x] `tags`: `TagsRefValidator`
    - [x] `external_docs`: `ExternalDocsRefValidator`
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
    - [x] `external_docs`: `ExternalDocsRefValidator`
    - [ ] `bindings`: `MessageBindingsRefValidator`
    - [ ] `traits`: `MessageTraitsRefValidator`
- [ ] `security_schemes`: `SecuritySchemes | None` (
  dict[str, SecurityScheme | Reference])
- [ ] `server_variables`: `ServerVariables | None` (
  dict[str, ServerVariable | Reference])
- [ ] `parameters`: `Parameters | None` (dict[str, Parameter | Reference])
- [ ] `correlation_ids`: `CorrelationIDs | None` (dict[str, CorrelationID | Reference])
- [ ] `replies`: `Replies | None` (dict[str, OperationReply | Reference])
  - [ ] `Reference` values: `RepliesRefValidator`
  - [ ] `OperationReply` values:
    - [ ] `address`: `ReplyAddressesRefValidator`
    - [ ] `channel`: `ChannelsRefValidator`
    - [ ] `messages`: `MessagesRefValidator`
- [ ] `reply_addresses`: `ReplyAddresses | None` (
  dict[str, OperationReplyAddress | Reference])
- [ ] `external_docs`: `ExternalDocs | None` (
  dict[str, ExternalDocumentation | Reference])
- [ ] `tags`: `TagsDict | None` (dict[str, Tag | Reference])
  - [x] `Reference` values: `TagsRefValidator`
  - [ ] `Tag` values:
    - [x] `external_docs`: `ExternalDocsRefValidator`
- [ ] `operation_traits`: `OperationTraits | None` (
  dict[str, OperationTrait | Reference])
  - [ ] `Reference` values: `OperationTraitsRefValidator`
  - [ ] `OperationTrait` values:
    - [ ] `security`: `SecuritySchemesRefValidator`
    - [x] `tags`: `TagsRefValidator`
    - [x] `external_docs`: `ExternalDocsRefValidator`
    - [ ] `bindings`: `OperationBindingsRefValidator`
- [ ] `message_traits`: `MessageTraits | None` (dict[str, MessageTrait | Reference])
  - [ ] `Reference` values: `MessageTraitsRefValidator`
  - [ ] `MessageTrait` values:
    - [ ] `headers`: `SchemasRefValidator`
    - [ ] `correlation_id`: `CorrelationIdsRefValidator`
    - [x] `tags`: `TagsRefValidator`
    - [x] `external_docs`: `ExternalDocsRefValidator`
    - [ ] `bindings`: `MessageBindingsRefValidator`
- [ ] `server_bindings`: `ServerBindings | None`
  (dict[str, ServerBindingsObject | Reference])
- [ ] `channel_bindings`: `ChannelBindings | None`
  (dict[str, ChannelBindingsObject | Reference])
- [ ] `operation_bindings`: `OperationBindings | None`
  (dict[str, OperationBindingsObject | Reference])
- [ ] `message_bindings`: `MessageBindings | None`
  (dict[str, MessageBindingsObject | Reference])

### `asyncapi3/models/schema.py`

#### Schema

- [ ] `external_docs`: `ExternalDocumentation | Reference | None`
  - [ ] Validated by `ExternalDocsRefValidator`; Allows the following values:
    - [ ] External values with warning
    - [ ] `#/components/externalDocs/{external_doc_name}`

### `asyncapi3/models/bindings/http.py`

#### HTTPOperationBindings

- [ ] `query`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

#### HTTPMessageBindings

- [ ] `headers`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

### `asyncapi3/models/bindings/mqtt.py`

#### MQTTServerBindings

- [ ] `session_expiry_interval`: `int | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `maximum_packet_size`: `int | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

#### MQTTOperationBindings

- [ ] `message_expiry_interval`: `int | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

#### MQTTMessageBindings

- [ ] `correlation_data`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `response_topic`: `str | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

### `asyncapi3/models/bindings/kafka.py`

#### KafkaOperationBindings

- [ ] `group_id`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `client_id`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

#### KafkaMessageBindings

- [ ] `key`: `Schema | Reference | dict[str, Any] | None`
  - [ ] Validated by `SchemasRefValidator`

### `asyncapi3/models/bindings/websockets.py`

#### WebSocketsChannelBindings

- [ ] `query`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `headers`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

### `asyncapi3/models/bindings/mqtt5.py`

#### MQTT5ServerBindings

- [ ] `session_expiry_interval`: `int | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

### `asyncapi3/models/bindings/jms.py`

#### JMSMessageBindings

- [ ] `headers`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

### `asyncapi3/models/bindings/anypointmq.py`

#### AnypointMQMessageBindings

- [ ] `headers`: `Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

### `asyncapi3/models/bindings/solace.py`

#### SolaceOperationBindings

- [ ] `time_to_live`: `int | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`
- [ ] `priority`: `int | Schema | Reference | None`
  - [ ] Validated by `SchemasRefValidator`

## Per Validator data

### `asyncapi3/validators/channel_bindings_ref_validator.py`

#### ChannelBindingsRefValidator

- [ ] Verified fields:
  - [ ] `AsyncAPI3.channels[].bindings`
  - [ ] `AsyncAPI3.components.channels[].bindings`
  - [ ] `AsyncAPI3.components.channelBindings[]`

### `asyncapi3/validators/channels_ref_validator.py`

#### ChannelsRefValidator

- [ ] Verified fields:
  - [ ] `AsyncAPI3.channels[]`
  - [ ] `AsyncAPI3.operations[].channel`
  - [ ] `AsyncAPI3.operations[].reply.channel`
  - [ ] `AsyncAPI3.components.channels[]`

### `asyncapi3/validators/correlation_ids_ref_validator.py`

#### CorrelationIdsRefValidator

- [ ] Verified fields:
  - [ ] `AsyncAPI3.messages[].correlation_id`
  - [ ] `AsyncAPI3.messageTraits[].correlation_id`
  - [ ] `AsyncAPI3.channels[].messages[].correlation_id`
  - [ ] `AsyncAPI3.channels[].messages[].traits[].correlation_id`
  - [ ] `AsyncAPI3.components.messages[].correlation_id`
  - [ ] `AsyncAPI3.components.messageTraits[].correlation_id`
  - [ ] `AsyncAPI3.components.channels[].messages[].correlation_id`
  - [ ] `AsyncAPI3.components.channels[].messages[].traits[].correlation_id`
  - [ ] `AsyncAPI3.components.correlationIds[]`

### `asyncapi3/validators/external_docs_ref_validator.py`

#### ExternalDocsRefValidator

- [x] Allowed values:
  - [x] External values with warning
  - [x] `#/components/externalDocs/{external_doc_name}`
- [x] Verified fields:
  - [x] `AsyncAPI3.info.external_docs`
  - [x] `AsyncAPI3.info.tags[].external_docs`
  - [x] `AsyncAPI3.servers[].external_docs`
  - [x] `AsyncAPI3.channels[].external_docs`
  - [x] `AsyncAPI3.channels[].messages[].external_docs`
  - [x] `AsyncAPI3.channels[].messages[].traits[].external_docs`
  - [x] `AsyncAPI3.channels[].messages[].traits[].tags[].external_docs`
  - [x] `AsyncAPI3.operations[].external_docs`
  - [x] `AsyncAPI3.operations[].traits[].external_docs`
  - [x] `AsyncAPI3.operations[].traits[].tags[].external_docs`
  - [x] `AsyncAPI3.components.schemas[].external_docs`
  - [x] `AsyncAPI3.components.servers[].external_docs`
  - [x] `AsyncAPI3.components.channels[].external_docs`
  - [x] `AsyncAPI3.components.channels[].messages[].external_docs`
  - [x] `AsyncAPI3.components.channels[].messages[].traits[].external_docs`
  - [x] `AsyncAPI3.components.channels[].messages[].traits[].tags[].external_docs`
  - [x] `AsyncAPI3.components.operations[].external_docs`
  - [x] `AsyncAPI3.components.operations[].traits[].external_docs`
  - [x] `AsyncAPI3.components.operations[].traits[].tags[].external_docs`
  - [x] `AsyncAPI3.components.messages[].external_docs`
  - [x] `AsyncAPI3.components.messages[].traits[].external_docs`
  - [x] `AsyncAPI3.components.messages[].traits[].tags[].external_docs`
  - [x] `AsyncAPI3.components.tags[].external_docs`
  - [x] `AsyncAPI3.components.operationTraits[].external_docs`
  - [x] `AsyncAPI3.components.messageTraits[].external_docs`
  - [x] `AsyncAPI3.components.external_docs`

### `asyncapi3/validators/message_bindings_ref_validator.py`

#### MessageBindingsRefValidator

- [ ] Verified fields:
  - [ ] `AsyncAPI3.messages[].bindings`
  - [ ] `AsyncAPI3.messageTraits[].bindings`
  - [ ] `AsyncAPI3.channels[].messages[].bindings`
  - [ ] `AsyncAPI3.channels[].messages[].traits[].bindings`
  - [ ] `AsyncAPI3.components.messages[].bindings`
  - [ ] `AsyncAPI3.components.messageTraits[].bindings`
  - [ ] `AsyncAPI3.components.channels[].messages[].bindings`
  - [ ] `AsyncAPI3.components.channels[].messages[].traits[].bindings`
  - [ ] `AsyncAPI3.components.messageBindings[]`

### `asyncapi3/validators/message_traits_ref_validator.py`

#### MessageTraitsRefValidator

- [ ] Verified fields:
  - [ ] `AsyncAPI3.messages[].traits[]`
  - [ ] `AsyncAPI3.channels[].messages[].traits[]`
  - [ ] `AsyncAPI3.components.messages[].traits[]`
  - [ ] `AsyncAPI3.components.channels[].messages[].traits[]`
  - [ ] `AsyncAPI3.components.messageTraits[]`

### `asyncapi3/validators/messages_ref_validator.py`

#### MessagesRefValidator

- [ ] Verified fields:
  - [ ] `AsyncAPI3.channels[].messages[]`
  - [ ] `AsyncAPI3.operations[].messages[]`
  - [ ] `AsyncAPI3.operations[].reply.messages[]`
  - [ ] `AsyncAPI3.components.channels[].messages[]`
  - [ ] `AsyncAPI3.components.operations[].messages[]`
  - [ ] `AsyncAPI3.components.replies[].messages[]`
  - [ ] `AsyncAPI3.components.messages[]`

### `asyncapi3/validators/operation_bindings_ref_validator.py`

#### OperationBindingsRefValidator

- [ ] Verified fields:
  - [ ] `AsyncAPI3.operations[].bindings`
  - [ ] `AsyncAPI3.operations[].traits[].bindings`
  - [ ] `AsyncAPI3.components.operations[].bindings`
  - [ ] `AsyncAPI3.components.operationTraits[].bindings`
  - [ ] `AsyncAPI3.components.operationBindings[]`

### `asyncapi3/validators/operation_traits_ref_validator.py`

#### OperationTraitsRefValidator

- [ ] Verified fields:
  - [ ] `AsyncAPI3.operations[].traits[]`
  - [ ] `AsyncAPI3.components.operations[].traits[]`
  - [ ] `AsyncAPI3.components.operationTraits[]`

### `asyncapi3/validators/operations_ref_validator.py`

#### OperationsRefValidator

- [ ] Verified fields:
  - [ ] `AsyncAPI3.operations[]`
  - [ ] `AsyncAPI3.components.operations[]`

### `asyncapi3/validators/parameters_ref_validator.py`

#### ParametersRefValidator

- [ ] Verified fields:
  - [ ] `AsyncAPI3.channels[].parameters[]`
  - [ ] `AsyncAPI3.components.channels[].parameters[]`
  - [ ] `AsyncAPI3.components.parameters[]`

### `asyncapi3/validators/replies_ref_validator.py`

#### RepliesRefValidator

- [ ] Verified fields:
  - [ ] `AsyncAPI3.operations[].reply`
  - [ ] `AsyncAPI3.components.operations[].reply`
  - [ ] `AsyncAPI3.components.replies[]`

### `asyncapi3/validators/reply_addresses_ref_validator.py`

#### ReplyAddressesRefValidator

- [ ] Verified fields:
  - [ ] `AsyncAPI3.operations[].reply.address`
  - [ ] `AsyncAPI3.components.operations[].reply.address`
  - [ ] `AsyncAPI3.components.replies[].address`
  - [ ] `AsyncAPI3.components.replyAddresses[]`

### `asyncapi3/validators/schemas_ref_validator.py`

#### SchemasRefValidator

- [ ] Verified fields:
  - [ ] `AsyncAPI3.messages[].headers`
  - [ ] `AsyncAPI3.messages[].payload`
  - [ ] `AsyncAPI3.messageTraits[].headers`
  - [ ] `AsyncAPI3.channels[].messages[].headers`
  - [ ] `AsyncAPI3.channels[].messages[].payload`
  - [ ] `AsyncAPI3.channels[].messages[].traits[].headers`
  - [ ] `AsyncAPI3.operations[].messages[].headers`
  - [ ] `AsyncAPI3.operations[].messages[].payload`
  - [ ] `AsyncAPI3.operations[].reply.messages[].headers`
  - [ ] `AsyncAPI3.operations[].reply.messages[].payload`
  - [ ] `AsyncAPI3.components.schemas`
  - [ ] `AsyncAPI3.components.messages[].headers`
  - [ ] `AsyncAPI3.components.messages[].payload`
  - [ ] `AsyncAPI3.components.messageTraits[].headers`
  - [ ] `AsyncAPI3.components.channels[].messages[].headers`
  - [ ] `AsyncAPI3.components.channels[].messages[].payload`
  - [ ] `AsyncAPI3.components.channels[].messages[].traits[].headers`
  - [ ] `AsyncAPI3.components.operations[].messages[].headers`
  - [ ] `AsyncAPI3.components.operations[].messages[].payload`
  - [ ] `AsyncAPI3.components.replies[].messages[].headers`
  - [ ] `AsyncAPI3.components.replies[].messages[].payload`
  - [ ] `AsyncAPI3.servers[].bindings.http.query` (HTTPOperationBindings)
  - [ ] `AsyncAPI3.servers[].bindings.mqtt.session_expiry_interval` (MQTTServerBindings)
  - [ ] `AsyncAPI3.servers[].bindings.mqtt.maximum_packet_size` (MQTTServerBindings)
  - [ ] `AsyncAPI3.servers[].bindings.mqtt5.session_expiry_interval` (
    MQTT5ServerBindings)
  - [ ] `AsyncAPI3.operations[].bindings.http.query` (HTTPOperationBindings)
  - [ ] `AsyncAPI3.operations[].bindings.mqtt.message_expiry_interval` (
    MQTTOperationBindings)
  - [ ] `AsyncAPI3.operations[].bindings.kafka.group_id` (KafkaOperationBindings)
  - [ ] `AsyncAPI3.operations[].bindings.kafka.client_id` (KafkaOperationBindings)
  - [ ] `AsyncAPI3.operations[].bindings.solace.time_to_live` (SolaceOperationBindings)
  - [ ] `AsyncAPI3.operations[].bindings.solace.priority` (SolaceOperationBindings)
  - [ ] `AsyncAPI3.operations[].traits[].bindings.http.query` (HTTPOperationBindings)
  - [ ] `AsyncAPI3.operations[].traits[].bindings.mqtt.message_expiry_interval` (
    MQTTOperationBindings)
  - [ ] `AsyncAPI3.operations[].traits[].bindings.kafka.group_id` (
    KafkaOperationBindings)
  - [ ] `AsyncAPI3.operations[].traits[].bindings.kafka.client_id` (
    KafkaOperationBindings)
  - [ ] `AsyncAPI3.operations[].traits[].bindings.solace.time_to_live` (
    SolaceOperationBindings)
  - [ ] `AsyncAPI3.operations[].traits[].bindings.solace.priority` (
    SolaceOperationBindings)
  - [ ] `AsyncAPI3.channels[].bindings.websockets.query` (WebSocketsChannelBindings)
  - [ ] `AsyncAPI3.channels[].bindings.websockets.headers` (WebSocketsChannelBindings)
  - [ ] `AsyncAPI3.messages[].bindings.http.headers` (HTTPMessageBindings)
  - [ ] `AsyncAPI3.messages[].bindings.mqtt.correlation_data` (MQTTMessageBindings)
  - [ ] `AsyncAPI3.messages[].bindings.mqtt.response_topic` (MQTTMessageBindings)
  - [ ] `AsyncAPI3.messages[].bindings.kafka.key` (KafkaMessageBindings)
  - [ ] `AsyncAPI3.messages[].bindings.jms.headers` (JMSMessageBindings)
  - [ ] `AsyncAPI3.messages[].bindings.anypointmq.headers` (AnypointMQMessageBindings)
  - [ ] `AsyncAPI3.messageTraits[].bindings.http.headers` (HTTPMessageBindings)
  - [ ] `AsyncAPI3.messageTraits[].bindings.mqtt.correlation_data` (MQTTMessageBindings)
  - [ ] `AsyncAPI3.messageTraits[].bindings.mqtt.response_topic` (MQTTMessageBindings)
  - [ ] `AsyncAPI3.messageTraits[].bindings.kafka.key` (KafkaMessageBindings)
  - [ ] `AsyncAPI3.messageTraits[].bindings.jms.headers` (JMSMessageBindings)
  - [ ] `AsyncAPI3.messageTraits[].bindings.anypointmq.headers` (
    AnypointMQMessageBindings)
  - [ ] `AsyncAPI3.channels[].messages[].bindings.http.headers` (HTTPMessageBindings)
  - [ ] `AsyncAPI3.channels[].messages[].bindings.mqtt.correlation_data` (
    MQTTMessageBindings)
  - [ ] `AsyncAPI3.channels[].messages[].bindings.mqtt.response_topic` (
    MQTTMessageBindings)
  - [ ] `AsyncAPI3.channels[].messages[].bindings.kafka.key` (KafkaMessageBindings)
  - [ ] `AsyncAPI3.channels[].messages[].bindings.jms.headers` (JMSMessageBindings)
  - [ ] `AsyncAPI3.channels[].messages[].bindings.anypointmq.headers` (
    AnypointMQMessageBindings)
  - [ ] `AsyncAPI3.channels[].messages[].traits[].bindings.http.headers` (
    HTTPMessageBindings)
  - [ ] `AsyncAPI3.channels[].messages[].traits[].bindings.mqtt.correlation_data` (
    MQTTMessageBindings)
  - [ ] `AsyncAPI3.channels[].messages[].traits[].bindings.mqtt.response_topic` (
    MQTTMessageBindings)
  - [ ] `AsyncAPI3.channels[].messages[].traits[].bindings.kafka.key` (
    KafkaMessageBindings)
  - [ ] `AsyncAPI3.channels[].messages[].traits[].bindings.jms.headers` (
    JMSMessageBindings)
  - [ ] `AsyncAPI3.channels[].messages[].traits[].bindings.anypointmq.headers` (
    AnypointMQMessageBindings)
  - [ ] `AsyncAPI3.components.servers[].bindings.http.query` (HTTPOperationBindings)
  - [ ] `AsyncAPI3.components.servers[].bindings.mqtt.session_expiry_interval` (
    MQTTServerBindings)
  - [ ] `AsyncAPI3.components.servers[].bindings.mqtt.maximum_packet_size` (
    MQTTServerBindings)
  - [ ] `AsyncAPI3.components.servers[].bindings.mqtt5.session_expiry_interval` (
    MQTT5ServerBindings)
  - [ ] `AsyncAPI3.components.operations[].bindings.http.query` (HTTPOperationBindings)
  - [ ] `AsyncAPI3.components.operations[].bindings.mqtt.message_expiry_interval` (
    MQTTOperationBindings)
  - [ ] `AsyncAPI3.components.operations[].bindings.kafka.group_id` (
    KafkaOperationBindings)
  - [ ] `AsyncAPI3.components.operations[].bindings.kafka.client_id` (
    KafkaOperationBindings)
  - [ ] `AsyncAPI3.components.operations[].bindings.solace.time_to_live` (
    SolaceOperationBindings)
  - [ ] `AsyncAPI3.components.operations[].bindings.solace.priority` (
    SolaceOperationBindings)
  - [ ] `AsyncAPI3.components.operationTraits[].bindings.http.query` (
    HTTPOperationBindings)
  - [ ] `AsyncAPI3.components.operationTraits[].bindings.mqtt.message_expiry_interval` (
    MQTTOperationBindings)
  - [ ] `AsyncAPI3.components.operationTraits[].bindings.kafka.group_id` (
    KafkaOperationBindings)
  - [ ] `AsyncAPI3.components.operationTraits[].bindings.kafka.client_id` (
    KafkaOperationBindings)
  - [ ] `AsyncAPI3.components.operationTraits[].bindings.solace.time_to_live` (
    SolaceOperationBindings)
  - [ ] `AsyncAPI3.components.operationTraits[].bindings.solace.priority` (
    SolaceOperationBindings)
  - [ ] `AsyncAPI3.components.channels[].bindings.websockets.query` (
    WebSocketsChannelBindings)
  - [ ] `AsyncAPI3.components.channels[].bindings.websockets.headers` (
    WebSocketsChannelBindings)
  - [ ] `AsyncAPI3.components.messages[].bindings.http.headers` (HTTPMessageBindings)
  - [ ] `AsyncAPI3.components.messages[].bindings.mqtt.correlation_data` (
    MQTTMessageBindings)
  - [ ] `AsyncAPI3.components.messages[].bindings.mqtt.response_topic` (
    MQTTMessageBindings)
  - [ ] `AsyncAPI3.components.messages[].bindings.kafka.key` (KafkaMessageBindings)
  - [ ] `AsyncAPI3.components.messages[].bindings.jms.headers` (JMSMessageBindings)
  - [ ] `AsyncAPI3.components.messages[].bindings.anypointmq.headers` (
    AnypointMQMessageBindings)
  - [ ] `AsyncAPI3.components.messageTraits[].bindings.http.headers` (
    HTTPMessageBindings)
  - [ ] `AsyncAPI3.components.messageTraits[].bindings.mqtt.correlation_data` (
    MQTTMessageBindings)
  - [ ] `AsyncAPI3.components.messageTraits[].bindings.mqtt.response_topic` (
    MQTTMessageBindings)
  - [ ] `AsyncAPI3.components.messageTraits[].bindings.kafka.key` (KafkaMessageBindings)
  - [ ] `AsyncAPI3.components.messageTraits[].bindings.jms.headers` (JMSMessageBindings)
  - [ ] `AsyncAPI3.components.messageTraits[].bindings.anypointmq.headers` (
    AnypointMQMessageBindings)
  - [ ] `AsyncAPI3.components.channels[].messages[].bindings.http.headers` (
    HTTPMessageBindings)
  - [ ] `AsyncAPI3.components.channels[].messages[].bindings.mqtt.correlation_data` (
    MQTTMessageBindings)
  - [ ] `AsyncAPI3.components.channels[].messages[].bindings.mqtt.response_topic` (
    MQTTMessageBindings)
  - [ ] `AsyncAPI3.components.channels[].messages[].bindings.kafka.key` (
    KafkaMessageBindings)
  - [ ] `AsyncAPI3.components.channels[].messages[].bindings.jms.headers` (
    JMSMessageBindings)
  - [ ] `AsyncAPI3.components.channels[].messages[].bindings.anypointmq.headers` (
    AnypointMQMessageBindings)
  - [ ] `AsyncAPI3.components.channels[].messages[].traits[].bindings.http.headers` (
    HTTPMessageBindings)
  - [ ]
    `AsyncAPI3.components.channels[].messages[].traits[].bindings.mqtt.
    correlation_data` (MQTTMessageBindings)
  - [ ]
    `AsyncAPI3.components.channels[].messages[].traits[].bindings.mqtt.response_topic` (
    MQTTMessageBindings)
  - [ ] `AsyncAPI3.components.channels[].messages[].traits[].bindings.kafka.key` (
    KafkaMessageBindings)
  - [ ] `AsyncAPI3.components.channels[].messages[].traits[].bindings.jms.headers` (
    JMSMessageBindings)
  - [ ]
    `AsyncAPI3.components.channels[].messages[].traits[].bindings.anypointmq.headers` (
    AnypointMQMessageBindings)

### `asyncapi3/validators/security_schemes_ref_validator.py`

#### SecuritySchemesRefValidator

- [ ] Verified fields:
  - [ ] `AsyncAPI3.servers[].security[]`
  - [ ] `AsyncAPI3.channels[].servers[]` (indirectly via server references)
  - [ ] `AsyncAPI3.operations[].security[]`
  - [ ] `AsyncAPI3.operations[].traits[].security[]`
  - [ ] `AsyncAPI3.components.servers[].security[]`
  - [ ] `AsyncAPI3.components.channels[].servers[]` (indirectly via server references)
  - [ ] `AsyncAPI3.components.operations[].security[]`
  - [ ] `AsyncAPI3.components.operationTraits[].security[]`
  - [ ] `AsyncAPI3.components.securitySchemes[]`

### `asyncapi3/validators/server_bindings_ref_validator.py`

#### ServerBindingsRefValidator

- [ ] Verified fields:
  - [ ] `AsyncAPI3.servers[].bindings`
  - [ ] `AsyncAPI3.components.servers[].bindings`
  - [ ] `AsyncAPI3.components.serverBindings[]`

### `asyncapi3/validators/server_variables_ref_validator.py`

#### ServerVariablesRefValidator

- [ ] Verified fields:
  - [ ] `AsyncAPI3.servers[].variables[]`
  - [ ] `AsyncAPI3.components.servers[].variables[]`
  - [ ] `AsyncAPI3.components.serverVariables[]`

### `asyncapi3/validators/servers_ref_validator.py`

#### ServersRefValidator

- [ ] Verified fields:
  - [ ] `AsyncAPI3.servers[]`
  - [ ] `AsyncAPI3.channels[].servers[]`
  - [ ] `AsyncAPI3.components.channels[].servers[]`
  - [ ] `AsyncAPI3.components.servers[]`

### `asyncapi3/validators/tags_ref_validator.py`

#### TagsRefValidator

- [x] Allowed values:
  - [x] External values with warning
  - [x] `#/components/tags/{tag_name}`
- [x] Verified fields:
  - [x] `AsyncAPI3.info.tags`
  - [x] `AsyncAPI3.servers[].tags`
  - [x] `AsyncAPI3.channels[].tags`
  - [x] `AsyncAPI3.channels[].messages[].tags`
  - [x] `AsyncAPI3.operations[].tags`
  - [x] `AsyncAPI3.components.messages[].tags`
  - [x] `AsyncAPI3.components.channels[].tags`
  - [x] `AsyncAPI3.components.channels[].messages[].tags`
  - [x] `AsyncAPI3.components.operations[].tags`
  - [x] `AsyncAPI3.components.servers[].tags`
  - [x] `AsyncAPI3.components.operationTraits[].tags`
  - [x] `AsyncAPI3.components.messageTraits[].tags`
  - [x] `AsyncAPI3.components.tags[]`
