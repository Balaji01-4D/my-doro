from ast import With
from textual.screen import ModalScreen
from textual.widgets import MaskedInput, Label, Button
from textual.containers import Container, Vertical, Horizontal


class GetDuration(ModalScreen):

    def compose(self):
        self.pomodoro_input = MaskedInput(template="D0;_",value="25",id='pomodoro_input')
        self.short_break_input = MaskedInput(template="D0;_",value="5",id='short_break_input')
        self.long_break_input = MaskedInput(template="D0;_",value="15",id='long_break_input')

        with Container():
            yield Label("DURATION",id="header")
            with Horizontal():
                with Vertical(classes="maskinput-container"):
                    yield self.pomodoro_input
                    yield Label("POMODORO")
                with Vertical(classes="maskinput-container"):
                    yield self.short_break_input
                    yield Label("BREAK")
                with Vertical(classes="maskinput-container"):
                    yield self.long_break_input
                    yield Label("LONG BREAK")
            with Horizontal(id="button-container"):
                yield Button(label="OK", id="ok_button" , variant="success")
                yield Button(label="CANCEL", id="cancel_button", variant="error")


    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok_button":
            self.dismiss([self.pomodoro_input.value,
                        self.short_break_input.value,
                        self.long_break_input.value])
        elif event.button.id == "cancel_button":
            self.dismiss(False)
