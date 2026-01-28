# ⚙️ Configuration Guide

## Overview

Alien Invasion stores runtime settings in `Configuration` at
`src/config/configuration.py`. These values are read when the game starts and
are used across logic, rendering, and entities. After changing settings, restart
the game to apply them.

## Key Settings

### Display and Background

- `screen_width` / `screen_height`: Set automatically from the current display
  resolution.
- `use_gradient_background`: Enables the gradient background.
- `gradient_top_color` / `gradient_bottom_color`: Gradient colors.
- `use_stars`, `star_count`, `star_color`: Star field configuration.
- `bg_color`: Fallback background when gradients are disabled.

### Debug

- `show_fps`: Toggle the FPS counter.

### Ship

- `ship_count`: Number of lives.
- `ship_speed_factor`: Movement speed (dynamic).

### Bullets

- `bullet_width`, `bullet_height`, `bullet_color`
- `bullets_allowed`: Max simultaneous bullets.
- `bullets_speed_factor`: Bullet speed (dynamic).

### Aliens

- `alien_speed_factor`: Alien speed (dynamic).
- `fleet_drop_speed`: Vertical step when fleet changes direction.
- `fleet_direction`: 1 (right) or -1 (left).
- `alien_points`: Score per alien (dynamic).
- `acceleration_scale`, `score_scale`: Difficulty scaling per level.

## Dynamic Configuration

Dynamic values are reset with `initialize_dynamic_configurations()` and scaled
on level-up with `boost_speed()`. This is how the game increases difficulty over
time.

## Editing Settings

Update values directly in `Configuration.__init__` to customize defaults:

```python
class Configuration:
        def __init__(self) -> None:
                self.use_gradient_background = True
                self.star_count = 150
                self.ship_count = 3
                self.bullets_allowed = 4
```

## Best Practices

1. **Avoid hard-coded values**
    - Use configuration attributes instead of fixed sizes or speeds.

2. **Keep changes versioned**
    - Track configuration changes in git for easy rollback.

3. **Validate gameplay feel**
    - Test changes at multiple resolutions and difficulty levels.

## Troubleshooting

If you encounter issues after changing settings:

1. Reset values in `Configuration` to defaults
2. Check the [Troubleshooting Guide](./reference/troubleshooting/README.md)
3. Open an [issue](https://github.com/avilesxd/code-destroy-aliens/issues)

## Next Steps

- Read the [Quick Start Guide](quick-start.md) to start playing
- Check out the [Game Guide](../gameplay/basics.md) to learn more about gameplay
- Explore the [Development Guide](../development/core-concepts.md) for advanced
  configuration
