from pathlib import Path

from pydevman.config.core import create_config, merge_config_from_file


def test_from_dict():
    config = create_config({"DEBUG": False})
    assert not config.settings.debug


def test_from_file():
    default_path = Path(__file__).parent.joinpath("settings.default.toml")
    dev_path = Path(__file__).parent.joinpath("settings.dev.toml")

    config = create_config(default_path)
    assert config.app.name == "default-app"
    assert not config.app.debug

    new_config = merge_config_from_file(config, dev_path)
    assert new_config.app.name == "default-app"
    assert config.app.debug
