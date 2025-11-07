from pathlib import Path

import typer
from typing_extensions import Annotated

ARG_SRC = Annotated[Path, typer.Argument(help="源文件路径")]
ARG_DST = Annotated[
    Path, typer.Argument(help="目标文件路径", show_default="默认输出到剪贴板")
]


ARG_FORCE_COVER_DST = Annotated[
    bool,
    typer.Option(
        "--force", "-f", help="是否强制覆盖 DST 目录", show_default="默认强制"
    ),
]

ARG_VERBOSE = Annotated[
    bool, typer.Option("--verbose", "-v", help="详细输出", show_default=False)
]
