"""递归拷贝/统计文件夹
创建时间: 2025-03-20
作者: Jacky
"""

import logging
from pathlib import Path

import typer
from rich import print
from rich.logging import RichHandler

handler = RichHandler()
logging.basicConfig(level=logging.DEBUG, handlers=[handler])

log = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def copy(src: str, dst: str, max_depth: int = 4, file: bool = True):
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


@app.command()
def stat(src: str, max_depth: int = 4):
    """统计文件夹个数大小，文件个数大小"""
    src_dir = Path(src)
    # 校验：防止 dst 覆盖 src
    if not src_dir.exists():
        log.info(f"{src_dir} 源文件夹不存在，请检查路径")
        return
    # 用队列解决
    total_file = 0
    total_folder = 0
    queue = [(src_dir, 0)]
    while queue:
        p, level = queue.pop()
        if level > max_depth:  # 如果递归深度大于最大深度，跳出递归
            continue
        try:
            for p in p.iterdir():
                if p.is_dir():
                    total_folder += 1
                    queue.append((p, level + 1))  # 递归进入下一层
                else:
                    total_file += 1
        except PermissionError:
            log.info(f"无权限访问，跳过... {p}")
            continue
        except Exception as e:
            log.error("未知错误...")
            log.exception(e)
    print(f"目标文件夹 : {src_dir} ")
    print(f"文件数量   : {total_file}")
    print(f"文件夹数量 : {total_folder}")


def clear_blank(src):
    pass


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


if __name__ == "__main__":
    app()
