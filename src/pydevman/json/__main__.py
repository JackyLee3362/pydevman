import json
import logging

import typer
from rich.console import Console
from typing_extensions import Annotated

from pydevman.args import (
    ARG_DST,
    ARG_DST_OR_TO_CLIP,
    ARG_QUIET,
    ARG_SRC,
    ARG_SRC_OR_FROM_CLIP,
    ARG_VERBOSE,
    OPT_FORCE,
)
from pydevman.helper.interactive import from_clipboard_or_file, to_clipboard_or_file
from pydevman.json.api import api_parse_str_to_json
from pydevman.json.core import api_dump_json
from pydevman.log import config_log

app = typer.Typer()
console = Console()

ARG_RECURSIVE = Annotated[
    bool,
    typer.Option(
        "--recursive", "-r", help="是否递归去转义", show_default="默认关闭递归"
    ),
]

ARG_DEL_HTML_TAG = Annotated[
    bool,
    typer.Option("--del-tag", help="是否去除标签", show_default="默认关闭剔除标签"),
]
ARG_INLINE = Annotated[
    bool, typer.Option("--inline", help="是否单行输出", show_default="默认多行")
]

ARG_PREFIX = Annotated[list[str], typer.Option("--prefix", help="过滤的字段前缀")]
ARG_SUFFIX = Annotated[list[str], typer.Option("--suffix", help="过滤的字段后缀")]


@app.command("parse")
def cmd_recursive_parse_json(
    src: ARG_SRC_OR_FROM_CLIP = None,
    dst: ARG_DST_OR_TO_CLIP = None,
    recursive: ARG_RECURSIVE = False,
    del_tag: ARG_DEL_HTML_TAG = False,
    inline: ARG_INLINE = False,
    prefix: ARG_PREFIX = None,
    suffix: ARG_SUFFIX = None,
    force: OPT_FORCE = False,
    verbose: ARG_VERBOSE = False,
    quiet: ARG_QUIET = False,
):
    """解析字符串为 json"""
    # TODO: 解决模板代码的问题
    # TODO: 解决日志配置的问题
    console.quiet = quiet
    if verbose:
        config_log(logging.DEBUG)
    dump_text = None
    try:
        ori_text = from_clipboard_or_file(src)
        parse_text = api_parse_str_to_json(
            ori_text, recursive=recursive, del_tag=del_tag, prefix=prefix, suffix=suffix
        )
        dump_text = api_dump_json(parse_text, inline)
        to_clipboard_or_file(dst, dump_text, force, quiet)
        console.print_json(dump_text)
    except AssertionError as e:
        console.print("断言错误", e)
    except json.JSONDecodeError as e:
        console.print("无法解析字符串为 json", e)
    except Exception as e:
        console.print("未知异常", e)
        console.print("使用 -v 详细输出")


@app.command("dump")
def cmd_dump_json_to_str(
    src: ARG_SRC = None,
    dst: ARG_DST = None,
    force: OPT_FORCE = False,
    verbose: ARG_VERBOSE = False,
    quiet: ARG_QUIET = False,
):
    """将 json 序列化为字符串"""
    console.quiet = quiet
    if verbose:
        config_log(logging.DEBUG)
    dump_content = None
    try:
        origin_content = from_clipboard_or_file(src)
        dump_content = api_dump_json(origin_content, inline=False)
        to_clipboard_or_file(dst, dump_content, force, quiet)
        console.print_json(dump_content)
    except AssertionError as e:
        console.print("断言错误", e)
    except json.JSONDecodeError as e:
        console.print("无法解析字符串为 json", e)
    except Exception as e:
        console.print("未知异常", e)
        console.print("使用 -v 详细输出")


if __name__ == "__main__":
    app()
