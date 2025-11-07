"""
create_time: 2025-03-20
author: Jacky Lee
description: 文件夹复制操作
1. 首先删除目标文件夹
2. 然后复制源文件夹
"""

# ⚠️高危操作
# TODO 测试如果 DST 存在文件不删除，直接复制过去会怎么样
import logging
import shutil
from pathlib import Path

from rich.console import Console
from send2trash import send2trash

console = Console()
log = logging.getLogger(__name__)


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


def confirm() -> bool:
    while True:
        flag = input("是否继续(y/n)...").strip().lower()  # 获取用户输入并处理为小写
        if flag.startswith("y"):  # 如果以'y'开头
            log.info("继续执行...")
            return True
        elif flag.startswith("n"):  # 如果以'n'开头
            log.info("退出程序...")
            return False
        log.info("无效输入，请输入'y'或'n'。")  # 提示用户输入无效，继续询问


def copy_struct(src: str, dst: str, max_depth: int = 4, file: bool = True):
    """复制文件夹结构，文件内容为 0 KB
    level: 递归深度，默认为 8 层
    """
    src_dir = Path(src)
    dst_dir = Path(dst)
    # 校验：防止 dst 覆盖 src
    if not src_dir.exists():
        log.info(f"{src_dir} 源文件夹不存在，请检查路径")
        return
    if dst_dir.exists():
        log.info(f"{dst_dir} 目标文件夹已存在，请检查路径")
        return
    dst_dir.mkdir()
    log.info(f"准备复制 {src_dir} -> {dst_dir}, max_depth={max_depth}, file={file}")

    if not confirm():
        log.info("退出程序...")
        return
    queue = [(src_dir, 0)]
    while queue:
        dir, level = queue.pop()
        if level > max_depth:  # 如果递归深度大于最大深度，跳出递归
            continue
        try:
            for p in dir.iterdir():
                # 文件夹
                parts = p.relative_to(src_dir).parts
                dst_path = dst_dir.joinpath(*parts)
                if p.is_dir():
                    queue.append((p, level + 1))  # 递归进入下一层
                    dst_path.mkdir()
                    continue
                # 文件
                if p.is_file() and file:
                    log.info(f"复制 {p} -> {dst_path}")
                    dst_path.touch()
        except PermissionError:
            log.info(f"无权限访问，跳过... {p}")
            continue
