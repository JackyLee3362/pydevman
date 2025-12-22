from pathlib import Path

import typer
from typing_extensions import Annotated

# common argument
ARG_SRC_OR_FROM_CLIP = Annotated[
    Path, typer.Argument(help="源文件路径，不指定则从剪贴板读取")
]
ARG_DST_OR_TO_CLIP = Annotated[
    Path, typer.Argument(help="源文件路径，不指定则粘贴至剪贴板")
]
ARG_SRC = Annotated[Path, typer.Argument(help="源文件路径")]
ARG_DST = Annotated[Path, typer.Argument(help="目标文件路径")]

# common option
OPT_MAX_DEPTH = Annotated[int, typer.Option(help="遍历最大深度")]
OPT_INCLUDE_FILE_SUFFIX = Annotated[list[str], typer.Argument(help="文件扩展名")]
OPT_INCLUDE_FILE_PREFIX = Annotated[list[str], typer.Argument(help="文件前缀")]
OPT_EXCLUDE_DIR_PREFIX = Annotated[
    list[str], typer.Option("--prefix", help="需要排除的文件夹前缀")
]
OPT_EXCLUDE_DIR_SUFFIX = Annotated[
    list[str], typer.Option("--suffix", help="需要排除的文件夹后缀")
]
OPT_DRY_RUN = Annotated[bool, typer.Option(help="是否 DRY-RUN 模式")]

OPT_FORCE = Annotated[
    bool,
    typer.Option("--force", "-f", help="是否强制"),
]

OPT_VERBOSE = Annotated[
    bool, typer.Option("--verbose", "-v", help="详细输出", show_default=False)
]

OPT_QUIET = Annotated[
    bool, typer.Option("--quiet", "-q", help="静默输出", show_default=False)
]
