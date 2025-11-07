from pathlib import Path


def assert_path_not_exist(src: Path):
    assert src is not None, "参数不能为 None"
    # src 必须存在
    assert not src.exists(), f"${src} 必须不存在，但是该路径存在"


def assert_path_exist(src: Path):
    assert src is not None, "参数不能为 None"
    # src 必须存在
    assert src.exists(), f"${src} 必须存在，但是该路径不存在"


def assert_path_exist_and_is_file(src: Path):
    assert_path_exist(src)
    # src 必须是文件
    assert src.is_file(), f"${src} 文件必须是文件"


def assert_path_not_exist_and_is_file(src: Path):
    assert_path_not_exist(src)
    # src 必须是文件
    assert src.is_file(), f"${src} 文件必须是文件"


def assert_path_exist_and_is_dir(src: Path):
    assert_path_exist(src)
    # src 必须是文件夹
    assert src.is_dir(), f"${src} 文件必须是文件夹"


def assert_path_not_exist_and_is_dir(src: Path):
    assert_path_not_exist(src)
    # src 必须是文件夹
    assert src.is_dir(), f"${src} 文件必须是文件夹"


def is_empty_directory(dir: Path) -> bool:
    if not dir.is_dir():
        return False
    empty = True
    for item in dir.iterdir():
        # 递归查询子目录
        empty = empty and is_empty_directory(item)
    return empty


def is_dot_path(path: Path) -> bool:
    assert_path_exist()
    return path.name.startswith(".")
