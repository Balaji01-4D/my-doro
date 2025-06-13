from textual.widgets import Digits
from textual.events import Event, Click


class DoroTimer(Digits):

    def __init__(self, value="", *, name=None, id=None, classes=None, disabled=False):
        super().__init__(value, name=name, id=id, classes=classes, disabled=disabled)

    def on_click(self, event: Click): ...
