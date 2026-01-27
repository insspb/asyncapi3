"""Tests for validators utils helpers."""

from __future__ import annotations

from typing import cast

import pytest

from pydantic import BaseModel, ConfigDict, Field

from asyncapi3.models.asyncapi import AsyncAPI3
from asyncapi3.validators import utils


class RootContainer:
    """Simple object that exposes a root dict for navigation."""

    def __init__(self, root: dict[str, object]) -> None:
        self.root = root


class FakeModel(BaseModel):
    """Minimal Pydantic model for reference helper tests."""

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    value: object | None = Field(default=None, alias="valueAlias")
    alias_only: str = Field(default="alias", alias="aliasName")


class MissingAttrModel(BaseModel):
    """Pydantic model with a field removed to trigger AttributeError."""

    model_config = ConfigDict(
        extra="allow",
        revalidate_instances="always",
        validate_assignment=True,
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    missing: str


def _build_spec() -> AsyncAPI3:
    return AsyncAPI3(
        asyncapi="3.0.0",
        info={"title": "Test API", "version": "1.0.0"},
        channels={
            "test": {
                "address": "test",
                "messages": {
                    "msg": {
                        "payload": {"type": "object"},
                    },
                },
            },
        },
        components={
            "messages": {
                "refMessage": {"$ref": "#/channels/test/messages/msg"},
            },
        },
    )


class TestReferenceUtils:
    """Coverage tests for reference utility helpers."""

    def test_initialize_visited_refs_detects_cycles(self) -> None:
        with pytest.raises(ValueError, match="Circular reference detected"):
            utils._initialize_visited_refs(
                ref="#/channels/test",
                visited_refs={"#/channels/test"},
            )

    def test_initialize_visited_refs_initializes_set(self) -> None:
        assert utils._initialize_visited_refs(
            ref="#/channels/test",
            visited_refs=None,
        ) == {"#/channels/test"}

    def test_is_external_reference_http_true(self) -> None:
        assert utils._is_external_reference("https://example.com") is True

    def test_is_external_reference_internal_false(self) -> None:
        assert utils._is_external_reference("#/channels/test") is False

    def test_parse_reference_path_unsupported_format(self) -> None:
        with pytest.raises(ValueError, match="Unsupported reference format"):
            utils._parse_reference_path("channels/test")

    def test_parse_reference_path_invalid_path(self) -> None:
        with pytest.raises(ValueError, match="Invalid reference path"):
            utils._parse_reference_path("#")

    def test_resolve_reference_external_returns_none(self) -> None:
        spec = _build_spec()
        assert utils.resolve_reference("http://example.com/schema", spec) is None

    def test_resolve_reference_external_logs_warning(
        self,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        spec = _build_spec()
        with caplog.at_level("WARNING"):
            utils.resolve_reference("http://example.com/schema", spec)
        assert "External reference" in caplog.text

    def test_resolve_reference_value_error_on_attribute_error(self) -> None:
        model = MissingAttrModel(missing="value")
        object.__delattr__(model, "missing")
        spec = cast(AsyncAPI3, model)
        with pytest.raises(ValueError, match="Failed to resolve reference"):
            utils.resolve_reference("#/missing", spec)

    def test_resolve_reference_follows_reference_chain_returns_result(self) -> None:
        spec = _build_spec()
        result = utils.resolve_reference("#/components/messages/refMessage", spec)
        assert result is not None

    def test_resolve_reference_follows_reference_chain_path(self) -> None:
        spec = _build_spec()
        result = utils.resolve_reference("#/components/messages/refMessage", spec)
        assert result.path == "spec.channels.test.messages.msg"

    def test_resolve_reference_follows_reference_chain_type(self) -> None:
        spec = _build_spec()
        result = utils.resolve_reference("#/components/messages/refMessage", spec)
        assert result.resolved_type.__name__ == "Message"

    def test_resolve_reference_invalid_format(self) -> None:
        spec = _build_spec()
        with pytest.raises(ValueError, match="Unsupported reference format"):
            utils.resolve_reference("invalid", spec)

    def test_resolve_path_part_root(self) -> None:
        root_obj = RootContainer({"item": {"nested": "value"}})
        next_obj, next_type = utils._resolve_path_part(root_obj, "item", "spec.item")
        assert next_obj == {"nested": "value"}

    def test_resolve_path_part_root_type(self) -> None:
        root_obj = RootContainer({"item": {"nested": "value"}})
        _next_obj, next_type = utils._resolve_path_part(root_obj, "item", "spec.item")
        assert next_type is dict

    def test_resolve_path_part_dict(self) -> None:
        next_obj, _next_type = utils._resolve_path_part(
            {"item": 1},
            "item",
            "spec.item",
        )
        assert next_obj == 1

    def test_resolve_path_part_dict_type(self) -> None:
        _next_obj, next_type = utils._resolve_path_part(
            {"item": 1},
            "item",
            "spec.item",
        )
        assert next_type is int

    def test_resolve_path_parts_skips_empty_segments_path(self) -> None:
        spec = _build_spec()
        _resolved, _resolved_type, path = utils._resolve_path_parts(
            spec,
            ["channels", "", "test"],
        )
        assert path == "spec.channels.test"

    def test_resolve_path_parts_skips_empty_segments_type(self) -> None:
        spec = _build_spec()
        _resolved, resolved_type, _path = utils._resolve_path_parts(
            spec,
            ["channels", "", "test"],
        )
        assert resolved_type.__name__ == "Channel"

    def test_resolve_path_parts_skips_empty_segments_object(self) -> None:
        spec = _build_spec()
        resolved, _resolved_type, _path = utils._resolve_path_parts(
            spec,
            ["channels", "", "test"],
        )
        assert hasattr(resolved, "address")

    def test_resolve_path_part_root_missing_key_error(self) -> None:
        with pytest.raises(ValueError, match="Reference key 'missing' not found"):
            utils._resolve_path_part(RootContainer({"item": 1}), "missing", "spec")

    def test_resolve_path_part_invalid_object_error(self) -> None:
        with pytest.raises(ValueError, match="Cannot navigate"):
            utils._resolve_path_part(1, "item", "spec")

    def test_resolve_from_dict_missing_key_error(self) -> None:
        with pytest.raises(ValueError, match="Reference key 'missing' not found"):
            utils._resolve_from_dict({}, "missing", "spec.missing")

    def test_resolve_from_model_value(self) -> None:
        model = FakeModel(value="value")
        next_obj, next_type = utils._resolve_from_model(model, "value", "spec.value")
        assert next_obj == "value"

    def test_resolve_from_model_value_type(self) -> None:
        model = FakeModel(value="value")
        _next_obj, next_type = utils._resolve_from_model(model, "value", "spec.value")
        assert next_type is str

    def test_resolve_from_model_alias(self) -> None:
        model = FakeModel(value="value")
        next_obj, _next_type = utils._resolve_from_model(
            model,
            "aliasName",
            "spec.alias",
        )
        assert next_obj == "alias"

    def test_resolve_from_model_alias_type(self) -> None:
        model = FakeModel(value="value")
        _next_obj, next_type = utils._resolve_from_model(
            model,
            "aliasName",
            "spec.alias",
        )
        assert next_type is str

    def test_resolve_from_model_none_value_error(self) -> None:
        model_none = FakeModel(value=None)
        with pytest.raises(ValueError, match=r"Reference path 'spec.value' is None"):
            utils._resolve_from_model(model_none, "value", "spec.value")

    def test_resolve_from_model_missing_field_error(self) -> None:
        model_none = FakeModel(value=None)
        with pytest.raises(ValueError, match="Field 'missing' not found"):
            utils._resolve_from_model(model_none, "missing", "spec.missing")

    def test_find_model_field_name_direct(self) -> None:
        model = FakeModel(value="value")
        assert utils._find_model_field_name(model, "value") == "value"

    def test_find_model_field_name_alias(self) -> None:
        model = FakeModel(value="value")
        assert utils._find_model_field_name(model, "aliasName") == "alias_only"

    def test_find_model_field_name_missing(self) -> None:
        model = FakeModel(value="value")
        assert utils._find_model_field_name(model, "missing") is None
