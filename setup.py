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
    if file.endswith((".mp3", ".wav", ".ogg", ".mid", ".midi")):
        music_files.append(os.path.join("src/assets/music", file))

# Get the list of sound effect files
sound_files = []
sound_dir = "src/assets/sounds"
if os.path.exists(sound_dir):
    for file in os.listdir(sound_dir):
        if file.endswith((".mp3", ".wav", ".ogg")):
            sound_files.append(os.path.join(sound_dir, file))

# Get the list of icon files
icon_files = []
for file in os.listdir("src/assets/icons"):
    if file.endswith((".ico", ".png", ".icns")):
        icon_files.append(os.path.join("src/assets/icons", file))

# Create .data directory if it doesn't exist
data_dir = ".data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

DATA_FILES = [
    ("src/assets/images", image_files),
    ("src/assets/music", music_files),
    ("src/assets/sounds", sound_files),
    ("src/assets/icons", icon_files),
    (".data", []),  # Include the .data directory
]

OPTIONS = {
    "argv_emulation": True,
    "includes": [
        "pygame",
        "random",
        "math",
        "json",
        "os",
        "sys",
        "time",
        "datetime"
    ],
    "packages": [
        "src.config",
        "src.entities",
        "src.core",
        "src.utils",
        "src.assets"
    ],
    "iconfile": "src/assets/icons/icon-apple.icns",
    "plist": {
        "CFBundleName": "Alien Invasion",
        "CFBundleDisplayName": "Alien Invasion",
        "CFBundleIdentifier": "com.CodeWaveInnovation.AlienInvasion",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0",
        "CFBundlePackageType": "APPL",
        "CFBundleSignature": "????",
        "LSMinimumSystemVersion": "10.10.0",
        "NSHighResolutionCapable": True,
        "NSRequiresAquaSystemAppearance": False,
    },
}

setup(
    app=APP,
    name="Alien Invasions",
    version="1.0.0",
    description="A modern Space Invaders game with unique mechanics",
    author="Ignacio Avilés",
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
    install_requires=[
        "pygame>=2.5.0",
    ],
)
