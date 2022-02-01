import pytest


@pytest.fixture(scope="session")
def search_dict():
    return {
        'key1': 'valor1',
        'key2': [
            {'inner_lst_key1': 1, 'inner_lst_key2': 2},
            {'inner_lst_key1': 3, 'inner_lst_key2': 4},
            {'inner_lst_key3': 'valor2'}
        ],
        'key3': {
            'inner_dict_key1': 'a',
            'inner_dict_key2': 'b'
        },
        'key4': True
    }
