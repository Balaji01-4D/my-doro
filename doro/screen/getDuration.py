from ast import With
from textual.screen import ModalScreen
from textual.widgets import MaskedInput, Label, Button
from textual.containers import Container, Vertical, Horizontal


class GetDuration(ModalScreen):

    def compose(self):

        with Container():
            yield Label("DURATIONS",id="header")
            with Horizontal():
                with Vertical():
                    yield MaskedInput(template="D0;_",value="25")
                    yield Label("POMODORO")
                with Vertical():
                    yield MaskedInput(template="D0;_",value="5")
                    yield Label("BREAK")
                with Vertical():
                    yield MaskedInput(template="D0;_", value="15")
                    yield Label("LONG BREAK")
            yield Button()
