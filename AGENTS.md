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
- `asyncapi3/__init__.py` - Package exports
- `tests/` - project tests:
- `tests/fixtures/` - Test fixtures (JSON/YAML specs)

## Specification Location

The AsyncAPI 3 and related bindings specifications documentation are included as a git
submodules:

- **Main specification**: `spec/asyncapi/spec/asyncapi.md`
- **Bindings specifications**: `spec/bindings/` directory (each subdirectory contains
  documentation for a specific binding type)
- **Examples and scripts**: `spec/asyncapi/examples/` directory

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


# Case functions for pytest-cases
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


class TestMQTTServerBindings:
    """Tests for MQTTServerBindings model."""

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

    def test_mqtt_server_binding_session_expiry_interval_schema(self) -> None:
        """Test MQTTServerBindings with sessionExpiryInterval as Schema."""
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

#### Testing Serialization (model_dump/model_dump_json)

When testing models based on examples from documentation, create tests that verify
serialization:

1. **Create Python object** from example data
2. **Serialize to JSON** using `model_dump()` or `model_dump_json()`
3. **Verify the resulting JSON** matches expected structure

```python
def test_mqtt_server_binding_serialization(self) -> None:
    """Test MQTTServerBindings serialization to JSON."""
    yaml_data = """
    mqtt:
      clientId: guest
      cleanSession: true
      bindingVersion: 0.2.0
    """
    data = yaml.safe_load(yaml_data)
    mqtt_binding = MQTTServerBindings.model_validate(data["mqtt"])

    # Serialize to dict and verify all fields
    dumped = mqtt_binding.model_dump(by_alias=True, exclude_none=True)
    assert dumped["clientId"] == "guest"
    assert dumped["cleanSession"] is True
    assert dumped["bindingVersion"] == "0.2.0"

    # Or serialize to JSON string
    json_str = mqtt_binding.model_dump_json(by_alias=True, exclude_none=True)
    assert "guest" in json_str
```

#### Testing Static Objects

When testing with static objects (not parametrized), verify **all fields** in the
resulting object:

```python
def test_mqtt_server_binding_last_will(self) -> None:
    """Test MQTTServerBindings with lastWill object."""
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
initialization and verify default values are dumped:

```python
def test_mqtt_channel_binding_empty(self) -> None:
    """Test MQTTChannelBindings empty object initialization."""
    # Empty object initialization
    mqtt_binding = MQTTChannelBindings()

    # Verify it can be serialized
    dumped = mqtt_binding.model_dump(by_alias=True, exclude_none=True)
    assert dumped == {}

    # If model has default values, verify they are included
    # Example for models with binding_version default:
    server_binding = MQTTServerBindings()
    dumped = server_binding.model_dump(by_alias=True, exclude_none=True)
    assert dumped["bindingVersion"] == "0.2.0"  # Default value
```

#### Key Points

- **Always use `model_validate`** with parsed YAML/JSON data (via `yaml.safe_load()` or
  `json.loads()`)
- **Extract only relevant objects** from examples (e.g., only `mqtt` binding object,
  not the entire server structure)
- **Group tests in classes** by model type for better organization
- **Use pytest-cases** for parametrized tests with multiple examples (YAML, JSON, or
  any test data)
- **Store case functions in the same file** as tests
- **Include all valid examples** from the specification for comprehensive coverage
- **Test serialization** using `model_dump()`/`model_dump_json()` to verify round-trip
  compatibility
- **Verify all fields** when testing static objects
- **Test empty initialization** for models with optional/default fields
- **Add additional tests** for edge cases (e.g., Schema objects, optional fields)

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

All Pydantic models should use the following standard configuration:

```python
model_config = ConfigDict(
  extra="allow",
  revalidate_instances="always",
  validate_assignment=True,
)
```

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

## Development Workflow

1. **Read the specification**: Always refer to `spec/asyncapi/spec/asyncapi.md` when
   creating models
2. **Check existing models**: Review similar models in `asyncapi3/models/` for
   consistency
3. **Follow naming conventions**: Use snake_case for Python, camelCase aliases for JSON
4. **Add descriptions**: Copy field descriptions exactly from the specification
5. **Write tests**: Create tests in `tests/` directory if requested
6. **Run linting**: Run `uv run pre-commit run --all-files` before committing
7. **Run checks**: Ensure code passes Ruff, MyPy, and pre-commit hooks
8. **Document**: Add appropriate docstrings and comments (in English)

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
  - [ ] Use `model_validate` with parsed YAML data
  - [ ] Include all valid examples from specification
- [ ] Code/Markdown files passes pre-commit hooks (`uv run pre-commit run --all-files`)
- [ ] EditorConfig rules are followed
