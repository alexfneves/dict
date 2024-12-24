import os

from typing import List, Generic, TypeVar, Tuple
from functools import singledispatch
from logging import error
from textual import on
from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Label, Input, ListView, ListItem


T = TypeVar('T')

@singledispatch
def get_text(item: T):
    """Default behavior if no specialization exists."""
    raise TypeError(f"Unsupported type: {type(item)}")

@get_text.register
def _(item: str):
    """Specialized behavior for `str`."""
    return item

@get_text.register
def _(item: tuple):
    """Specialized behavior for `Tuple[str, str]`."""
    return f"{item[0]}>{item[1]}"


class ListFilter(ModalScreen, Generic[T]):
    
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

    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, list_data: List[T]):
        super().__init__()
        self.list_data = list_data

    def compose(self) -> ComposeResult:
        self.input = Input("", id="file_name", placeholder="type filename")
        yield self.input
        self.list_view = ListView()
        with self.list_view:
            for f in self.list_data:
                yield ListItem(Label(get_text(f)))

    def action_cancel(self) -> None:
        self.dismiss()

    @on(ListView.Selected)
    def file_list_selected(self, event: ListView.Selected) -> None:
        if self.list_view.highlighted_child is None:
            return
        if len(self.list_view.highlighted_child.children) == 0:
            self.dismiss()
        r = event.item.children[0].renderable
        for d in self.list_data:
            if r == get_text(d):
                self.dismiss(d)

    @on(Input.Submitted)
    def file_name_selected(self, event: Input.Submitted) -> None:
        if self.list_view.highlighted_child is None:
            return
        if len(self.list_view.highlighted_child.children) == 0:
            self.dismiss()
        r = self.list_view.highlighted_child.children[0].renderable
        for d in self.list_data:
            if r == get_text(d):
                self.dismiss(d)

    @on(Input.Changed)
    async def file_name_changed(self, event: Input.Changed) -> None:
        self.list_view.clear()
        for d in self.list_data:
            t = get_text(d)
            if self.input.value in t:
                self.list_view.append(ListItem(Label(t)))
