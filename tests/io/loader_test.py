import pytest
from sbk_utils.io.loader import JsonLoader, YamlLoader, InvalidSyntaxFile, FileLoaderFactory
from pathlib import Path


@pytest.fixture(scope="session")
def file_path():
    return Path('/workspace/sbk-utils/tests/test_data/parsers.json')


@pytest.fixture(scope="session")
def invalid_file():
    return Path('/workspace/sbk-utils/tests/test_data/book_to_scrape.html')


def test_build(file_path):
    s = FileLoaderFactory(file_path)
    result = s.build()
    print(file_path.suffix)
    assert isinstance(result, dict)


def test_load_json(file_path):
    file = JsonLoader(file_path)
    file_loaded = file.load()
    assert isinstance(file_loaded, dict)


def test_load_yaml(file_path):
    file = JsonLoader(file_path)
    file_loaded = file.load()
    assert isinstance(file_loaded, dict)


#  def test_invalid_content_jsonfile(invalid_file):
    #  with pytest.raises(
        #  InvalidSyntaxFile,
        #  match='The json file has invalid content'
    #  ):
        #  _ = JsonLoader(invalid_file)
#
#
#  def test_invalid_yaml_file(invalid_file):
    #  with pytest.raises(
        #  InvalidSyntaxFile,
        #  match='YAML file has a syntax error'
    #  ):
        #  _ = YamlLoader(invalid_file)
