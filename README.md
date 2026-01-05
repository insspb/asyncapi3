# Python AsyncAPI 3 object model

This package provides a Python implementation for interacting with [AsyncAPI 3
specification] as pydantic models. There are tons of python applications, that use
AsyncAPI to generate some kind of documentation or code, each of observed
applications tries to reinvent the wheel and make own AsyncAPI spec.

This object model aims to provide a robust and efficient way to work with AsyncAPI 3
specifications in Python, reducing the need for developers to write custom
implementation. By leveraging pydantic models, this package ensures
type safety and validation, making it easier to work with complex AsyncAPI
specifications.

This SDK focused only on AsyncAPI 3 specification, no other versions are supported.

Current implemented AsyncAPI 3 and bindings specification (and its hash) can be
found in [spec](spec) folder.

## Features

- [ ] Pydantic models for AsyncAPI 3 specification. Complete specification coverage.
- [x] Always valid AsyncAPI3 instance (check:
  [Model Validation Behavior](#model-validation-behavior))
- [x] snake_case internals, following PEP8 as in normal python application.
- [ ] CLI support for input AsyncAPI 3 files validation. JSON/YAML format supported.
- [ ] Heavy tested

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

## Known Issues

### Invalid Example Specification

The example specification file `adeo-kafka-request-reply-asyncapi.yml` (located in
`spec/asyncapi/examples/adeo-kafka-request-reply-asyncapi.yml`) contain vendor-specific
extensions (e.g., `x-key.subject.name.strategy`, `x-value.subject.name.strategy`) that
are not valid according to the Kafka binding json-schema version 0.5.0, which
requires `additionalProperties: false` for channel and operation bindings
(`spec/asyncapi-json-schema/bindings/kafka/0.5.0`).

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

## Usage

### Parse schema file to python object

```python
from asyncapi3 import AsyncAPI3

with open("/path/to/asyncapi3.json") as fileobj:
    spec = AsyncAPI3.model_validate_json(fileobj)
```

[AsyncAPI 3 specification]: https://github.com/asyncapi/spec/blob/master/spec/asyncapi.md
