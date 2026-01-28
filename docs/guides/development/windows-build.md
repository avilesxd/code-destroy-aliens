# 🪟 Windows Build Guide

This guide explains how to build Alien Invasion for Windows using the current
project scripts and configuration.

## Requirements

- Windows 10 or higher
- Python 3.13 or higher
- Node.js 18+

## Install Dependencies

```bash
npm install
python -m venv env
env\Scripts\activate
npm run deps:install
```

## Build (Recommended)

Use the project script, which relies on the PyInstaller spec file:

```bash
npm run build:windows
```

The executable will be in `dist/Alien Invasion.exe`.

## CI/CD

The Windows build runs on tag pushes (`v*`) and uses `Alien Invasion.spec`.

## Troubleshooting

- Ensure the virtual environment is active when running Python commands.
- If the executable is missing, check the build logs for PyInstaller errors.

## Related Documentation

- [Release Process](../contributing/release-process.md)
