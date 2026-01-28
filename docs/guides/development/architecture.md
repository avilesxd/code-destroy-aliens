# 🏗️ Game Architecture

## Overview

Alien Invasion follows a layered, configuration-first architecture. The `Game`
object is the central hub, and gameplay behavior is organized by clear
separation of concerns: input, logic, rendering, and configuration.

Key goals:

- **Modularity**: Features are grouped by responsibility
- **Maintainability**: Clear boundaries between logic and rendering
- **Testability**: Logic functions accept a `Game` instance and are easy to
  exercise in isolation
- **Performance**: Uses sprite groups and efficient collision checks

## Layered Configuration Architecture

The project is organized under `src/` with focused layers:

```
src/
├── config/       # Behavior + configuration (logic, rendering, controls)
├── entities/     # Pygame Sprite subclasses (Ship, Alien, Bullet)
├── core/         # Core utilities (path_utils)
└── utils/        # Shared helpers (number_formatter)
```

### Configuration Layer (`src/config/`)

- **configuration.py**: Runtime settings (screen size, speeds, colors)
- **logic/**: Game state updates (movement, collisions, scoring)
- **rendering/**: Display-only logic (drawing to screen)
- **controls/**: Input handling
- **actors/**: Factory functions for entities and fleets
- **statistics/**: Score, level, lives, and high-score persistence
- **music/**: Audio orchestration

### Entity Layer (`src/entities/`)

Entities are `pygame.sprite.Sprite` subclasses. Position is stored as `float`
for smooth movement and synced to an integer rect for rendering.

```python
class Ship(pygame.sprite.Sprite):
    def __init__(self, ...):
        self.x = 100.0
        self.rect.x = int(self.x)

    def update(self) -> None:
        self.x += self.speed
        self.rect.x = int(self.x)
```

## Game Loop Order

The runtime update order is intentional and consistent:

1. `verify_events(game)` → input processing
2. `ship.update()` → player movement
3. `update_bullets(game)` → bullet physics + collisions
4. `update_aliens(game)` → fleet movement + collisions
5. `update_screen(game)` → rendering

This order ensures inputs affect movement before collisions and rendering.

## Asset Loading

All assets are loaded through `resource_path()` so builds work in both source
and bundled executables:

```python
from src.core.path_utils import resource_path

icon_path = resource_path("src/assets/icons/icon.png")
icon = pygame.image.load(icon_path)
```

## State and Statistics

Gameplay state is stored in `game.statistics` and includes:

- `game_active`, `game_paused`, `game_over`
- `score`, `level`, `ships_remaining`
- `high_score` with encrypted persistence

This avoids duplicated global state and keeps game flow consistent.

## Testing Strategy

Logic functions accept a `Game` object, making unit tests straightforward. The
test suite uses a headless Pygame setup and a `MockGame` fixture.

## Next Steps

- Learn about the [Entity System](entity-system.md)
- Explore the [Audio System](audio-system.md)
- Read about [Testing](../testing/README.md)
