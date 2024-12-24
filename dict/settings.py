import tomllib
from functools import wraps
from logging import error, info, warning
from pathlib import Path
from sys import exit
from typing import Optional

import tomli_w
from textual.theme import BUILTIN_THEMES


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
class Settings:
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
            error(
                f"Failed to create folder {data_path}: {e}. Since the folder is necessary, the program will exit"
            )
            exit()

        try:
            f = open(self.settings_path, "rb")
        except FileNotFoundError:
            info(
                f"Failed to load file {self.settings_path}. Using default configuration values."
            )
        else:
            self.toml_data: dict = tomllib.load(f)
            if "theme" in self.toml_data.keys():
                if self.toml_data["theme"] in BUILTIN_THEMES.keys():
                    self.theme = self.toml_data["theme"]
                else:
                    warning(
                        f"Theme {self.toml_data['theme']} doesn't exist. Ignoring configuration."
                    )
            if "locale" in self.toml_data.keys():
                if self.toml_data["locale"] in Settings.LOCALES.values():
                    self.locale = self.toml_data["locale"]
                else:
                    warning(
                        f"Locale {toml_data['locale']} is not defined. Ignoring configuration and setting it to en."
                    )
                    self.locale = "en"
            else:
                self.locale = "en"
            f.close()

    def set_locale(self, locale: str) -> bool:
        if locale not in Settings.LOCALES.values():
            info("Can't save locale {locale} because it's not available.")
            return False
        try:
            f = open(self.settings_path, "wb")
        except FileNotFoundError:
            info(
                f"Failed to open file {self.settings_path}. Giving up on saving settings."
            )
            return False
        self.toml_data["locale"] = locale
        tomli_w.dump(self.toml_data, f)
        f.close()
        self.locale = locale
        return True
