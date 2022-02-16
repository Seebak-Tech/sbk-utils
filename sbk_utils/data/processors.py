from typing import Iterable, Any


def take_first(values: Iterable) -> Any:
    for value in values:
        if value is not None and value != '':
            return value
