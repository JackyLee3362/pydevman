from rich.console import Console

from pydevman.json.service import parse_str_to_json

console = Console()


def test_parse_simple():
    assert parse_str_to_json("str") == "str"
    assert parse_str_to_json("1") == 1
    assert parse_str_to_json("1.1") == 1.1


def test_parse_str_list():
    assert parse_str_to_json('[1, "b"]') == [1, "b"]
    assert parse_str_to_json('["a", "b"]') == ["a", "b"]


def test_parse_recursive():
    s = '"[\\"1\\", \\"2\\"]"'
    assert parse_str_to_json(s, recursive=True) == [1, 2]
    s = r'{"json-str": "{\"foo\":\"bar\"}", "normal-str": "foobar", "boolean": true, "integer": 200, "float": 1.1, "list": [true, 2]}'
    parse_str_to_json(s, recursive=True)


def test_parse_del_tag():
    s = '["a", "123<p>b</p>"]'
    res = parse_str_to_json(s, del_tag=True)
    assert res == ["a", "123b"]


def test_filter_key():
    s = r'{"list": [true, "foo", 2], "key": "boo"}'
    res = parse_str_to_json(s, prefix=["k"])
    assert res == {"list": [True, "foo", 2]}


def test_filter_key_v2():
    s = r'{"list": [true, "foo", 2], "key": {"innerKey":1, "innerKey2":2, "foo":3}}'
    res = parse_str_to_json(s, prefix=["inner"])
    assert res == {"list": [True, "foo", 2], "key": {"foo": 3}}
