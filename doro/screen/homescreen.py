from textual.screen import Screen
from textual.widgets import Digits, ProgressBar, Button, Header
from textual.color import Gradient
from textual.containers import Container, Center, Middle, Horizontal, Right

from textual.events import Click
from plyer import notification

from doro.screen.getDuration import GetDuration


class HomeScreen(Screen):

    AUTO_FOCUS = None

    timer_running = False

    timer_object = None

    second = 0
    minute = 0

    pomodoro = 25
    pomodoro_count = 0
    short_break = 5
    long_break = 15

    cycles = 3

    def native_notify(self, message, title="Doro Clock"):
        """Display a native system notification.
        
        Args:
            message: The notification message to display
            title: The title of the notification (defaults to 'Doro Clock')
        """
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="Doro",
                timeout=5  # seconds
            )
        except Exception as e:
            # Fallback to in-app notification if native notification fails
            self.notify(f"{message}")
    
    def compose(self):
        """Create and layout the UI elements for the pomodoro timer screen.
        
        Creates the main timer display, progress bar, and control buttons.
        """
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
            "#881177",
            "#aa3355",
            "#cc6666",
            "#ee9944",
        )
        yield Header("Doro Clock")
        with Right():
            yield Button("➕ ADD", id="add_button", variant="success")
        with Container(id="home-screen-container"):
            with Center():
                with Middle():
                    yield Digits("00:00", id="clock")
                    self.progress_bar = ProgressBar(
                        total=self.pomodoro * 60,
                        id="progress_bar",
                        show_eta=False,
                    )
                    yield self.progress_bar
        with Horizontal(id="home-screen-controls-horizontal"):
            yield Button("▶/||", id="start_pause_button", variant="success", classes="button")   
            yield Button("⟳", id="reset_button", variant="error", classes="button")



    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events on the home screen."""
        if event.button.id == "start_pause_button":
            self.toggle_timer()
        elif event.button.id == "reset_button":
            self.reset__timer()
        elif event.button.id == "add_button":
            self.app.push_screen(GetDuration(), self.set_timer_limits)


    def on_click(self, event: Click) -> None:
        """Handle click events on the clock widget."""
        if event.widget.id == "clock":
            self.toggle_timer()

    def reset__timer(self):
        """Reset the timer to its initial state."""
        self.timer_running = False
        self.second = 0
        self.minute = 0
        self.pomodoro_count = 0
        self.timer_object.pause() if self.timer_object else None
        self.update_clock()
        self.progress_bar.update(progress=0)
        self.native_notify("Timer reset")
        self.notify("Timer reset")

    def toggle_timer(self):
        """Start, pause, or resume the timer.
        
        Creates a new timer interval if one doesn't exist, pauses if running,
        or resumes if paused.
        """
        if not self.timer_object:
            self.timer_object = self.set_interval(1, self.start_timer)
            self.timer_running = True
            self.native_notify("Timer started")
            self.notify("Timer started")
        elif self.timer_running:
            self.timer_object.pause()
            self.timer_running = False
            self.native_notify("Timer paused")
            self.notify("Timer paused")
        else:
            self.timer_object.resume()
            self.timer_running = True
            self.native_notify("Timer resumed")
            self.notify("Timer resumed")


    def update_clock(self) -> None:
        """Reset the clock display to 00:00."""
        self.query_one(Digits).update(f"00:00")

    def start_timer(self):
        """Increment the timer by one second and update the display.
        
        Handles pomodoro cycle transitions between work and break periods,
        manages notifications, and updates the UI elements.
        """
        self.second += 1
        self.progress_bar.update(progress=(self.minute * 60) + self.second)
        if self.second == 60:
            self.second = 0
            self.minute += 1

        if self.minute >= self.pomodoro:
            self.minute = 0
            self.second = 0
            self.pomodoro_count += 1

            if self.pomodoro_count == self.cycles:
                self.native_notify("Time for a long break!")
                self.notify("Time for a long break!")
                self.current_period = self.long_break
            else:
                self.native_notify("Time for a short break!")
                self.notify("Time for a short break!")
                self.current_period = self.short_break

        elif hasattr(self, "current_period") and self.minute >= self.current_period:
            self.minute = 0
            self.second = 0
            self.native_notify("Break over! Time to work!")
            self.notify("Break over! Time to work!")
            self.current_period = None

        timer_format = f"{self.minute:02d}:{self.second:02d}"
        self.query_one(Digits).update(f"{timer_format}")

    def key_m(self):
        """Open the duration settings screen when 'm' key is pressed."""
        self.app.push_screen(GetDuration(), self.set_timer_limits)

    def set_timer_limits(self, pomodorolist: list[int]):
        """Set the timer limits based on user input."""
        self.pomodoro = int( pomodorolist[0])
        self.short_break = int(pomodorolist[1])
        self.long_break = int(pomodorolist[2])
        self.cycles = int(pomodorolist[3])
        self.progress_bar.total = self.pomodoro * 60
        self.update_clock()
        self.native_notify("Timer limits updated")
        self.notify("Timer limits updated")
