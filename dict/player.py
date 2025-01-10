import os
from logging import debug

import pygame
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Checkbox, Label
from textual_slider import Slider

from dict.utils.timer import Timer


def time_to_text(t: float) -> str:
    return "" if t < 0 else f"{t:.3f}"


class Player(ModalScreen):
    DEFAULT_CSS = """
    Player {
        align: center middle;
        width: auto;
        # width: 0.75fr;
        height: auto;
    }
    # Vertical {
    Player > Vertical {
        content-align: center middle;
        align: center middle;
        # width: auto;
        width: 0.75fr;
        height: auto;
    }
    Horizontal {
    # Player > Vertical  > Horizontal {
        content-align: center middle;
        align: center middle;
        # width: auto;
        # width: 0.75fr;
        height: auto;
        # height: 0.1fr;
    }
    Checkbox {
        # align: center top;
        width: 50;
        overflow-y: auto;
    }
    .time {
        # height: auto;
        height: 3;
        width: 10;
        background: red;
        content-align-horizontal: center;
        content-align-vertical: middle;
    }
    .text {
        width: 0.5fr;
        height: 12;
    }
    #checkboxes {
        width: 0.25fr;
        height: auto;
    }
    """

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("h", "step_backwards", "Step backwards"),
        ("j", "next", "Next"),
        ("k", "previous", "Previous"),
        ("l", "step_forwards", "Step forwards"),
        ("space", "play_pause", "Play/pause"),
        ("a", "autoplay", "Autoplay"),
        ("p", "phrase", "Phrase"),
        ("b", "beginning", "Beginning"),
        ("r", "repeat", "Repeat"),
    ]

    def __init__(self, text_id: str, autoplay: bool):
        super().__init__()
        self._text_id = text_id
        self._is_playing = False
        self._sound_file_index = 0
        self._sound_files = [
            "/home/alexfneves/Downloads/sample-0.mp3",
            "/home/alexfneves/Downloads/sample-2.mp3",
            "/home/alexfneves/Downloads/sample-5.mp3",
        ]
        os.environ["SDL_AUDIODRIVER"] = "pulseaudio"
        pygame.mixer.init()

        self._cur_time = Label("00.00", classes="time")
        self._total_time = Label("00.00", classes="time")
        self._slider = Slider(min=0, max=100, step=1, id="slider")
        self._autoplay = Checkbox("Autoplay", autoplay)
        self._repeat = Checkbox("Repeat")
        self._start_pos = 0

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal():
                yield self._slider
                yield self._cur_time
                yield self._total_time
            with Horizontal():
                with Vertical(id="checkboxes"):
                    yield self._autoplay
                    yield Checkbox("Phrase (or word)")
                    yield self._repeat
                yield Label(
                    "Some word or some phrase.Some word or some phrase.Some word or some phrase.Some word or some phrase.Some word or some phrase.Some word or some phrase.",
                    classes="text",
                )

        self.load_audio()
        self._timer = Timer(0.05, self.timer_cb)

    def load_audio(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        self._start_pos = 0
        self._audio_length = pygame.mixer.Sound(
            self._sound_files[self._sound_file_index]
        ).get_length()
        self._slider.max = self._audio_length * 1000.0
        self._slider.value = 0
        self._total_time.update(time_to_text(self._audio_length))
        pygame.mixer.music.load(self._sound_files[self._sound_file_index])
        self._audio_started_playing = False
        if self._autoplay.value:
            self.action_play_pause()

    async def timer_cb(self) -> None:
        cur_time = pygame.mixer.music.get_pos()
        self._cur_time.update(time_to_text((cur_time + self._start_pos) / 1000.0))
        self._slider.value = cur_time + self._start_pos
        if cur_time < 0:
            self._slider.value = 0
            self._start_pos = 0
            self._audio_started_playing = False

        if not pygame.mixer.music.get_busy() and cur_time < 0:
            if self._autoplay.value:
                if self._repeat.value and self._is_playing:
                    self.action_beginning()
                elif self._sound_file_index < len(self._sound_files) - 1:
                    self.action_next()
                    self._is_playing = True
                else:
                    self._is_playing = False
            else:
                self._is_playing = False

    def step(self, s: int):
        debug(f"step {s}")
        cur_pos = pygame.mixer.music.get_pos()
        debug(cur_pos)
        self._start_pos = cur_pos + self._start_pos + s
        debug(self._start_pos)
        pygame.mixer.music.play(start=self._start_pos / 1000.0)
        self._is_playing = True

    def action_cancel(self) -> None:
        debug("cancel")
        self._timer.cancel()
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        self.dismiss()

    def action_step_backwards(self):
        self.step(-500)

    def action_next(self):
        debug("next")
        if self._sound_file_index < len(self._sound_files) - 1:
            self._sound_file_index += 1
        self.load_audio()

    def action_previous(self):
        debug("previous")
        if self._sound_file_index > 0:
            self._sound_file_index -= 1
        self.load_audio()

    def action_step_forwards(self):
        self.step(500)

    def action_play_pause(self):
        debug("play_pause")
        if not self._audio_started_playing:
            pygame.mixer.music.play()
            self._is_playing = True
            self._audio_started_playing = True
            return
        if pygame.mixer.music.get_busy():
            self._is_playing = False
            pygame.mixer.music.pause()
        else:
            self._is_playing = True
            pygame.mixer.music.unpause()

    def action_autoplay(self):
        debug("autoplay")
        self._autoplay.value = not self._autoplay.value

    def action_phrase(self):
        debug("phrase")

    def action_beginning(self):
        debug("beginning")
        self._start_pos = 0
        pygame.mixer.music.play(start=self._start_pos / 1000.0)

    def action_repeat(self):
        debug("repeat")
        self._repeat.value = not self._repeat.value
