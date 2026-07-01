from importlib.metadata import version as get_version

import typer

from pydevman.echo import app as echo_app
from pydevman.file.__main__ import app as file_app
from pydevman.json.__main__ import app as json_app

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


@app.callback(invoke_without_command=True)
def main_callback(
    version: bool = typer.Option(False, "--version", "-V", help="显示版本号"),
):
    """pydevman - 开发工具集"""
    if version:
        typer.echo(get_version("pydevman"))
        raise typer.Exit()


def main():
    app.add_typer(echo_app, name="echo", help="echo 工具")
    app.add_typer(json_app, name="json", help="json 工具")
    app.add_typer(file_app, name="file", help="file 工具")
    app()


if __name__ == "__main__":
    main()
