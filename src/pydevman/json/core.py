"""
Author: Jacky Lee
Date: 2025-10-22
Description: 递归解析 json 代码
"""

import json
from typing import Union


def recursive_parse(
    arg: Union[dict, list, str, int, float],
) -> Union[dict, list, str, int, float]:
    """递归解析,参数为 dict, list, str, int, float 中的一种

    Args:
        param (Union[dict, list, str, int, float]):

    Raises:
        TypeError: 类型错误

    Returns:
        Union[dict, list, str, int, float]: 返回类型是该五种基本类型
    """
    if arg is None:
        raise ValueError("Argument can't be None.")
    if isinstance(arg, list):
        return parse_list(arg)
    elif isinstance(arg, dict):
        return parse_dict(arg)
    elif isinstance(arg, str):
        return parse_str(arg)
    elif isinstance(arg, int):
        return arg
    elif isinstance(arg, float):
        return arg
    else:
        raise TypeError("Argument is not any of List, Object, String or Number.")


def parse_str(text: str) -> Union[dict, list, str]:
    try:
        # 如果可以被解析
        shallow_parsed = json.loads(text)
    except json.JSONDecodeError:
        return text
    deep_parsed = recursive_parse(shallow_parsed)
    return deep_parsed


def parse_list(li: list) -> list:
    _list = []
    for _, item in enumerate(li):
        tmp = recursive_parse(item)
        _list.append(tmp)
    return _list


def parse_dict(di: dict) -> dict:
    _di = {}
    for k, v in di.items():
        _di[k] = recursive_parse(v)
    return _di
