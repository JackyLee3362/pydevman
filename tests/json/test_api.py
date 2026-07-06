from rich.console import Console

from pydevman.core.json.handler import (
    dump_json,
    filter_prefix,
    parse_json,
    recursive_unescape,
    strip_html_tags,
)

console = Console()


def test_parse_simple():
    assert parse_json('"str"') == "str"
    assert parse_json("1") == 1
    assert parse_json("1.1") == 1.1


def test_parse_str_list():
    assert parse_json('[1, "b"]') == [1, "b"]
    assert parse_json('["a", "b"]') == ["a", "b"]


def test_recursive_unescape():
    s = parse_json('"[\\"1\\", \\"2\\"]"')
    assert recursive_unescape(s) == [1, 2]

    s = parse_json(
        r'{"json-str": "{\"foo\":\"bar\"}", "normal-str": "foobar", '
        r'"boolean": true, "integer": 200, "float": 1.1, "list": [true, 2]}'
    )
    recursive_unescape(s)


def test_strip_html_tags():
    s = parse_json('["a", "123<p>b</p>"]')
    res = strip_html_tags(s)
    assert res == ["a", "123b"]


def test_filter_prefix():
    s = parse_json(r'{"list": [true, "foo", 2], "key": "boo"}')
    res = filter_prefix(s, ["k"])
    assert res == {"list": [True, "foo", 2]}


def test_filter_prefix_v2():
    s = parse_json(
        r'{"list": [true, "foo", 2], "key": {"innerKey":1, "innerKey2":2, "foo":3}}'
    )
    res = filter_prefix(s, ["inner"])
    assert res == {"list": [True, "foo", 2], "key": {"foo": 3}}


def test_dump_json():
    assert dump_json({"a": 1}, inline=True) == '{"a": 1}'
