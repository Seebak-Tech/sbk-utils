from typing import Any
from dataclasses import dataclass
from pathlib import Path
import abc
import sbk_utils.constants as cnst
from sbk_utils.logger import Logger


logger = Logger(__name__).get_logger()


class InvalidSyntaxFile(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class InvalidFile(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


@dataclass
class FileHandler(abc.ABC):

    @abc.abstractmethod
    def load(self) -> Any:
        pass

    @abc.abstractmethod
    def build(self) -> Any:
        pass


@dataclass(init=False)
class FileHandlerFactory():

    @classmethod
    def build_from_file(cls, file_path) -> FileHandler:
        ensure_path_exists(file_path)
        loader_type = file_path.suffix
        switcher = {
            cnst.SUFFIX_JSON: JsonHandler,
            cnst.SUFFIX_YAML: YamlHandler
        }
        file_handler = switcher.get(
            loader_type,
            NullHandler
        ).build(file_path)
        return file_handler


@dataclass()
class NullHandler(FileHandler):
    data: dict

    @classmethod
    def build(cls, file_path) -> FileHandler:
        msg = '\n*Cause: The file suffix is not valid'\
              '\n*Action: The suffixes permited are [json, yaml]'
        raise InvalidFile(msg)

    def load(self) -> dict:
        return self.data


@dataclass()
class JsonHandler(FileHandler):
    data: dict

    @classmethod
    def build(cls, file_path) -> FileHandler:
        import json
        from json.decoder import JSONDecodeError
        try:
            with file_path.open() as file:
                data = json.load(file)
            return cls(data)
        except JSONDecodeError:
            msg = '\n*Cause: The json file has invalid content'\
                '\n*Action: Validate that the json file is correct'
            raise InvalidSyntaxFile(msg)

    def load(self) -> dict:
        return self.data


@dataclass()
class YamlHandler(FileHandler):
    data: dict

    @classmethod
    def build(cls, file_path) -> FileHandler:
        import yaml
        from yaml.scanner import ScannerError
        from yaml.parser import ParserError
        try:
            with file_path.open() as file:
                data = yaml.safe_load(file)
            return cls(data)
        except (ScannerError, ParserError):
            msg = '\n*Cause: The yaml file has a syntax error'\
                  f'in ({file_path})'\
                  '\n*Action: Validate that the yaml file is correct'
            raise InvalidSyntaxFile(msg)

    def load(self) -> dict:
        return self.data


def ensure_path_exists(path: Path):
    msg = f'\n*Cause: The Path does not exists'\
        f'\n*Action: Validate the following Path exists: ({path})'
    if not path.exists():
        raise ValueError(msg)
