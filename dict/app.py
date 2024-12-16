from logging import info, basicConfig, debug
from textual.logging import TextualHandler
from textual.app import App, ComposeResult, Binding
from textual.widgets import Footer, Label, Tabs, Tab, TabbedContent, TabPane, Markdown, Static, Button, Checkbox, TextArea
from textual.keys import Keys
from textual.events import Key
from textual.containers import Horizontal, Vertical, Container
from dict.settings import Settings
from sys import exit


class DictText(TextArea):
    BINDINGS = [
        Binding("w", "select_word()", "Select word"),
        Binding("p", "play", "Play selection"),
    ]

    def action_select_word(self):
        info(self.cursor_location)
        info(self.selection)

    def action_play(self):
        info("play")


class DictApp(App):
    BINDINGS = [
        Binding("1", "tab_meaning()", "Meaning"),
        Binding("2", "tab_translate()", "Translate"),
        Binding("3", "tab_settings()", "Settings"),
        Binding("q", "quit()", "Quit"),
    ]
    CSS = """
        Horizontal#footer-outer {
            height: 1;
            dock: bottom;
        }
        TabPane{
            layout: horizontal;
        }
        .box#hhhh {
            height: 1fr;
            width: 0.1fr;
        }
        .box#file {
            height: 1fr;
            width: 0.1fr;
        }
        Label#right-label {
            # width: 25%;
            text-align: right;
        }
    """

    def compose(self) -> ComposeResult:
        self.tabs = TabbedContent(classes="box")
        self.meaning_tab = TabPane("Meaning", id="meaning", classes="box")
        self.translate_tab = TabPane("Translate", id="translate", classes="box")
        self.settings_tab = TabPane("Settings", id="settings", classes="box")
        self.meaning = Markdown("asdf\n\n\n\n\n\n\n\n\n\nifgfgj", classes="box")
        self.meaning.styles.height = "1fr"
        self.file = DictText("fdsa", id="file", classes="box", language="python", read_only=True)
        self.settings = Markdown("asdf\n\n\n\n\n\n\n\n\n\nifgfgj", classes="box")
        self.settings.styles.height = "1fr"
        with self.tabs:
            with self.meaning_tab:
                yield self.meaning
            with self.translate_tab:
                yield Container(
                    Horizontal(
                        self.file,
                        Markdown("hhhh", id="hhhh", classes="box"),
                    ),
                )
            with self.settings_tab:
                yield self.settings
        self.footer = Footer()
        self.footer.show_command_palette = False
        self.languages = Label("languages", id="right-label", classes="box")
        with Horizontal(id="footer-outer", classes="box"):
            with Horizontal(id="footer-inner", classes="box"):
                yield self.footer
            yield self.languages

    def on_mount(self) -> None:
        settings = Settings()
        if settings.theme is not None:
            self.theme = settings.theme

    def action_tab_meaning(self):
        self.set_focus(None)
        self.tabs.focus()
        self.tabs.active = "meaning"

    def action_tab_translate(self):
        self.set_focus(None)
        self.file.focus()
        self.tabs.active = "translate"

    def action_tab_settings(self):
        self.set_focus(None)
        self.tabs.focus()
        self.tabs.active = "settings"

    def action_quit(self):
        info("Request to quit the application")
        self.exit()

    def action_search(self) -> None:
        info("Search")

    def action_open(self) -> None:
        info("Open file")

    def on_tabbed_content_tab_activated(
        self, event: TabbedContent.TabActivated
    ) -> None:
        key_search = "slash"
        if event.tab.id == "--content-tab-meaning":
            self.bind(key_search, "search", description="Search")
        else:
            if key_search in self.active_bindings.keys():
                self._bindings.key_to_bindings.pop(key_search)
                self.refresh_bindings()

        key_open = "o"
        if event.tab.id == "--content-tab-translate":
            self.bind(key_open, "open", description="Open file")
        else:
            if key_open in self.active_bindings.keys():
                self._bindings.key_to_bindings.pop(key_open)
                self.refresh_bindings()
