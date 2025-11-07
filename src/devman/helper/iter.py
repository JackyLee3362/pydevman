from pathlib import Path
from typing import Generator

import pytest


def stat_info_in_dir(path: Path) -> tuple[int, int]:
    assert path.is_dir()
    file_cnt = dir_cnt = other_cnt = 0
    for item in path.iterdir():
        if item.is_file():
            file_cnt += 1
        elif item.is_dir():
            dir_cnt += 1
        else:
            other_cnt += 1
    return file_cnt, dir_cnt, other_cnt


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
    assert path.is_dir() and path.exists()
    q = [(path, 0)]
    while q:
        _path, depth = q.pop(0)
        if depth > max_depth:
            continue
        if _path.is_file():
            yield _path
        elif _path.is_dir():
            for item in _path.iterdir():
                q.append((item, depth + 1))


def test_1():
    for item in iter_files(Path("."), 16):
        print(item)


if __name__ == "__main__":
    pytest.main(["vs", __file__])
