# macOS Build Guide

This guide explains how to build Alien Invasion for macOS.

## Requirements

- macOS 10.13 or higher
- Python 3.13 or higher
- py2app (for compilation)
- Pygame

## Installing Dependencies

1. Make sure you have Python 3.13 or higher installed:

```bash
python3 --version
```

2. Create a virtual environment and install dependencies:

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install py2app
```

## Building

### Development Mode (Alias)

For quick development and testing, use alias mode:

```bash
python3 setup.py py2app -A
```

The compiled application will be found in `dist/Alien Invasion.app`. This mode
is faster for development but requires the source code to be present.

### Production Mode

To create a standalone application:

```bash
python3 setup.py py2app
```

The compiled application will be found in `dist/Alien Invasion.app`. This
version includes all necessary dependencies and resources.

## Bundle Structure

The generated `.app` bundle contains:

- Main executable
- Resources (images, sounds, etc.)
- Python runtime
- All necessary dependencies

## Verification

To verify that the application compiled correctly:

```bash
open dist/Alien\ Invasion.app
```

## Troubleshooting

### Launch Error

If you encounter a "Launch Error":

1. Verify all dependencies are installed
2. Ensure resources are in the correct locations
3. Compile in alias mode for debugging
4. Check logs in Console.app

### Common Issues

- **Permission Error**: Run
  `chmod +x dist/Alien\ Invasion.app/Contents/MacOS/Alien\ Invasion`
- **Resources Not Found**: Check bundle structure with
  `find dist/Alien\ Invasion.app -type f`
- **Missing Dependencies**: Check with
  `otool -L dist/Alien\ Invasion.app/Contents/MacOS/Alien\ Invasion`

## CI/CD

The project uses GitHub Actions to automate building. The workflow triggers
when:

- A new tag with format `v*` is created (example: `v1.0.0`)
- A push to main branch occurs

To create a new version:

1. Update version number in `version_macOS.txt`
2. Create and push a new tag:

```bash
git tag v1.0.0
git push origin v1.0.0
```

The workflow:

- Builds the application
- Creates a GitHub release
- Uploads the compiled artifact
- Runs all tests

## Additional Notes

- Application is optimized for Apple Silicon (arm64)
- Code signing included for distribution
- Retina Display support
- Automatic localization
