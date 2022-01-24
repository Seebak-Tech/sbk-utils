import pytest
from pathlib import Path
from sbk_utils.io.loader import (
    JsonLoader,
    YamlLoader,
    InvalidSyntaxFile,
    FileLoaderFactory
)


@pytest.fixture(scope="session")
def file_path():
    return Path('tests/test_data/parsers.json')


@pytest.fixture(scope="session")
def invalid_file():
    return Path('tests/test_data/book_to_scrape.html')


def test_build(file_path):
    data_file = FileLoaderFactory(file_path)
    result = data_file.build()
    assert isinstance(result, dict)
    #  assert 'hola' == result


def test_load_json(file_path):
    file = JsonLoader(file_path)
    file_loaded = file.load()
    assert isinstance(file_loaded, dict)


def test_load_yaml(file_path):
    file = JsonLoader(file_path)
    file_loaded = file.load()
    assert isinstance(file_loaded, dict)


def test_invalid_content_jsonfile(invalid_file):
    with pytest.raises(
        InvalidSyntaxFile,
        match='The json file has invalid content'
    ):
        _ = JsonLoader(invalid_file).load()


def test_invalid_yaml_file(invalid_file):
    with pytest.raises(
        InvalidSyntaxFile,
        match='YAML file has a syntax error'
    ):
        _ = YamlLoader(invalid_file).load()
