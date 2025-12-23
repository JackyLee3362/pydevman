import logging
from pathlib import Path

import pyperclip

from pydevman.file.common import assert_path_exist_and_is_file

log = logging.getLogger(__name__)


def from_clipboard_or_file(src: Path) -> str:
    if src is None:
        return pyperclip.paste()
    assert_path_exist_and_is_file(src)
    return src.read_text()


def to_clipboard_or_file(dst: Path, content: str, force: bool) -> bool:
    # 写入剪贴板
    if dst is None:
        pyperclip.copy(content)
        return True
    # dst 非空,路径
    if dst.exists() and force:
        dst.write_text(content)
        return True
    return False
