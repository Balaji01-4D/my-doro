from textual.screen import ModalScreen
from textual.widgets import MaskedInput, Label, Button
from textual.containers import Container, Vertical, Horizontal
from typing import List, Optional, Union


class GetDuration(ModalScreen):

    DEFAULT_CSS = """
    #header {
        text-align: center;
        margin-bottom: 1;
    }
    
    .maskinput-container {
        width: 1fr;
        height: auto;
        margin: 0 1;
    }
    
    #button-container {
        margin-top: 1;
        height: auto;
        align: center middle;
    }
    
    .button {
        margin: 0 1;
    }
    """

    def compose(self):
        """Create and layout the UI elements for the duration settings screen."""
        self.pomodoro_input = MaskedInput(
            template="D0;_", value="25", id="pomodoro_input"
        )
        self.short_break_input = MaskedInput(
            template="D0;_", value="5", id="short_break_input"
        )
        self.long_break_input = MaskedInput(
            template="D0;_", value="15", id="long_break_input"
        )
        self.cycles_input = MaskedInput(template="D0;_", value="4", id="cycles_input")

        with Container():
            yield Label("DURATION", id="header")
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
                with Vertical(classes="maskinput-container"):
                    yield self.cycles_input
                    yield Label("CYCLES")
            with Horizontal(id="button-container"):
                yield Button(label="OK", id="ok_button", variant="success", classes="button")
                yield Button(label="CANCEL", id="cancel_button", variant="error", classes="button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events on the duration settings screen.
        
        Args:
            event: The button press event
        """
        if event.button.id == "ok_button":
            # Validate that all values are at least 1
            values = [
                max(1, int(self.pomodoro_input.value or "1")),
                max(1, int(self.short_break_input.value or "1")),
                max(1, int(self.long_break_input.value or "1")),
                max(1, int(self.cycles_input.value or "1")),
            ]
            self.dismiss(values)
        elif event.button.id == "cancel_button":
            self.dismiss([])
