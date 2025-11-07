from pathlib import Path
from typing import Generator

from devman.file.common import assert_path_exist_and_is_dir, is_dot_path


def iter_dirs(path: Path, max_depth: int):
    assert path.is_dir() and path.exists()
    q = [(path, 0)]
    while q:
        _dir, depth = q.pop(0)
        if depth > max_depth:
            continue
        for item in _dir.iterdir():
            if item.is_dir():
                q.append((item, depth + 1))
        yield _dir


def iter_files(path: Path, max_depth: int) -> Generator[Path, None, None]:
    assert_path_exist_and_is_dir(path)
    q = [(path, 1)]
    while q:
        _path, depth = q.pop(0)
        if depth > max_depth:
            continue
        if _path.is_file():
            yield _path
        elif _path.is_dir() and is_dot_path(_path):
            for item in _path.iterdir():
                q.append((item, depth + 1))
