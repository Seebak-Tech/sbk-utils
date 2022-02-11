from sbk_utils.logger import LoggerFactory, InvalidDictStructure
from sbk_utils.io.loader import FileHandlerFactory, ensure_path_exists
import sbk_utils.constants as cnst
from pathlib import Path
import logging.config
import logging
import pytest


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
    assert logging.getLevelName(logger.level) == 'DEBUG'


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


def test_logger_config_level_default():
    logger = LoggerFactory(
        logger_name="sbk_utils.logger",
        log_level="CRITICAL"
    ).build()
    assert logging.getLevelName(logger.level) == 'CRITICAL'


def test_invalid_level_default():
    with pytest.raises(
        ValueError,
        match="The logger level is invalid"
    ):
        _ = LoggerFactory(
                logger_name="sbk_utils.logger",
                log_level="INCORRECT_LEVEL"
            ).build()
