from typing import Any
from dataclasses import dataclass
from pathlib import Path
from sbk_utils.loader.file_loader import YamlLoader, JsonLoader 
from sbk_utils.loader.common import open_file


@dataclass
class ParserFactory():
    file_path: Path
    file_type: str

    def extract_suffix(self, path):
        return path.suffix 


    def build_file_loader(self, loader_type, path):
        loader_type = self.extract_suffix(path)
        match loader_type:
            case '.json':
                return self.build_json_loader(path) 
            case '.yaml':
                return self.build_yaml_loader(path)

    def build_json_loader(self, path):
        data_file = open_file(path)
        JsonLoader(data_file)

    def build_yaml_loader(self, path):
        data_file = open_file(path)
        YamlLoader(data_file)

    def build(self, loader):
        pass
