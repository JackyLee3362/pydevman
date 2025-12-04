from os import PathLike
from typing import Dict, Union

from dynaconf import Dynaconf


def create_config(arg: Union[PathLike, Dict], env: str = None):
    """单文件配置导入，可以导入 json,toml,yaml 等文件"""
    if isinstance(arg, Dict):
        return Dynaconf(settings=arg)
    assert isinstance(arg, PathLike), "只能是单文件"
    if env is None:
        return Dynaconf(
            # root_path=root_path,
            settings_files=arg,
            # merge_enabled=True,
        )
    return Dynaconf(
        # root_path=root_path,
        environments=True,
        default_env=env,
        settings_files=arg,
        # merge_enabled=True,
    )


def merge_config_from_file(config: Dynaconf, arg: PathLike, env: str = None):
    """从路径中合并配置"""
    new_config = config.from_env(env) if env else config
    new_config.load_file(path=arg)
    return new_config
