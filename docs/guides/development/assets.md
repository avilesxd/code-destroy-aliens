# 🎨 Asset Management

## Overview

Alien Invasion loads all assets from `src/assets/` and uses `resource_path()` so
assets work both in source mode and bundled builds.

## Asset Layout

```
src/assets/
├── icons/
├── images/
├── music/
├── sounds/
└── translations/
```

## Loading Assets

Always use `resource_path()` to resolve file locations:

```python
from src.core.path_utils import resource_path

ship_image = pygame.image.load(resource_path("src/assets/images/ship.png"))
```

This avoids path issues when running packaged builds.

## Scaling for Resolution

Entities scale assets based on the current screen resolution. The ship, alien,
and bullet sizes are scaled from a 1280×720 baseline using a `scale_factor`. If
you add new sprites, follow the same pattern for consistent visuals.

## Best Practices

- Keep filenames descriptive and consistent.
- Store new images under `src/assets/images` and new audio under
  `src/assets/sounds` or `src/assets/music`.
- Use `resource_path()` for every asset load.

## Next Steps

- Read the [Audio System Guide](audio-system.md)
- Check out the [Entity System Guide](entity-system.md)
- Learn about [Performance Optimization](performance.md)
