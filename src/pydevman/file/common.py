from pathlib import Path

# TODO: 如果需要生产级别的错误提示，推荐使用 raise 代替 assert


def assert_path_is_Path(path):
    assert _path_type_check(path), "Argument type must be Path."


def assert_path_not_exist(path: Path):
    assert_path_is_Path(path)
    assert _path_not_exist(path), f"Expect path={path} not exist, actually exist."


def assert_path_exist(path: Path):
    assert_path_is_Path(path)
    assert _path_exist(path), f"Expect path={path} exist, actually not exist."


def assert_path_exist_and_is_file(path: Path):
    assert_path_is_Path(path)
    assert _path_exist(path), f"Expect path={path} exist, actually not exist."
    assert _path_is_file(path), f"Expect path={path} is file, actually not."


def assert_path_exist_and_is_dir(path: Path):
    assert_path_is_Path(path)
    assert _path_exist(path), f"Expect path={path} exist, actually not exist."
    assert _path_is_dir(path), f"Expect path={path} is directory."


def assert_not_exist_or_empty_dir(path: Path):
    assert_path_is_Path(path)
    assert _path_not_exist(path) or _path_is_dir_without_any_path(path), (
        f"Expect path={path} not exist or is empty dir, actually not."
    )


def _path_is_dir_without_any_path(path: Path) -> bool:
    return path.is_dir() and not any(path.iterdir())


def _path_is_dir_without_any_file(path: Path) -> bool:
    # TODO 如果入口是文件，其实是有问题的
    if not path.is_dir():
        return False
    for item in path.iterdir():
        if item.is_file():
            # Fast Fail
            return False
        # Recursively check
        if item.is_dir() and not _path_is_dir_without_any_file(item):
            return False
    return True


def _path_is_dot_path(path: Path) -> bool:
    assert_path_exist(path)
    return path.name.startswith(".")


def _path_type_check(path):
    return isinstance(path, Path)


def _path_exist(path: Path):
    return path.exists()


def _path_not_exist(path: Path):
    return not path.exists()


def _path_is_file(path: Path):
    return path.is_file()


def _path_is_dir(path: Path):
    return path.is_dir()
