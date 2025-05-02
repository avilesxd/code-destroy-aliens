# Windows Build Guide

This guide explains how to build Alien Invasion for Windows.

## Requirements

- Windows 10 or higher
- Python 3.13 or higher
- PyInstaller (for compilation)
- Pygame

## Installing Dependencies

1. Make sure you have Python 3.13 or higher installed:
```bash
python --version
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller
```

## Building

### Development Mode

For quick development and testing, use development mode:

```bash
python -m PyInstaller --name "Alien Invasion" --windowed --add-data "src/assets;assets" main.py
```

The compiled application will be found in `dist/Alien Invasion`. This mode is faster for development but requires the source code to be present.

### Production Mode

To create a standalone application:

```bash
python -m PyInstaller --name "Alien Invasion" --windowed --onefile --add-data "src/assets;assets" --icon "src/assets/icons/icon.ico" main.py
```

The compiled application will be found in `dist/Alien Invasion.exe`. This version includes all necessary dependencies and resources.

## Bundle Structure

The generated executable contains:

- Main executable
- Resources (images, sounds, etc.)
- Python runtime
- All necessary dependencies

## Verification

To verify that the application compiled correctly:

```bash
.\dist\Alien Invasion\Alien Invasion.exe
```

## Troubleshooting

### Launch Error
If you encounter a "Launch Error":
1. Verify all dependencies are installed
2. Ensure resources are in the correct locations
3. Check Windows Event Viewer for error logs
4. Run the application from command line to see error messages

### Common Issues
- **Missing DLLs**: Install Visual C++ Redistributable
- **Resources Not Found**: Check bundle structure with `dir /s dist\Alien Invasion`
- **Permission Issues**: Run as administrator if needed
- **Antivirus Blocking**: Add exception for the executable

## CI/CD

The project uses GitHub Actions to automate building. The workflow triggers when:
- A new tag with format `v*` is created (example: `v1.0.0`)
- A push to main branch occurs

To create a new version:

1. Update version number in `version_windows.txt`
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

- Application is optimized for Windows 10/11
- Includes Windows-specific optimizations
- Supports high DPI displays
- Automatic localization
- Windows taskbar integration
- Windows notification support

## Windows-Specific Features

### High DPI Support
The application automatically handles high DPI displays and scaling.

### Windows Integration
- Taskbar progress indicators
- Jump lists
- Windows notifications
- File associations

### Performance Optimizations
- DirectX acceleration when available
- Hardware acceleration for graphics
- Optimized for Windows memory management

### Security
- Windows Defender compatible
- Code signing support
- UAC (User Account Control) aware
- Windows security best practices

## Distribution

### Creating an Installer
You can create a Windows installer using tools like:
- Inno Setup
- NSIS
- WiX Toolset

Example Inno Setup script:
```inno
[Setup]
AppName=Alien Invasion
AppVersion=1.0.0
DefaultDirName={pf}\Alien Invasion
DefaultGroupName=Alien Invasion

[Files]
Source: "dist\Alien Invasion\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\Alien Invasion"; Filename: "{app}\Alien Invasion.exe"
Name: "{commondesktop}\Alien Invasion"; Filename: "{app}\Alien Invasion.exe"
```

### Windows Store
The application can be packaged for the Microsoft Store using:
- MSIX packaging
- Windows App Certification Kit
- Partner Center submission 