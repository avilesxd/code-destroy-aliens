"""
This is a script to compile the game for MacOS using py2app.

Usage:
    python setup.py py2app
"""

from setuptools import setup
import os

APP = ["main.py"]

# Get the list of image files
image_files = []
for file in os.listdir("src/assets/images"):
    if file.endswith((".png", ".bmp")):
        image_files.append(os.path.join("src/assets/images", file))

# Get the list of music files
music_files = []
for file in os.listdir("src/assets/music"):
    if file.endswith(".mp3"):
        music_files.append(os.path.join("src/assets/music", file))

# Get the list of icon files
icon_files = []
for file in os.listdir("src/assets/icons"):
    if file.endswith((".ico", ".png", ".icns")):
        icon_files.append(os.path.join("src/assets/icons", file))

DATA_FILES = [
    ("src/assets/images", image_files),
    ("src/assets/music", music_files),
    ("src/assets/icons", icon_files),
]

OPTIONS = {
    "argv_emulation": True,
    "includes": [],
    "packages": ["src.config", "src.entities", "src.core"],
    "iconfile": "src/assets/icons/icon-apple.icns",
    "plist": {
        "CFBundleName": "Alien Invasion",
        "CFBundleDisplayName": "Alien Invasion",
        "CFBundleIdentifier": "com.CodeWaveInnovation.DestroyAliens",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0",
    },
}

setup(
    app=APP,
    name="Alien Invasion",
    version="1.0.0",
    description="Space Invader 2D Game",
    author="Ignacio Avilés",
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
