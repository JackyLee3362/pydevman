from pydevman.core.json.handler import filter_suffix


def test_浅层_dict():
    alice = {"firstname": "", "lastname": "", "age": ""}
    res = filter_suffix(alice, ["name"])
    assert res == {"age": ""}


def test_深层_dict():
    alice = {"firstname": "", "lastname": "", "age": ""}
    bob = {"firstname": "", "lastname": "", "age": ""}
    all_students = {"students": {"alice": alice, "bob": bob}}
    filter_students = filter_suffix(all_students, ["name"])
    assert filter_students == {"students": {"alice": {"age": ""}, "bob": {"age": ""}}}


def test_浅层_list():
    alice = [{"firstname": "", "lastname": "", "age": ""}]
    res = filter_suffix(alice, ["name"])
    assert res == [{"age": ""}]


def test_深层_list():
    alice = {"firstname": "", "lastname": "", "age": ""}
    bob = {"firstname": "", "lastname": "", "age": ""}
    all_students = {"students": [alice, bob]}
    filter_students = filter_suffix(all_students, ["name"])
    assert filter_students == {"students": [{"age": ""}, {"age": ""}]}
