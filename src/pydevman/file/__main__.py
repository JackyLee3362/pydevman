"""
create_time: 2025-06-23 17:19:11
author: Jacky Lee
"""

import logging
import re
from pathlib import Path

import inquirer
import typer
from rich.console import Console

from pydevman.args import ARG_DIR_FILTER_PREFIX, ARG_SRC
from pydevman.file.copy import copytree
from pydevman.file.delete import del_dir, del_empty_dir_recursive
from pydevman.file.move import move_match_pattern_file, move_prefix_ext
from pydevman.file.stat import (
    api_stat_cnt,
    api_stat_line,
    api_stat_prefix,
    api_stat_suffix,
)
from pydevman.helper.table import api_build_table
from pydevman.query.query import QueryCache

console = Console()
app = typer.Typer()
query_cache = QueryCache()

log = logging.getLogger(__name__)


@app.command("stat-cnt", help="统计: 递归统计文件夹中每个文件的数目")
def stat_cnt_controller(src: ARG_SRC, filter_dir: ARG_DIR_FILTER_PREFIX = None):
    console.rule("根据文件夹统计递归文件")
    if filter_dir is None:
        filter_dir = ["."]
    try:
        rows = api_stat_cnt(src.resolve(), filter_dir)
        header = ["路径", "文件数", "目录数", "其他文件"]
        table = api_build_table("根据目录统计文件", header, rows)
        console.print(table)
    except Exception as e:
        console.print(e)


@app.command("stat-suffix", help="统计: 根据文件后缀统计文件")
def stat_suffix_controller(src: ARG_SRC, suffix: list[str] = None):
    console.rule("根据 suffix 文件计数")
    try:
        rows = api_stat_suffix(src, suffix)
        header = ["文件类型", "数量"]
        table = api_build_table(title="根据 SUFFIX 计数", header=header, rows=rows)
        console.print(table)
    except Exception as e:
        console.print(e)


@app.command("stat-prefix", help="统计: 统计文件并根据前缀分类")
def stat_prefix_controller(src: ARG_SRC, prefix: list[str] = None):
    console.rule("根据目录统计递归文件前缀")
    try:
        rows = api_stat_prefix(Path(src), prefix)
        table = api_build_table("根据目录统计文件", ["前缀 PREFIX", "数目"], rows)
        console.print(table)
    except Exception as e:
        console.print(e)


@app.command("stat-line", help="统计: 统计目录中文件行数")
def stat_line_for_file(src: ARG_SRC, suffix: list[str] = None, max_depth: int = 16):
    console.rule("根据目录统计文件行数")
    try:
        rows = api_stat_line(src, suffix, max_depth)
        table = api_build_table("统计文件行数", ["文件名", "行数"], rows)
        console.print(table)
    except Exception as e:
        console.print(e)


@app.command("copy-dir", help="删除: 删除 dst 文件夹内容并复制 src 内容")
def copy_dir_query():
    func = "copy-dir"
    console.rule("复制文件夹 SRC -> DST")
    src = query_cache.query_list(func, "src", "请输入源文件夹目录")
    dst = query_cache.query_list(func, "dst", "请输入目标文件夹目录")
    dry = inquirer.confirm("是否 DRY-RUN 模式", default=True)
    console.rule("高危操作，请谨慎操作⚠️")
    console.log(f"源文件夹='{src}' -> 目标文件夹='{dst}'")
    copytree(Path(src), Path(dst), dry)


@app.command("del-dir", help="删除: 删除 dst 文件夹内容到回收站")
def del_dir_query():
    console.rule("删除文件夹内容")
    func = "del-dir"
    dst = query_cache.query_list(func, "dst", "请输入目标文件夹目录")
    dry = inquirer.confirm("是否 DRY-RUN 模式", default=True)
    del_dir(Path(dst), dry)


@app.command("del-empty-dir", help="删除: 删除目录中的空文件夹")
def del_empty_dir_query():
    func = "del-empty-dir"
    console.rule("删除空文件夹")
    dst = query_cache.query_list(func, "dst", "请输入目标文件夹目录")
    dry = inquirer.confirm("是否 DRY-RUN 模式", default=True)
    del_empty_dir_recursive(Path(dst), dry)


@app.command("move-prefix-ext", help="删除: 按照文件末尾移动文件")
def move_prefix_ext_query():
    func = "move-prefix-ext"

    src = query_cache.query_list(func, "src", "请输入源文件夹目录")
    dst = query_cache.query_list(func, "dst", "请输入目标文件夹目录")
    prefix = query_cache.query_list(func, "prefix", "请输入文件前缀")
    ext = query_cache.query_check(func, "ext", "请输入文件拓展名")
    dry = inquirer.confirm("是否 DRY-RUN 模式", default=True)
    dry = inquirer.confirm("是否 DRY-RUN 模式", default=True)
    move_prefix_ext(
        Path(src), Path(dst), prefix=re.compile(prefix, re.I), ext=ext, dry=dry
    )


@app.command("move-pattern-dst", help="删除: 将文件移动到根目录")
def move_pattern_dst_query():
    func = "del-dir"
    src = query_cache.query_list(func, "src", "请输入源文件夹目录")
    dst = Path(query_cache.query_list(func, "dst", "请输入目标文件夹目录"))
    pattern = query_cache.query_list(func, "pattern", "请输入正则表达式")
    dry = inquirer.confirm("是否 DRY-RUN 模式", default=True)
    move_match_pattern_file(Path(src), Path(dst), re.compile(pattern), dry)


if __name__ == "__main__":
    app()
