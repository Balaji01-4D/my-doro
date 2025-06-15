from textual.app import App
from textual.widgets import Header
from doro.screen.homescreen import HomeScreen
from doro.utils.config import ConfigHandler


class Doro(App):

    AUTO_FOCUS = None
    CSS_PATH = "./app.css"
    
    def __init__(self, *args, config_overrides=None, **kwargs):
        """Initialize the Doro application.
        
        Args:
            config_overrides: Optional dictionary of config values to override
        """
        super().__init__(*args, **kwargs)
        self.config_handler = ConfigHandler()
        self.config_overrides = config_overrides or {}

    def compose(self):
        """Create and layout the UI elements for the main application."""
        yield Header("Doro Clock")
        

    def on_mount(self):
        """Handle the application mount event."""
        # Apply any config overrides from command line arguments
        if self.config_overrides:
            self.config_handler.set_multiple(self.config_overrides)
            
        # Set the theme from config
        self.theme = self.config_handler.get("theme", "dracula")
        
        # Create the home screen
        home_screen = HomeScreen(id="home-screen")
        
        # Store configuration values on the home screen before pushing it
        home_screen.pomodoro = self.config_handler.get("pomodoro", 25)
        home_screen.short_break = self.config_handler.get("short_break", 5)
        home_screen.long_break = self.config_handler.get("long_break", 15)
        home_screen.cycles = self.config_handler.get("cycles", 3)
        
        # Push the screen - this will call compose() and create the progress_bar
        self.push_screen(home_screen)
        

def main(args=None):
    """Run the Doro application.
    
    Args:
        args: Optional command-line arguments
    """
    config_overrides = {}
    
    # Process command line arguments if provided
    if args:
        if hasattr(args, "pomodoro") and args.pomodoro is not None:
            config_overrides["pomodoro"] = args.pomodoro
        if hasattr(args, "short_break") and args.short_break is not None:
            config_overrides["short_break"] = args.short_break
        if hasattr(args, "long_break") and args.long_break is not None:
            config_overrides["long_break"] = args.long_break
        if hasattr(args, "cycles") and args.cycles is not None:
            config_overrides["cycles"] = args.cycles
        if hasattr(args, "theme") and args.theme is not None:
            config_overrides["theme"] = args.theme
    
    app = Doro(config_overrides=config_overrides)
    app.run()


if __name__ == "__main__":
    main()
