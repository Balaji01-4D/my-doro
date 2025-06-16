from textual.screen import Screen
from textual.widgets import ProgressBar, Button, Static
from textual.containers import Container, Center, Middle, Horizontal, Right
from typing import List
from textual.events import Click
from plyer import notification

from mydoro.screen.getDuration import GetDuration
from mydoro.timer_state import TimerState
from mydoro.utils.timer_utils import format_time, calculate_progress
from mydoro.widgets.digits import DoroTimer


class HomeScreen(Screen):
    AUTO_FOCUS = None

    DEFAULT_POMODORO = 25
    DEFAULT_SHORT_BREAK = 5
    DEFAULT_LONG_BREAK = 15
    DEFAULT_CYCLES = 3
    
    timer_running = False
    timer_object = None
    timer_state = TimerState.IDLE

    second = 0
    minute = 0

    pomodoro = DEFAULT_POMODORO
    pomodoro_count = 0
    short_break = DEFAULT_SHORT_BREAK
    long_break = DEFAULT_LONG_BREAK
    is_working = False

    cycles = DEFAULT_CYCLES

    def on_mount(self):
        if hasattr(self, "progress_bar") and self.progress_bar is not None:
            self.progress_bar.total = self.pomodoro * 60

    def native_notify(self, message, title="Doro Clock"):
        self.app.bell()
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="Doro",
                timeout=5
            )
        except:
            self.notify(message)
    
    def compose(self):
        self.state_label = Static("Pomodoro", id="state_label")
        with Right():
            yield Button("➕ ADD", id="add_button", variant="success")
            
        yield self.state_label                        
        with Container(id="home-screen-container"):
            with Center():
                with Middle():
                    self.clock = DoroTimer("00:00", id="clock")
                    yield self.clock
                    self.progress_bar = ProgressBar(
                        total=self.pomodoro * 60,
                        id="progress_bar",
                        show_eta=False,
                    )
                    yield self.progress_bar
        with Horizontal(id="home-screen-controls-horizontal"):
            yield Button("▶/||", id="start_pause_button", variant="success", classes="button")   
            yield Button("⟳", id="reset_button", variant="error", classes="button")


    def on_button_pressed(self, event):
        if event.button.id == "start_pause_button":
            self.toggle_timer()
        elif event.button.id == "reset_button":
            self.reset_timer()
        elif event.button.id == "add_button":
            self.app.push_screen(GetDuration(), self.set_timer_limits)


    def on_click(self, event):
        if event.widget.id == "clock":
            self.toggle_timer()

    def reset_timer(self):
        self.timer_running = False
        self.timer_state = TimerState.IDLE
        self.second = 0
        self.minute = 0
        self.pomodoro_count = 0
        
        if self.timer_object:
            self.timer_object.pause()
            
        self.update_clock()
        self.progress_bar.update(progress=0)
        self.progress_bar.total = self.pomodoro * 60
        self.native_notify("Timer reset")
        self.state_label.update("Pomodoro")
        self.state_label.remove_class("-working","-break")
        self.notify("Timer reset")
        
        if hasattr(self.clock, "set_timer_state"):
            self.clock.set_timer_state("idle")
        
        if hasattr(self, "current_period"):
            self.current_period = None

    def toggle_timer(self):
        if not self.timer_object:
            self.timer_object = self.set_interval(1, self.start_timer)
            self.timer_running = True
            self.timer_state = TimerState.WORKING
            self.native_notify("Timer started")
            self.notify("Timer started")
            self.state_label.update("Work")
            
            if hasattr(self.clock, "set_timer_state"):
                self.clock.set_timer_state("working")

        elif self.timer_running:
            self.timer_object.pause()
            self.timer_running = False
            self.timer_state = TimerState.PAUSED
            self.native_notify("Timer paused")
            self.notify("Timer paused")
            self.state_label.update("Paused")
            
            if hasattr(self.clock, "set_timer_state"):
                self.clock.set_timer_state("paused")

        else:
            self.timer_object.resume()
            self.timer_running = True
            
            if self.timer_state == TimerState.PAUSED:
                if hasattr(self, "current_period") and self.current_period is not None:
                    is_long_break = self.current_period == self.long_break
                    self.timer_state = TimerState.LONG_BREAK if is_long_break else TimerState.SHORT_BREAK
                    self.state_label.update("Break")
                    
                    if hasattr(self.clock, "set_timer_state"):
                        self.clock.set_timer_state("break")
                else:
                    self.timer_state = TimerState.WORKING
                    self.state_label.update("Work")
                    
                    if hasattr(self.clock, "set_timer_state"):
                        self.clock.set_timer_state("working")
            
            self.native_notify("Timer resumed")
            self.notify("Timer resumed")
            self.state_label.remove_class("-break")

        self.state_label.add_class("-working" if self.timer_running else "-break")


    def update_clock(self):
        self.clock.update(format_time(0, 0))

    def start_timer(self):
        self.second += 1
        progress = calculate_progress(self.minute, self.second)
        self.progress_bar.update(progress=progress)
        
        if self.second == 60:
            self.second = 0
            self.minute += 1

        if self.timer_state == TimerState.WORKING and self.minute >= self.pomodoro:
            self._handle_work_period_complete()
            
        elif (self.timer_state in (TimerState.SHORT_BREAK, TimerState.LONG_BREAK) and 
              hasattr(self, "current_period") and 
              self.current_period is not None and 
              self.minute >= self.current_period):
            self._handle_break_period_complete()

        timer_format = format_time(self.minute, self.second)
        self.clock.update(timer_format)

    def _handle_work_period_complete(self):
        self.minute = 0
        self.second = 0
        self.pomodoro_count += 1

        if self.pomodoro_count == self.cycles:
            self.timer_state = TimerState.LONG_BREAK
            self.native_notify("Time for a long break!")
            self.state_label.update("Long Break")
            self.notify("Time for a long break!")
            self.current_period = self.long_break
            self.progress_bar.total = self.long_break * 60
            
            if hasattr(self.clock, "set_timer_state"):
                self.clock.set_timer_state("break")
        else:
            self.timer_state = TimerState.SHORT_BREAK
            self.native_notify("Time for a short break!")
            self.state_label.update("Short Break")
            self.notify("Time for a short break!")
            self.current_period = self.short_break
            self.progress_bar.total = self.short_break * 60
            
            if hasattr(self.clock, "set_timer_state"):
                self.clock.set_timer_state("break")
        
        self.progress_bar.update(progress=0)
        
    def _handle_break_period_complete(self):
        self.minute = 0
        self.second = 0
        self.timer_state = TimerState.WORKING
        self.native_notify("Break over! Time to work!")
        self.state_label.update("Work")
        self.notify("Break over! Time to work!")
        self.current_period = None
        
        if hasattr(self.clock, "set_timer_state"):
            self.clock.set_timer_state("working")
            
        self.progress_bar.total = self.pomodoro * 60
        self.progress_bar.update(progress=0)

    def key_m(self):
        self.app.push_screen(GetDuration(), self.set_timer_limits)

    def set_timer_limits(self, settings):
        if settings:
            self.pomodoro = int(settings[0])
            self.short_break = int(settings[1])
            self.long_break = int(settings[2])
            self.cycles = int(settings[3])
            
            self.progress_bar.total = self.pomodoro * 60
            self.update_clock()
            
            if hasattr(self.app, "config_handler"):
                self.app.config_handler.set_multiple({
                    "pomodoro": self.pomodoro,
                    "short_break": self.short_break,
                    "long_break": self.long_break,
                    "cycles": self.cycles
                })
                
            self.native_notify("Timer limits updated")
            self.notify("Timer limits updated")


    def on_button_pressed(self, event):
        if event.button.id == "start_pause_button":
            self.toggle_timer()
        elif event.button.id == "reset_button":
            self.reset_timer()
        elif event.button.id == "add_button":
            self.app.push_screen(GetDuration(), self.set_timer_limits)


    def on_click(self, event):
        if event.widget.id == "clock":
            self.toggle_timer()

    def reset_timer(self):
        self.timer_running = False
        self.timer_state = TimerState.IDLE
        self.second = 0
        self.minute = 0
        self.pomodoro_count = 0
        
        if self.timer_object:
            self.timer_object.pause()
            
        self.update_clock()
        self.progress_bar.update(progress=0)
        self.progress_bar.total = self.pomodoro * 60
        self.native_notify("Timer reset")
        self.state_label.update("Pomodoro")
        self.state_label.remove_class("-working","-break")
        self.notify("Timer reset")
        
        if hasattr(self.clock, "set_timer_state"):
            self.clock.set_timer_state("idle")
        
        if hasattr(self, "current_period"):
            self.current_period = None

    def toggle_timer(self):
        if not self.timer_object:
            # First start
            self.timer_object = self.set_interval(1, self.start_timer)
            self.timer_running = True
            self.timer_state = TimerState.WORKING
            self.native_notify("Timer started")
            self.notify("Timer started")
            self.state_label.update("Work")
            
            if hasattr(self.clock, "set_timer_state"):
                self.clock.set_timer_state("working")

        elif self.timer_running:
            # Pause timer
            self.timer_object.pause()
            self.timer_running = False
            self.timer_state = TimerState.PAUSED
            self.native_notify("Timer paused")
            self.notify("Timer paused")
            self.state_label.update("Paused")
            
            if hasattr(self.clock, "set_timer_state"):
                self.clock.set_timer_state("paused")

        else:
            # Resume timer
            self.timer_object.resume()
            self.timer_running = True
            
            if self.timer_state == TimerState.PAUSED:
                if hasattr(self, "current_period") and self.current_period is not None:
                    self.timer_state = (TimerState.LONG_BREAK 
                                      if self.current_period == self.long_break 
                                      else TimerState.SHORT_BREAK)
                    self.state_label.update("Break")
                    
                    if hasattr(self.clock, "set_timer_state"):
                        self.clock.set_timer_state("break")
                else:
                    self.timer_state = TimerState.WORKING
                    self.state_label.update("Work")
                    
                    if hasattr(self.clock, "set_timer_state"):
                        self.clock.set_timer_state("working")
            
            self.native_notify("Timer resumed")
            self.notify("Timer resumed")
            self.state_label.remove_class("-break")

        # Update UI
        self.state_label.add_class("-working" if self.timer_running else "-break")


    def update_clock(self) -> None:
        self.clock.update(format_time(0, 0))

    def start_timer(self):
        self.second += 1
        progress = calculate_progress(self.minute, self.second)
        self.progress_bar.update(progress=progress)
        
        if self.second == 60:
            self.second = 0
            self.minute += 1

        # Check if work period is complete
        if self.timer_state == TimerState.WORKING and self.minute >= self.pomodoro:
            self._handle_work_period_complete()
            
        # Check if break period is complete
        elif (self.timer_state in (TimerState.SHORT_BREAK, TimerState.LONG_BREAK) and 
              hasattr(self, "current_period") and 
              self.current_period is not None and 
              self.minute >= self.current_period):
            self._handle_break_period_complete()

        # Update the timer display
        timer_format = format_time(self.minute, self.second)
        self.clock.update(timer_format)

    def _handle_work_period_complete(self):
        self.minute = 0
        self.second = 0
        self.pomodoro_count += 1

        if self.pomodoro_count == self.cycles:
            self.timer_state = TimerState.LONG_BREAK
            self.native_notify("Time for a long break!")
            self.state_label.update("Long Break")
            self.notify("Time for a long break!")
            self.current_period = self.long_break
            self.progress_bar.total = self.long_break * 60
            
            if hasattr(self.clock, "set_timer_state"):
                self.clock.set_timer_state("break")
        else:
            self.timer_state = TimerState.SHORT_BREAK
            self.native_notify("Time for a short break!")
            self.state_label.update("Short Break")
            self.notify("Time for a short break!")
            self.current_period = self.short_break
            self.progress_bar.total = self.short_break * 60
            
            if hasattr(self.clock, "set_timer_state"):
                self.clock.set_timer_state("break")
        
        # Reset progress bar for the break period
        self.progress_bar.update(progress=0)
        
    def _handle_break_period_complete(self):
        self.minute = 0
        self.second = 0
        self.timer_state = TimerState.WORKING
        self.native_notify("Break over! Time to work!")
        self.state_label.update("Work")
        self.notify("Break over! Time to work!")
        self.current_period = None
        
        if hasattr(self.clock, "set_timer_state"):
            self.clock.set_timer_state("working")
            
        # Reset progress bar for work period
        self.progress_bar.total = self.pomodoro * 60
        self.progress_bar.update(progress=0)

    def key_m(self):
        self.app.push_screen(GetDuration(), self.set_timer_limits)

    def set_timer_limits(self, pomodorolist: List[str]) -> None:
        if pomodorolist:
            # Convert string values to integers
            self.pomodoro = int(pomodorolist[0])
            self.short_break = int(pomodorolist[1])
            self.long_break = int(pomodorolist[2])
            self.cycles = int(pomodorolist[3])
            
            # Update the progress bar total
            self.progress_bar.total = self.pomodoro * 60
            self.update_clock()
            
            # Save settings to configuration
            if hasattr(self.app, "config_handler"):
                self.app.config_handler.set_multiple({
                    "pomodoro": self.pomodoro,
                    "short_break": self.short_break,
                    "long_break": self.long_break,
                    "cycles": self.cycles
                })
                
            self.native_notify("Timer limits updated")
            self.notify("Timer limits updated")
