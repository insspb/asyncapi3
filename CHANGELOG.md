# Changelog

## Unreleased

### ADDED

- #8: Strict pylint rules for imports location and other style issues
- #8: validate_patterned_key function for key validation in AsyncAPI models

### FIXED

- #8: Style issues

## [0.0.2] - 2026-01-14

### ADDED

- #5: Added: `__setitem__`, `__delitem__`, `__contains__`, `__len__` methods to
  PatternedRootModel and child models.

### CHANGED

- #4: Strict patterned object key validation - dots no longer allowed in keys for:
  - `AsyncAPI3.servers`;
  - `AsyncAPI3.channels`;
  - `AsyncAPI3.channels.messages`;
  - `AsyncAPI3.channels.parameters`;
  - `AsyncAPI3.operations`;
  - `AsyncAPI3.components.servers`;
  - `AsyncAPI3.components.channels`;
  - `AsyncAPI3.components.operations`;
  - `AsyncAPI3.components.messages`;
  - `AsyncAPI3.components.securitySchemes`;
  - `AsyncAPI3.components.serverVariables`;
  - `AsyncAPI3.components.parameters`;
  - `AsyncAPI3.components.correlationIds`;
  - `AsyncAPI3.components.replies`;
  - `AsyncAPI3.components.replyAddresses`;
  - `AsyncAPI3.components.externalDocs`;
  - `AsyncAPI3.components.tags`;
  - `AsyncAPI3.components.operationTraits`;
  - `AsyncAPI3.components.messageTraits`;
  - `AsyncAPI3.components.serverBindings`;
  - `AsyncAPI3.components.channelBindings`;
  - `AsyncAPI3.components.operationBindings`;
  - `AsyncAPI3.components.messageBindings`;

### FIXED

- #5: Remove `__getattr__` access type from PatternedRootModel and child models.
  Unified dict-like API for patterned objects - replaced `__getattr__` with proper dict
  methods to support keys starting with digits;

## [0.0.1] - 2026-01-11

### ADDED

- Complete AsyncAPI 3.0 specification implementation with Pydantic models
- Full bindings support for all major protocols:
  - AMQP, AMQP 1.0, AnypointMQ, Google Pub/Sub, HTTP, IBM MQ
  - JMS, Kafka, Mercure, MQTT, MQTT 5, NATS, Pulsar, Redis
  - SNS, Solace, SQS, STOMP, WebSockets
- Comprehensive test suite with 100% model coverage
- Type-safe validation with Pydantic v2
- Snake_case Python API with camelCase JSON serialization
- Extensive documentation and examples
- CI/CD pipeline with automated testing and publishing
- Pre-commit hooks for code quality assurance
