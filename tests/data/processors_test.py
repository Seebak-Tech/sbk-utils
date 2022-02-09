from sbk_utils.data.processors import take_first


def test_take_first():
    data = ['', 'one', 'two', 'three']
    take_first(data)
    assert 'one' == take_first(data)
