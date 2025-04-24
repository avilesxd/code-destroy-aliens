"""
This is a script to compile the game for MacOS using py2app.

Usage:
    python setup.py py2app
"""

import os
from typing import cast

from setuptools import setup

# Read version from version.txt
with open("version.txt", "r") as f:
    version = f.read().strip()

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
    (".data", cast(list[str], [])),  # Include the .data directory
]

# Read requirements from requirements.txt
with open("requirements.txt", "r") as f:
    requirements = [
        line.strip() for line in f if line.strip() and not line.startswith("#")
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
        "datetime",
        "typing",
        "pathlib",
    ],
    "packages": [
        "src.config",
        "src.entities",
        "src.core",
        "src.utils",
        "src.assets",
    ],
    "iconfile": "src/assets/icons/icon-apple.icns",
    "plist": {
        "CFBundleName": "Alien Invasion",
        "CFBundleDisplayName": "Alien Invasion",
        "CFBundleIdentifier": "com.CodeWaveInnovation.AlienInvasion",
        "CFBundleVersion": version,
        "CFBundleShortVersionString": version,
        "CFBundlePackageType": "APPL",
        "CFBundleSignature": "????",
        "LSMinimumSystemVersion": "10.10.0",
        "NSHighResolutionCapable": True,
        "NSRequiresAquaSystemAppearance": False,
    },
}

setup(
    app=APP,
    name="Alien Invasion",
    version=version,
    description="A modern Space Invaders game with unique mechanics",
    author="Ignacio Avilés",
    author_email="nacho72001@gmail.com",
    url="https://github.com/avilesxd/code-destroy-aliens",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
    install_requires=requirements,
    python_requires=">=3.8",
)
