import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Union

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def get_app_directory() -> str:
    """Get the base directory for the application.

    Returns:
        str: The executable directory if running as a bundle, otherwise the project root.

    Examples:
        >>> get_app_directory()
        '/path/to/application'
    """
    if getattr(sys, "frozen", False):
        if sys.platform == "darwin":
            if hasattr(sys, "_MEIPASS"):
                # Running from a macOS .app bundle with py2app in non-alias mode
                return os.path.dirname(os.path.dirname(os.path.dirname(sys.executable)))
            else:
                # Running from a macOS .app bundle in alias mode
                return os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    # If running from source
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def ensure_data_directory() -> str:
    """Create and return the data directory path based on the operating system.

    The directory will be created if it doesn't exist.

    Returns:
        str: Path to the data directory

    Examples:
        >>> ensure_data_directory()
        '/path/to/application/Alien Invasion'  # On Unix-like systems
        'C:\\Users\\username\\AppData\\Local\\Alien Invasion'  # On Windows
    """
    if os.name == "nt":  # Windows
        # Use AppData/Local for Windows
        appdata = os.getenv("LOCALAPPDATA")
        if not appdata:
            appdata = os.path.expanduser("~\\AppData\\Local")
        data_dir = os.path.join(appdata, "Alien Invasion")
    else:  # Unix-like systems (Linux, macOS)
        if sys.platform == "darwin" and getattr(sys, "frozen", False):
            # macOS .app bundle
            data_dir = os.path.expanduser("~/Library/Application Support/Alien Invasion")
        else:
            # Other Unix-like systems
            data_dir = os.path.join(get_app_directory(), "Alien Invasion")

    try:
        os.makedirs(data_dir, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create data directory: {e}")
        raise

    return data_dir


def resource_path(relative_path: Union[str, Path]) -> str:
    """Gets the correct path to files, whether in development or in a packaged executable.

    Args:
        relative_path (Union[str, Path]): The relative path to the resource

    Returns:
        str: The absolute path to the resource

    Examples:
        >>> resource_path("assets/image.png")
        '/path/to/application/assets/image.png'
    """
    try:
        if getattr(sys, "frozen", False):
            if sys.platform == "darwin":
                if hasattr(sys, "_MEIPASS"):
                    # Running from a macOS .app bundle with py2app in non-alias mode
                    base_path = sys._MEIPASS  # type: ignore[attr-defined]
                else:
                    # Running from a macOS .app bundle in alias mode
                    base_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            else:
                # Running from a regular frozen executable
                base_path = sys._MEIPASS  # type: ignore[attr-defined]
        else:
            # Running from source
            base_path = os.path.abspath(".")

        path = os.path.normpath(os.path.join(base_path, str(relative_path)))
        logger.info(f"Resolved resource path: {path}")
        return path
    except Exception as e:
        logger.error(f"Error resolving resource path for {relative_path}: {e}")
        return os.path.normpath(os.path.join(os.path.abspath("."), str(relative_path)))


def load_json_file(file_path: Union[str, Path], default_value: Any = None) -> Any:
    """Load data from a JSON file.

    Args:
        file_path (Union[str, Path]): Path to the JSON file
        default_value (Any, optional): Default value to return if file doesn't exist or is invalid

    Returns:
        Any: The loaded JSON data or default_value if loading fails

    Examples:
        >>> load_json_file("config.json", {"default": "value"})
        {"setting": "value"}
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.warning(f"Failed to load JSON file {file_path}: {e}")
        return default_value
    except Exception as e:
        logger.error(f"Unexpected error loading JSON file {file_path}: {e}")
        return default_value


def save_json_file(file_path: Union[str, Path], data: Any, indent: int = 4) -> bool:
    """Save data to a JSON file.

    Args:
        file_path (Union[str, Path]): Path to save the JSON file
        data (Any): Data to save
        indent (int, optional): Number of spaces for indentation

    Returns:
        bool: True if save was successful, False otherwise

    Examples:
        >>> save_json_file("config.json", {"setting": "value"})
        True
    """
    try:
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent)
        return True
    except Exception as e:
        logger.error(f"Failed to save JSON file {file_path}: {e}")
        return False
