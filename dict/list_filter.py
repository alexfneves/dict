import os

from typing import List
from logging import info, error
from textual import on
from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Label, Input, ListView, ListItem

class ListFilter(ModalScreen):
    
    DEFAULT_CSS = """
    ListFilter {
        align: center middle;
        width: auto;
        height: auto;
    }
    ListFilter > Input {
        width: 0.75fr;
        border: blank;
    }
    ListFilter > ListView {
        align: center top;
        width: 0.75fr;
        height: 0.75fr;
        max-height: 0.75fr;
        overflow-y: auto;
        border: heavy blank;
    }
    ListFilter > ListView:focus {
        border: heavy $primary
    }
    """

    BINDINGS = [("escape", "handle_escape", "Handle Escape")]

    def __init__(self, list_data: List[str]):
        super().__init__()
        self.list_data = list_data

    def compose(self) -> ComposeResult:
        self.input = Input("", id="file_name", placeholder="type filename")
        yield self.input
        self.list_view = ListView()
        with self.list_view:
            for f in self.list_data:
                yield ListItem(Label(f))

    def action_handle_escape(self) -> None:
        self.dismiss()

    @on(ListView.Selected)
    def file_list_selected(self, event: ListView.Selected) -> None:
        if self.list_view.highlighted_child is None:
            return
        if len(self.list_view.highlighted_child.children) == 0:
            self.dismiss()
        self.dismiss(event.item.children[0].renderable)

    @on(Input.Submitted)
    def file_name_selected(self, event: Input.Submitted) -> None:
        if self.list_view.highlighted_child is None:
            return
        if len(self.list_view.highlighted_child.children) == 0:
            self.dismiss()
        self.dismiss(self.list_view.highlighted_child.children[0].renderable)

    @on(Input.Changed)
    async def file_name_changed(self, event: Input.Changed) -> None:
        self.list_view.clear()
        for d in self.list_data:
            if self.input.value in d:
                self.list_view.append(ListItem(Label(d)))
