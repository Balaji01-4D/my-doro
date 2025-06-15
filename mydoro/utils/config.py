"""Configuration handling for the Doro application."""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigHandler:
    """Handler for application configuration."""
    
    DEFAULT_CONFIG = {
        "pomodoro": 25,
        "short_break": 5, 
        "long_break": 15,
        "cycles": 3,
        "theme": "dracula",
        "notifications_enabled": True
    }
    
    def __init__(self, config_dir: Optional[str] = None):
        """Initialize the configuration handler.
        
        Args:
            config_dir: Optional directory for configuration files.
                       If None, uses the user's home directory.
        """
        if config_dir is None:
            self.config_dir = os.path.join(
                str(Path.home()), 
                ".config", 
                "doro"
            )
        else:
            self.config_dir = config_dir
            
        self.config_file = os.path.join(self.config_dir, "config.json")
        self._ensure_config_dir()
        self.config = self._load_config()
    
    def _ensure_config_dir(self) -> None:
        """Ensure the configuration directory exists."""
        os.makedirs(self.config_dir, exist_ok=True)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from the config file.
        
        Returns:
            The configuration as a dictionary
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                # Ensure all keys from DEFAULT_CONFIG exist
                for key, value in self.DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
            except (json.JSONDecodeError, IOError):
                # Return default if the file is invalid
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create a new config file with defaults
            self._save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to the config file.
        
        Args:
            config: The configuration to save
        """
        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=4)
        except IOError:
            # Handle error gracefully
            print(f"Error: Could not save configuration to {self.config_file}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: The configuration key
            default: The default value if the key does not exist
            
        Returns:
            The configuration value or default
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.
        
        Args:
            key: The configuration key
            value: The configuration value
        """
        self.config[key] = value
        self._save_config(self.config)
    
    def set_multiple(self, config_dict: Dict[str, Any]) -> None:
        """Set multiple configuration values at once.
        
        Args:
            config_dict: A dictionary of configuration keys and values
        """
        self.config.update(config_dict)
        self._save_config(self.config)
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        self.config = self.DEFAULT_CONFIG.copy()
        self._save_config(self.config)
