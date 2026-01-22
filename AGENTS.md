# AI Agent Guidelines for AsyncAPI3 Project

This document provides comprehensive guidelines for AI agents working on the AsyncAPI3
project.

## Project Overview

- **Goal**: Create a complete Python object model for the
  [AsyncAPI 3.0 specification](spec/asyncapi/spec/asyncapi.md).
- Focuses **only** on AsyncAPI 3 specification, no other versions are supported
- **Core Technology**: [Pydantic](https://docs.pydantic.dev/) (v2+).
- **Scope**: **AsyncAPI 3.0 only**.
- **Repository Status**: Public GitHub repository.

## Project Structure

NOTE: All paths declared from project root.

- `asyncapi3/` - main library code
- `asyncapi3/models/` - Pydantic models for AsyncAPI 3 specification
- `asyncapi3/models/bindings/` - Pydantic models for bindings specifications
- `asyncapi3/validators/` - reference validation functions and validator classes
- `asyncapi3/__init__.py` - Package exports
- `tests/` - project tests:
- `tests/fixtures/` - Test fixtures (JSON/YAML specs)

## Validation Functions

The project includes common validation functions in `asyncapi3/validators/common.py`
that are used by all reference validators:

- **`is_external_ref(ref_value: str, context: str) -> bool`**: Checks if a reference
  is external (starts with "http" or other protocols) and logs a warning. Returns
  `True` if external (validation skipped), `False` if internal.

- **`validate_component_exists(spec, ref_value, component_path, context) -> None`**:
  Validates that a reference points to an existing component in `spec.components.{component_path}`.
  Raises `ValueError` if component doesn't exist.

- **`validate_root_channel_ref(spec: AsyncAPI3, ref_value: str, context: str) -> None`**:
  Validates that a reference points to a channel in the root `spec.channels` object.
  Raises `ValueError` if the channel doesn't exist.

- **`validate_root_operation_ref(spec: AsyncAPI3, ref_value: str, context: str) -> None`**:
  Validates that a reference points to an operation in the root `spec.operations` object.
  Raises `ValueError` if the operation doesn't exist.

All reference validators inherit from `ProcessorProtocol` and use these common functions
to validate references throughout AsyncAPI specifications.

## Specification Location

The AsyncAPI 3 and related bindings specifications documentation are included as a git
submodules:

- **Main specification**: `spec/asyncapi/spec/asyncapi.md`
- **Bindings specifications**: `spec/bindings/` directory (each subdirectory contains
  documentation for a specific binding type)
- **Examples and scripts**: `spec/asyncapi/examples/` directory

## JSON Schema Validation

The project includes official JSON Schema files for AsyncAPI 3.0 specification validation
as a git submodule (`spec/asyncapi-json-schema/`). These schemas can be used to validate
AsyncAPI documents, but with important caveats.

### JSON Schema Locations

**CRITICAL**: When working with JSON schemas, **prefer using definitions** over bundled
schemas, as definitions are the source of truth and bundled schemas are automatically
generated.

- **Binding schemas**: `spec/asyncapi-json-schema/bindings/` - contains JSON schemas for
  all binding types (MQTT, Kafka, HTTP, etc.)
- **Object definitions**: `spec/asyncapi-json-schema/definitions/3.0.0/` - contains
  individual JSON schema definitions for all AsyncAPI 3.0 objects (channels, messages,
  operations, servers, etc.)
- **Valid examples**: `spec/asyncapi-json-schema/examples/3.0.0/` - contains valid JSON
  examples for individual definitions that can be used for testing
- **Bundled schema**: `spec/asyncapi-json-schema/schemas/3.0.0.json` - complete bundled
  schema (automatically generated, **do not edit manually**)
- **Repository documentation**: `spec/asyncapi-json-schema/README.md` - contains
  important information about JSON schemas, their limitations, and usage guidelines

### Important Limitations

**CRITICAL**: JSON schemas have important limitations that must be understood:

1. **Not 1:1 with specification**: JSON Schema files do not reflect 1:1 the specification
   and shouldn't be treated as specification itself but rather as a tool (e.g., for
   validation).

2. **Incomplete validation**: These JSON Schema files shouldn't be used as the **only**
   tool for validating AsyncAPI documents because some rules described in the AsyncAPI
   specification can't be described with JSON Schema.

3. **Two schema types**: There are two types of JSON Schema files, with and without `$id`
   feature. Some tools require `$id`, others don't understand it. The project uses
   schemas without `$id` by default.

4. **Auto-generated bundled schemas**: Schemas in `spec/asyncapi-json-schema/schemas/`
   are automatically generated from definitions in `spec/asyncapi-json-schema/definitions/`.
   **Never edit bundled schemas manually** - always edit definitions instead.

### Usage Guidelines

When using JSON schemas for validation or reference:

1. **Use definitions for reference**: When checking field structures, types, or required
   fields, refer to individual definition files in `spec/asyncapi-json-schema/definitions/3.0.0/`
   rather than the bundled schema.

2. **Use examples for testing**: The `spec/asyncapi-json-schema/examples/3.0.0/` directory
   contains valid examples that can be used as test fixtures or validation references.

3. **Cross-reference with specification**: Always cross-reference JSON schema definitions
   with the actual specification in `spec/asyncapi/spec/asyncapi.md` to ensure accuracy.

4. **Validate model implementation**: Use JSON schemas to verify that Pydantic models
   correctly implement the specification, but remember that JSON Schema validation alone
   is not sufficient.

5. **Check binding schemas**: When implementing binding models, refer to corresponding
   JSON schemas in `spec/asyncapi-json-schema/bindings/{binding_name}/` to understand the
   expected structure.

### Additional Information

For more details about JSON schemas, their structure, limitations, and usage, refer to
`spec/asyncapi-json-schema/README.md`.

## Language and Documentation Rules

**CRITICAL**: All comments, documentation, docstrings, and code-related text in the
project **MUST** be in **English**. This includes:

- Code comments
- Docstrings
- Documentation files
- Commit messages
- Variable names (following Python conventions)

## Code Style and Linting Rules

### Python Code (ruff)

The project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting:

- **Line length**: 88 characters
- **Python version**: 3.10+
- **Indentation**: 4 spaces
- **Naming**: follow PEP8, snake_case for variables and functions, CamelCase for
  class names
- **Configuration**: Rules are defined in `pyproject.toml`. **Do not ignore** these
  rules
- **Enabled rule sets**: See `pyproject.toml` `[tool.ruff.lint.select]` section for
  complete list
- **Ignored rules**: See `pyproject.toml` `[tool.ruff.lint.ignore]` section

**Key Rules:**

- Follow all enabled Ruff linting rules
- Use Ruff formatter for code formatting
- Check `pyproject.toml` `[tool.ruff]` section first when in doubt
- Per-file ignores:
  - `__init__.py`: Allows unused imports (F401, F403)
  - `test_*.py`: Allows assert statements (S101) and long lines (E501)

**File Structure Rules:**

- All imports must be at the beginning of the file
- In Pydantic models: first model configuration (if any), then all field declarations,
  then validation functions

### Markdown Documentation Rules

The project uses markdownlint as `pre-commit` hook (`.markdownlint.jsonc`):

- **Line length**: 88 characters
- **Indentation**: 2 spaces
- **Heading style**: ATX (`# Heading`)
- **List style**: Consistent
- **Code fence style**: Backtick (`` ``` ``)
- **Emphasis style**: Asterisk (`*text*`)
- **Strong style**: Asterisk (`**text**`)
- Files must end with a single newline

### EditorConfig

The project uses EditorConfig (`.editorconfig`):

- **Indent style**: Spaces
- **Indent size**: 4 spaces (Python), 2 spaces (Markdown, YAML, JSON, etc.)
- **End of line**: LF
- **Charset**: UTF-8
- **Trim trailing whitespace**: Yes
- **Insert final newline**: Yes

### Pre-commit Hooks

The project uses pre-commit hooks (`.pre-commit-config.yaml`):

- AST checking
- JSON/YAML/TOML validation
- Ruff linting and formatting
- Markdown linting
- MyPy type checking

**Always ensure code passes all pre-commit checks before committing.**

## Testing Guidelines

### Test Framework

- Use **pytest** as the testing framework
- Follow pytest best practices and conventions
- Test files should be named `test_*.py`
- Test functions should be named `test_*`

### Test Location

- **ALL** tests must be located in the `tests/` directory
- Test fixtures should be in `tests/fixtures/`

### Parametrization

- Use `@pytest.mark.parametrize` for parameterized tests
- For complex parametrization scenarios, you **MAY** use `pytest-cases` library
- Provide meaningful test IDs when using parametrization

### Test Writing Rules

- Use standard `assert` statements, not `self.assert*` methods
- Follow flake8-pytest-style (PT rules from ruff)
- Use pytest fixtures and parametrization

### Pytest Configuration

Pytest is configured in `pyproject.toml` with the following options:

```ini
addopts = """
          --junit-xml=./xunit.xml
          --cov=.
          --cov-report=xml
          --cov-report=term-missing:skip-covered
          -vvv
"""
```

- Coverage is measured using `pytest-cov`
- Test results are exported to JUnit XML format
- Verbose output is enabled by default

### Test Style Example

```python
from pathlib import Path
import pytest
from asyncapi3 import AsyncAPI3


@pytest.mark.parametrize(
  "path",
  [Path("tests/fixtures/valid_spec.json")],
  ids=["valid_spec"],
)
def test_parse_valid_spec(path: Path) -> None:
  assert AsyncAPI3.model_validate_json(path.read_text()) is not None
```

### Testing Based on Specification Examples

When writing tests for models based on examples from specification documentation,
follow these guidelines:

#### Source of Examples

Examples can be found in:

- **Main specification**: `spec/asyncapi/spec/asyncapi.md` - contains examples for
  AsyncAPI 3.0 objects
- **Binding specifications**: `spec/bindings/{binding_name}/README.md` - contains
  examples for specific binding types (e.g., MQTT, Kafka, etc.)
- **Full specification files**: Developer may provide complete specification files
  (YAML/JSON) for extracting examples of specific objects

#### Test Organization

**CRITICAL**: Organize tests in **classes** grouped by model type to allow running
specific test groups:

```python
class TestMQTTServerBindings:
    """Tests for MQTTServerBindings model."""
    # ... tests for server bindings ...

class TestMQTTOperationBindings:
    """Tests for MQTTOperationBindings model."""
    # ... tests for operation bindings ...
```

This allows developers to run tests for specific bindings:

```bash
pytest tests/models/bindings/test_mqtt.py::TestMQTTServerBindings -v
```

#### Using pytest-cases for Test Data

Use `pytest-cases` library to store test data (YAML, JSON, or any other format):

1. **CRITICAL**: Store case functions **in the same file** as the tests (not in separate
   files)

2. **Create case functions** with `case_` prefix (no `@case` decorator needed if id
   matches function name without prefix):

```python
from pytest_cases import parametrize_with_cases
import yaml

def case_server_binding_full() -> str:
    """Server binding with all fields."""
    return """
    mqtt:
      clientId: guest
      cleanSession: true
      bindingVersion: 0.2.0
    """
```

1. **Use `parametrize_with_cases`** to parametrize test methods:

```python
class TestMQTTServerBindings:
    @parametrize_with_cases(
        "yaml_data",
        cases=[case_server_binding_full, case_server_binding_with_schema],
    )
    def test_mqtt_server_bindings(self, yaml_data: str) -> None:
        """Test MQTTServerBindings model validation."""
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTServerBindings.model_validate(data["mqtt"])
        assert mqtt_binding is not None
        assert mqtt_binding.binding_version == "0.2.0"
```

#### Extracting Examples from Documentation

When extracting examples from specification files:

1. **From binding specifications**: Extract only the relevant binding object from YAML
   examples. For example, if the spec shows:
   ```yaml
   servers:
     production:
       bindings:
         mqtt:
           clientId: guest
   ```
   Extract only the `mqtt` object:
   ```yaml
   mqtt:
     clientId: guest
   ```

2. **From full specification files**: If developer provides a complete specification
   file, extract only the relevant objects you're testing. For example, if testing
   `MQTTServerBindings`, extract only the `mqtt` binding object from the server
   bindings section.

3. **Multiple examples**: Include all valid examples from the specification to ensure
   comprehensive coverage.

#### Complete Test Example

```python
"""Tests for MQTT bindings models."""

import yaml

from pytest_cases import parametrize_with_cases

from asyncapi3.models.bindings.mqtt import (
    MQTTServerBindings,
    MQTTOperationBindings,
)
from asyncapi3.models.schema import Schema


# Validation Test Cases
def case_server_binding_full() -> str:
    """Server binding with all fields."""
    return """
    mqtt:
      clientId: guest
      cleanSession: true
      bindingVersion: 0.2.0
    """


def case_server_binding_with_schema() -> str:
    """Server binding with Schema objects."""
    return """
    mqtt:
      sessionExpiryInterval:
        type: integer
        minimum: 30
        maximum: 1200
      bindingVersion: 0.2.0
    """


# Serialization Test Cases
def case_mqtt_server_binding_serialization_empty() -> tuple[MQTTServerBindings, dict]:
    """MQTTServerBindings serialization empty."""
    mqtt_binding = MQTTServerBindings()
    expected = {"bindingVersion": "0.2.0"}
    return mqtt_binding, expected


def case_mqtt_server_binding_serialization_full() -> tuple[MQTTServerBindings, dict]:
    """MQTTServerBindings serialization with all fields."""
    mqtt_binding = MQTTServerBindings(
        client_id="guest",
        clean_session=True,
    )
    expected = {
        "clientId": "guest",
        "cleanSession": True,
        "bindingVersion": "0.2.0",
    }
    return mqtt_binding, expected


def case_mqtt_server_binding_serialization_with_schema() -> tuple[MQTTServerBindings, dict]:
    """MQTTServerBindings serialization with Schema objects."""
    mqtt_binding = MQTTServerBindings(
        session_expiry_interval=Schema(
            type="integer",
            minimum=30,
            maximum=1200,
        ),
    )
    expected = {
        "sessionExpiryInterval": {
            "type": "integer",
            "minimum": 30,
            "maximum": 1200,
        },
        "bindingVersion": "0.2.0",
    }
    return mqtt_binding, expected


class TestMQTTServerBindings:
    """Tests for MQTTServerBindings model."""

    @parametrize_with_cases(
        "yaml_data",
        cases=[case_server_binding_full, case_server_binding_with_schema],
    )
    def test_mqtt_server_bindings_validation(self, yaml_data: str) -> None:
        """Test MQTTServerBindings model validation."""
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTServerBindings.model_validate(data["mqtt"])
        assert mqtt_binding is not None
        assert mqtt_binding.binding_version == "0.2.0"

    @parametrize_with_cases(
        "mqtt_binding,expected",
        cases=[
            case_mqtt_server_binding_serialization_empty,
            case_mqtt_server_binding_serialization_full,
            case_mqtt_server_binding_serialization_with_schema,
        ],
    )
    def test_mqtt_server_bindings_serialization(
        self,
        mqtt_binding: MQTTServerBindings,
        expected: dict,
    ) -> None:
        """Test MQTTServerBindings serialization."""
        dumped = mqtt_binding.model_dump()
        assert dumped == expected

    def test_mqtt_server_binding_session_expiry_interval_schema_validation(self) -> None:
        """Test MQTTServerBindings with sessionExpiryInterval as Schema validation."""
        yaml_data = """
        mqtt:
          sessionExpiryInterval:
            type: integer
            minimum: 30
            maximum: 1200
          bindingVersion: 0.2.0
        """
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTServerBindings.model_validate(data["mqtt"])
        assert mqtt_binding.session_expiry_interval is not None
        assert isinstance(mqtt_binding.session_expiry_interval, Schema)
        assert mqtt_binding.session_expiry_interval.type == "integer"
```

#### Testing Serialization (model_dump)

**CRITICAL**: Tests for validation and serialization **MUST** be separated into
distinct test methods.

When testing serialization:

1. **Create Python object directly** by instantiating the model class (not via
   `model_validate` from YAML)
2. **Serialize to dict** using `model_dump()`
3. **Compare the entire result** with a complete expected dictionary
4. **Use pytest-cases** for parametrization to test multiple serialization variants
   (e.g., with `$ref` and with full objects)

**Important**: Separate `model_dump_json()` tests are **NOT** required with this
approach, as `model_dump()` covers serialization testing.

```python
# Serialization Test Cases
def case_mqtt_server_binding_serialization_full() -> tuple[MQTTServerBindings, dict]:
    """MQTTServerBindings serialization with all fields."""
    mqtt_binding = MQTTServerBindings(
        client_id="guest",
        clean_session=True,
    )
    expected = {
        "clientId": "guest",
        "cleanSession": True,
        "bindingVersion": "0.2.0",
    }
    return mqtt_binding, expected


def case_mqtt_server_binding_serialization_empty() -> tuple[MQTTServerBindings, dict]:
    """MQTTServerBindings serialization empty."""
    mqtt_binding = MQTTServerBindings()
    expected = {"bindingVersion": "0.2.0"}
    return mqtt_binding, expected


class TestMQTTServerBindings:
    """Tests for MQTTServerBindings model."""

    @parametrize_with_cases("yaml_data", cases=[case_server_binding_full])
    def test_mqtt_server_bindings_validation(self, yaml_data: str) -> None:
        """Test MQTTServerBindings model validation."""
        data = yaml.safe_load(yaml_data)
        mqtt_binding = MQTTServerBindings.model_validate(data["mqtt"])
        assert mqtt_binding is not None
        assert mqtt_binding.binding_version == "0.2.0"

    @parametrize_with_cases(
        "mqtt_binding,expected",
        cases=[
            case_mqtt_server_binding_serialization_empty,
            case_mqtt_server_binding_serialization_full,
        ],
    )
    def test_mqtt_server_bindings_serialization(
        self,
        mqtt_binding: MQTTServerBindings,
        expected: dict,
    ) -> None:
        """Test MQTTServerBindings serialization."""
        dumped = mqtt_binding.model_dump()
        assert dumped == expected
```

#### Testing Static Objects

When testing with static objects (not parametrized), verify **all fields** in the
resulting object. These tests should focus on **validation**:

```python
def test_mqtt_server_binding_last_will_validation(self) -> None:
    """Test MQTTServerBindings with lastWill object validation."""
    yaml_data = """
    mqtt:
      lastWill:
        topic: /last-wills
        qos: 2
        message: Guest gone offline.
        retain: false
      bindingVersion: 0.2.0
    """
    data = yaml.safe_load(yaml_data)
    mqtt_binding = MQTTServerBindings.model_validate(data["mqtt"])

    # Verify all fields
    assert mqtt_binding.last_will is not None
    assert isinstance(mqtt_binding.last_will, MQTTLastWill)
    assert mqtt_binding.last_will.topic == "/last-wills"
    assert mqtt_binding.last_will.qos == 2
    assert mqtt_binding.last_will.message == "Guest gone offline."
    assert mqtt_binding.last_will.retain is False
    assert mqtt_binding.binding_version == "0.2.0"
```

#### Testing Empty Objects with Default Values

If a model has all optional fields or fields with default values, test empty object
initialization in **serialization tests**:

```python
# Serialization Test Cases
def case_mqtt_channel_binding_serialization_empty() -> tuple[MQTTChannelBindings, dict]:
    """MQTTChannelBindings serialization empty."""
    mqtt_binding = MQTTChannelBindings()
    expected = {}
    return mqtt_binding, expected


def case_mqtt_server_binding_serialization_empty() -> tuple[MQTTServerBindings, dict]:
    """MQTTServerBindings serialization empty."""
    server_binding = MQTTServerBindings()
    expected = {"bindingVersion": "0.2.0"}  # Default value
    return server_binding, expected


class TestMQTTChannelBindings:
    """Tests for MQTTChannelBindings model."""

    @parametrize_with_cases(
        "mqtt_binding,expected",
        cases=[case_mqtt_channel_binding_serialization_empty],
    )
    def test_mqtt_channel_bindings_serialization(
        self,
        mqtt_binding: MQTTChannelBindings,
        expected: dict,
    ) -> None:
        """Test MQTTChannelBindings serialization."""
        dumped = mqtt_binding.model_dump()
        assert dumped == expected
```

#### Separation of Validation and Serialization Tests

**CRITICAL**: Validation and serialization tests **MUST** be separated into distinct
test methods:

1. **Validation tests** (`test_*_validation`):
   - Use `model_validate()` with parsed YAML/JSON data
   - Verify that the model is created correctly
   - Check specific field values and types

2. **Serialization tests** (`test_*_serialization`):
   - Create model instances directly (not via `model_validate`)
   - Use `model_dump()` to serialize
   - Compare the entire result with a complete expected dictionary
   - Use `pytest-cases` for parametrization to test multiple variants

#### Key Points

- **Always use `model_validate`** with parsed YAML/JSON data (via `yaml.safe_load()` or
  `json.loads()`) for validation tests
- **Create model instances directly** for serialization tests (not via `model_validate`)
- **Extract only relevant objects** from examples (e.g., only `mqtt` binding object,
  not the entire server structure)
- **Group tests in classes** by model type for better organization
- **Use pytest-cases** for parametrized tests with multiple examples (YAML, JSON, or
  any test data)
- **Store case functions in the same file** as tests
- **Separate case functions** for validation (return `str` with YAML) and serialization
  (return `tuple[Model, dict]` with model instance and expected dictionary)
- **Include all valid examples** from the specification for comprehensive coverage
- **Test serialization** using `model_dump()` to verify round-trip compatibility
- **Compare full dictionaries** in serialization tests (not individual fields)
- **Verify all fields** when testing static objects in validation tests
- **Test empty initialization** for models with optional/default fields
- **Add additional tests** for edge cases (e.g., Schema objects, optional fields)
- **Separate `model_dump_json()` tests are NOT required** - `model_dump()` covers
  serialization testing

#### Testing Empty Models

For empty models (models without fields) that have `extra="forbid"` configuration and
are reserved for future use (e.g., AMQP1 bindings), create **4 tests** to fix the behavior:

1. **Serialization test** - Test that empty object serializes to empty dict
2. **Python validation error test** - Test that creating object with any arguments
   raises `ValidationError`
3. **YAML validation error test** - Test that reading YAML with any fields raises
   `ValidationError`
4. **YAML empty validation test** - Test that reading empty YAML object succeeds

**CRITICAL**: For empty models, store test data **directly in the test methods**,
not in separate case functions.

#### Testing Custom Model Validators

For custom model validators that check model integrity and are written by us (not built-in
Pydantic validations), create comprehensive tests using `pytest-cases`:

1. **Test all error scenarios** with exact error messages
2. **Use `pytest-cases`** for parametrized tests
3. **Return `tuple[str, str]`** from case functions (YAML data, expected error message)
4. **Use exact message matching** with `pytest.raises(ValueError, match=expected_error)`

**Example for custom validator testing (AMQPChannelBindings validator):**

```python
"""Tests for AMQP bindings models."""

import pytest
import yaml
from pydantic import ValidationError

from pytest_cases import parametrize_with_cases
from asyncapi3.models.bindings.amqp import AMQPChannelBindings


# Validation error test cases for AMQPChannelBindings validator
def case_amqp_channel_binding_validator_routing_key_without_exchange() -> tuple[str, str]:
    """RoutingKey without exchange - should fail validation."""
    yaml_data = """
    amqp:
      is: routingKey
      bindingVersion: 0.3.0
    """
    expected_error = "exchange must be provided when is='routingKey'"
    return yaml_data, expected_error


def case_amqp_channel_binding_validator_routing_key_with_queue() -> tuple[str, str]:
    """RoutingKey with queue - should fail validation."""
    yaml_data = """
    amqp:
      is: routingKey
      exchange:
        name: myExchange
        type: topic
      queue:
        name: myQueue
      bindingVersion: 0.3.0
    """
    expected_error = "queue must not be provided when is='routingKey'"
    return yaml_data, expected_error


class TestAMQPChannelBindingsValidator:
    """Tests for AMQPChannelBindings model validator."""

    @parametrize_with_cases(
        "yaml_data,expected_error",
        cases=[
            case_amqp_channel_binding_validator_routing_key_without_exchange,
            case_amqp_channel_binding_validator_routing_key_with_queue,
        ],
    )
    def test_amqp_channel_bindings_validator_errors(self, yaml_data: str, expected_error: str) -> None:
        """Test AMQPChannelBindings validator errors for invalid field combinations."""
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValueError, match=expected_error):
            AMQPChannelBindings.model_validate(data["amqp"])
```

**Example for empty model testing:**

```python
"""Tests for EmptyModel bindings models."""

import pytest
import yaml
from pydantic import ValidationError

from asyncapi3.models.bindings.empty import EmptyModel


class TestEmptyModel:
    """Tests for EmptyModel model."""

    def test_empty_model_serialization(self) -> None:
        """Test EmptyModel serialization."""
        empty_model = EmptyModel()
        dumped = empty_model.model_dump()
        assert dumped == {}

    def test_empty_model_python_validation_error(self) -> None:
        """Test EmptyModel Python validation error with any arguments."""
        with pytest.raises(ValidationError):
            EmptyModel(some_field="value")

    def test_empty_model_yaml_validation_error(self) -> None:
        """Test EmptyModel YAML validation error with any fields."""
        yaml_data = """
        empty:
          some_field: value
        """
        data = yaml.safe_load(yaml_data)
        with pytest.raises(ValidationError):
            EmptyModel.model_validate(data["empty"])

    def test_empty_model_yaml_empty_validation(self) -> None:
        """Test EmptyModel YAML validation with no fields."""
        yaml_data = """
        empty: {}
        """
        data = yaml.safe_load(yaml_data)
        empty_model = EmptyModel.model_validate(data["empty"])
        assert empty_model is not None
```

## Type Checking

The project uses **MyPy** for type checking:

- MyPy configuration is in `pyproject.toml`
- Pydantic plugin is enabled
- Import-untyped errors are disabled
- Ensure all code passes MyPy type checking

## Dependencies

### Runtime Dependencies

- `pydantic` (>=2.12.5)
- `pyaml` (>=25.7.0)

### Development Dependencies

- `pytest` (>=9.0.2)
- `pytest-cases` (>=3.9.1)
- `pytest-cov` (>=7.0.0)
- `ruff` (for linting and formatting)
- `pre-commit` (>=4.5.1)
- `mypy` (for type checking)

Dependencies are managed via `pyproject.toml`.

## Pydantic Model Creation Rules

When creating Pydantic models based on the AsyncAPI 3 specification:

### Field Declarations

- **ALL** Pydantic fields **MUST** be declared using the `Field` class
- Each field **MUST** include a `description` parameter that matches the field
  description from `spec/asyncapi/spec/asyncapi.md`
- Use `exclude_if=is_null` helper for optional fields that should be excluded when null
- Use `alias` parameter when the JSON field name differs from Python variable name (
  e.g., `externalDocs` → `external_docs`)

### Field Validators

When implementing custom field validators using `@field_validator`:

- **ALWAYS** use the field name as the parameter name instead of generic names like
  `v` or `value`
- Parameter name **MUST** match the field name being validated
- This improves code readability and makes validation logic clearer

**Example:**

```python
@field_validator("priority")
@classmethod
def validate_priority(cls, priority: Any) -> Any:
    """Validate priority range when it's an integer."""
    if isinstance(priority, int) and (priority < 0 or priority > 255):
        raise ValueError("priority must be between 0 and 255")
    return priority
```

### Binding Version Fields

**CRITICAL**: When working with binding models, the `binding_version` field **MUST**
have a default value that matches the current version of the binding specification.

- When updating binding specifications, **ALWAYS** update the `default` value of
  `binding_version` fields in the corresponding binding model files
- The default value should match the version declared in the binding specification's
  README.md file (e.g., `spec/bindings/mqtt/README.md` declares version `0.2.0`)
- The `binding_version` field should be typed as `str` (not `str | None`) and have a
  default value set to the current binding version
- Do not use `exclude_if=is_null` for `binding_version` fields since they always have
  a default value

**Example:**

```python
binding_version: str = Field(
    default="0.2.0",  # Must match the version in spec/bindings/mqtt/README.md
    alias="bindingVersion",
    description="The version of this binding. If omitted, 'latest' MUST be assumed",
)
```

When updating a binding specification:

1. Check the version in `spec/bindings/{binding_name}/README.md`
2. Update all `binding_version` fields in `asyncapi3/models/bindings/{binding_name}.py`
3. Ensure the default value matches the specification version

### Model Docstrings

- **ALL** Pydantic model docstrings **MUST** match the corresponding object description
  from `spec/asyncapi/spec/asyncapi.md` or related binding in `spec/bindings/`.
- Docstrings should include the object name and its description from the specification
- Include any relevant notes about extensions or special behaviors mentioned in the spec

### Naming Conventions

- Use `snake_case` for all Python variables and field names
- Use `CamelCase` for class names
- Use Pydantic's `alias` parameter to map between JSON field names (camelCase) and
  Python field names (snake_case)
- Configure Pydantic models to parse and write JSON correctly using `ConfigDict`

#### Bindings Naming Rules

**CRITICAL**: For bindings models, additional helper classes (classes that are not
the main Server/Channel/Operation/Message bindings) **MUST** be prefixed with the
protocol name to avoid naming conflicts between different protocols.

Examples:

- `Queue` → `SQSQueue`, `AMQPQueue`, `SolaceQueue`
- `Policy` → `SNSPolicy`, `SQSPolicy`
- `Statement` → `SNSStatement`, `SQSStatement`
- `Destination` → `SolaceDestination`
- `Identifier` → `SNSIdentifier`, `SQSIdentifier`
- `TopicConfiguration` → `KafkaTopicConfiguration`
- `LastWill` → `MQTTLastWill`

This rule applies to all helper classes defined within binding modules, except for
the four main binding classes (ServerBindings, ChannelBindings, OperationBindings,
MessageBindings) which already have the protocol prefix.

### Model Configuration

**CRITICAL**: All Pydantic models **MUST** use the following standard configuration
with required parameters:

```python
model_config = ConfigDict(
  extra="allow",
  revalidate_instances="always",
  validate_assignment=True,
  serialize_by_alias=True,
  validate_by_name=True,
  validate_by_alias=True,
)
```

**Required Parameters:**

- `serialize_by_alias=True` - Ensures serialization uses field aliases (camelCase)
  instead of Python field names (snake_case)
- `validate_by_name=True` - Allows validation using Python field names
- `validate_by_alias=True` - Allows validation using JSON field aliases

**Note:** Some models may use `extra="forbid"` instead of `extra="allow"` based on
specification requirements (e.g., binding helper classes), but all three validation
and serialization parameters **MUST** always be present.

### Type Safety

- Use strict typing
- Use Pydantic's validation capabilities (`Annotated`, `conint`, `constr`, etc.)
  to enforce constraints defined in the spec

### Example Structure

#### Example model

```python
from pydantic import BaseModel, ConfigDict, Field
from asyncapi3.models.helpers import is_null


class ExampleModel(BaseModel):
  """
  Example Object.

  Description from spec/asyncapi/spec/asyncapi.md matching the specification exactly.
  """

  model_config = ConfigDict(
    extra="allow",
    revalidate_instances="always",
    validate_assignment=True,
    serialize_by_alias=True,
    validate_by_name=True,
    validate_by_alias=True,
  )

  field_name: str | None = Field(
    default=None,
    exclude_if=is_null,
    alias="fieldName",  # If JSON uses camelCase
    description="Exact description from spec/asyncapi/spec/asyncapi.md",
  )
```

#### Fields Common Patterns

##### Optional Fields with Null Exclusion

```python
field_name: str | None = Field(
  default=None,
  exclude_if=is_null,
  description="Field description from spec",
)
```

##### Required Fields

```python
field_name: str = Field(
  description="Field description from spec",
)
```

##### Fields with Default Values

```python
field_name: str = Field(
  default="default_value",
  description="Field description from spec",
)
```

##### Fields with Aliases

```python
field_name: str = Field(
  alias="fieldName",  # JSON field name
  description="Field description from spec",
)
```

##### Union Types with Reference

Many fields in AsyncAPI specification can accept either a model object or a
Reference object. Use Union types (`|`) to express this:

```python
from asyncapi3.models.base import Reference

external_docs: ExternalDocumentation | Reference | None = Field(
  default=None,
  exclude_if=is_null,
  alias="externalDocs",
  description="Additional external documentation.",
)
```

For dictionary fields that can contain models or references:

```python
from asyncapi3.models.base import Reference

channels: dict[str, Channel | Reference] | None = Field(
  default=None,
  exclude_if=is_null,
  description="An object to hold reusable Channel Objects.",
)
```

**Important**: Always import `Reference` from `asyncapi3.models.base` when using
Union types with references.

### Type Aliases

When a field can be a list of models or references, create a type alias:

```python
from asyncapi3.models.base import Reference, Tag

# Type alias for a list of Tag objects or references
Tags = list[Tag | Reference]
```

Type aliases should be defined in the same module where the related model is defined,
and exported via `__all__`.

### Custom Types

For fields that require special validation and JSON schema generation, create custom types
in `asyncapi3/models/helpers.py` using Pydantic's `__get_pydantic_core_schema__` and
`__get_pydantic_json_schema__` methods.

#### EmailStr Type

The `EmailStr` type provides email validation and proper JSON schema generation.

**Usage:**

```python
from asyncapi3.models.helpers import EmailStr
from pydantic import BaseModel

class User(BaseModel):
    email: EmailStr

# Generates JSON schema: {"type": "string", "format": "email"}
```

**Benefits:**

- Automatic email validation
- Type safety (isinstance check works)
- Proper JSON Schema generation with `"format": "email"`
- Reusable across the entire project

### Model Exports

**ALL** models and type aliases **MUST** be exported using `__all__` at the top
of each module file:

```python
"""Module description."""

__all__ = [
  "ModelName",
  "TypeAlias",
  "AnotherModel",
]

from pydantic import BaseModel, ConfigDict, Field

# ... model definitions ...
```

**Rules for `__all__`:**

- Place `__all__` immediately after the module docstring
- Include all public models and type aliases defined in the module
- Use alphabetical ordering for better readability
- Export models that are imported by other modules
- Do not export private models (starting with `_`)

**Example from `asyncapi3/models/base.py`:**

```python
"""Base models for AsyncAPI 3.0 specification."""

__all__ = ["ExternalDocumentation", "Reference", "Tag", "Tags"]

from pydantic import BaseModel, ConfigDict, Field

# ... model definitions ...

Tags = list[Tag | Reference]
```

Models exported via `__all__` should also be imported and re-exported in
`asyncapi3/models/__init__.py` for package-level access.

## Reference Extra Validators Implementation

AsyncAPI 3.0 uses `Reference` objects extensively. To ensure data integrity, we
implement extra validators that run after basic Pydantic validation.

### Workflow for Implementing/Updating Validators

When you need to implement a new validator or update an existing one (e.g., adding
more fields to check), follow these steps:

1. **Validator Location**: All reference validators are located in
    `asyncapi3/validators/`.
2. **Implementation**:
    - Each validator must implement the `ProcessorProtocol` (from
      `asyncapi3.protocols`).
    - It must have a `__call__(self, spec: AsyncAPI3) -> AsyncAPI3` method.
    - Use `spec` to traverse the model and validate `Reference` objects against
      their expected targets in `components`.
3. **Registration**:
    - Add the validator class to `asyncapi3/validators/__init__.py`.
    - Add the validator to the `extra_validators` list in `AsyncAPI3.as_builder`
      method within `asyncapi3/models/asyncapi.py` (if it should be enabled by
      default).
4. **Documentation**:
    - Update `docs/extra_validators/references.md`.
    - **CRITICAL**: This document has a dual structure. You MUST update both:
        1. The **Per model section**: Mark the specific fields in the model
            definitions (e.g., `## asyncapi3/models/info.py`).
        2. The **Per validator section**: Mark the fields in the validator's
            own section at the end of the document (e.g.,
            `## asyncapi3/validators/tags_ref_validator.py`).
    - Use checkboxes `[ ]` and `[x]` to mark progress.
    - Ensure the "Statistics section" remains accurate if new fields are added.
5. **Testing**:
    - Create or update tests in `tests/validators/test_<validator_name>.py`.
    - Use `pytest` and `pytest-cases` for comprehensive testing of valid and
      invalid references.

### Files to Review and Update

- `asyncapi3/validators/`: Directory for validator implementations.
- `asyncapi3/validators/__init__.py`: Package exports for validators.
- `asyncapi3/models/asyncapi.py`: `AsyncAPI3` root model where validators are
  registered.
- `docs/extra_validators/references.md`: Source of truth for validation status and
  requirements.
- `tests/validators/`: Directory for validator tests.

### Validation Status Tracking

Always refer to `docs/extra_validators/references.md` to see the current state of
reference validation. If you implement validation for a field, make sure to mark it
as `[x]` in this document.

## Development Workflow

1. **Read the specification**: Always refer to `spec/asyncapi/spec/asyncapi.md` when
   creating models
2. **Check JSON schemas** (optional): Cross-reference with JSON schema definitions in
   `spec/asyncapi-json-schema/definitions/3.0.0/` to verify field structures, types, and
   required fields. Remember that JSON schemas are not 1:1 with specification and have
   limitations.
3. **Check existing models**: Review similar models in `asyncapi3/models/` for
   consistency
4. **Follow naming conventions**: Use snake_case for Python, camelCase aliases for JSON
5. **Add descriptions**: Copy field descriptions exactly from the specification
6. **Write tests**: Create tests in `tests/` directory if requested
7. **Run linting**: Run `uv run pre-commit run --all-files` before committing
8. **Run checks**: Ensure code passes Ruff, MyPy, and pre-commit hooks
9. **Document**: Add appropriate docstrings and comments (in English)

## Tool Usage

### UV (for Python projects)

- **Always use `uv run`** for running commands in Python projects
- Default working folder is project root.
- Example: `uv run pytest`, `uv run ruff check .`, etc.

### Pre-commit Hooks

Run `uv run pre-commit run --all-files` before commit or final user request answer.

### Context7 MCP

When working with this project, you **SHOULD** use Context7 MCP to:

- Get up-to-date Pydantic documentation
- Get Ruff linting rules documentation
- Get pytest best practices
- Get any other library documentation needed

**Example usage:**

- Use `mcp_context7_resolve-library-id` to find library IDs
- Use `mcp_context7_query-docs` to query documentation

**Example library paths:**

- `/pydantic/pydantic` or `/websites/pydantic_dev` for Pydantic
- `/pytest-dev/pytest` for pytest
- `/astral-sh/ruff` for Ruff

**Common queries:**

- "pydantic v2 alias_generator" or "pydantic v2 fields" for Pydantic V2
  implementation details
- Check `pyproject.toml` `[tool.ruff]` section first for Ruff rules

## Questions and Clarifications

When in doubt:

1. Refer to the specification: `spec/asyncapi/spec/asyncapi.md`
2. Check existing model implementations in `asyncapi3/models/`
3. Review test examples in `tests/`
4. Use Context7 MCP to query library documentation
5. Ask for clarification if needed

When working on the project, ask clarifying questions about:

- Unclear points in AsyncAPI specification
- Architectural decisions
- Conflicting requirements
- Missing information in documentation

## Summary Checklist

Before submitting code, ensure:

- [ ] Read the relevant section in `spec/asyncapi/spec/asyncapi.md`
- [ ] (Optional) Cross-reference with JSON schema definitions in
  `spec/asyncapi-json-schema/definitions/3.0.0/` to verify field structures and types
- [ ] (Optional) Check JSON schema examples in `spec/asyncapi-json-schema/examples/3.0.0/`
  for valid test cases
- [ ] **For validators**: Use common validation functions from
  `asyncapi3/validators/common.py`
- [ ] Implement the Pydantic model in `asyncapi3/models/`
- [ ] Add `description` from spec to `Field()`
- [ ] All Pydantic fields use `Field` with descriptions from spec
- [ ] Model docstrings match the specification
- [ ] Code follows snake_case naming (variables/functions) and CamelCase (classes)
- [ ] All comments and documentation are in English
- [ ] Tests are in `tests/` directory using pytest
- [ ] (If required) Add tests in `tests/`:
  - [ ] Tests are organized in classes grouped by model type
  - [ ] Tests use examples from specification documentation
  - [ ] Use `pytest-cases` for parametrized tests with YAML examples
  - [ ] Extract only relevant objects from examples (e.g., only binding object, not
    full spec)
  - [ ] **Separate validation and serialization tests** into distinct test methods
  - [ ] Validation tests use `model_validate` with parsed YAML data
  - [ ] Serialization tests create model instances directly and compare `model_dump()`
    with complete expected dictionaries
  - [ ] Use separate case functions for validation (return `str`) and serialization
    (return `tuple[Model, dict]`)
  - [ ] Include all valid examples from specification
- [ ] **Add tests fixing validation error behavior** for models with `extra="forbid"`
  or other validation constraints:
  - [ ] Python validation error test (invalid arguments raise ValidationError)
  - [ ] YAML validation error test (invalid fields raise ValidationError)
- [ ] **Add tests for custom model validators** that check model integrity and are written
  by us (not built-in Pydantic validations):
  - [ ] Test all error scenarios with exact error messages
  - [ ] Use `pytest-cases` for parametrized tests
  - [ ] Return `tuple[str, str]` from case functions (YAML data, expected error message)
  - [ ] Use `pytest.raises(ValueError, match=expected_error)` for exact message matching
  - [ ] **For empty models** (without fields, `extra="forbid"`), create 4 tests fixing behavior:
    - [ ] Serialization test (empty dict)
    - [ ] Python validation error test (any arguments raise ValidationError)
    - [ ] YAML validation error test (any fields raise ValidationError)
    - [ ] YAML empty validation test (empty object succeeds)
    - [ ] **Store test data directly in test methods** (not in case functions)
- [ ] Code/Markdown files passes pre-commit hooks (`uv run pre-commit run --all-files`)
- [ ] EditorConfig rules are followed
