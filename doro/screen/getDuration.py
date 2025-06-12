from textual.screen import ModalScreen
from textual.widgets import MaskedInput, Label, Input
from textual.containers import Container, Horizontal, Vertical


class GetDuration(ModalScreen):

    def compose(self):

        with Container():
            with Horizontal():
                yield Label("Duration")
                yield MaskedInput(template="d9")
                # yield Input(placeholder="sonething")
