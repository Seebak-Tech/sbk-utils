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


class FileLoader(abc.ABC):
    @abc.abstractmethod
    def load(self) -> Any:
        pass
    

@dataclass
class FileLoaderFactory():
    file_path: Path

    def invalid_suffix(self):
        msg = '\n*Cause: The file suffix is not valid'\
              '\n*Action: Validate that the suffix of the file is correct'
        raise InvalidFile(msg)

    def build(self):
        ensure_path_exists(self.file_path)
        loader_type = self.file_path.suffix

        switch_loader_type = {
            ".json": JsonLoader(self.file_path).load(),

            ".yaml": YamlLoader(self.file_path).load()
        }
        return switch_loader_type.get(loader_type, self.invalid_suffix)


class JsonLoader(FileLoaderFactory):

    def load(self) -> dict:
        import json
        from json.decoder import JSONDecodeError
        try:
            with self.file_path.open() as file:
                data = json.load(file)
            return data
        except JSONDecodeError:
            msg = '\n*Cause: The json file has invalid content'\
                '\n*Action: Validate that the json file is correct'
            raise InvalidSyntaxFile(msg)


class YamlLoader(FileLoaderFactory):

    def load(self) -> dict:
        import yaml
        from yaml.scanner import ScannerError
        from yaml.parser import ParserError
        try:
            with self.file_path.open() as file:
                data = yaml.safe_load(file)
            return data
        except (ScannerError, ParserError):
            msg = f'\n*Cause: YAML file has a syntax error in ({self.file_path})'\
                '\n*Action: Validate that the yaml file is correct'
            raise InvalidSyntaxFile(msg)


def ensure_path_exists(path: Path):
    msg = f'\n*Cause: The Path does not exists'\
        f'\n*Action: Validate the following Path exists: ({path})'
    if not path.exists():
        raise ValueError(msg)
