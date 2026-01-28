# 🍎 macOS Build Guide

This guide explains how to build Alien Invasion for macOS using the current
project scripts.

## Requirements

- macOS 10.13 or higher
- Python 3.13 or higher
- Node.js 18+

## Install Dependencies

```bash
npm install
python3 -m venv env
source env/bin/activate
npm run deps:install
```

## Build (Recommended)

```bash
npm run build:macos
```

The `.app` bundle and `.dmg` will be created in `dist/`.

## CI/CD

The macOS build runs on tag pushes (`v*`) and uses `npm run build:macos`.

## Troubleshooting

- If the build fails, check `setup.py` and the build logs.
- Ensure the virtual environment is active.

## Related Documentation

- [Release Process](../contributing/release-process.md)
