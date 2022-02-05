import logging.config
import logging
from attrs import define


@define
class Logger():
    logger_name: str

    def get_logger(self, dict_config: dict = None):
        if dict_config is None:
            logger = logging.getLogger(self.logger_name)
            self.__build_dflt_config(logger)
        else:
            logging.config.dictConfig(dict_config)
            logger = logging.getLogger(self.logger_name)
        return logger

    def __build_dflt_config(self, logger):
        logger.setLevel(logging.INFO)
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '[%(asctime)s] %(name)s:%(lineno)d %(levelname)s - %(message)s'
        )

        consoleHandler.setFormatter(formatter)
        logger.addHandler(consoleHandler)
        return logger
