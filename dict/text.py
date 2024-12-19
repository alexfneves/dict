import string

from logging import info
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
        Binding("w", "go_to_word_right", "Go to next word"),
        Binding("p", "play", "Play selection"),
    ]

    def is_symbol(char):
        """Check if the character is a standalone symbol."""
        symbols = list(string.punctuation.replace('-', '')) + [' ', '\t', '\n']
        return char in symbols

    def is_word_character(char):
        """Check if the character is a word character (alphanumeric or underscore)."""
        return char.isalnum() or char == '_'

    def is_word_hyphen(text, index):
        """
        Evaluate if a hyphen at the given index is part of a compound word
        or a standalone symbol.
        """
        if text[index] != '-':
            return False  # The character at the index is not a hyphen.

        # Check characters on both sides of the hyphen
        if index > 0 and index < len(text) - 1:
            if is_word_character(text[index - 1]) and is_word_character(text[index + 1]):
                return True  # Hyphen is part of a compound word.

        return False  # Otherwise, treat the hyphen as a symbol.

    def action_left(self):
        self.action_cursor_left()

    def action_down(self):
        self.action_cursor_down()

    def action_up(self):
        self.action_cursor_up()

    def action_right(self):
        self.action_cursor_right()

    def action_select_all(self):
        self.select_all()

    def action_go_to_word_right(self):
        info(self.cursor_location)
        info(self.selection)
        
        row, col = self.cursor_location
        lines = self.text.splitlines()
        if 0 <= row < len(lines) and 0 <= col < len(lines[row]):
            char_at_cursor = lines[row][col]
            info(f"Character at cursor: {char_at_cursor}")
        else:
            info("Cursor is out of bounds.")
        # info(self.text[self.cursor_position])

        # if not (is_word_character() or () self.selected_text

    def action_play(self):
        info("play")

