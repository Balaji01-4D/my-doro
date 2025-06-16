from textual.app import App
from mydoro.screen.homescreen import HomeScreen
from mydoro.utils.config import ConfigHandler


class MyDoro(App):
    AUTO_FOCUS = None
    CSS_PATH = "./app.css"
    
    def __init__(self, *args, config_overrides=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_handler = ConfigHandler()
        self.config_overrides = config_overrides or {}
        
    def on_mount(self):
        if self.config_overrides:
            self.config_handler.set_multiple(self.config_overrides)
            
        self.theme = self.config_handler.get("theme", "dracula")
        
        home = HomeScreen(id="home-screen")
        home.pomodoro = self.config_handler.get("pomodoro", 25)
        home.short_break = self.config_handler.get("short_break", 5)
        home.long_break = self.config_handler.get("long_break", 15)
        home.cycles = self.config_handler.get("cycles", 3)
        
        self.push_screen(home)
        

def main(args=None):
    config = {}
    
    if args:
        for setting in ["pomodoro", "short_break", "long_break", "cycles", "theme"]:
            if hasattr(args, setting) and getattr(args, setting) is not None:
                config[setting] = getattr(args, setting)
    
    app = MyDoro(config_overrides=config)
    app.run()
