import re
from pathlib import Path

import typer
from rich.console import Console

console = Console()
cli = typer.Typer()


def move_pattern_dst(
    src: Path,
    dst: Path = None,
    pattern: str = None,
    dry: bool = True,
    max_cnt: int = 16,
):
    # assert dst.is_dir() and dst.name.lower() in ("src", "out", "collection")
    console.print(f"提取文件到目录: {src}")
    assert src.is_dir()
    assert dst.is_dir()
    assert pattern is not None
    pat = re.compile(pattern, re.IGNORECASE)
    cnt = 0
    for file in src.rglob("*"):
        if file.is_file() and pat.search(file.stem):
            dst_file = dst.joinpath(file.name)
            console.print(f"移动文件({not dry}: {file} -> {dst_file}")
            if not dry and not dst_file.exists():
                file.rename(dst_file)
            cnt += 1
        if cnt >= max_cnt:
            break
    console.print(f"总共移动文件({not dry}): {cnt} 个(最大移动文件为 {max_cnt})")


def move_prefix_ext(
    src: Path, dst: Path, *, prefix: re.Pattern, ext: list[str] = None, dry: bool = True
):
    console.rule(f"移动文件到目录 prefix='{prefix}' ext={ext}")
    ext_set = set([e.lower() for e in ext])
    cnt = exist = not_match = 0
    for file in src.rglob("*"):
        if not file.is_file():
            continue
        # console.print(file, prefix.match(file.stem), file.suffix.lower() in ext_set)
        if file.suffix.lower() in ext_set and prefix.match(file.stem):
            dst_file = dst.joinpath(file.name)
            console.log(f"移动({not dry}) {file} -> {dst_file}")
            if not dst_file.exists():
                cnt += 1
                if not dry:
                    file.rename(dst_file)
            else:
                exist += 1
                console.print(f"{file} -> {dst_file} 文件已存在，无法移动")
        else:
            console.print(f"文件={file} 不匹配")
            not_match += 1
    console.print(
        f"总共移动文件数量={cnt}, 无法移动的文件数量={exist}, 不匹配文件数量={not_match}"
    )
