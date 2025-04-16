import os
import sys
import ctypes
import json


def get_app_directory():
    """Get the base directory for the application.
    Returns the executable directory if running as a bundle, otherwise the project root.
    """
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle (compiled)
        return os.path.dirname(sys.executable)
    else:
        # If the application is run from a Python interpreter
        return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def ensure_data_directory():
    """Create and return the .data directory path.
    The directory will be created if it doesn't exist and will be hidden on Windows.
    """
    data_dir = os.path.join(get_app_directory(), ".data")
    os.makedirs(data_dir, exist_ok=True)

    # Make the directory hidden in Windows
    if os.name == "nt":  # Check if running on Windows
        try:
            # Set the directory as hidden using Windows API
            ctypes.windll.kernel32.SetFileAttributesW(
                data_dir, 0x02
            )  # 0x02 is FILE_ATTRIBUTE_HIDDEN
        except Exception:
            pass  # Silently fail if we can't set the attribute

    return data_dir


def resource_path(relative_path):
    """Gets the correct path to files, whether in development or in a packaged executable."""
    try:
        # For when the packed file is executed
        base_path = sys._MEIPASS
    except Exception:
        # For when the file is executed directly from source code
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def load_json_file(file_path, default_value=None):
    """Load data from a JSON file.
    Returns the default value if the file doesn't exist or is invalid.
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default_value


def save_json_file(file_path, data):
    """Save data to a JSON file."""
    with open(file_path, "w") as f:
        json.dump(data, f) 