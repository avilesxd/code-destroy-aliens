"""
This is a script to compile the game for MacOS using py2app.

Usage:
    python setup.py py2app
"""

from setuptools import setup
import os

APP = ['main.py']

DATA_FILES = [
    ('src/imagenes', [
        'src/imagenes/alien.bmp',
        'src/imagenes/aliens.png',
        'src/imagenes/F16.png',
        'src/imagenes/icono.ico',
        'src/imagenes/icono.png',
        'src/imagenes/nave.bmp',
        'src/imagenes/rocket.png',
    ]),
    ('src/musica', [
        'src/musica/musica.mp3',
    ]),
]

OPTIONS = {
    'argv_emulation': True,
    'includes': [],
    'packages': ['src.configuracion', 'src.objetos'],
    'iconfile': 'src/imagenes/icono.icns',  
    'resources': [],
    'plist': {
        'CFBundleName': 'Code Destroy Aliens',
        'CFBundleDisplayName': 'Code Destroy Aliens',
        'CFBundleIdentifier': 'com.avilesxd.codeDestroyAliens',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0',
    }
}

setup(
    app=APP,
    name='Code Destroy Aliens',
    version='1.0.0',
    description='Un juego clásico tipo Space Invaders',
    author='Ignacio Avilés',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

