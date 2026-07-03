"""cli/git_cmd.py — Git 相关 CLI 命令"""

from pathlib import Path

import typer
from rich.console import Console
from typing_extensions import Annotated

from pydevman.core.git.diff import diff_stat
from pydevman.cli.table import api_build_table

console = Console()
app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})

ARG_PROJECT_DIR = Annotated[Path, typer.Argument(help="Git 仓库根目录")]
ARG_TARGET_BRANCH = Annotated[str, typer.Argument(help="待分析分支")]
OPT_BASE_BRANCH = Annotated[
    str | None,
    typer.Option("--base", "-b", help="基准分支（默认自动检测 main/master）"),
]


@app.command("diff-stat", rich_help_panel="分析")
def cmd_diff_stat(
    project_dir: ARG_PROJECT_DIR,
    target_branch: ARG_TARGET_BRANCH,
    base_branch: OPT_BASE_BRANCH = None,
):
    """分析两个分支间的代码变更行数汇总"""
    console.rule("Git 分支差异分析")
    try:
        stat = diff_stat(project_dir.resolve(), target_branch, base_branch)
        rows = [
            ("变更文件数", str(stat.files_changed)),
            ("新增代码行数", str(stat.added)),
            ("删除代码行数", str(stat.deleted)),
            ("变更代码总行数", str(stat.changed)),
        ]
        title = f"{stat.base_branch}  →  {stat.target_branch}"
        table = api_build_table(title, ["指标", "数值"], rows)
        console.print(table)
    except Exception:
        console.print_exception()


if __name__ == "__main__":
    app()
