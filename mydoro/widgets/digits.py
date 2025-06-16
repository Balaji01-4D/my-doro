from textual.widgets import Digits
from typing import Optional, ClassVar


class DoroTimer(Digits):
    _value_cache: ClassVar[dict] = {}
    
    DEFAULT_CSS = """
    DoroTimer {
        padding: 0 1;
        content-align: center middle;
        text-style: bold;
    }
    
    DoroTimer.-paused {
        color: $text-muted;
    }
    
    DoroTimer.-working {
        color: $success;
    }
    
    DoroTimer.-break {
        color: $warning;
    }
    """

    def __init__(
        self, 
        value="", 
        *, 
        name=None, 
        id=None, 
        classes=None, 
        disabled=False
    ):
        super().__init__(value, name=name, id=id, classes=classes, disabled=disabled)
        
    def update(self, value):
        if value != self.value:
            super().update(value)
            
    def set_timer_state(self, state):
        self.remove_class("-working", "-break", "-paused")
        
        if state == "working":
            self.add_class("-working")
        elif state == "break":
            self.add_class("-break")
        elif state == "paused":
            self.add_class("-paused")
            
