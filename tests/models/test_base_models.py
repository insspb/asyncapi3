"""Tests for base model classes."""

import pytest
import yaml

from pydantic import ValidationError

from asyncapi3.models.base_models import ExtendableBaseModel, NonExtendableBaseModel


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
