from pathlib import Path

from send2trash import send2trash
import logging

log = logging.getLogger(__name__)


def del_empty_dir(dst: Path, dry: bool):
    assert dst.is_dir() and dst.name.lower() == "src"
    log.debug(f"遍历目录: 目标文件夹='{dst}'")

    def is_empty_dir(_dir: Path) -> bool:
        if not _dir.is_dir():
            return False
        empty = True
        for item in _dir.iterdir():
            # 递归查询子目录
            empty &= is_empty_dir(item)
        if empty:
            log.debug(f"删除空目录({not dry}): 目标文件夹='{_dir}'")
            if not dry:
                _dir.rmdir()
        return empty

    for item in dst.iterdir():
        is_empty_dir(item)


def del_dir(dst: Path, dry: bool):
    log.debug(f"删除到回收站({not dry}): 目标文件夹='{dst}'")
    if not dry and dst.exists():
        send2trash(dst)
        log.debug(f"目标文件夹='{dst}' 删除成功...")
