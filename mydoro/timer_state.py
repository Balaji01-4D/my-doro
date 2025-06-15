"""Timer state definitions for the Doro application."""
from enum import Enum, auto


class TimerState(Enum):
    """Enum representing the different states of the Pomodoro timer."""
    IDLE = auto()
    WORKING = auto()
    SHORT_BREAK = auto()
    LONG_BREAK = auto()
    PAUSED = auto()
