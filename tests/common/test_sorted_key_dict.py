from pydevman.common.sorted_key_dict import SortedKeyDict


def test_sorted():
    d = SortedKeyDict()
    d[1] = "alice"
    d[3] = "bob"
    d[2] = "cindy"
    d[4] = "david"
    iterators = iter(d)
    k, v = next(iterators)
    assert k == 4 and v == "david"
    k, v = next(iterators)
    assert k == 3 and v == "bob"
    k, v = next(iterators)
    assert k == 2 and v == "cindy"
    k, v = next(iterators)
    assert k == 1 and v == "alice"

    del d[k]
    assert len(d) == 3

    assert d.get(10, "foo") == "foo"
