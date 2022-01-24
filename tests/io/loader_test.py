import pytest
from pathlib import Path
from sbk_utils.io.loader import (
    JsonLoader,
    YamlLoader,
    InvalidFile,
    InvalidSyntaxFile,
    FileLoaderFactory
)


invalid_file = Path('tests/test_data/book_to_scrape.html')

validatios_to_try = [
    (r".*The json file has invalid content*", JsonLoader(invalid_file)),
    (r".*YAML file has a syntax error*", YamlLoader(invalid_file)),
]

validatios_ids = [
    "The Json file has invalid content",
    "The Yaml file has invalid content",
]


@pytest.mark.parametrize(
    'match_msg, loader',
    validatios_to_try,
    ids=validatios_ids
)
def test_invalid_content(match_msg, loader):
    with pytest.raises(
        InvalidSyntaxFile,
        match=match_msg
    ):
        _ = loader.load()


file_path_json = Path('tests/test_data/parsers.json')
file_path_yaml = Path('tests/test_data/logging_config.yaml')

tasks_to_try = [
    (JsonLoader(file_path_json)),
    (YamlLoader(file_path_yaml)),
]

tasks_ids = [
    "Test a Json File",
    "Test a Yaml File",
]


@pytest.mark.parametrize(
    'data_file',
    tasks_to_try,
    ids=tasks_ids
)
def test_load_file(data_file):
    file_loaded = data_file.load()
    assert isinstance(file_loaded, dict)


tasks = [
    (Path('tests/test_data/logging_config.yaml'), YamlLoader),
    (Path('tests/test_data/parsers.json'), JsonLoader),
]

ids = [
    "Test build a JsonLoader instance from a json file ",
    "Test build a YamlLoader instance from a yaml file ",
]


@pytest.mark.parametrize(
    'file_path, loader',
    tasks,
    ids=ids
)
def test_build(file_path, loader):
    data_file = FileLoaderFactory(file_path)
    result = data_file.build()
    assert isinstance(result, dict)
    #  assert isinstance(result, loader)


def test_build_yaml():
    file_path = Path('tests/test_data/logging_config.yaml')
    data_file = FileLoaderFactory(file_path)
    result = data_file.build()
    #  print(type(result))
    #  assert isinstance(result, YamlLoader)
    assert isinstance(result, dict)


def test_invalid_suffix():
    file_path = Path('tests/test_data/book_to_scrape.html')
    with pytest.raises(
        InvalidFile,
        match = 'The file suffix is not valid'
    ):
        _ = FileLoaderFactory(file_path).build()

