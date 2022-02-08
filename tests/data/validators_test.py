import pytest
from sbk_utils.data.validators import (
    find_dict_keys,
    validate_dict_keys,
    instance_of
)


def test_find_dict_keys(search_dict):
    found_keys = []
    fields = ['key1', 'inner_lst_key1', 'inner_dict_key1', 'key10']
    expected = ['key1', 'inner_lst_key1', 'inner_dict_key1']

    found_keys = find_dict_keys(search_dict, fields)

    assert sorted(set(expected)) == sorted(set(found_keys))


def test_validate_bad_keys(search_dict):
    fields = ['key1', 'inner_lst_key1', 'inner_dict_key1', 'key10']
    match_str = r".*The dictionary must contain all the following*"

    with pytest.raises(ValueError,
                       match=match_str):
        validate_dict_keys(search_dict, fields)


@pytest.mark.parametrize(
    'value, attr_type',
    [
        ('test', dict),
        (34, str),
        (3.45, list)
    ],
    ids=[
        "Invalid dict type",
        "Invalid string type",
        "Invalid list type"
    ]
)
def test_is_instance_of(value, attr_type):
    with pytest.raises(TypeError,
                       match=r".*The object must be type of*"):
        instance_of(value, attr_type)
