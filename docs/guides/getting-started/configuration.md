# ⚙️ Configuration Guide

## Game Settings

Alien Invasion can be customized through various configuration options. These
settings can be modified in the `src/config/configuration.py` file.

### Display Settings

```python
# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Frames per second
FPS = 60

# Fullscreen mode
FULLSCREEN = False
```

### Gameplay Settings

```python
# Ship settings
SHIP_SPEED = 5
SHIP_LIVES = 3

# Bullet settings
BULLET_SPEED = 10
BULLET_WIDTH = 3
BULLET_HEIGHT = 15
BULLET_COLOR = (255, 255, 255)

# Alien settings
ALIEN_SPEED = 1
ALIEN_DROP_SPEED = 10
ALIEN_POINTS = 50
```

### Audio Settings

```python
# Volume levels (0.0 to 1.0)
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.7

# Enable/disable audio
MUSIC_ENABLED = True
SFX_ENABLED = True
```

## Configuration Methods

### 1. In-Game Settings

You can modify some settings through the game's options menu:

1. Access the **Options** menu from the main menu
2. Select **Settings**
3. Adjust the following:
    - Display resolution
    - Fullscreen mode
    - Music volume
    - Sound effects volume
    - Language

### 2. Configuration File

For advanced settings, edit the configuration file:

1. Navigate to `src/config/configuration.py`
2. Modify the desired settings
3. Save the file
4. Restart the game

### 3. Command Line Arguments

Some settings can be modified through command line arguments:

```bash
# Run in fullscreen mode
python main.py --fullscreen

# Set custom resolution
python main.py --width 1920 --height 1080

# Disable audio
python main.py --no-audio
```

## Best Practices

1. **Backup Configuration**

    - Always backup your configuration file before making changes
    - Use version control to track configuration changes

2. **Performance Considerations**

    - Higher resolutions may impact performance
    - Consider your system's capabilities when adjusting settings

3. **Testing Changes**
    - Test configuration changes in a controlled environment
    - Verify that changes don't introduce new issues

## Troubleshooting

If you encounter issues after changing settings:

1. Reset to default settings
2. Check the [Troubleshooting Guide](./reference/troubleshooting/README.md)
3. Open an [issue](https://github.com/avilesxd/code-destroy-aliens/issues)

## Next Steps

- Read the [Quick Start Guide](quick-start.md) to start playing
- Check out the [Game Guide](../gameplay/basics.md) to learn more about gameplay
- Explore the [Development Guide](../development/core-concepts.md) for advanced
  configuration
