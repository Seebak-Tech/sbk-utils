import json
import yaml
from json.decoder import JSONDecodeError
from yaml.scanner import ScannerError
from yaml.parser import ParserError
from typing import Dict
import sbk_utils.loader.common as cmn


class InvalidSyntaxFile(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


def JsonLoader(data_file, cmn.FileLoader) -> Dict:
    try:
        data = json.load(data_file)
        return data
    except JSONDecodeError:
        msg = '\n*Cause: The json file has invalid content'\
            '\n*Action: Validate that the json file is correct'
        raise InvalidSyntaxFile(msg)


def YamlLoader(data_file, cmn.FileLoader) -> Dict:
    try:
        data = yaml.safe_load(data_file)
        return data
    except (ScannerError, ParserError):
        msg = '\n*Cause: YAML file has a syntax error'\
            '\n*Action: Validate that the yaml file is correct'
        raise InvalidSyntaxFile(msg)


#  class FileLoader():
    #  path: Path
#
    #  def load(self, path):
        #  try:
            #  data_file = path.open()
            #  return data_file
        #  except (IOError, OSError):
            #  msg = '\n*Cause: Error while opening the file'\
                #  '\n*Action: Validate that the file is correct'
            #  raise InvalidSyntaxFile(msg)
#
#
#  def open_file(path: Path):
    #  msg = '\n*Cause: Error while opening the file'\
          #  '\n*Action: Validate that the file is correct'
    #  ensure_path_exists(path)
    #  if not path.open():
        #  raise InvalidSyntaxFile(msg)
    #  return path.open()


