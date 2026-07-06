"""编码/解码 CLI 命令

提供命令行下的编码与解码功能。
输入优先级：text 参数 > --input 文件 > stdin（管道）
输出：打印到标准输出，可通过 --output/-o 写入文件

用法示例：
    # 纯字符串编码（输出到控制台）
    pydevman enc encode -t base64 "hello world"
    pydevman enc encode -t url "你好"

    # 纯字符串解码
    pydevman enc decode -t base64 "aGVsbG8="
    pydevman enc decode -t hex 68656c6c6f

    # 从文件读取 / 写入文件
    pydevman enc encode -t base64 -i input.txt -o output.txt

    # 管道模式
    echo "hello" | pydevman enc encode -t base64
"""

import logging
import sys
from pathlib import Path

import typer
from typing_extensions import Annotated

from pydevman.cli.args import OPT_FORCE, OPT_QUIET, OPT_VERBOSE
from pydevman.core.encoding.enum import EncodingFormat
from pydevman.log import config_log

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})

# ---- 共用选项 ----

OPT_FORMAT = Annotated[
    EncodingFormat,
    typer.Option(
        "--format",
        "-t",
        case_sensitive=False,
        help="编解码格式",
    ),
]

OPT_TEXT = Annotated[
    str | None,
    typer.Argument(
        help="要编码/解码的文本（不指定则从 stdin、--input 文件或剪贴板读取）"
    ),
]

OPT_INPUT_FILE = Annotated[
    Path | None,
    typer.Option(
        "--input",
        "-i",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="从文件读取输入",
    ),
]

OPT_OUTPUT_FILE = Annotated[
    Path | None,
    typer.Option(
        "--output",
        "-o",
        file_okay=True,
        dir_okay=False,
        writable=True,
        help="写入到文件（默认输出到控制台/剪贴板）",
    ),
]


# ---- 编码函数调度（函数名映射定义在 core.encoding.enum 中） ----


# ============================================================================
# 命令
# ============================================================================


@app.command("encode")
def cmd_encode(
    text: OPT_TEXT = None,
    format: OPT_FORMAT = EncodingFormat.BASE64,
    input_file: OPT_INPUT_FILE = None,
    output_file: OPT_OUTPUT_FILE = None,
    force: OPT_FORCE = False,
):
    """将文本编码为指定格式。

    输入优先级：text 参数 > --input 文件 > stdin（管道） > 剪贴板

    Examples:
        pydevman enc encode -t base64 "hello"
        pydevman enc encode -t url -i input.txt -o output.txt
        echo "hello" | pydevman enc encode -t hex
    """
    _do_transform(text, input_file, output_file, format, force, direction="encode")


@app.command("decode")
def cmd_decode(
    text: OPT_TEXT = None,
    format: OPT_FORMAT = EncodingFormat.BASE64,
    input_file: OPT_INPUT_FILE = None,
    output_file: OPT_OUTPUT_FILE = None,
    force: OPT_FORCE = False,
):
    """将文本从指定格式解码。

    输入优先级：text 参数 > --input 文件 > stdin（管道） > 剪贴板

    Examples:
        pydevman enc decode -t base64 "aGVsbG8="
        pydevman enc decode -t url "%E4%BD%A0%E5%A5%BD"
    """
    _do_transform(text, input_file, output_file, format, force, direction="decode")


@app.command("list")
def cmd_list_formats():
    """列出所有支持的编解码格式。"""
    print("支持的编解码格式：\n")
    for fmt in EncodingFormat:
        print(f"  {fmt.value:20s}  {fmt.description}")


# ============================================================================
# 内部实现
# ============================================================================


def _read_input(text: str | None, input_file: Path | None) -> str:
    """按优先级获取输入文本。

    优先级：text 参数 > --input 文件 > stdin（管道）
    """
    # 1) 直接传入的 text 参数
    if text is not None:
        return text

    # 2) --input / -i 指定的文件
    if input_file is not None:
        return input_file.read_text()

    # 3) stdin 管道输入
    if not sys.stdin.isatty():
        return sys.stdin.read().rstrip("\n")

    typer.echo("错误：未提供输入文本。请通过参数、--input 文件或管道提供输入。", err=True)
    raise SystemExit(1)


def _write_output(result: str, output_file: Path | None, force: bool) -> None:
    """输出结果。

    输出优先级：--output 文件 > stdout
    """
    # 1) --output / -o 指定的文件
    if output_file is not None:
        if output_file.exists() and not force:
            raise FileExistsError(f"文件已存在: {output_file}（使用 -f 强制覆盖）")
        output_file.write_text(result)
        return

    # 2) 打印到标准输出
    print(result)


def _do_transform(
    text: str | None,
    input_file: Path | None,
    output_file: Path | None,
    fmt: EncodingFormat,
    force: bool,
    direction: str,
) -> None:
    """执行编码或解码转换。"""
    try:
        input_text = _read_input(text, input_file)

        if direction == "encode":
            func_name = fmt.encode_func
        else:
            func_name = fmt.decode_func

        result = _call_encoding_func(func_name, input_text)
        _write_output(result, output_file, force)

    except Exception as e:
        typer.echo(f"{direction} 失败: {e}", err=True)
        logging.getLogger(__name__).debug("encoding error", exc_info=True)
        raise SystemExit(1)


def _call_encoding_func(func_name: str, text: str) -> str:
    """动态调用 core.encoding 中的编解码函数。"""
    import pydevman.core.encoding as enc_mod

    func = getattr(enc_mod, func_name)
    return func(text)


# ============================================================================
# 回调
# ============================================================================


@app.callback(invoke_without_command=True)
def cmd_callback(
    verbose: OPT_VERBOSE = False,
    quiet: OPT_QUIET = False,
    list_formats: Annotated[
        bool,
        typer.Option("--list", "-l", help="列出所有支持的编解码格式"),
    ] = False,
):
    """编码/解码工具——支持 Base64、Hex、URL、Unicode 等多种格式"""
    if quiet:
        # 静默模式：重定向 stderr，stdout 仍正常输出结果
        pass
    if verbose:
        config_log(logging.DEBUG)
    if list_formats:
        cmd_list_formats()
        raise typer.Exit()


if __name__ == "__main__":
    app()
