from pathlib import Path

from pydevman.file.stat import (
    api_stat_by_prefix,
    api_stat_by_suffix,
    api_stat_cnt,
)

root_dir = Path(__file__).parent.parent.parent


def test_api_stat_suffix():
    res = api_stat_by_suffix(root_dir, None)
    print(res)


def test_api_stat_prefix():
    res = api_stat_by_prefix(root_dir, ["test"])
    print(res)


def test_api_stat_cnt():
    res = api_stat_cnt(root_dir, None)
    print(res)
