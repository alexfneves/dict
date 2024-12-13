from logging import info, basicConfig, debug
from textual.logging import TextualHandler
from textual.app import App, ComposeResult
from textual.widgets import Footer, Label, Tabs, Tab, TabbedContent, TabPane, Markdown
from textual.keys import Keys
from textual.events import Key
from dict.config import Config
from sys import exit


class DictApp(App):
    def compose(self) -> ComposeResult:
        self.tabs = TabbedContent(classes="box")
        self.meaning_tab = TabPane("Meaning [1]", id="meaning", classes="box")
        self.translate_tab = TabPane("Translate [2]", id="translate", classes="box")
        self.meaning = Markdown("asdf\n\n\n\n\n\n\n\n\n\nifgfgj", classes="box")
        self.meaning.styles.height = "1fr"
        self.translate = Markdown("fdsa", classes="box")
        self.translate.styles.height = "1fr"
        with self.tabs:
            with self.meaning_tab:
                yield self.meaning
            with self.translate_tab:
                yield self.translate
        self.footer = Footer()
        yield self.footer

    def on_mount(self) -> None:
        config = Config()
        if config.theme is not None:
            self.theme = config.theme

    def on_key(self, event: Key) -> None:
        if event.key == "1":
            self.tabs.active = "meaning"
        elif event.key == "2":
            self.tabs.active = "translate"
        elif event.key == "q":
            info("Request to quit the application")
            self.exit()
