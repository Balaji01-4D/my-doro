from enum import Enum, auto


class TimerState(Enum):
    IDLE = auto()
    WORKING = auto()
    SHORT_BREAK = auto()
    LONG_BREAK = auto()
    PAUSED = auto()
