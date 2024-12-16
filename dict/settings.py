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
class Settings():
    LOCALES = {
        "English": "en",
        "Português (Brasil)": "pt_br",
        "Dansk": "da",
    }

    def load(self, data_path: str):
        self.language_input: str = "en"
        self.language_output: str = "en"
        self.data_path: str = Path.joinpath(Path.home(), ".dict")
        self.settings_path: str = Path.joinpath(self.data_path, "settings.toml")
        self.theme: Optional[str] = None

        if data_path is not None:
            self.data_path = Path(data_path)
            self.settings_path = Path.joinpath(Path(self.data_path), "settings.toml")

        try:
            self.data_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            error(f"Failed to create folder {data_path}: {e}. Since the folder is necessary, the program will exit")
            exit()

        try:
            f = open(self.settings_path, 'rb')
        except FileNotFoundError:
            info(f'Failed to load file {self.settings_path}. Using default configuration values.')
        else:
            toml_data: dict = tomllib.load(f)
            if 'theme' in toml_data.keys():
                if toml_data['theme'] in BUILTIN_THEMES.keys():
                    self.theme = toml_data['theme']
                else:
                    warning(f"Theme {toml_data['theme']} doesn't exist. Ignoring configuration.")
            if 'locale' in toml_data.keys():
                if toml_data['locale'] in Settings.LOCALES.values():
                    self.locale = toml_data['locale']
                else:
                    warning(f"Locale {toml_data['locale']} is not defined. Ignoring configuration and setting it to en.")
                    self.locale = "en"
            else:
                self.locale = "en"
            f.close()
