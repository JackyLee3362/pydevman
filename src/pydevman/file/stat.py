import logging
from collections import OrderedDict
from pathlib import Path
from typing import Iterable, Union

from pydevman.file.common import assert_path_exist_and_is_dir, path_is_dot_path
from pydevman.file.iter import get_line_for_file, iter_dirs, iter_files

log = logging.getLogger(__name__)


def api_stat_suffix(root: Path, suffix: list[str], max_depth: int = 16):
    res = {}
    suffix_set = _to_set(suffix)

    for file in iter_files(root, max_depth):
        _suffix = file.suffix
        if _suffix in suffix_set:
            continue
        val = res.get(_suffix, 0)
        res[_suffix] = val + 1

    rows = [(k, str(v)) for k, v in res.items()]
    return rows


def api_stat_prefix(root: Path, prefix: list[str], max_depth: int = 16):
    res = {}
    prefix_set = set(e.lower() for e in prefix)

    for file in iter_files(root, max_depth):
        if file.suffix.lower() not in prefix_set:
            continue
        prefix = file.stem.split("_")[0]
        val = res.get(prefix, 0)
        res[prefix] = val + 1

    rows = [(k, str(v)) for k, v in res.items()]
    return rows


def api_stat_line(root: Path, suffix: list[str] = None, max_depth: int = 16):
    res = []
    ext_set = set()
    if isinstance(suffix, str):
        ext_set = set([suffix])
    elif isinstance(suffix, list):
        ext_set = set(e.lower() for e in suffix)

    for file in iter_files(root, max_depth):
        if file.suffix.lower() not in ext_set:
            continue
        line = get_line_for_file(file)
        res.append((file.stem, line))
    res.sort(key=lambda x: x[1], reverse=True)
    limit_res = res[: min(len(res), max_depth)]
    total_cnt = len(res)
    total_line_cnt = sum([val for _, val in res])

    rows = [(k, str(v)) for k, v in limit_res]
    rows.append(("总文件数", str(total_cnt)))
    rows.append(("平均行数", str(round(total_line_cnt / total_cnt, 2))))
    return rows


def api_stat_info_in_dir(path: Path) -> tuple[int, int]:
    assert_path_exist_and_is_dir(path)
    file_cnt = dir_cnt = other_cnt = 0
    for item in path.iterdir():
        if item.is_file():
            file_cnt += 1
        elif item.is_dir():
            dir_cnt += 1
        else:
            other_cnt += 1
    return file_cnt, dir_cnt, other_cnt


def api_stat_cnt(root: Path, filter_dir: list[str] = None, max_depth: int = 16):
    res: dict[Path, tuple] = OrderedDict()
    # todo: 把 dot path 加入其中
    filter_dir = _to_set(filter_dir, set([".", "__"]))

    def adder(path: Path, f, d, o):
        parts = path.relative_to(root).parts
        for i in range(len(parts)):
            _path = root.joinpath(*parts[:i])
            _f, _d, _o = res.get(_path, (0, 0, 0))
            res[_path] = (f + _f, d + _d, o + _o)

    for dir in iter_dirs(root, filter_dir, max_depth=max_depth):
        f, d, o = api_stat_info_in_dir(dir)
        if path_is_dot_path(dir):
            continue
        res[dir] = (f, d, o)
        adder(dir, f, d, o)
    rows = [
        (str(k.relative_to(root)), str(f), str(d), str(o))
        for k, (f, d, o) in res.items()
    ]
    return rows


def stat(src: Path, max_depth: int = 4):
    """统计文件夹个数大小，文件个数大小"""
    assert_path_exist_and_is_dir(src)
    # 用队列解决
    total_file = 0
    total_folder = 0
    queue = [(src, 0)]
    while queue:
        p, level = queue.pop()
        if level > max_depth:  # 如果递归深度大于最大深度，跳出递归
            continue
        try:
            for p in p.iterdir():
                if p.is_dir():
                    total_folder += 1
                    queue.append((p, level + 1))  # 递归进入下一层
                else:
                    total_file += 1
        except PermissionError:
            log.info(f"无权限访问，跳过... {p}")
            continue
        except Exception as e:
            log.error("未知错误...")
            log.exception(e)
    # print(f"文件夹 : {src} ")
    # print(f"文件数量   : {total_file}")
    # print(f"文件夹数量 : {total_folder}")
    return src, total_file, total_folder


def _to_set(arg: Union[str, Iterable, None], default_set=None):
    _default_set = set(default_set)
    if arg is None:
        return _default_set
    elif isinstance(arg, str):
        return _default_set.union([arg])
    elif isinstance(arg, Iterable):
        return _default_set.union(arg)
    raise TypeError("类型错误")
