import string
from logging import debug
from typing import List, Tuple

from textual.app import Binding
from textual.message import Message
from textual.widgets import TextArea


def is_symbol(char):
    """Check if the character is a standalone symbol."""
    symbols = list(string.punctuation.replace("-", "")) + [" ", "\t", "\n"]
    return char in symbols


def is_word_character(char):
    """Check if the character is a word character (alphanumeric or underscore)."""
    return char.isalnum() or char == "_"


def is_word_hyphen(text, index):
    """
    Evaluate if a hyphen at the given index is part of a compound word
    or a standalone symbol.
    """
    if text[index] != "-":
        return False  # The character at the index is not a hyphen.

    # Check characters on both sides of the hyphen
    if index > 0 and index < len(text) - 1:
        if is_word_character(text[index - 1]) and is_word_character(text[index + 1]):
            return True  # Hyphen is part of a compound word.

    return False  # Otherwise, treat the hyphen as a symbol.


class Text(TextArea):
    BINDINGS = [
        Binding("hjkl", "", "Movement"),
        Binding("h", "left", show=False),
        Binding("j", "down", show=False),
        Binding("k", "up", show=False),
        Binding("l", "right", show=False),
        Binding("H", "left_selecting", show=False),
        Binding("J", "down_selecting", show=False),
        Binding("K", "up_selecting", show=False),
        Binding("L", "right_selecting", show=False),
        Binding("%", "select_all", "Select all"),
        Binding("w", "go_to_word_right", "Go to next word"),
        Binding("b", "go_to_word_left", "Go to previous word"),
        Binding("m", "meaning", "Word meaning"),
        Binding("p", "play", "Play selection"),
    ]

    class GoToMeaning(Message):
        def __init__(self, word: str) -> None:
            self.word = word
            super().__init__()

    def __init__(self, *args, **kwargs):
        # Ensure show_line_numbers is set to True
        kwargs["show_line_numbers"] = True
        super().__init__(*args, **kwargs)

    def find(
        self,
        word: bool,
        lines: List[str],
        init_row: int,
        init_col: int,
        to_right: bool,
        multiple_lines: bool = True,
    ) -> Tuple[int, int] | None:
        if to_right:
            direction = 1
            ran = range(init_row, len(lines))
        else:
            direction = -1
            ran = range(init_row, -1, -1)
            debug(ran)
        c = None
        for r in ran:
            debug(f"checking line {r}")
            if c is None:
                c = init_col + direction
            else:
                c = 0 if to_right else len(lines[r]) - 1
            debug(c)
            while 0 <= c < len(lines[r]):
                char_at_cursor = lines[r][c]
                is_word = is_word_character(char_at_cursor) or is_word_hyphen(
                    self.text, self.document.get_index_from_location((r, c))
                )
                debug(f"Character ({r}, {c}): {char_at_cursor}")
                if (word and is_word) or (not word and not is_word):
                    return (r, c)
                c = c + direction
            debug("Cursor is out of bounds.")
            if not multiple_lines:
                return (r, c)
        return None

    def go_to_word(self, to_right):
        row, col = self.cursor_location
        lines = self.text.splitlines()
        char_at_cursor = None
        if 0 <= row < len(lines) and 0 <= col < len(lines[row]):
            char_at_cursor = lines[row][col]
            debug(f"Character at cursor: {char_at_cursor}")
        else:
            debug("Cursor is out of bounds.")

        if char_at_cursor is not None and (
            is_word_character(char_at_cursor)
            or is_word_hyphen(
                self.text, self.document.get_index_from_location((row, col))
            )
        ):
            debug(f"is word at ({row}, {col})")
            found = self.find(
                word=False,
                lines=lines,
                init_row=row,
                init_col=col,
                to_right=to_right,
                multiple_lines=False,
            )
            if found is None:
                debug("Failed to find next non word")
                return
            row, col = found
            debug(f"is not word at ({row}, {col})")
        found = self.find(
            word=True, lines=lines, init_row=row, init_col=col, to_right=to_right
        )
        if found is None:
            debug("Failed to find next word")
            return
        row, col = found
        debug(f"is word at ({row}, {col})")
        self.cursor_location = (row, col)

    def get_cursor_word(self, text, lines, document, row, col):
        char_at_cursor = None
        if 0 <= row < len(lines) and 0 <= col < len(lines[row]):
            char_at_cursor = lines[row][col]
        else:
            return None

        if not is_word_character(char_at_cursor) and not is_word_hyphen(
            text, document.get_index_from_location((row, col))
        ):
            return None
        _, col_right = self.find(
            word=False,
            lines=lines,
            init_row=row,
            init_col=col,
            to_right=True,
            multiple_lines=False,
        )
        _, col_left = self.find(
            word=False,
            lines=lines,
            init_row=row,
            init_col=col,
            to_right=False,
            multiple_lines=False,
        )
        word = self.get_text_range((row, col_left + 1), (row, col_right))
        return word

    def action_left(self):
        self.action_cursor_left()

    def action_down(self):
        self.action_cursor_down()

    def action_up(self):
        self.action_cursor_up()

    def action_right(self):
        self.action_cursor_right()

    def action_left_selecting(self):
        self.action_cursor_left(True)

    def action_down_selecting(self):
        self.action_cursor_down(True)

    def action_up_selecting(self):
        self.action_cursor_up(True)

    def action_right_selecting(self):
        self.action_cursor_right(True)

    def action_select_all(self):
        self.select_all()

    def action_go_to_word_right(self):
        self.go_to_word(to_right=True)

    def action_go_to_word_left(self):
        self.go_to_word(to_right=False)

    def action_meaning(self):
        row, col = self.cursor_location
        lines = self.text.splitlines()
        word = self.get_cursor_word(self.text, lines, self.document, row, col)
        if word is None:
            debug("The cursor is not in a word to get the meaning")
            return
        debug(f"Will fetch meaning of word {word}")
        self.post_message(self.GoToMeaning(word))

    def action_play(self):
        debug("play")
