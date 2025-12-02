from pathlib import Path

from pydevman.config.core import create_config


def test_from_dict():
    config = create_config({"DEBUG": True})
    assert config.settings.debug


def test_from_file():
    path = Path(__file__).parent.joinpath("config.toml")
    config = create_config(path)
    assert config.app.name == "test-app"
