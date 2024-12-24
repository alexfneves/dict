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
        self.tabs = TabbedContent(classes="box")
        self.meaning_tab = TabPane("Meaning", id="meaning", classes="box")
        self.translate_tab = TabPane("Translate", id="translate", classes="box")
        self.settings_tab = TabPane("Settings", id="settings", classes="box")
        self.meaning = Text(
            "", id="meaning", classes="box", language="python", read_only=True
        )
        self.meaning.styles.height = "1fr"
        self.file = Text(
            "", id="file", classes="box", language="python", read_only=True
        )
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
        self.footer = Footer()
        self.footer.show_command_palette = False
        self.dictionary_meaning = default_dictionary()
        self.dictionary_translate = default_dictionary()
        self.languages = Label("", id="right-label", classes="box")
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
        debug("Request to quit the application")
        self.exit()

    def action_search(self) -> None:
        debug("Search")
        self.list_filter = ListFilter(
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
            self.meaning.text = word

        self.push_screen(self.list_filter, selected_word)

    def action_open(self) -> None:
        debug("Open file")
        self.list_filter = ListFilter(list_files_recursively())

        def file_to_open(data: str | None) -> None:
            if data is None:
                return
            file_text = file_content(data)
            if file_text is None:
                return
            self.file.text = file_text

        self.push_screen(self.list_filter, file_to_open)

    def dictionary_language(self, tab_name):
        self.list_filter = ListFilter(list_of_dictionaries())

        def select_dictionary(data: str | None) -> None:
            if data is None:
                return
            if self.tabs.active == "meaning":
                self.dictionary_meaning = data
            if self.tabs.active == "translate":
                self.dictionary_translate = data
            self.languages.update(mount_footer_text(data))

        self.push_screen(self.list_filter, select_dictionary)

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
            if self.tabs.active == "meaning":
                text = mount_footer_text(self.dictionary_meaning)
            elif self.tabs.active == "translate":
                text = mount_footer_text(self.dictionary_translate)
            else:
                text = mount_footer_text()
            self.languages.update(text)

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
            self.languages.update(mount_footer_text(self.dictionary_meaning))
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
            self.languages.update(mount_footer_text(self.dictionary_translate))
        else:
            if key_open in self.active_bindings.keys():
                self._bindings.key_to_bindings.pop(key_open)
                self.refresh_bindings()

        if event.tab.id == "--content-tab-settings":
            self.languages.update(mount_footer_text())

    @on(Text.GoToMeaning)
    def on_go_to_meaning(self, event: Text.GoToMeaning) -> None:
        debug(f"handling meaning of word {event.word}")
        self.meaning.text = event.word
        self.action_tab_meaning()
