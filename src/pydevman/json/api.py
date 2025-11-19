import re
from datetime import datetime
from typing import Union

from pydevman.json.core import DelHtmlTagHandler, JsonProcessor, RecursiveHandler


def api_parse_str_to_json(
    arg: str, *, recursive: bool, del_html_tag: bool
) -> Union[dict, list, str, int, float]:
    # 递归解析
    processor = JsonProcessor()
    if recursive:
        processor.register(RecursiveHandler())
    if del_html_tag:
        processor.register(DelHtmlTagHandler())

    parsed = processor.process(arg)
    return processor.dump_readable(parsed)


def get_possible_datetime_from_str(line: str) -> datetime:
    raise NotImplementedError("Not Finish.")
    dt_pat = re.compile(r"(\d{4}-?\d{2}-?\d{2}\s?\d{2}:?\d{2}:?\d{2}(\.\d{3})?)")
    return dt_pat


def get_possible_json_from_str(line: str) -> dict:
    raise NotImplementedError("Not Finish.")
    json_pat = re.compile(r"(?<!#)(\[?{.*}\]?)(?!#)")
    return json_pat


def parse_lines(lines: list[str]) -> list:
    raise NotImplementedError("Not Finish.")
    res = []
    for idx, line in enumerate(lines):
        get_possible_datetime_from_str(line)
        get_possible_json_from_str(line)
    return res
