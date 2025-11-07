from pathlib import Path

import pyperclip
import typer
from rich.console import Console

from devman.json.api import api_json_dump_obj_to_str, api_recurse_parse_str_to_json

app = typer.Typer()
console = Console()


@app.command("parse", help="解析字符串为 json")
def recursive_parse_json(
    src: Path, dst: Path = None, add: bool = False, recursive: bool = True
):
    "TODO: recursive 控制"
    console.rule("解析 json 字符串")
    try:
        if not src.exists():
            console.print("文件不存在")
            return
        parsed = api_recurse_parse_str_to_json(src.read_text())
        content = api_json_dump_obj_to_str(parsed)
        # 写入 src 目录
        if add:
            dst = src.with_stem(src.stem + "-parsed")
        # 写入剪贴板
        if not dst:
            pyperclip.copy(content)
            console.print("已复制到剪贴板")
            return
        # 写入文件
        if not dst.parent.exists():
            dst.parent.mkdir(parents=True)
        dst.write_text(content)
        console.print(f"已写入文件 {dst.name}")
    except Exception as e:
        console.print("异常", e)


if __name__ == "__main__":
    app()
