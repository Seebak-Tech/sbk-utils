import pytest
import sbk_utils.constants as cnst
from sbk_utils.io.loader import FileHandlerFactory
from pathlib import Path


@pytest.fixture(scope="session")
def search_dict():
    return {
        'key1': 'valor1',
        'key2': [
            {'inner_lst_key1': 1, 'inner_lst_key2': 2},
            {'inner_lst_key1': 3, 'inner_lst_key2': 4},
            {'inner_lst_key3': 'valor2'}
        ],
        'key3': {
            'inner_dict_key1': 'a',
            'inner_dict_key2': 'b'
        },
        'key4': True
    }


@pytest.fixture()
def default_config():
    config_file = cnst.LOGGER_CONFIG_FILE
    file_handler = FileHandlerFactory.build_from_file(Path(config_file))
    return file_handler.load()


@pytest.fixture()
def invalid_key_dict(default_config):
    config = default_config.copy()
    config["handlers"]["file"]["backupCount"] = 20
    return config


@pytest.fixture()
def invalid_path_dict(default_config):
    config = default_config.copy()
    config["handlers"]["file"]["filename"] = "/work"
    return config


@pytest.fixture()
def invalid_value_dict(default_config):
    config = default_config.copy()
    config["handlers"]["console"]["level"] = "hola"
    return config
