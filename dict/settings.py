import tomllib
from enum import Enum
from functools import wraps
from logging import debug, error, info, warning
from pathlib import Path
from sys import exit
from typing import IO, Any, Callable, List, Optional, Tuple

import tomli_w
from pydantic import BaseModel


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


def open_file(write: bool):
    """Generic decorator to handle file opening and closing."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs) -> bool:
            toml: dict | None = None
            open_failed = False
            f2 = None
            try:
                f = open(self._settings_path, "rb")
                toml = tomllib.load(f)
                f.close()
                if write:
                    f2 = open(self._settings_path, "wb")
            except FileNotFoundError:
                info(
                    f"Failed to open file {self._settings_path}. Giving up on saving settings."
                )
                open_failed = True
            if write:
                ret, toml = func(self, toml, *args, **kwargs)
                if ret is not None:
                    tomli_w.dump(toml, f2)
            else:
                ret = func(self, toml, *args, **kwargs)
            if not open_failed and f2 is not None:
                f2.close()
            return ret

        return wrapper

    return decorator


def open_file_read(func: Callable) -> Callable:
    """Decorator for reading files."""
    return open_file(write=False)(func)


def open_file_write(func: Callable) -> Callable:
    """Decorator for writing files."""
    return open_file(write=True)(func)


class SettingsFile(BaseModel):
    filename: str
    language_input: str = "en"
    language_output: str = "en"
    translate_when_file_is_opened: bool = True
    line_break_ends_phrase: bool = False


class SettingsGeneralLanguages(str, Enum):
    da_da = "da__da"
    da_en = "da__en"
    da_pt_br = "da__pt_br"
    en_da = "en__da"
    en_en = "en__en"
    en_pt_br = "en__pt_br"
    pt_br_da = "pt_br__da"
    pt_br_en = "pt_br__en"
    pt_br_pt_br = "pt_br__pt_br"


class SettingsGeneralLocales(str, Enum):
    da = "da"
    en = "en"
    pt_br = "pt_br"

    @staticmethod
    def locale(code: str) -> "SettingsGeneralLocales":
        if code == SettingsGeneralLocales.da.value:
            return SettingsGeneralLocales.da
        if code == SettingsGeneralLocales.pt_br.value:
            return SettingsGeneralLocales.pt_br
        return SettingsGeneralLocales.en

    def to_str(self) -> str:
        if self == SettingsGeneralLocales.da:
            return "Danish"
        if self == SettingsGeneralLocales.pt_br:
            return "Português (Brasil)"
        return "English"


class SettingsGeneral(BaseModel):
    language_input: SettingsGeneralLanguages = SettingsGeneralLanguages.en_en
    language_output: SettingsGeneralLanguages = SettingsGeneralLanguages.en_en
    locale: SettingsGeneralLocales = SettingsGeneralLocales.en
    theme: str = "textual-dark"


@singleton
class Settings:
    def load(self, data_path: str):
        self._data_path: Path = Path.joinpath(Path.home(), ".dict")
        self._settings_path: Path = Path.joinpath(self._data_path, "settings.toml")

        if data_path is not None:
            self._data_path = Path(data_path)
            self._settings_path = Path.joinpath(Path(self._data_path), "settings.toml")

        try:
            self._data_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            error(
                f"Failed to create folder {data_path}: {e}. Since the folder is necessary, the program will exit"
            )
            exit()

    @open_file_read
    def get_general(self, toml: dict) -> SettingsGeneral:
        if toml is None:
            return SettingsGeneral()
        if "general" in toml.keys():
            return SettingsGeneral(**toml["general"])
        return SettingsGeneral()

    @open_file_write
    def set_general(self, toml: dict, settings: SettingsGeneral) -> Tuple[bool, dict]:
        if toml is None:
            return (False, toml)
        toml["general"] = settings.dict()
        return (True, toml)

    @open_file_read
    def get_file(self, toml, filename: str) -> SettingsFile:
        if toml is None:
            return SettingsFile(filename=filename)
        if "files" not in toml.keys():
            return SettingsFile(filename=filename)
        name: Path = Path.joinpath(Path().resolve(), filename)
        if name.as_posix() in toml["files"].keys():
            sf = toml["files"][name.as_posix()]
            return SettingsFile(**sf)
        return SettingsFile(filename=filename)

    @open_file_write
    def set_file(self, toml: dict, settings: SettingsFile) -> Tuple[bool, dict]:
        if toml is None:
            return (False, toml)
        name: Path = Path.joinpath(Path().resolve(), settings.filename)
        if "files" not in toml.keys():
            toml["files"] = {}
        toml["files"][name.as_posix()] = settings.dict()
        return (True, toml)
