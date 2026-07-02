"""JsonProcessor — 责任链调度器 + JsonHandler 枚举"""

import json
from enum import Enum, auto

from loguru import logger

from pydevman.core.json.handler import (
    DelHtmlTagHandler,
    FilterFieldByPrefixHandler,
    FilterFieldBySuffixHandler,
    JsonFieldHandlerInterface,
    RecursiveUnescapeHandler,
)


class JsonHandler(Enum):
    """JSON 处理 handler 类型，上游传枚举，按注册顺序执行"""

    RECURSIVE_UNESCAPE = auto()
    DEL_HTML_TAG = auto()
    FILTER_FIELD_BY_PREFIX = auto()
    FILTER_FIELD_BY_SUFFIX = auto()


class JsonProcessor:
    """管理 handler 链，按 register() 顺序依次处理"""

    def __init__(self):
        self.handlers: list[JsonFieldHandlerInterface] = []

    def register(self, handler_type: JsonHandler, **kwargs):
        """按类型注册 handler。

        kwargs 仅对需参数的 handler 有效：
        - FILTER_FIELD_BY_PREFIX: prefix_filter=Iterable[str]
        - FILTER_FIELD_BY_SUFFIX: suffix_filter=Iterable[str]
        """
        match handler_type:
            case JsonHandler.RECURSIVE_UNESCAPE:
                self.handlers.append(RecursiveUnescapeHandler())
            case JsonHandler.DEL_HTML_TAG:
                self.handlers.append(DelHtmlTagHandler())
            case JsonHandler.FILTER_FIELD_BY_PREFIX:
                self.handlers.append(
                    FilterFieldByPrefixHandler(kwargs.get("prefix_filter", []))
                )
            case JsonHandler.FILTER_FIELD_BY_SUFFIX:
                self.handlers.append(
                    FilterFieldBySuffixHandler(kwargs.get("suffix_filter", []))
                )

    def process(self, text: str):
        """按注册顺序执行所有 handler"""
        try:
            _text = json.loads(text)
        except json.JSONDecodeError:
            _text = text
        except Exception as e:
            logger.error(f'无法处理文本, text="{text}"')
            raise e

        for handler in self.handlers:
            _text = handler.handle(_text)
        return _text
