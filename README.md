# Python AsyncAPI 3 object model

[![PyPI version](https://badge.fury.io/py/asyncapi3.svg)](https://pypi.org/project/asyncapi3/)
[![Python versions](https://img.shields.io/pypi/pyversions/asyncapi3)](https://pypi.org/project/asyncapi3/)
[![codecov](https://codecov.io/gh/insspb/asyncapi3/branch/main/graph/badge.svg)](https://codecov.io/gh/insspb/asyncapi3)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)

**asyncapi3** is a complete Python implementation for working with
[AsyncAPI 3.0 Specification](https://github.com/asyncapi/spec/tree/master/spec/asyncapi.md)
using Pydantic v2 models. It provides robust, type-safe, and efficient
way to parse, validate, and manipulate AsyncAPI specifications in Python applications.

This library eliminates the need for developers to implement custom AsyncAPI parsing
logic by providing comprehensive models with full validation and type safety.

**Key highlights:**

- ✅ **Production ready** - Complete AsyncAPI 3.0 specification coverage
- ✅ **Type safe** - Full MyPy support with strict typing
- ✅ **Well tested** - 100% model coverage with comprehensive test suite
- ✅ **Modern Python** - Uses latest Pydantic v2 features

> ⚠️ **Early Development Notice**: This project is in its early stages (v0.0.1).
> While the core functionality is stable and well-tested, you may encounter bugs,
> incomplete features, or API changes in future versions. Use with caution in
> production environments and stay updated with the latest releases.
>
> **Help us improve!** Please [report bugs](https://github.com/insspb/asyncapi3/issues)
> and [share your use cases](https://github.com/insspb/asyncapi3/issues) in our GitHub issues.
> Your feedback is invaluable for shaping the future of this project!

The SDK supports only AsyncAPI 3.0 specification. For other versions, consider using
different libraries.

Current AsyncAPI 3.0 and bindings specifications (with their commit hashes) can be
found in the [spec](spec) folder.

## ✨ Features

- [x] **Complete AsyncAPI 3.0 specification coverage** with Pydantic v2 models
- [x] **Always valid instances** with comprehensive validation (
  see [Model Validation Behavior](#model-validation-behavior))
- [x] **Pythonic snake_case API** with automatic camelCase JSON serialization
- [x] **Full protocol bindings support** for 18+ messaging protocols:
  - AMQP, AMQP 1.0, AnypointMQ, Google Pub/Sub, HTTP, IBM MQ
  - JMS, Kafka, Mercure, MQTT, MQTT 5, NATS, Pulsar, Redis
  - SNS, Solace, SQS, STOMP, WebSockets
- [x] **Comprehensive test suite** with 100% model coverage
- [x] **Type-safe development** with MyPy support
- [x] **Modern tooling** - Ruff, pre-commit, GitHub Actions CI/CD

### Model Validation Behavior

All AsyncAPI 3 models in this library use special Pydantic configuration settings
that ensure data integrity and validation at all times:

- **`validate_assignment=True`**: Validates field assignments after model instantiation,
  preventing invalid data from being stored in model instances
- **`revalidate_instances="always"`**: Revalidates all model instances during
  validation, ensuring nested models remain consistent

These settings guarantee that your AsyncAPI specification objects always contain
valid data, regardless of how they are modified after creation.

#### Example: Field Assignment Validation

```python
from asyncapi3.models.bindings.anypointmq import AnypointMQChannelBindings
from pydantic import ValidationError

# Create a valid channel binding
binding = AnypointMQChannelBindings(destination_type="queue")
print("Initial destination_type:", binding.destination_type)

# Valid assignment
binding.destination_type = "exchange"
print("Changed to:", binding.destination_type)

# Invalid assignment will raise ValidationError
try:
    binding.destination_type = "invalid-type"
except ValidationError as e:
    print("ValidationError: Invalid destination_type value")
```

#### Example: Instance Revalidation

```python
from asyncapi3.models.schema import Schema
from asyncapi3.models.asyncapi import AsyncAPI3
from asyncapi3.models.info import Info
from pydantic import ValidationError

# Create a schema with boolean field
schema = Schema(deprecated=False)
print("Initial deprecated value:", schema.deprecated)

# Modify the field (this would normally bypass validation in other libraries)
schema.deprecated = True  # Valid boolean
print("Changed deprecated to:", schema.deprecated)

# Invalid assignment will be caught
try:
    schema.deprecated = "not-a-boolean"
except ValidationError as e:
    print("ValidationError: deprecated must be boolean")

# Create AsyncAPI spec with nested schema
spec = AsyncAPI3(
    info=Info(title="My API", version="1.0.0")
)
spec.info.description = "API description"  # Valid string
print("Description set successfully")

# Invalid type assignment will fail
try:
    spec.info.version = 123  # Should be string
except ValidationError as e:
    print("ValidationError: version must be string")
```

#### Example: Serialization Consistency

```python
from asyncapi3.models.bindings.anypointmq import AnypointMQChannelBindings

# Create binding with default values
binding = AnypointMQChannelBindings()
print("Default destination_type:", binding.destination_type)  # queue

# Change to valid value
binding.destination_type = "exchange"
print("Changed destination_type:", binding.destination_type)  # exchange

# Invalid assignment will fail
try:
    binding.destination_type = "invalid-type"
except ValidationError as e:
    print("ValidationError:", e)
```

These validation behaviors ensure that AsyncAPI specification objects maintain
their integrity throughout their lifecycle, providing reliable and type-safe
data structures for your applications.

### Binding Version Behavior

When working with binding models, the `binding_version` field behaves as follows:

- **Validation**: Any value provided for `binding_version` will be validated according
  to the binding specification schema
- **Default Value**: If `binding_version` is not specified during deserialization, the
  model will use the default value corresponding to the current version of the binding
  specification
- **Serialization**: During serialization, if `binding_version` was not explicitly set
  (i.e., it uses the default value), it will be included in the output with the current
  binding version value

This ensures that binding version information is always present in serialized output,
making it clear which version of the binding specification is being used, even when
the version was not explicitly provided in the input.

### Implementation Specific Behavior

#### Patterned Object Key Validation

All patterned objects (`Servers`, `Channels`, `Operations`, `Messages`, `Parameters`,
and all objects in `components`) use strict validation with the pattern
`^[A-Za-z0-9_\-]+$` for keys, allowing only letters, digits, hyphens, and underscores.

This strict validation ensures:

- **Full compliance** with AsyncAPI 3.0 specification requirements
- **Consistency** across all patterned objects in specific location(`components`) and
  other root objects.

The implementation is intentionally stricter than some interpretations of the
specification to provide robust and predictable behavior.

List of changed objects available at [CHANGELOG v0.0.2](CHANGELOG.md#002---2026-01-14)

## ⚠️ Known Issues

### Invalid Example Specification

The example specification file `adeo-kafka-request-reply-asyncapi.yml` (located in
`spec/asyncapi/examples/adeo-kafka-request-reply-asyncapi.yml`) contains vendor-specific
extensions (e.g., `x-key.subject.name.strategy`, `x-value.subject.name.strategy`) that
are not valid according to the Kafka binding json-schema version 0.5.0, which
requires `additionalProperties: false` for channel and operation bindings
(`spec/asyncapi-json-schema/bindings/kafka/0.5.0`).

### Anypoint MQ Binding Implementation Issues

The AnypointMQ binding implementation (`asyncapi3/models/bindings/anypointmq.py`) may
contain errors due to version mismatch between the code implementation and available
JSON schemas.

**Known issues:**

- Version mismatch: Code and [Anypoint MQ Binding] uses `0.1.0` but JSON schemas
  only provide `0.0.1`.

[Anypoint MQ Binding]: https://github.com/asyncapi/bindings/blob/master/anypointmq/README.md

### SNS Binding Implementation Issues

The SNS binding implementation (`asyncapi3/models/bindings/sns.py`) may contain errors
because there is no up-to-date JSON schema for this binding object, and the initial
specification contains errors. The implementation follows best guess approach with
changes made to address identified issues.

**Known issues:**

- Version mismatch: Code and [sns binding] uses `1.0.0` but JSON schemas only
  provide `0.1.0` and `0.2.0`.

[sns binding]: https://github.com/asyncapi/bindings/blob/master/sns/3.0.0/README.md

### Pydantic Field Name Shadowing Warnings

When using the library, you may encounter `UserWarning` messages about field names
shadowing attributes in parent `BaseModel`:

```console
UserWarning: Field name "schema" in "MultiFormatSchema" shadows an attribute in parent "BaseModel"
UserWarning: Field name "schema" in "GooglePubSubMessageBindings" shadows an attribute in parent "BaseModel"
```

**Affected classes:**

- `MultiFormatSchema` in `asyncapi3/models/schema.py`
- `GooglePubSubMessageBindings` in `asyncapi3/models/bindings/googlepubsub.py`

**Note:** These warnings are related to the `schema` attribute being deprecated in
the current version of Pydantic. The field name `schema` is required by the AsyncAPI
specification and cannot be changed. These warnings are harmless and will disappear
automatically as Pydantic removes the deprecated `schema` attribute in future
versions.

## 🚀 Usage

### Installation

```bash
pip install asyncapi3
```

### Parse AsyncAPI Specification

```python
from asyncapi3 import AsyncAPI3

# Parse JSON specification
with open("asyncapi-spec.json", "r") as f:
    spec = AsyncAPI3.model_validate_json(f.read())

# Parse YAML specification
with open("asyncapi-spec.yaml", "r") as f:
    spec = AsyncAPI3.model_validate_yaml(f.read())

# Access specification data
print(f"API Title: {spec.info.title}")
print(f"Version: {spec.info.version}")
print(f"Description: {spec.info.description}")
```

### Working with Bindings

```python
from asyncapi3.models.bindings.mqtt import MQTTServerBindings

# Create MQTT server binding with validation
mqtt_binding = MQTTServerBindings(
    client_id="my-client",
    clean_session=True,
    binding_version="0.2.0"
)

# Serialize to JSON (automatic camelCase conversion)
json_data = mqtt_binding.model_dump_json()
print(json_data)
# {"clientId": "my-client", "cleanSession": true, "bindingVersion": "0.2.0"}
```

### Type-Safe Operations

```python
from asyncapi3.models.info import Info

# Create info object
info = Info(title="My API", version="1.0.0")

# Type-safe field access and modification
info.title = "Updated API Title"  # ✅ Valid string
info.description = "API description"  # ✅ Valid optional string

# Validation prevents invalid data
try:
    info.version = 123  # ❌ ValidationError - must be string
except ValidationError as e:
    print("Validation error:", e)
```

### Local Development

To run the same checks locally:

```bash
# Install dependencies
uv sync --dev

# Run tests
uv run pytest

# Run pre-commit checks on all files
uvx pre-commit run --all-files

# Run pre-commit checks on staged files only
uvx pre-commit run
```
