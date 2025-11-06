from pathlib import Path
from pprint import pprint

import typer

from pydevman.json.api import api_json_dump_obj_to_str, api_recurse_parse_str_to_json

app = typer.Typer()


@app.command("parse-json")
def recursive_parse_json(src: Path, dst: Path = None):
    parsed = api_recurse_parse_str_to_json(src.read_text())
    if dst and not dst.exists():
        dst.mkdir(parents=True)
        content = api_json_dump_obj_to_str(parsed)
        dst.write_text(content)
    else:
        pprint(parsed)


if __name__ == "__main__":
    app()
