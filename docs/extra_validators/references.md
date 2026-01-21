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
```

### Statistics section

- **Total fields with Reference**: int
- **Validated fields**: int
- **Non-validated fields**: int
