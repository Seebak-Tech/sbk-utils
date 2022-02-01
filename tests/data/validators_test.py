import pytest
from sbk_utils.data.validators import find_dict_keys, validate_keys


def test_find_dict_keys(search_dict):
    found_keys = []
    fields = ['key1', 'inner_lst_key1', 'inner_dict_key1', 'key10']
    expected = ['key1', 'inner_lst_key1', 'inner_dict_key1']

    found_keys = find_dict_keys(search_dict, fields)

    assert sorted(set(expected)) == sorted(set(found_keys))


def test_validate_bad_keys(search_dict):
    fields = ['key1', 'inner_lst_key1', 'inner_dict_key1', 'key10']

    with pytest.raises(ValueError,
                       match=r".*The dictionary must contain the following*"):
        validate_keys(search_dict, fields)
