from pathlib import Path

import typer
from helper.query import query_list
from rich.console import Console
from send2trash import send2trash

import inquirer

console = Console()
cli = typer.Typer()


def del_empty_dir(dst: Path, dry: bool):
    assert dst.is_dir() and dst.name.lower() == "src"
    console.print(f"遍历目录: 目标文件夹='{dst}'")

    def is_empty_dir(_dir: Path) -> bool:
        if not _dir.is_dir():
            return False
        empty = True
        for item in _dir.iterdir():
            # 递归查询子目录
            empty &= is_empty_dir(item)
        if empty:
            console.print(f"删除空目录({not dry}): 目标文件夹='{_dir}'")
            if not dry:
                _dir.rmdir()
        return empty

    for item in dst.iterdir():
        is_empty_dir(item)


def del_dir(dst: Path, dry: bool):
    console.log(f"删除到回收站({not dry}): 目标文件夹='{dst}'")
    if not dry and dst.exists():
        send2trash(dst)
        console.log(f"目标文件夹='{dst}' 删除成功...")


@cli.command("del-dir", help="删除 dst 文件夹内容到回收站")
def del_dir_query():
    console.rule("删除文件夹内容")
    func = "del-dir"
    dst = query_list(func, "dst", "请输入目标文件夹目录")
    dry = inquirer.confirm("是否 DRY-RUN 模式", default=True)
    del_dir(Path(dst), dry)


@cli.command("del-empty-dir", help="删除目录中的空文件夹")
def del_empty_dir_query():
    func = "del-empty-dir"
    console.rule("删除空文件夹")
    dst = query_list(func, "dst", "请输入目标文件夹目录")
    dry = inquirer.confirm("是否 DRY-RUN 模式", default=True)
    del_empty_dir(Path(dst), dry)


if __name__ == "__main__":
    cli()
