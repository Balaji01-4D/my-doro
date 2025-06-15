from textual.widgets import Digits
from typing import Optional, ClassVar


class DoroTimer(Digits):
    """An enhanced Digits widget for the Doro timer.
    
    This widget adds click handling and caching optimizations.
    """
    # Cache for previously rendered values to avoid re-rendering the same value
    _value_cache: ClassVar[dict] = {}
    
    # Custom CSS for the timer
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
        value: str = "", 
        *, 
        name: Optional[str] = None, 
        id: Optional[str] = None, 
        classes: Optional[str] = None, 
        disabled: bool = False
    ):
        """Initialize the DoroTimer widget.
        
        Args:
            value: The initial value to display
            name: The name of the widget
            id: The ID of the widget
            classes: The CSS classes to apply
            disabled: Whether the widget is disabled
        """
        super().__init__(value, name=name, id=id, classes=classes, disabled=disabled)
        
    def update(self, value: str) -> None:
        """Update the displayed value with caching for better performance.
        
        Args:
            value: The new value to display
        """
        # Only update if the value has changed
        if value != self.value:
            super().update(value)
            
    def set_timer_state(self, state: str) -> None:
        """Set the visual state of the timer.
        
        Args:
            state: The state to set (working, break, paused)
        """
        # Remove all state classes
        self.remove_class("-working", "-break", "-paused")
        
        # Add the new state class
        if state == "working":
            self.add_class("-working")
        elif state == "break":
            self.add_class("-break")
        elif state == "paused":
            self.add_class("-paused")
            
