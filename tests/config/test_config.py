from pathlib import Path

from pydevman.config.core import create_config, merge_config


def test_from_dict():
    config = create_config({"debug": False})
    assert not config.debug


def test_from_file():
    default_path = Path(__file__).parent.joinpath("settings.default.toml")
    dev_path = Path(__file__).parent.joinpath("settings.dev.toml")

    config = create_config(default_path)
    assert config.app.name == "default-app"
    assert not config.app.debug
    assert config.user.list == [1, 2, 3]

    merge_config(config, dev_path)
    assert config.app.name == "dev-app"
    assert config.app.debug
    assert config.app.version == "0.0.1"
    assert config.user.list == [4, 5, 6]
    assert config.user.names == ["default"]
