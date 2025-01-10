import os
from asyncio import Task, create_task, get_running_loop, sleep
from functools import singledispatch
from logging import error
from typing import Any, List, Optional, Tuple, TypeVar

from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Input, Label, ListItem, ListView


@singledispatch
def get_text(item: Any) -> str:
    """Default behavior if no specialization exists."""
    raise TypeError(f"Unsupported type: {type(item)}")


@get_text.register
def _(item: str) -> str:
    """Specialized behavior for `str`."""
    return item


@get_text.register
def _(item: tuple) -> str:
    """Specialized behavior for `Tuple[str, str]`."""
    return f"{item[0]}>{item[1]}"


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

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("j", "down", "Down"),
        ("k", "up", "Up"),
    ]

    def __init__(self, list_data: List[Any]):
        super().__init__()
        self._list_data: List[Any] = list_data
        self._list_view: ListView = ListView()
        self._input: Input = Input("", id="file_name", placeholder="type filename")
        self._my_task: Optional[Task] = None

    def compose(self) -> ComposeResult:
        yield self._input
        with self._list_view:
            for f in self._list_data:
                yield ListItem(Label(get_text(f)))

    def action_cancel(self) -> None:
        self.dismiss()

    def action_down(self):
        self._list_view.action_cursor_down()

    def action_up(self):
        self._list_view.action_cursor_up()

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

    async def select_first_element(self):
        self._list_view.index = 0

    async def compile_list(self) -> None:
        self._list_view.styles.visibility = "hidden"
        new_list: List[ListItem] = []
        for d in self._list_data:
            t = get_text(d)
            if self._input.value in t:
                new_list.append(ListItem(Label(t)))
        await self._list_view.clear()
        await self._list_view.extend(new_list)
        self._list_view.styles.visibility = "visible"
        create_task(self.select_first_element())

    @on(Input.Changed)
    async def file_name_changed(self, event: Input.Changed) -> None:
        loop = get_running_loop()
        if (
            loop.is_closed()
            and self._my_task is not None
            and not self._my_task.cancelled()
        ):
            self._my_task.cancel()
        self._my_task = create_task(self.compile_list())
