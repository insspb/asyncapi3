from pathlib import Path

import pytest

from asyncapi3 import AsyncAPI3

VALID_JSON_SPECS_FOLDER = "tests/fixtures/json_specs/valid"


@pytest.mark.parametrize(
    "path",
    list(Path.iterdir(Path(VALID_JSON_SPECS_FOLDER))),
    ids=[str(file) for file in Path.iterdir(Path(VALID_JSON_SPECS_FOLDER))],
)
def test_async_api3_parse_any_valid_json_spec(path: Path) -> None:
    assert AsyncAPI3.model_validate_json(path.read_text()) is not None
