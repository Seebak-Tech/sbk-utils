import abc
from pydantic import BaseModel as PydanticBaseModel, constr
from typing import Optional, Any, Literal
from pathlib import Path


class BaseModel(PydanticBaseModel):
    class Config:
        pass


class FileLoader(abc.ABC):
    @abc.abstractmethod
    def load(self) -> Any:
        pass


class InvalidFile(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


def open_file(path: Path):
    msg = '\n*Cause: Error while opening the file'\
          '\n*Action: Validate that the file is correct'
    ensure_path_exists(path)
    if not path.open():
        raise InvalidFile(msg)
    return path.open()


def ensure_path_exists(path: Path):
    msg = f'\n*Cause: The Path does not exists'\
        f'\n*Action: Validate the following Path exists: ({path})'
    if not path.exists():
        raise ValueError(msg)
