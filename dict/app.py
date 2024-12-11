from textual.app import App
from dict.config import Config

class DictApp(App):
    def on_mount(self) -> None:
        config = Config()
        if config.theme is not None:
            self.theme = config.theme
