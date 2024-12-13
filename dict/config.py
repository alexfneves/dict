import tomllib

from logging import info, error, warning
from typing import Optional
from functools import wraps
from pathlib import Path
from textual.theme import BUILTIN_THEMES
from sys import exit


def singleton(orig_cls):
    orig_new = orig_cls.__new__
    instance = None

    @wraps(orig_cls.__new__)
    def __new__(cls, *args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = orig_new(cls, *args, **kwargs)
        return instance
    orig_cls.__new__ = __new__
    return orig_cls


@singleton
class Config():
    def load(self, data_path: str):
        self.language_input: str = "en"
        self.language_output: str = "en"
        self.data_path: str = Path.joinpath(Path.home(), ".dict")
        self.config_path: str = Path.joinpath(self.data_path, "config.toml")
        self.theme: Optional[str] = None

        if data_path is not None:
            self.data_path = Path(data_path)
            self.config_path = Path.joinpath(Path(self.data_path), "config.toml")

        try:
            self.data_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            error(f"Failed to create folder {data_path}: {e}. Since the folder is necessary, the program will exit")
            exit()

        try:
            f = open(self.config_path, 'rb')
        except FileNotFoundError:
            info(f'Failed to load file {self.config_path}. Using default configuration values.')
        else:
            toml_data: dict = tomllib.load(f)
            if 'theme' in toml_data.keys():
                if toml_data['theme'] in BUILTIN_THEMES.keys():
                    self.theme = toml_data['theme']
                else:
                    warning(f"Theme {toml_data['theme']} doesn't exist. Ignoring configuration.")
            f.close()
