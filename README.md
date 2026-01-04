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
- [ ] snake_case internals, following PEP8 as in normal python application.
- [ ] Type safety and validation provided by pydantic models.
- [ ] CLI support for input AsyncAPI 3 files validation. JSON/YAML format supported.
- [ ] Heavy tested

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

### Kafka Bindings - Specification Extensions Support

The `KafkaChannelBindings` and `KafkaOperationBindings` classes allow extra fields
(Specification Extensions) via `extra="allow"`, which does not strictly conform to
the Kafka binding specification that states "This object MUST contain only the
properties defined below."

This deviation was made to support real-world specifications that include
vendor-specific extensions (e.g., `x-key.subject.name.strategy`,
`x-value.subject.name.strategy`).

**Affected files:**

- `asyncapi3/models/bindings/kafka.py` - `KafkaChannelBindings` and
  `KafkaOperationBindings` classes

**Example specification using extensions:**

- `tests/fixtures/yaml_specs/valid/single_file/adeo-kafka-request-reply-asyncapi.yml`

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
