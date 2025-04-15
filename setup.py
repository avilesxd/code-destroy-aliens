"""
This is a script to compile the game for MacOS using py2app.

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ["main.py"]

DATA_FILES = [
    (
        "src/images",
        [
            "src/images/alien.png",
            "src/images/F16.png",
            "src/images/rocket.png",
        ],
    ),
    (
        "src/music",
        [
            "src/music/music.mp3",
        ],
    ),
    ("src/icons", ["src/icons/icon.ico", "src/icons/icon.png"]),
]

OPTIONS = {
    "argv_emulation": True,
    "includes": [],
    "packages": ["src.configuration", "src.objects"],
    "iconfile": "src/icons/icon-apple.icns",
    "plist": {
        "CFBundleName": "Aliens Invasion",
        "CFBundleDisplayName": "Aliens Invasion",
        "CFBundleIdentifier": "com.CodeWaveInnovation.DestroyAliens",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0",
    },
}

setup(
    app=APP,
    name="Aliens Invasion",
    version="1.0.0",
    description="Space Invader 2D Game",
    author="Ignacio Avilés",
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
