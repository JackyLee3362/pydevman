from pathlib import Path

import typer
from rich.console import Console

from devman.json.api import api_json_dump_obj_to_str, api_recurse_parse_str_to_json

app = typer.Typer()
console = Console()


@app.command("parse", help="解析字符串为 json")
def recursive_parse_json(src: Path, dst: Path = None, recursive: bool = True):
    "TODO: recursive 控制"
    try:
        if not src.exists():
            console.print("文件不存在")
            return
        parsed = api_recurse_parse_str_to_json(src.read_text())
        if dst and not dst.exists():
            dst.mkdir(parents=True)
            content = api_json_dump_obj_to_str(parsed)
            dst.write_text(content)
        else:
            console.print(parsed)
    except Exception as e:
        console.print("异常", e)


if __name__ == "__main__":
    app()
