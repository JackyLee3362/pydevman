from devman.json.api import recursive_parse


def test_parse_simple():
    assert recursive_parse("str") == "str"
    assert recursive_parse("1") == 1
    assert recursive_parse("1.1") == 1.1


def test_parse_str_list():
    assert recursive_parse('[1, "b"]') == [1, "b"]
    assert recursive_parse('["a", "b"]') == ["a", "b"]
    assert recursive_parse('"[\\"1\\", \\"2\\"]"') == [1, 2]
