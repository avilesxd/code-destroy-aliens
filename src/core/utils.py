import os
import sys


def resource_path(relative_path):
    """
    Gets the correct path to files, whether in development or in a packaged executable.
    """
    try:
        # For when the packed file is executed
        base_path = sys._MEIPASS
    except Exception:
        # For when the file is executed directly from source code
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
