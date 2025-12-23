from pydevman.json.api import api_parse_str_to_json
from pydevman.json.core import FilterKeyBySuffixHandler


def test_浅层_dict():
    handler = FilterKeyBySuffixHandler(suffix_filter=["name"])
    alice = {"firstname": "", "lastname": "", "age": ""}
    res = handler.handle(alice)
    assert res == {"age": ""}


def test_深层_dict():
    handler = FilterKeyBySuffixHandler(suffix_filter=["name"])
    alice = {"firstname": "", "lastname": "", "age": ""}
    bob = {"firstname": "", "lastname": "", "age": ""}
    all_students = {"students": {"alice": alice, "bob": bob}}
    filter_students = handler.handle(all_students)
    assert filter_students == {"students": {"alice": {"age": ""}, "bob": {"age": ""}}}


def test_浅层_list():
    handler = FilterKeyBySuffixHandler(suffix_filter=["name"])
    alice = [{"firstname": "", "lastname": "", "age": ""}]
    res = handler.handle(alice)
    assert res == [{"age": ""}]


def test_深层_list():
    handler = FilterKeyBySuffixHandler(suffix_filter=["name"])
    alice = {"firstname": "", "lastname": "", "age": ""}
    bob = {"firstname": "", "lastname": "", "age": ""}
    all_students = {"students": [alice, bob]}
    filter_students = handler.handle(all_students)
    assert filter_students == {"students": [{"age": ""}, {"age": ""}]}
