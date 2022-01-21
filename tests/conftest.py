import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def path():
    return Path('/workspace/sbk-utils/tests/test_data/parsers.json')


@pytest.fixture(scope="session")
def invalid_path():
    return Path('/workspace/sbk-utils/tests/test_data/book_to_scrape.html')
