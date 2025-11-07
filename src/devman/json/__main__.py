import logging

import pyperclip
import typer
from rich.console import Console
from typing_extensions import Annotated

from devman.args import ARG_DST, ARG_FORCE_COVER_DST, ARG_SRC, ARG_VERBOSE
from devman.common import assert_path_exist_and_is_file
from devman.helper.intereaction import to_clipboard_or_file
from devman.json.api import api_json_dump_obj_to_str, api_parse_str_to_json
from devman.log import config_log

app = typer.Typer()
console = Console()

ARG_RECURSIVE = Annotated[
    bool, typer.Option(help="是否递归解析", show_default="默认递归解析")
]


@app.command("parse", help="解析字符串为 json，并输出到剪贴板")
def recursive_parse_json(
    src: ARG_SRC,
    dst: ARG_DST = None,
    recursive: ARG_RECURSIVE = True,
    force: ARG_FORCE_COVER_DST = False,
    verbose: ARG_VERBOSE = False,
):
    console.rule("解析 json 字符串")
    if verbose:
        console.rule("开启详细输出")
        config_log(logging.DEBUG)
    try:
        assert_path_exist_and_is_file(src)
        parsed = api_parse_str_to_json(src.read_text(), recursive)
        content = api_json_dump_obj_to_str(parsed)
        to_clipboard_or_file(dst, content, force)
    except Exception as e:
        console.print("出现异常", e)
        console.print("使用 -v 详细输出")


if __name__ == "__main__":
    app()
