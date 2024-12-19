from textual.app import Binding
from textual.widgets import TextArea

class Text(TextArea):
    BINDINGS = [
        Binding("hjkl", "", "Movement"),
        Binding("h", "left", show=False),
        Binding("j", "down", show=False),
        Binding("k", "up", show=False),
        Binding("l", "right", show=False),
        Binding("%", "select_all", "Select all"),
        Binding("w", "select_word", "Select word"),
        Binding("p", "play", "Play selection"),
    ]

    def action_left(self):
        self.cursor_location = self.get_cursor_left_location()

    def action_down(self):
        self.cursor_location = self.get_cursor_down_location()

    def action_up(self):
        self.cursor_location = self.get_cursor_up_location()

    def action_right(self):
        self.cursor_location = self.get_cursor_right_location()

    def action_select_all(self):
        info("select_all")

    def action_select_word(self):
        info(self.cursor_location)
        info(self.selection)

    def action_play(self):
        info("play")

