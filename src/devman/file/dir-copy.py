"""
文件夹复制操作
1. 首先删除目标文件夹
2. 然后复制源文件夹
"""

# ⚠️高危操作
# TODO 测试如果 DST 存在文件不删除，直接复制过去会怎么样
import shutil
from pathlib import Path

import typer
from helper.query import query_list
from rich.console import Console
from send2trash import send2trash

import inquirer

console = Console()
cli = typer.Typer()


def copy_dir(src: Path, dst: Path, dry: bool):
    # 该操作非常危险
    console.rule("高危操作，请谨慎操作⚠️")
    console.log(f"源文件夹='{src}' -> 目标文件夹='{dst}'")
    assert "tmp" in src.parts and "tmp" in dst.parts
    # 约束
    assert src.exists() and src.is_dir()
    if dry:
        return

    if dst.exists():
        console.log(f"目标文件夹='{dst}': 删除到回收站")
        send2trash(dst)
    try:
        shutil.copytree(src, dst, dirs_exist_ok=True)
        console.log(f"目标文件夹='{dst}': 复制完成")
    except FileExistsError:
        console.log(f"目标文件夹='{dst}': 已经存在同名文件，复制失败")


@cli.command("copy-dir", help="删除 dst 文件夹内容并复制 src 内容")
def copy_dir_query():
    func = "copy-dir"
    console.rule("复制文件夹 SRC -> DST")
    src = query_list(func, "src", "请输入源文件夹目录")
    dst = query_list(func, "dst", "请输入目标文件夹目录")
    dry = inquirer.confirm("是否 DRY-RUN 模式", default=True)
    copy_dir(Path(src), Path(dst), dry)


if __name__ == "__main__":
    cli()
