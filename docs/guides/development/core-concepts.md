# 🧠 Core Concepts

## Overview

Alien Invasion uses a layered architecture centered around the `Game` object.
Behavior is grouped into clear modules for configuration, logic, rendering, and
entities. This keeps the game loop readable and the codebase easy to extend.

## The `Game` Object

`Game` is the hub that owns shared state:

- `ai_configuration`: runtime settings
- `statistics`: score, lives, level, and game state
- `music`: audio manager
- sprite groups: `aliens`, `bullets`
- UI helpers: `scoreboard`, `controls_screen`, `play_button`

Most logic functions take a `Game` instance instead of using globals.

## Layered Modules

```
src/
├── config/       # Behavior + configuration
├── entities/     # Pygame Sprite subclasses
├── core/         # Shared utilities
└── utils/        # Small helpers
```

Key layers:

- **config/logic**: state updates and collisions
- **config/rendering**: drawing and visual effects
- **config/controls**: input handling
- **config/actors**: factory functions for entity creation

## Sprite-Based Entities

Entities inherit from `pygame.sprite.Sprite` and store position as `float` for
smooth movement while syncing to `rect` for rendering.

```python
class Alien(Sprite):
    def __init__(self, ...):
        self.x = float(self.rect.x)

    def update(self) -> None:
        self.x += self.ai_configuration.alien_speed_factor
        self.rect.x = int(self.x)
```

## Factory Functions

Entity creation is centralized in `src/config/actors/` to keep initialization
consistent. Use these factories instead of direct instantiation in logic.

## Game Loop Order

The update order is deliberate:

1. Input handling
2. Ship update
3. Bullet update + collisions
4. Alien update + collisions
5. Rendering

This ensures player actions affect movement before collisions and drawing.

## Asset Loading

All assets are loaded with `resource_path()` to support both source and bundled
executables.

```python
from src.core.path_utils import resource_path

image = pygame.image.load(resource_path("src/assets/images/ship.png"))
```

## Game State and Statistics

The `Statistics` module owns game state, including `game_active`, `game_paused`,
`game_over`, score, and encrypted high score persistence. This keeps state
consistent and avoids duplicated logic.

## Testing Strategy

Logic functions are designed to be testable with a `MockGame` fixture. Tests run
in headless mode and focus on deterministic state changes.

## Next Steps

- Read about [Game Architecture](architecture.md)
- Learn about the [Entity System](entity-system.md)
- Explore the [Audio System](audio-system.md)
