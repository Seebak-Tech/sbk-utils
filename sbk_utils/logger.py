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

    @logger_name.validator
    def validate_logger_name(self, attribute, value) -> None:
        instance_of(value, attribute.type)

    def __set_handler(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '[%(asctime)s] %(name)s:%(lineno)d %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        return console_handler

    def get_logger(self):
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(logging.INFO)
        console_handler = self.__set_handler()
        logger.addHandler(console_handler)
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
            return DefaultLogger(self.logger_name).get_logger()
        else:
            return ConfigDictLogger(
                self.logger_name, **self.kargs
            ).get_logger()
