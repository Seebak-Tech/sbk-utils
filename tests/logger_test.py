import pytest
import sbk_utils.constants as cnst
from sbk_utils.logger import LoggerFactory, InvalidDictStructure
from sbk_utils.io.loader import FileHandlerFactory, ensure_path_exists
from pathlib import Path
import logging
import logging.config


config_to_try = [
    ("invalid_key_dict"),
    ("invalid_path_dict"),
    ("invalid_value_dict")
]


@pytest.mark.parametrize(
    'dict_config',
    config_to_try,
    ids=[
        "Test invalid keys in dictionary",
        "Test invalid log path or file",
        "Test invalid values in dictionary",
    ]
)
def test_invalid_dict_config(dict_config, request):
    config = request.getfixturevalue(dict_config)
    with pytest.raises(
        InvalidDictStructure,
        match="Validate that the dictionary"
    ):
        _ = LoggerFactory(
                logger_name="sbk_scraping.parser.factories",
                config=config
            ).build()


def test_logger_config_default():
    logger = LoggerFactory(
        logger_name="sbk_utils.logger"
    ).build()
    assert logging.getLevelName(logger.level) == 'INFO'


def test_logger_valid_config():
    file_handler = FileHandlerFactory.build_from_file(
        Path(cnst.LOGGER_CONFIG_FILE)
    )
    config = file_handler.load()
    logger = LoggerFactory(
        logger_name="sbk_utils.logger",
        config=config
    ).build()
    assert logging.getLevelName(logger.level) == 'DEBUG'


def test_logger_message(caplog):
    path_invalid = Path("/home")
    ensure_path_exists(path_invalid)
    assert 'The path exists' in caplog.text
