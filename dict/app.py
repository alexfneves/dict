from logging import basicConfig, debug
from sys import exit

from textual import on
from textual.app import App, Binding, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.events import Key
from textual.keys import Keys
from textual.logging import TextualHandler
from textual.widgets import (
    Button,
    Checkbox,
    Footer,
    Input,
    Label,
    ListItem,
    ListView,
    Markdown,
    Select,
    Static,
    Tab,
    TabbedContent,
    TabPane,
    Tabs,
)

from dict.dictionary import default_dictionary, list_of_dictionaries
from dict.list_filter import ListFilter
from dict.settings import Settings
from dict.text import Text
from dict.utils.files import file_content, list_files_recursively


def mount_footer_text(dictionary=None):
    settings = Settings()
    ret = "\["
    if dictionary is not None:
        ret += f"{dictionary[0]}>{dictionary[1]}|"
    ret += f"{settings.locale}]"
    return ret


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
        settings = Settings()
        self._tabs = TabbedContent(classes="box")
        self._meaning_tab = TabPane("Meaning", id="meaning", classes="box")
        self._translate_tab = TabPane("Translate", id="translate", classes="box")
        self._settings_tab = TabPane("Settings", id="settings", classes="box")
        self._meaning = Text(
            "", id="meaning", classes="box", language="python", read_only=True
        )
        self._meaning.styles.height = "1fr"
        self._file = Text(
            "", id="file", classes="box", language="python", read_only=True
        )
        self._settings = Markdown("asdf\n\n\n\n\n\n\n\n\n\nifgfgj", classes="box")
        self._settings.styles.height = "1fr"
        with self._tabs:
            with self._meaning_tab:
                yield self._meaning
            with self._translate_tab:
                yield Container(
                    Horizontal(
                        self._file,
                        Markdown("hhhh", id="hhhh", classes="box"),
                    ),
                )
            with self._settings_tab:
                yield Container(
                    Vertical(
                        Horizontal(
                            Label("Locale"),
                            Select(
                                [(k, v) for k, v in Settings.LOCALES.items()],
                                value=settings.locale,
                                allow_blank=False,
                                id="locale",
                            ),
                        )
                    )
                )
        self._footer = Footer()
        self._footer.show_command_palette = False
        self._dictionary_meaning = default_dictionary()
        self._dictionary_translate = default_dictionary()
        self._languages = Label("", id="right-label", classes="box")
        with Horizontal(id="footer-outer", classes="box"):
            with Horizontal(id="footer-inner", classes="box"):
                yield self._footer
            yield self._languages

    def on_mount(self) -> None:
        settings = Settings()
        if settings.theme is not None:
            self.theme = settings.theme

    def action_tab_meaning(self):
        self.set_focus(None)
        self._tabs.focus()
        self._tabs.active = "meaning"

    def action_tab_translate(self):
        self.set_focus(None)
        self._file.focus()
        self._tabs.active = "translate"

    def action_tab_settings(self):
        self.set_focus(None)
        self._tabs.focus()
        self._tabs.active = "settings"

    def action_quit(self):
        debug("Request to quit the application")
        self.exit()

    def action_search(self) -> None:
        debug("Search")
        list_filter = ListFilter(
            [
                "this",
                "is",
                "a",
                "fake",
                "dictionary",
            ]
        )

        def selected_word(word: str | None) -> None:
            if word is None:
                return
            self._meaning.text = word

        self.push_screen(list_filter, selected_word)

    def action_open(self) -> None:
        debug("Open file")
        list_filter = ListFilter(list_files_recursively())

        def file_to_open(data: str | None) -> None:
            if data is None:
                return
            file_text = file_content(data)
            if file_text is None:
                return
            self._file.text = file_text

        self.push_screen(list_filter, file_to_open)

    def dictionary_language(self, tab_name):
        list_filter = ListFilter(list_of_dictionaries())

        def select_dictionary(data: str | None) -> None:
            if data is None:
                return
            if self._tabs.active == "meaning":
                self._dictionary_meaning = data
            if self._tabs.active == "translate":
                self._dictionary_translate = data
            self._languages.update(mount_footer_text(data))

        self.push_screen(list_filter, select_dictionary)

    def action_dictionary_language_meaning(self):
        debug("action_dictionary_language_meaning")
        self.dictionary_language("meaning")

    def action_dictionary_language_translate(self):
        debug("action_dictionary_language_transalte")
        self.dictionary_language("translate")

    @on(Select.Changed)
    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "locale":
            settings = Settings()
            settings.set_locale(event.value)
            if self._tabs.active == "meaning":
                text = mount_footer_text(self._dictionary_meaning)
            elif self._tabs.active == "translate":
                text = mount_footer_text(self._dictionary_translate)
            else:
                text = mount_footer_text()
            self._languages.update(text)

    def on_tabbed_content_tab_activated(
        self, event: TabbedContent.TabActivated
    ) -> None:
        key_dictionary_language = "d"
        if key_dictionary_language in self.active_bindings.keys():
            self._bindings.key_to_bindings.pop(key_dictionary_language)

        key_search = "slash"
        if event.tab.id == "--content-tab-meaning":
            self.bind(
                key_dictionary_language,
                "dictionary_language_meaning",
                description="Dictionary",
            )
            self.bind(key_search, "search", description="Search")
            self._languages.update(mount_footer_text(self._dictionary_meaning))
        else:
            if key_search in self.active_bindings.keys():
                self._bindings.key_to_bindings.pop(key_search)
                self.refresh_bindings()

        key_open = "o"
        if event.tab.id == "--content-tab-translate":
            self.bind(
                key_dictionary_language,
                "dictionary_language_translate",
                description="Dictionary",
            )
            self.bind(key_open, "open", description="Open file")
            self._languages.update(mount_footer_text(self._dictionary_translate))
        else:
            if key_open in self.active_bindings.keys():
                self._bindings.key_to_bindings.pop(key_open)
                self.refresh_bindings()

        if event.tab.id == "--content-tab-settings":
            self._languages.update(mount_footer_text())

    @on(Text.GoToMeaning)
    def on_go_to_meaning(self, event: Text.GoToMeaning) -> None:
        debug(f"handling meaning of word {event.word}")
        self._meaning.text = event.word
        self.action_tab_meaning()
