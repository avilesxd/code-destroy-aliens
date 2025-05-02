"""
Setup script to compile the Alien Invasion game for macOS using py2app.

Usage:
    python3 setup.py py2app

This will generate a macOS .app bundle inside the 'dist' directory.
"""

import os
import sys
from typing import List, Tuple

from setuptools import setup

APP = ["main.py"]
VERSION_FILE = "version_macOS.txt"


def collect_data_files(directory: str) -> List[Tuple[str, List[str]]]:
    paths = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if not filename.startswith("."):  # Skip hidden files
                file_path = os.path.join(root, filename)
                dest_path = os.path.dirname(os.path.relpath(file_path))
                paths.append((dest_path, [file_path]))
    return paths


def main() -> None:
    # Ensure we're running on macOS
    if sys.platform != "darwin":
        print("This setup script is for macOS only.")
        sys.exit(1)

    # Load version from file
    with open(VERSION_FILE, "r") as f:
        version = f.read().strip()

    # Collect all resources
    data_files = collect_data_files("src/assets")

    OPTIONS = {
        "argv_emulation": False,
        "iconfile": "src/assets/icons/icon-apple.icns",
        "plist": {
            "CFBundleName": "Alien Invasion",
            "CFBundleDisplayName": "Alien Invasion",
            "CFBundleGetInfoString": "Alien Invasion Game",
            "CFBundleIdentifier": "com.codewaveinnovation.alieninvasion",
            "CFBundleVersion": version,
            "CFBundleShortVersionString": version,
            "LSMinimumSystemVersion": "10.13.0",
            "NSHighResolutionCapable": True,
            "NSHumanReadableCopyright": "© 2025 Ignacio Avilés. All rights reserved.",
        },
        "packages": ["pygame", "src"],
        "includes": [
            "src.config",
            "src.config.game_functions",
            "src.config.configuration",
            "src.config.language",
            "src.config.music",
            "src.config.statistics",
            "src.core",
            "src.core.path_utils",
            "src.entities",
            "src.entities.alien",
            "src.entities.bullet",
            "src.entities.button",
            "src.entities.controls_screen",
            "src.entities.heart",
            "src.entities.scoreboard",
            "src.entities.ship",
        ],
        "resources": ["src/assets"],
        "site_packages": True,
        "strip": True,
        "optimize": 2,
        "arch": "arm64",
        "dist_dir": "dist",
        "bdist_base": "build",
        "alias": True,
        "semi_standalone": True,
    }

    setup(
        name="Alien Invasion",
        app=APP,
        data_files=data_files,
        options={"py2app": OPTIONS},
        setup_requires=["py2app"],
    )


if __name__ == "__main__":
    main()
