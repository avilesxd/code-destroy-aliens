# 🎮 Entity System

## Overview

Alien Invasion uses Pygame’s sprite model rather than an ECS. Entities are
`pygame.sprite.Sprite` subclasses that manage their own update and rendering
behavior, and are grouped for efficient batch updates and collision checks.

## Core Entities

- **Ship** (`src/entities/ship.py`)
- **Alien** (`src/entities/alien.py`)
- **Bullet** (`src/entities/bullet.py`)
- UI sprites such as buttons, hearts, and scoreboards

## Position and Movement

Entities store their position as `float` for smooth movement and sync to `rect`
for rendering:

```python
class Alien(Sprite):
    def __init__(self, ...):
        self.x = float(self.rect.x)

    def update(self) -> None:
        self.x += self.ai_configuration.alien_speed_factor
        self.rect.x = int(self.x)
```

## Sprite Groups

The `Game` object owns sprite groups for fast batch operations:

- `game.aliens` for the fleet
- `game.bullets` for projectiles

Groups support `update()`, `draw()`, and collision helpers.

## Factory Functions

Entity creation is centralized in `src/config/actors/` (for example,
`create_alien()` and `create_fleet()`). Logic should call these factories
instead of instantiating entities directly.

## Bullet Pooling

`Bullet` uses a small object pool to reduce allocation during gameplay. Use
`Bullet.get_bullet()` to retrieve or create bullets and let the class manage
recycling.

## Best Practices

- Keep entity `update()` methods focused on movement/state changes.
- Use factory functions for consistent initialization.
- Store positions as `float` and sync to `rect` each frame.
- Use `resource_path()` for asset loading.

## Next Steps

- Read the [Asset Management Guide](assets.md)
- Check out the [Audio System Guide](audio-system.md)
- Learn about [Performance Optimization](performance.md)
