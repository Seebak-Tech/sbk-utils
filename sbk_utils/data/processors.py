from typing import Iterable


def take_first(values: Iterable):
    for value in values:
        if value is not None and value != '':
            return value
