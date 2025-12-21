from pathlib import Path

import typer
from typing_extensions import Annotated

ARG_SRC = Annotated[Path, typer.Argument(help="源文件路径")]
ARG_DST = Annotated[Path, typer.Argument(help="目标文件路径")]
ARG_FILE_SUFFIX = Annotated[list[str], typer.Argument(help="文件扩展名")]

ARG_DIR_FILTER_PREFIX = Annotated[
    list[str], typer.Option(help="需要过滤的文件夹prefix，默认是dot文件夹")
]
ARG_DRY_RUN = Annotated[bool, typer.Option(help="是否 DRY-RUN 模式")]

ARG_FORCE = Annotated[
    bool,
    typer.Option("--force", "-f", help="是否强制"),
]

ARG_VERBOSE = Annotated[
    bool, typer.Option("--verbose", "-v", help="详细输出", show_default=False)
]

ARG_QUIET = Annotated[
    bool, typer.Option("--quiet", "-q", help="静默输出", show_default=False)
]
