import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigHandler:
    DEFAULT_CONFIG = {
        "pomodoro": 25,
        "short_break": 5, 
        "long_break": 15,
        "cycles": 3,
        "theme": "dracula",
        "notifications_enabled": True
    }
    
    def __init__(self, config_dir=None):
        if not config_dir:
            self.config_dir = os.path.join(str(Path.home()), ".config", "doro")
        else:
            self.config_dir = config_dir
            
        self.config_file = os.path.join(self.config_dir, "config.json")
        os.makedirs(self.config_dir, exist_ok=True)
        self.config = self._load_config()
    
    def _load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                
                # Make sure all defaults exist
                for key, value in self.DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
            except:
                return self.DEFAULT_CONFIG.copy()
        else:
            self._save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def _save_config(self, config):
        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=4)
        except IOError:
            print(f"Error: Could not save configuration to {self.config_file}")
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        self._save_config(self.config)
        
    def set_multiple(self, config_dict):
        self.config.update(config_dict)
        self._save_config(self.config)
    
    def reset_to_defaults(self):
        self.config = self.DEFAULT_CONFIG.copy()
        self._save_config(self.config)
