from itertools import chain
from pathlib import Path

import pytest
import yaml

from asyncapi3 import AsyncAPI3

VALID_JSON_SPECS_FOLDER = "tests/fixtures/json_specs/valid"
VALID_YAML_SPECS_FOLDER = "tests/fixtures/yaml_specs/valid/single_file"
EXTRA_VALID_YAML_SPECS = [
    Path("tests/fixtures/yaml_specs/valid/multi_files/backend/asyncapi.yaml"),
    Path("tests/fixtures/yaml_specs/valid/multi_files/comments-service/asyncapi.yaml"),
    Path("tests/fixtures/yaml_specs/valid/multi_files/frontend/asyncapi.yaml"),
    Path(
        "tests/fixtures/yaml_specs/valid/multi_files/notification-service/asyncapi.yaml"
    ),
    Path("tests/fixtures/yaml_specs/valid/multi_files/public-api/asyncapi.yaml"),
]


@pytest.mark.parametrize(
    "path",
    list(Path.iterdir(Path(VALID_JSON_SPECS_FOLDER))),
    ids=[str(file) for file in Path.iterdir(Path(VALID_JSON_SPECS_FOLDER))],
)
def test_async_api3_parse_any_valid_json_spec(path: Path) -> None:
    assert AsyncAPI3.model_validate_json(path.read_text()) is not None


@pytest.mark.parametrize(
    "path",
    chain(list(Path.iterdir(Path(VALID_YAML_SPECS_FOLDER))), EXTRA_VALID_YAML_SPECS),
    ids=[
        str(file)
        for file in chain(
            list(Path.iterdir(Path(VALID_YAML_SPECS_FOLDER))), EXTRA_VALID_YAML_SPECS
        )
    ],
)
def test_async_api3_parse_any_valid_yaml_spec(path: Path) -> None:
    spec = yaml.safe_load(path.read_text())
    assert AsyncAPI3.model_validate(spec) is not None
