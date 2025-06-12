from datetime import datetime

from textual.app import App, ComposeResult
from textual.widgets import Digits

from screen.getDuration import GetDuration

class ClockApp(App):

    CSS_PATH = "./app.css"

    minute = 0
    second = 0

    def compose(self) -> ComposeResult:
        yield Digits("", id="clock")

    def on_ready(self) -> None:
        # self.update_clock()
        self.set_interval(1, self.start_timer)

    def update_clock(self) -> None:
        clock = datetime.now().time()
        self.query_one(Digits).update(f"{clock:%T}")

    def start_timer(self):
        self.second += 1
        if (self.second == 60):
            self.second = 0
            self.minute += 1
        timer_format = f'{self.minute:02d}:{self.second:02d}'
        self.query_one(Digits).update(f"{timer_format}")


    def key_m(self):
        self.push_screen(GetDuration())



if __name__ == "__main__":
    app = ClockApp()
    app.run()
