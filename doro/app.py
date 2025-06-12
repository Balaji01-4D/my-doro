from textual.app import App

from screen.homescreen import HomeScreen

class ClockApp(App):

    CSS_PATH = "./app.css"

    def on_mount(self):
        self.push_screen(HomeScreen())



if __name__ == "__main__":
    app = ClockApp()
    app.run()
