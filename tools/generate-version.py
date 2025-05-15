VERSION = "1.2.0"

macos_path = "versions/macos.txt"
windows_path = "versions/windows.txt"

windows_template = f"""# UTF-8 encoded

VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({VERSION.replace('.', ', ')}, 0),
    prodvers=({VERSION.replace('.', ', ')}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo([
      StringTable(
        '040904b0',
        [
          StringStruct('CompanyName', 'Code Wave Innovation'),
          StringStruct('FileDescription', 'Space Invader 2D Game'),
          StringStruct('FileVersion', '{VERSION}'),
          StringStruct('InternalName', 'Alien-Invasion'),
          StringStruct('OriginalFilename', 'Aliens Invasion.exe'),
          StringStruct('ProductName', 'Aliens Invasion'),
          StringStruct('ProductVersion', '{VERSION}'),
          StringStruct('LegalCopyright', '© 2025 Ignacio Avilés')
        ])
      ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"""

# Save macOS version
with open(macos_path, "w") as f:
    f.write(VERSION)

# Save Windows file
with open(windows_path, "w", encoding="utf-8") as f:
    f.write(windows_template)

print(f"✔ Version updated to {VERSION} in:")
print(f" - {macos_path}")
print(f" - {windows_path}")
