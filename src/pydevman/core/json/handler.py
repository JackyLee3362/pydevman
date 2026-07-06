"""
Author: Jacky Lee
Date: 2025-10-22
Description: JSON 工具函数 — 每个功能独立可调用，无组合/责任链
"""

import json
from typing import Any

from loguru import logger


def parse_json(text: str) -> Any:
    """普通去转义：解析 JSON 字符串为 Python 对象（单层，不递归）"""
    return json.loads(text)


def recursive_unescape(data: Any) -> Any:
    """递归去转义：深度遍历，对字符串值尝试 json.loads，成功则递归继续"""
    if data is None:
        return None
    if isinstance(data, (bool, int, float)):
        return data
    if isinstance(data, str):
        try:
            parsed = json.loads(data)
        except (json.JSONDecodeError, TypeError):
            return data
        return recursive_unescape(parsed)
    if isinstance(data, list):
        return [recursive_unescape(item) for item in data]
    if isinstance(data, dict):
        return {k: recursive_unescape(v) for k, v in data.items()}
    return data


def strip_html_tags(data: Any) -> Any:
    """去除 HTML 标签：递归去除所有字符串值中的 HTML 标签"""
    from bs4 import BeautifulSoup

    if data is None:
        return None
    if isinstance(data, (bool, int, float)):
        return data
    if isinstance(data, str):
        return BeautifulSoup(data, "html.parser").get_text()
    if isinstance(data, list):
        return [strip_html_tags(item) for item in data]
    if isinstance(data, dict):
        return {k: strip_html_tags(v) for k, v in data.items()}
    return data


def filter_prefix(data: Any, prefixes: list[str]) -> Any:
    """过滤前缀字段：递归删除键以指定前缀开头的字典项"""
    if isinstance(data, dict):
        return {
            k: filter_prefix(v, prefixes)
            for k, v in data.items()
            if not any(k.startswith(p) for p in prefixes)
        }
    if isinstance(data, list):
        return [filter_prefix(item, prefixes) for item in data]
    return data


def filter_suffix(data: Any, suffixes: list[str]) -> Any:
    """过滤后缀字段：递归删除键以指定后缀结尾的字典项"""
    if isinstance(data, dict):
        return {
            k: filter_suffix(v, suffixes)
            for k, v in data.items()
            if not any(k.endswith(s) for s in suffixes)
        }
    if isinstance(data, list):
        return [filter_suffix(item, suffixes) for item in data]
    return data


def dump_json(data: Any, inline: bool = False) -> str:
    """将 Python 对象序列化为 JSON 字符串"""
    if inline:
        return json.dumps(data, ensure_ascii=False)
    return json.dumps(data, indent=2, ensure_ascii=False)
