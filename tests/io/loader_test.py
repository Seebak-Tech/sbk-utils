import pytest
from pathlib import Path
from sbk_utils.io.loader import (
    JsonHandler,
    YamlHandler,
    InvalidFile,
    InvalidSyntaxFile,
    FileHandlerFactory
)

invalid_file = Path('tests/test_data/book_to_scrape.html')

validatios_to_try = [
    (r".*The json file has invalid content*", JsonHandler, invalid_file),
    (r".*The yaml file has a syntax error*", YamlHandler, invalid_file),
]

validatios_ids = [
    "The Json file has invalid content",
    "The Yaml file has invalid content",
]


@pytest.mark.parametrize(
    'match_msg, handler, invalid_file',
    validatios_to_try,
    ids=validatios_ids
)
def test_invalid_content(match_msg, handler, invalid_file):
    with pytest.raises(
        InvalidSyntaxFile,
        match=match_msg
    ):
        _ = handler.build(invalid_file)


file_path_json = Path('tests/test_data/parsers.json')
file_path_yaml = Path('tests/test_data/logging_config.yaml')

loads_to_try = [
    (JsonHandler, file_path_json),
    (YamlHandler, file_path_yaml),
]

tasks_ids = [
    "Test a Json File loaded is an instance of JsonHandler",
    "Test a Yaml File loaded is an instance of YamlHandler",
]


@pytest.mark.parametrize(
    'loader, file_path',
    loads_to_try,
    ids=tasks_ids
)
def test_load_file(loader, file_path):
    file = FileHandlerFactory.build_from_file(file_path)
    assert isinstance(file, loader)


def test_invalid_suffix():
    file_path = Path('tests/test_data/book_to_scrape.html')
    with pytest.raises(
        InvalidFile,
        match='The file suffix is not valid'
    ):
        _ = FileHandlerFactory.build_from_file(file_path)


#  def test_load_file():
    #  file_path = Path('tests/test_data/logging_config.yaml')
    #  file = FileHandlerFactory.build_from_file(file_path)
    #  print(file)
    #  assert file == '{}'
