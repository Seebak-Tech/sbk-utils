import pytest
import sbk_utils.constants as cnst
from sbk_utils.logger import Logger
from sbk_utils.io.loader import FileHandlerFactory
from pathlib import Path
import logging


@pytest.fixture
def dict_config():
    file_handler = FileHandlerFactory.build_from_file(
        Path(cnst.LOGGER_CONFIG_FILE))
    return file_handler.load()


def test_logger_level_default():
    logger = Logger(__name__).get_logger()
    assert logging.getLevelName(logger.level) == 'INFO'
