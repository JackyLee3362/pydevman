import json

import typer
from rich.console import Console
from typing_extensions import Annotated

from pathlib import Path

from pydevman.cli.args import (
    ARG_DST,
    ARG_SRC,
    OPT_FORCE,
    OPT_QUIET,
    OPT_VERBOSE,
)
from pydevman.core.json.handler import (
    dump_json,
    filter_prefix,
    filter_suffix,
    parse_json,
    recursive_unescape,
    strip_html_tags,
)
from pydevman.cli.clipboard_utils import from_clipboard_or_file, to_clipboard_or_file
from pydevman.log import config_log

console = Console()
app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})

# ---- 仅 json 模块使用的剪贴板参数 ----

ARG_SRC_OR_FROM_CLIP = Annotated[
    Path, typer.Argument(help="源文件路径，不指定则从剪贴板读取")
]
ARG_DST_OR_TO_CLIP = Annotated[
    Path, typer.Argument(help="目标文件路径，不指定则粘贴至剪贴板")
]

OPT_RECURSIVE = Annotated[
    bool,
    typer.Option(
        "--recursive", "-r", help="是否递归去转义", show_default="默认关闭递归"
    ),
]

OPT_DEL_HTML_TAG = Annotated[
    bool,
    typer.Option("--del-tag", help="是否去除标签", show_default="默认关闭剔除标签"),
]
OPT_INLINE = Annotated[
    bool, typer.Option("--inline", help="是否单行输出", show_default="默认多行")
]

OPT_PREFIX = Annotated[list[str], typer.Option("--prefix", help="过滤的字段前缀")]
OPT_SUFFIX = Annotated[list[str], typer.Option("--suffix", help="过滤的字段后缀")]


@app.command("parse")
def cmd_recursive_parse_json(
    src: ARG_SRC_OR_FROM_CLIP = None,
    dst: ARG_DST_OR_TO_CLIP = None,
    recursive: OPT_RECURSIVE = False,
    del_tag: OPT_DEL_HTML_TAG = False,
    inline: OPT_INLINE = False,
    prefix: OPT_PREFIX = None,
    suffix: OPT_SUFFIX = None,
    force: OPT_FORCE = False,
):
    """解析字符串为 json"""
    dump_text = None
    try:
        ori_text = from_clipboard_or_file(src)

        data = parse_json(ori_text)
        if recursive:
            data = recursive_unescape(data)
        if del_tag:
            data = strip_html_tags(data)
        if prefix:
            data = filter_prefix(data, prefix)
        if suffix:
            data = filter_suffix(data, suffix)

        dump_text = dump_json(data, inline)
        to_clipboard_or_file(dst, dump_text, force)
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
):
    """将 json 序列化为字符串"""
    dump_content = None
    try:
        origin_content = from_clipboard_or_file(src)
        dump_content = dump_json(origin_content, inline=False)
        to_clipboard_or_file(dst, dump_content, force)
        console.print_json(dump_content)
    except AssertionError as e:
        console.print("断言错误", e)
    except json.JSONDecodeError as e:
        console.print("无法解析字符串为 json", e)
    except Exception as e:
        console.print("未知异常", e)
        console.print("使用 -v 详细输出")


@app.callback()
def cmd_callback(verbose: OPT_VERBOSE = False, quiet: OPT_QUIET = False):
    console.quiet = quiet
    if verbose:
        config_log("DEBUG")


if __name__ == "__main__":
    app()
