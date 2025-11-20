from rich.console import Console

from pydevman.json.api import api_encode_json_to_str, api_parse_str_to_json

console = Console()


def test_parse_simple():
    assert api_parse_str_to_json("str") == "str"
    assert api_parse_str_to_json("1") == 1
    assert api_parse_str_to_json("1.1") == 1.1


def test_parse_str_list():
    assert api_parse_str_to_json('[1, "b"]') == [1, "b"]
    assert api_parse_str_to_json('["a", "b"]') == ["a", "b"]
    assert api_parse_str_to_json('"[\\"1\\", \\"2\\"]"') == [1, 2]


def test_parse_recursive():
    api_parse_str_to_json(
        r'{"json-str": "{\"foo\":\"bar\"}", "normal-str": "foobar", "boolean": true, "integer": 200, "float": 1.1, "list": [true, 2]}',
        recursive=True,
        del_html_tag=False,
    )


def test_inline():
    s = r'{"list": [true, "foo", 2]}'
    api_encode_json_to_str(s)
