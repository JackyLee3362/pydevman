import logging
from collections import OrderedDict
from pathlib import Path

from rich import print
from rich.console import Console

from devman.helper.iter import iter_dirs, iter_files, stat_info_in_dir
from devman.helper.table import build_table

console = Console()
log = logging.getLogger(__name__)


def stat_suffix(path: Path, suffixes: list, max_depth: int = 16, max_cnt: int = 4096):
    console.rule("根据 suffix 文件计数")
    max_cnt = 0
    suffix_set = set(suffixes)
    d = {}
    cnt = 0
    for file in iter_files(path, max_depth=max_depth):
        suffix = file.suffix
        if suffix in suffix_set:
            cnt += 1
            v = d.setdefault(suffix, 0)
            d[suffix] = v + 1
        if cnt > max_cnt:
            console.print("达到最大上限文件，停止搜索")
            break
    header = ["文件类型", "数量"]
    rows = [(k, str(v)) for k, v in d.items()]
    rows.append(("TOTAL", str(cnt)))
    table = build_table("根据 SUFFIX 计数", header, rows)
    console.print(table)


def stat_cnt(root: Path, max_depth: int = 16):
    console.rule("根据目录统计递归文件")
    res: dict[Path, tuple] = OrderedDict()

    def adder(path: Path, f, d, o):
        parts = path.relative_to(root).parts
        for i in range(len(parts)):
            _path = root.joinpath(*parts[:i])
            _f, _d, _o = res.get(_path, (0, 0, 0))
            res[_path] = (f + _f, d + _d, o + _o)

    for dir in iter_dirs(root, max_depth=max_depth):
        f, d, o = stat_info_in_dir(dir)
        res[dir] = (f, d, o)
        adder(dir, f, d, o)
    header = ["路径", "文件数", "目录数", "其他文件"]
    rows = [
        (str(k.relative_to(root)), str(f), str(d), str(o))
        for k, (f, d, o) in res.items()
    ]
    table = build_table("根据目录统计文件", header, rows)
    console.print(table)


def stat_prefix(root: Path, ext: list[str], max_depth: int = 16):
    console.rule("根据目录统计递归文件前缀")
    res = {}
    ext_set = set(e.lower() for e in ext)

    for file in iter_files(root, max_depth):
        file: Path
        if file.suffix.lower() in ext_set:
            prefix = file.stem.split("_")[0]
            val = res.get(prefix, 0)
            res[prefix] = val + 1

    header = ["前缀 PREFIX", "数目"]
    rows = [(k, str(v)) for k, v in res.items()]
    table = build_table("根据目录统计文件", header, rows)
    console.print(table)


def stat(src: str, max_depth: int = 4):
    """统计文件夹个数大小，文件个数大小"""
    src_dir = Path(src)
    # 校验：防止 dst 覆盖 src
    if not src_dir.exists():
        log.info(f"{src_dir} 源文件夹不存在，请检查路径")
        return
    # 用队列解决
    total_file = 0
    total_folder = 0
    queue = [(src_dir, 0)]
    while queue:
        p, level = queue.pop()
        if level > max_depth:  # 如果递归深度大于最大深度，跳出递归
            continue
        try:
            for p in p.iterdir():
                if p.is_dir():
                    total_folder += 1
                    queue.append((p, level + 1))  # 递归进入下一层
                else:
                    total_file += 1
        except PermissionError:
            log.info(f"无权限访问，跳过... {p}")
            continue
        except Exception as e:
            log.error("未知错误...")
            log.exception(e)
    print(f"目标文件夹 : {src_dir} ")
    print(f"文件数量   : {total_file}")
    print(f"文件夹数量 : {total_folder}")
