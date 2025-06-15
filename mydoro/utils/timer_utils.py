"""Utility functions for the Doro application."""
from typing import Dict
import platform


def get_platform_info() -> Dict[str, str]:
    """Get information about the current platform.
    
    Returns:
        A dictionary containing platform information
    """
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }


def format_time(minutes: int, seconds: int) -> str:
    """Format minutes and seconds as MM:SS.
    
    Args:
        minutes: The number of minutes
        seconds: The number of seconds
        
    Returns:
        A string in the format MM:SS
    """
    return f"{minutes:02d}:{seconds:02d}"


def calculate_progress(minutes: int, seconds: int) -> int:
    """Calculate the progress in seconds from minutes and seconds.
    
    Args:
        minutes: The number of minutes
        seconds: The number of seconds
        
    Returns:
        The total number of seconds
    """
    return (minutes * 60) + seconds
