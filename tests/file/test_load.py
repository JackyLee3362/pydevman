"""
Author: Jacky Lee
Date: 2025-12-07
Description:
"""

from pathlib import Path

import pytest

from pydevman.file.load import load_config_file

parent_dir = Path(__file__).parent


def test_json_file():
    cfg = load_config_file(parent_dir.joinpath("config.json"))
    assert cfg["app"] == {"name": "base-app", "version": "0.0.1", "debug": False}
    assert cfg["db"] == {"host": "localhost", "port": 3306, "user": ["foo", "bar"]}


def test_yaml_file():
    cfg = load_config_file(parent_dir.joinpath("config.yaml"))
    assert cfg["app"] == {"name": "base-app", "version": "0.0.1", "debug": False}
    assert cfg["db"] == {"host": "localhost", "port": 3306, "user": ["foo", "bar"]}


def test_toml_file():
    cfg = load_config_file(parent_dir.joinpath("config.toml"))
    assert cfg["app"] == {"name": "base-app", "version": "0.0.1", "debug": False}
    assert cfg["db"] == {"host": "localhost", "port": 3306, "user": ["foo", "bar"]}


def test_ini_file():
    # ini 文件无法配置数据!
    cfg = load_config_file(parent_dir.joinpath("config.ini"))
    assert cfg["app"] == {"name": "base-app", "version": "0.0.1", "debug": "false"}
    assert cfg["db"] == {"host": "localhost", "port": "3306", "user": "foo, bar"}


if __name__ == "__main__":
    pytest.main(["-vs", __file__])
