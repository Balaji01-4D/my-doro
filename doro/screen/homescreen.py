from textual.screen import Screen
from textual.widgets import Digits, ProgressBar
from textual.color import Gradient

from textual.events import Click

from screen.getDuration import GetDuration


class HomeScreen(Screen):
    timer_running = False
    timer_object = None

    second = 0
    minute = 0

    pomodoro = 25
    pomodoro_count = 0
    short_break = 5
    long_break = 15

    cycles = 3

    def compose(self):
        gradient = Gradient.from_colors(
            "#881177",
            "#aa3355",
            "#cc6666",
            "#ee9944",
            "#eedd00",
            "#99dd55",
            "#44dd88",
            "#22ccbb",
            "#00bbcc",
            "#0099cc",
            "#3366bb",
            "#663399",
        )
        yield Digits("00:00", id="clock")
        self.progress_bar = ProgressBar(
            total=self.pomodoro * 60, 
            id="progress_bar",
            show_eta=False,
            gradient=gradient
        )
        yield self.progress_bar


    def on_click(self, event: Click) -> None:
        """Handle click events on the clock widget."""
        if event.widget.id == 'clock':
            if not self.timer_object:
                self.timer_object = self.set_interval(1, self.start_timer)
                self.timer_running = True
                self.notify("Timer started")
            elif self.timer_running:
                self.timer_object.pause()
                self.timer_running = False
                self.notify("Timer paused")
            else:
                self.timer_object.resume()
                self.timer_running = True
                self.notify("Timer resumed")


    def update_clock(self) -> None:
        self.query_one(Digits).update(f"00:00")

    def start_timer(self):
        """Increment the timer by one second and update the display."""
        self.second += 1
        self.progress_bar.update(progress=(self.minute * 60 )+ self.second)
        if (self.second == 60):
            self.second = 0
            self.minute += 1
        
        # Handle Pomodoro cycle transitions
        if (self.minute >= self.pomodoro):
            self.minute = 0
            self.second = 0
            self.pomodoro_count += 1
            
            # Determine what type of break to take
            if (self.pomodoro_count == self.cycles):
                # Long break after completing all cycles
                self.notify("Time for a long break!")
                self.current_period = self.long_break
            else:
                # Short break after each pomodoro
                self.notify("Time for a short break!")
                self.current_period = self.short_break
        
        # Handle break time completion
        elif hasattr(self, 'current_period') and self.minute >= self.current_period:
            self.minute = 0
            self.second = 0
            self.notify("Break over! Time to work!")
            # Reset to work period
            self.current_period = None

        timer_format = f'{self.minute:02d}:{self.second:02d}'
        self.query_one(Digits).update(f"{timer_format}")


    def key_m(self):
        self.push_screen(GetDuration(self.set_timer_limits))
    
    def set_timer_limits(self, pomodorolist: list[int]):
        ...

