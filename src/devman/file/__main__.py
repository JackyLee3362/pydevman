"""
create_time: 2025-06-23 17:19:11
author: jackylee
"""

from collections import OrderedDict
from pathlib import Path

import typer
from helper.iter import iter_dirs, iter_files, stat_info_in_dir
from helper.query import query_check, query_list
from rich.console import Console
from rich.table import Table

console = Console()
app = typer.Typer()


# 幂等操作


def stat_suffix(path: Path, suffixes: list, max_depth: int = 16, max_cnt: int = 4096):
    console.rule("根据 suffix 文件计数")
    max_cnt = 0
    suffix_set = set(suffixes)
    d = {}
    cnt = 0
    for file in iter_files(path, max_depth=max_depth):
        suffix = file.suffix
        if suffix in suffix_set:
            cnt += 1
            v = d.setdefault(suffix, 0)
            d[suffix] = v + 1
        if cnt > max_cnt:
            console.print("达到最大上限文件，停止搜索")
            break
    header = ["文件类型", "数量"]
    rows = [(k, str(v)) for k, v in d.items()]
    rows.append(("TOTAL", str(cnt)))
    table = build_table("根据 SUFFIX 计数", header, rows)
    console.print(table)


def stat_cnt(root: Path, max_depth: int = 16):
    console.rule("根据目录统计递归文件")
    res: dict[Path, tuple] = OrderedDict()

    def adder(path: Path, f, d, o):
        parts = path.relative_to(root).parts
        for i in range(len(parts)):
            _path = root.joinpath(*parts[:i])
            _f, _d, _o = res.get(_path, (0, 0, 0))
            res[_path] = (f + _f, d + _d, o + _o)

    for dir in iter_dirs(root, max_depth=max_depth):
        f, d, o = stat_info_in_dir(dir)
        res[dir] = (f, d, o)
        adder(dir, f, d, o)
    header = ["路径", "文件数", "目录数", "其他文件"]
    rows = [
        (str(k.relative_to(root)), str(f), str(d), str(o))
        for k, (f, d, o) in res.items()
    ]
    table = build_table("根据目录统计文件", header, rows)
    console.print(table)


def stat_prefix(root: Path, ext: list[str], max_depth: int = 16):
    console.rule("根据目录统计递归文件前缀")
    res = {}
    ext_set = set(e.lower() for e in ext)

    for file in iter_files(root, max_depth):
        file: Path
        if file.suffix.lower() in ext_set:
            prefix = file.stem.split("_")[0]
            val = res.get(prefix, 0)
            res[prefix] = val + 1

    header = ["前缀 PREFIX", "数目"]
    rows = [(k, str(v)) for k, v in res.items()]
    table = build_table("根据目录统计文件", header, rows)
    console.print(table)


def build_table(title: str, header: list[str], rows: list):
    table = Table(show_header=True, header_style="bold magenta", title=title)
    for head in header:
        table.add_column(head)
    for row in rows:
        table.add_row(*row)
    return table


@app.command("stat-suffix", help="根据文件后缀统计文件")
def stat_suffix_query():
    func = "stat-suffix"
    src = query_list(func, "src", "请输入源文件夹目录")
    suffix = query_check(func, "suffix", "请输入文件名后缀(非拓展名)")
    stat_suffix(Path(src), suffix)


@app.command("stat-cnt", help="统计文件夹中每个文件的数目")
def stat_cnt_query():
    func = "stat-cnt"
    src = query_list(func, "src", "请输入源文件夹目录")
    stat_cnt(Path(src))


@app.command("stat-prefix", help="根据 PREFIX 统计文件")
def stat_prefix_query():
    func = "stat-prefix"
    src = query_list(func, "src", "请输入源文件夹目录")
    ext = query_check(func, "ext", "请输入文件拓展名")
    stat_prefix(Path(src), ext)


if __name__ == "__main__":
    app()
