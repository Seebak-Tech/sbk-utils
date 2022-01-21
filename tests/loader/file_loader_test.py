import pytest
from sbk_utils.loader.file_loader import JsonLoader, YamlLoader, InvalidSyntaxFile


def test_load_json(path):
    file_loaded = JsonLoader(path.open())
    assert isinstance(file_loaded, dict)


def test_load_yaml(path):
    load_file = YamlLoader(path.open())
    assert isinstance(load_file, dict)


def test_invalid_content_jsonfile(invalid_path):
    with pytest.raises(
        InvalidSyntaxFile,
        match='The json file has invalid content'
    ):
        _ = JsonLoader(invalid_path.open())


def test_invalid_yaml_file(invalid_path):
    with pytest.raises(
        InvalidSyntaxFile,
        match='YAML file has a syntax error'
    ):
        _ = YamlLoader(invalid_path.open())
