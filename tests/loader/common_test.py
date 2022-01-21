import pytest
from sbk_utils.loader.common import ensure_path_exists, open_file, InvalidFile
from pathlib import Path


def test_ensure_path_exists():
    with pytest.raises(
        ValueError,
        match='The Path does not exists'
    ):
        _ = ensure_path_exists(Path('/other'))


def test_open_file():
    corrupt_file = '' 
    with pytest.raises(
        InvalidFile,
        match='Error while opening the file'
    ):
        _ = open_file(corrupt_file)
