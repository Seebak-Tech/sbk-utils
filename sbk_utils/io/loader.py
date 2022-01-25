from typing import Any
from dataclasses import dataclass
from pathlib import Path
import abc


class InvalidSyntaxFile(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class InvalidFile(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


@dataclass
class FileHandler(abc.ABC):
    #  file_path: Path

    @abc.abstractmethod
    def load(self) -> Any:
        pass


@dataclass(init=False)
class FileHandlerFactory():

    @classmethod
    def invalid_suffix(cls):
        msg = '\n*Cause: The file suffix is not valid'\
              '\n*Action: The suffixes permited are [json, yaml]'
        raise InvalidFile(msg)

    @classmethod
    def build_from_file(cls, file_path) -> FileHandler:
        ensure_path_exists(file_path)
        loader_type = file_path.suffix
        print(loader_type)
        switcher = {
            ".json": JsonHandler,
            ".yaml": YamlHandler
        }
        return switcher.get(
            loader_type,
            cls.invalid_suffix()
        )(file_path).load()


@dataclass(init=False)
class JsonHandler(FileHandler):
    data: dict

    def load(self, file_path) -> dict:
        import json
        from json.decoder import JSONDecodeError
        try:
            with file_path.open() as file:
                data = json.load(file)
            return data
        except JSONDecodeError:
            msg = '\n*Cause: The json file has invalid content'\
                '\n*Action: Validate that the json file is correct'
            raise InvalidSyntaxFile(msg)


@dataclass(init=False)
class YamlHandler(FileHandler):
    data: dict

    def load(self, file_path) -> dict:
        import yaml
        from yaml.scanner import ScannerError
        from yaml.parser import ParserError
        try:
            with file_path.open() as file:
                data = yaml.safe_load(file)
            return data
        except (ScannerError, ParserError):
            msg = '\n*Cause: The yaml file has a syntax error'\
                  f'in ({file_path})'\
                  '\n*Action: Validate that the yaml file is correct'
            raise InvalidSyntaxFile(msg)


def ensure_path_exists(path: Path):
    msg = f'\n*Cause: The Path does not exists'\
        f'\n*Action: Validate the following Path exists: ({path})'
    if not path.exists():
        raise ValueError(msg)
