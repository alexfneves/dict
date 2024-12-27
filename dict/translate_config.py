from logging import debug

from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Checkbox

from dict.settings import Settings, SettingsFile


class TranslateConfig(ModalScreen):
    DEFAULT_CSS = """
    TranslateConfig {
        align: center middle;
        width: auto;
        height: auto;
    }
    TranslateConfig > Container {
        width: auto;
        height: auto;
        width: 0.75fr;
    }
    Checkbox {
        # align: center top;
        width: 1fr;
        # overflow-y: auto;
    }
    """

    BINDINGS = [("escape", "finish", "Finish")]

    def __init__(self, filename: str):
        super().__init__()
        self._filename = filename
        debug(self._filename)

    def compose(self) -> ComposeResult:
        s = Settings()
        sf: SettingsFile | None = s.get_file(self._filename)
        if sf is None:
            sf = SettingsFile(filename=self._filename)
        self._translate_when_file_is_opened = Checkbox(
            "Translate when file is opened", sf.translate_when_file_is_opened
        )
        self._line_break_ends_phrase = Checkbox(
            "Line break ends a phrase", sf.line_break_ends_phrase
        )
        with Container():
            yield self._translate_when_file_is_opened
            yield self._line_break_ends_phrase

    def action_finish(self) -> None:
        s = Settings()
        sf = SettingsFile(
            filename=self._filename,
            translate_when_file_is_opened=self._translate_when_file_is_opened.value,
            line_break_ends_phrase=self._line_break_ends_phrase.value,
        )
        s.set_file(settings=sf)
        self.dismiss()
