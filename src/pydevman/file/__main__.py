"""
create_time: 2025-06-23 17:19:11
author: Jacky Lee
"""

import logging
import re
from pathlib import Path

import typer
from rich.console import Console

from pydevman.args import (
    ARG_DST,
    ARG_SRC,
    OPT_DRY_RUN,
    OPT_FILE_PREFIX,
    OPT_FILE_SUFFIX,
    OPT_FILTER_DIR_PREFIX,
    OPT_FILTER_DIR_SUFFIX,
    OPT_MAX_DEPTH,
)
from pydevman.file.copy import copytree
from pydevman.file.delete import del_dir, del_empty_dir_recursive
from pydevman.file.move import move_match_pattern_file, move_prefix_ext
from pydevman.file.stat import (
    api_stat_by_prefix,
    api_stat_by_suffix,
    api_stat_cnt,
    api_stat_line,
)
from pydevman.helper.table import api_build_table

console = Console()
app = typer.Typer()

log = logging.getLogger(__name__)


@app.command("stat-cnt", rich_help_panel="统计")
def cmd_stat_cnt(
    src: ARG_SRC,
    filter_dir_prefix: OPT_FILTER_DIR_PREFIX = None,
    filter_dir_suffix: OPT_FILTER_DIR_SUFFIX = None,
    max_depth: OPT_MAX_DEPTH = 4,
):
    """统计文件夹中路径数量"""
    console.rule("统计文件夹中文件、文件夹数量")
    try:
        rows = api_stat_cnt(
            src.resolve(), filter_dir_prefix, filter_dir_suffix, max_depth
        )
        header = ["路径", "文件数", "文件夹数", "其他文件"]
        table = api_build_table("根据目录统计文件", header, rows)
        console.print(table)
    except Exception:
        console.print_exception()


@app.command("stat-suffix", rich_help_panel="统计")
def cmd_stat_suffix(src: ARG_SRC, suffix: OPT_FILE_SUFFIX = None):
    """根据文件后缀统计文件"""
    console.rule("根据文件后缀统计文件")
    try:
        rows = api_stat_by_suffix(src, suffix)
        header = ["文件类型", "数量"]
        table = api_build_table(title="根据 SUFFIX 计数", header=header, rows=rows)
        console.print(table)
    except Exception:
        console.print_exception()


@app.command("stat-prefix", rich_help_panel="统计")
def cmd_stat_prefix(src: ARG_SRC, prefix: OPT_FILE_PREFIX = None):
    """统计文件并根据前缀分类"""
    console.rule("统计文件并根据前缀分类")
    try:
        rows = api_stat_by_prefix(Path(src), prefix)
        header = ["前缀 PREFIX", "数目"]
        table = api_build_table("根据文件夹统计文件", header, rows)
        console.print(table)
    except Exception:
        console.print_exception()


@app.command("stat-line", rich_help_panel="统计")
def cmd_stat_line_for_file(
    src: ARG_SRC, suffix: OPT_FILE_SUFFIX = None, max_depth: OPT_MAX_DEPTH = 16
):
    """统计路径下所有文件行数，并按降序排列"""
    console.rule("根据文件夹统计文件行数")
    try:
        rows = api_stat_line(src, suffix, max_depth)
        header = ["文件名", "行数"]
        table = api_build_table("统计文件行数", header, rows)
        console.print(table)
    except Exception:
        console.print_exception()


# @app.command("copy-dir", rich_help_panel="删除")
def cmd_copy_dir_query(src: ARG_SRC, dst: ARG_DST, dry: OPT_DRY_RUN = True):
    """复制源路径至目标路径"""
    console.rule("复制文件夹 SRC -> DST")
    console.rule("高危操作，请谨慎操作⚠️")
    console.log(f"源文件夹='{src}' -> 目标文件夹='{dst}'")
    try:
        copytree(src, dst, dry)
    except Exception:
        console.print_exception()


# @app.command("del-dir", rich_help_panel="删除")
def cmd_del_dir_query(dst: ARG_DST, dry: OPT_DRY_RUN = True):
    """删除 dst 文件夹内容到回收站"""
    console.rule("删除文件夹内容")
    try:
        del_dir(Path(dst), dry)
    except Exception:
        console.print_exception()


# @app.command("del-empty-dir", rich_help_panel="删除")
def cmd_del_empty_dir_query(dst: ARG_DST, dry: OPT_DRY_RUN = True):
    """删除目录中的空文件夹"""
    console.rule("删除空文件夹")
    try:
        del_empty_dir_recursive(dst, dry)
    except Exception:
        console.print_exception()


# @app.command("move-prefix-ext", rich_help_panel="移动")
def cmd_move_prefix_ext_query(
    src: ARG_SRC,
    dst: ARG_DST,
    prefix: list[str],
    suffix: list[str],
    dry: OPT_DRY_RUN = True,
):
    """按照文件末尾移动文件"""
    console.rule("移动: 按照文件末尾移动文件")
    try:
        move_prefix_ext(src, dst, prefix=re.compile(prefix, re.I), ext=suffix, dry=dry)
    except Exception:
        console.print_exception()


# @app.command("move-pattern-dst", rich_help_panel="移动")
def cmd_move_pattern_dst_query(
    src: ARG_SRC, dst: ARG_DST, pattern: str, dry: OPT_DRY_RUN = True
):
    """将文件移动到根目录"""
    console.rule("移动: 将文件移动到根目录")
    try:
        move_match_pattern_file(src, dst, re.compile(pattern), dry)
    except Exception:
        console.print_exception()


if __name__ == "__main__":
    app()
