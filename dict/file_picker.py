import os
from logging import info, error
from textual import on
from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Label, Input, ListView, ListItem

class FilePicker(ModalScreen):
    
    DEFAULT_CSS = """
    FilePicker {
        align: center middle;
        width: auto;
        height: auto;
    }
    FilePicker > Input {
        width: 0.75fr;
        border: blank;
    }
    FilePicker > ListView {
        align: center top;
        width: 0.75fr;
        height: 0.75fr;
        max-height: 0.75fr;
        overflow-y: auto;
        border: heavy blank;
    }
    FilePicker > ListView:focus {
        border: heavy $primary
    }
    """

    BINDINGS = [("escape", "handle_escape", "Handle Escape")]

    def compose(self) -> ComposeResult:
        self.input = Input("", id="file_name", placeholder="type filename")
        yield self.input
        self.files = [f for f in os.listdir('.') if os.path.isfile(f) and not f.startswith('.')]
        self.files = []
        for root, dirs, filenames in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for filename in filenames:
                if not filename.startswith('.'):
                    full_path = os.path.join(root, filename)
                    normalized_path = os.path.relpath(full_path, '.')
                    self.files.append(normalized_path)
        # self.list_view = ListView(id="file_list")
        self.list_view = ListView()
        with self.list_view:
            for f in self.files:
                yield ListItem(Label(f))

    def action_handle_escape(self) -> None:
        self.dismiss()

    @on(ListView.Selected)
    def file_list_selected(self, event: ListView.Selected) -> None:
        filename = event.item.children[0].renderable
        with open(filename) as f:
            try:
                self.dismiss(f.read())
            except Exception as e:
                error(f"Could not read file {filename}: {str(e)}")
                self.dismiss()

    @on(Input.Submitted)
    def file_name_selected(self, event: Input.Submitted) -> None:
        filename = self.list_view.highlighted_child.children[0].renderable
        with open(filename) as f:
            try:
                self.dismiss(f.read())
            except Exception as e:
                error(f"Could not read file {filename}: {str(e)}")
                self.dismiss()

    @on(Input.Changed)
    async def file_name_changed(self, event: Input.Changed) -> None:
        current_index = self.list_view.index
        self.list_view.remove()
        self.list_view = ListView()
        self.mount(self.list_view)
        for f in self.files:
            if self.input.value in f:
                self.list_view.append(ListItem(Label(f)))
