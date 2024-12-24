import os
from functools import singledispatch
from logging import error
from typing import Generic, List, Tuple, TypeVar

from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Input, Label, ListItem, ListView

T = TypeVar("T")


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
        self._list_data = list_data

    def compose(self) -> ComposeResult:
        self._input = Input("", id="file_name", placeholder="type filename")
        yield self._input
        self._list_view = ListView()
        with self._list_view:
            for f in self._list_data:
                yield ListItem(Label(get_text(f)))

    def action_cancel(self) -> None:
        self.dismiss()

    @on(ListView.Selected)
    def file_list_selected(self, event: ListView.Selected) -> None:
        if self._list_view.highlighted_child is None:
            return
        if len(self._list_view.highlighted_child.children) == 0:
            self.dismiss()
        r = event.item.children[0].renderable
        for d in self._list_data:
            if r == get_text(d):
                self.dismiss(d)

    @on(Input.Submitted)
    def file_name_selected(self, event: Input.Submitted) -> None:
        if self._list_view.highlighted_child is None:
            return
        if len(self._list_view.highlighted_child.children) == 0:
            self.dismiss()
        r = self._list_view.highlighted_child.children[0].renderable
        for d in self._list_data:
            if r == get_text(d):
                self.dismiss(d)

    @on(Input.Changed)
    async def file_name_changed(self, event: Input.Changed) -> None:
        self._list_view.clear()
        for d in self._list_data:
            t = get_text(d)
            if self._input.value in t:
                self._list_view.append(ListItem(Label(t)))
