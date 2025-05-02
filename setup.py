"""
Setup script to compile the Alien Invasion game for macOS using py2app.

Usage:
    python3 setup.py py2app

This will generate a macOS .app bundle inside the 'dist' directory.
"""

from setuptools import setup

APP = ["main.py"]
VERSION_FILE = "version_macOS.txt"

# Load version from file
with open(VERSION_FILE, "r") as f:
    version = f.read().strip()

# Project Requirements
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

OPTIONS = {
    "argv_emulation": True,
    "iconfile": "assets/icons/icon-apple.icns",
    "packages": [
        "pygame",
    ],
    "resources": [
        "assets/icons",
        "assets/images",
        "assets/music",
        "assets/sounds",
        "assets/translations",
    ],
    "plist": {
        "CFBundleName": "Alien Invasion",
        "CFBundleShortVersionString": version,
        "CFBundleVersion": version,
        "CFBundleIdentifier": "com.codewaveinnovation.alieninvasion",
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
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
    install_requires=requirements,
    python_requires=">=3.8",
)
