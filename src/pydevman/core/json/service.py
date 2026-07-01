from typing import Iterable, Union

from pydevman.core.json.handler import (
    DelHtmlTagHandler,
    FilterKeyByPrefixHandler,
    FilterKeyBySuffixHandler,
    JsonProcessor,
    RecursiveHandler,
)


def parse_str_to_json(
    text: str,
    *,
    recursive: bool = False,
    del_tag: bool = False,
    prefix: Iterable[str] = None,
    suffix: Iterable[str] = None,
) -> Union[dict, list, str, int, float]:
    # 递归解析
    processor = JsonProcessor()
    if recursive:
        processor.register(RecursiveHandler())
    if del_tag:
        processor.register(DelHtmlTagHandler())
    if prefix:
        processor.register(FilterKeyByPrefixHandler(prefix))
    if suffix:
        processor.register(FilterKeyBySuffixHandler(suffix))

    parsed = processor.process(text)
    return parsed
