from textual.app import App
from textual.widgets import Header
from doro.screen.homescreen import HomeScreen


class Doro(App):

    CSS_PATH = "./app.css"

    theme = "monokai"


    def compose(self):
        yield Header("Doro Clock")
        

    def on_mount(self):
        self.push_screen(HomeScreen(id="home-screen"))


def main():
    app = Doro()
    app.run()


if __name__ == "__main__":
    main()
