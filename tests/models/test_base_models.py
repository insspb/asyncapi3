"""Tests for base model classes."""

import pytest
import yaml

from pydantic import ValidationError

from asyncapi3.models.base_models import (
    ExtendableBaseModel,
    NonExtendableBaseModel,
    PatternedRootModel,
)


class TestExtendableBaseModel:
    """Tests for ExtendableBaseModel."""

    def test_extendable_model_allows_valid_extensions(self) -> None:
        """Test that ExtendableBaseModel allows valid specification extensions."""

        class TestModel(ExtendableBaseModel):
            name: str

        # Valid extension starting with "x-"
        yaml_data = """
        name: test
        x-custom-field: value
        x-internal-id: 123
        x-more-extension: true
        """

        data = yaml.safe_load(yaml_data)
        model = TestModel.model_validate(data)

        assert model.name == "test"
        assert model.model_extra == {
            "x-custom-field": "value",
            "x-internal-id": 123,
            "x-more-extension": True,
        }

    def test_extendable_model_rejects_invalid_extensions(self) -> None:
        """Test that ExtendableBaseModel rejects invalid extensions."""

        class TestModel(ExtendableBaseModel):
            name: str

        # Invalid extension not starting with "x-"
        yaml_data = """
        name: test
        custom-field: value
        y-extension: invalid
        """

        data = yaml.safe_load(yaml_data)

        with pytest.raises(
            ValueError, match="does not match specification extension pattern"
        ):
            TestModel.model_validate(data)

    def test_extendable_model_serialization_with_extensions(self) -> None:
        """Test serialization of ExtendableBaseModel with extensions."""

        class TestModel(ExtendableBaseModel):
            name: str

        model = TestModel(name="test")
        # Manually set extra fields for testing
        model.__pydantic_extra__ = {"x-custom": "value"}

        dumped = model.model_dump()
        assert dumped == {"name": "test", "x-custom": "value"}

    def test_extendable_model_empty_extensions(self) -> None:
        """Test ExtendableBaseModel without extensions."""

        class TestModel(ExtendableBaseModel):
            name: str

        yaml_data = """
        name: test
        """

        data = yaml.safe_load(yaml_data)
        model = TestModel.model_validate(data)

        assert model.name == "test"
        assert model.model_extra is None or len(model.model_extra) == 0


class TestNonExtendableBaseModel:
    """Tests for NonExtendableBaseModel."""

    def test_non_extendable_model_forbids_extra_fields(self) -> None:
        """Test that NonExtendableBaseModel forbids any extra fields."""

        class TestModel(NonExtendableBaseModel):
            name: str

        yaml_data = """
        name: test
        extra_field: value
        """

        data = yaml.safe_load(yaml_data)

        with pytest.raises(ValidationError):
            TestModel.model_validate(data)

    def test_non_extendable_model_allows_defined_fields_only(self) -> None:
        """Test that NonExtendableBaseModel allows only defined fields."""

        class TestModel(NonExtendableBaseModel):
            name: str
            value: int

        yaml_data = """
        name: test
        value: 42
        """

        data = yaml.safe_load(yaml_data)
        model = TestModel.model_validate(data)

        assert model.name == "test"
        assert model.value == 42

    def test_non_extendable_model_serialization(self) -> None:
        """Test serialization of NonExtendableBaseModel."""

        class TestModel(NonExtendableBaseModel):
            name: str
            value: int

        model = TestModel(name="test", value=42)
        dumped = model.model_dump()

        assert dumped == {"name": "test", "value": 42}

    def test_non_extendable_model_python_validation_error(self) -> None:
        """Test NonExtendableBaseModel Python validation error with extra arguments."""

        class TestModel(NonExtendableBaseModel):
            name: str

        with pytest.raises(ValidationError):
            TestModel(name="test", extra_field="value")


class TestPatternedRootModel:
    """Tests for PatternedRootModel."""

    def test_patterned_object_valid_keys(self) -> None:
        """Test PatternedRootModel accepts valid keys."""

        class TestObject(PatternedRootModel[str]):
            pass

        # Valid keys
        data = {
            "user": "value1",
            "user123": "value2",
            "user-name": "value3",
            "user_name": "value4",
            "user.name": "value5",
        }

        obj = TestObject.model_validate(data)
        assert obj.root == data
        assert len(obj.root) == 5

    def test_patterned_object_invalid_keys(self) -> None:
        """Test PatternedRootModel rejects invalid keys."""

        class TestObject(PatternedRootModel[str]):
            pass

        # Invalid keys
        invalid_data = {
            "user id": "value1",  # space
            "user@id": "value2",  # special char @
            "user(id)": "value3",  # parentheses
        }

        with pytest.raises(
            ValueError, match="does not match patterned object key pattern"
        ):
            TestObject.model_validate(invalid_data)

    def test_patterned_object_iteration(self) -> None:
        """Test PatternedRootModel __iter__ method."""

        class TestObject(PatternedRootModel[str]):
            pass

        data = {"user1": "value1", "user2": "value2"}
        obj = TestObject.model_validate(data)

        keys = list(obj)
        assert len(keys) == 2
        assert "user1" in keys
        assert "user2" in keys

    def test_patterned_object_getitem(self) -> None:
        """Test PatternedRootModel __getitem__ method."""

        class TestObject(PatternedRootModel[str]):
            pass

        data = {"user1": "value1", "user2": "value2"}
        obj = TestObject.model_validate(data)

        assert obj["user1"] == "value1"
        assert obj["user2"] == "value2"

    def test_patterned_object_getattr(self) -> None:
        """Test PatternedRootModel __getattr__ method."""

        class TestObject(PatternedRootModel[str]):
            pass

        data = {"user1": "value1", "user2": "value2"}
        obj = TestObject.model_validate(data)

        assert obj.user1 == "value1"
        assert obj.user2 == "value2"

    def test_patterned_object_empty_dict(self) -> None:
        """Test PatternedRootModel with empty dictionary."""

        class TestObject(PatternedRootModel[str]):
            pass

        obj = TestObject.model_validate({})
        assert obj.root == {}
        assert len(obj.root) == 0

    def test_patterned_object_single_valid_key(self) -> None:
        """Test PatternedRootModel with single valid key."""

        class TestObject(PatternedRootModel[int]):
            pass

        data = {"validKey123": 42}
        obj = TestObject.model_validate(data)

        assert obj.root == data
        assert obj.validKey123 == 42
        assert obj["validKey123"] == 42
