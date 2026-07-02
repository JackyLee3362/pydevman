from rich.console import Console

from pydevman.core.json.processor import JsonHandler, JsonProcessor

console = Console()


def test_parse_simple():
    p = JsonProcessor()
    assert p.process("str") == "str"
    assert p.process("1") == 1
    assert p.process("1.1") == 1.1


def test_parse_str_list():
    p = JsonProcessor()
    assert p.process('[1, "b"]') == [1, "b"]
    assert p.process('["a", "b"]') == ["a", "b"]


def test_parse_recursive():
    p = JsonProcessor()
    p.register(JsonHandler.RECURSIVE_UNESCAPE)

    s = '"[\\"1\\", \\"2\\"]"'
    assert p.process(s) == [1, 2]

    s = r'{"json-str": "{\"foo\":\"bar\"}", "normal-str": "foobar", "boolean": true, "integer": 200, "float": 1.1, "list": [true, 2]}'
    p.process(s)


def test_parse_del_tag():
    s = '["a", "123<p>b</p>"]'
    p = JsonProcessor()
    p.register(JsonHandler.DEL_HTML_TAG)
    res = p.process(s)
    assert res == ["a", "123b"]


def test_filter_key():
    s = r'{"list": [true, "foo", 2], "key": "boo"}'
    p = JsonProcessor()
    p.register(JsonHandler.FILTER_FIELD_BY_PREFIX, prefix_filter=["k"])
    res = p.process(s)
    assert res == {"list": [True, "foo", 2]}


def test_filter_key_v2():
    s = r'{"list": [true, "foo", 2], "key": {"innerKey":1, "innerKey2":2, "foo":3}}'
    p = JsonProcessor()
    p.register(JsonHandler.FILTER_FIELD_BY_PREFIX, prefix_filter=["inner"])
    res = p.process(s)
    assert res == {"list": [True, "foo", 2], "key": {"foo": 3}}
