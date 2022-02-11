import logging.config
import logging
import abc
from attrs import define, field
from sbk_utils.data.validators import instance_of


class InvalidDictStructure(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class Logger(abc.ABC):

    @abc.abstractmethod
    def get_logger(self):
        pass


@define()
class DefaultLogger(Logger):
    logger_name: str = field()
    log_level: str = field(default="DEBUG")

    @logger_name.validator
    def validate_logger_name(self, attribute, value) -> None:
        instance_of(value, attribute.type)

    def __get_logger_level(self):
        switcher = {
            "CRITICAL": logging.CRITICAL,
            "ERROR": logging.ERROR,
            "WARNING": logging.WARNING,
            "INFO": logging.INFO,
            "DEBUG": logging.DEBUG
        }
        level = switcher.get(self.log_level, 0)
        if level == 0:
            msg = "\n*Cause: The logger level is invalid, given"\
                  f"({self.log_level})"\
                  "\n*Action: Assign the correct logger level value:"\
                  "['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']"
            raise ValueError(msg)
        return level

    def __build_console_handler(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.__get_logger_level())
        formatter = logging.Formatter(
            '[%(asctime)s] %(name)s:%(lineno)d %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        return console_handler

    def get_logger(self):
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.__get_logger_level())
        handler = self.__build_console_handler()
        logger.addHandler(handler)
        return logger


@define()
class ConfigDictLogger(Logger):
    logger_name: str = field()
    config: dict = field()


    @logger_name.validator
    def validate_logger_name(self, attribute, value) -> None:
        instance_of(value, attribute.type)

    def get_logger(self):
        try:
            logging.config.dictConfig(self.config)
            logger = logging.getLogger(self.logger_name)
            return logger
        except ValueError as exception:
            msg = f'\n*Cause: ({exception.__cause__})'\
                f'\n        ({exception.args[0]})'\
                '\n*Action: Validate that the dictionary structure'\
                ' is correct(keys, values)'
            raise InvalidDictStructure(msg) from exception


class LoggerFactory():

    def __init__(self, logger_name: str, **kargs):
        self.logger_name = logger_name
        self.kargs = kargs

    def build(self):
        if self.kargs.get("config") is None:
            return DefaultLogger(
                self.logger_name,
                **self.kargs
            ).get_logger()
        else:
            return ConfigDictLogger(
                self.logger_name,
                **self.kargs
            ).get_logger()
