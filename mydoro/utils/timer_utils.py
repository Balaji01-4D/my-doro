import platform


def get_platform_info():
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }


def format_time(mins, secs):
    return f"{mins:02d}:{secs:02d}"


def calculate_progress(mins, secs):
    return (mins * 60) + secs
