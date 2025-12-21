from pathlib import Path
from typing import Generator

from pydevman.file.common import (
    assert_path_exist_and_is_dir,
    assert_path_exist_and_is_file,
    path_is_dot_path,
)


def iter_dirs(
    path: Path, filter_prefix_dir: list[str], max_depth: int
) -> Generator[Path, None, None]:
    _path = path.absolute()
    assert_path_exist_and_is_dir(_path)
    q = [(_path, 0)]
    while q:
        _dir, depth = q.pop(0)
        if depth > max_depth:
            continue
        for item in _dir.iterdir():
            if item.is_dir():
                if any(item.name.startswith(p) for p in filter_prefix_dir):
                    continue
                q.append((item, depth + 1))
        yield _dir


def iter_files(path: Path, max_depth: int) -> Generator[Path, None, None]:
    _path = path.absolute()
    assert_path_exist_and_is_dir(_path)
    q = [(_path, 0)]
    while q:
        _path, depth = q.pop(0)
        if depth > max_depth:
            continue
        if _path.is_file():
            yield _path
        elif _path.is_dir() and not path_is_dot_path(_path):
            for item in _path.iterdir():
                q.append((item, depth + 1))


def get_line_for_file(path: Path):
    assert_path_exist_and_is_file(path)
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)
