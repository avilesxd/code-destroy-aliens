# Architecture & Code Organization

## Big Picture

**Alien Invasion** uses a **layered configuration architecture** with strict
separation between logic, rendering, and state management. The `Game` object is
the central hub that gets injected into all behavioral functions.

## Directory Structure

```
src/
├── config/           # Game behavior and configuration
│   ├── configuration.py    # Runtime settings (screen, speeds, colors)
│   ├── actors/             # Entity factories (create_fleet, ship_hit)
│   ├── logic/              # Pure game logic (update_bullets, update_aliens)
│   ├── rendering/          # Display logic (update_screen, update_stars)
│   ├── controls/           # Input handling (verify_events)
│   ├── statistics/         # Game state & score persistence
│   └── music/              # Audio system
├── entities/         # Pygame Sprite subclasses
├── core/             # Core utilities (path_utils, package setup)
└── utils/            # Helpers (number_formatter)
```

## Code Organization Principles

### Single Responsibility

Each module/class handles one concern:

- `game_logic.py` → game state updates
- `game_rendering.py` → display only
- `game_actors.py` → entity creation

### Composition Over Complexity

Prefer small, composable functions over large monolithic ones:

```python
# Good: Small, focused functions
def update_aliens(game: Game) -> None:
    check_fleet_edges(game)
    game.aliens.update()
    handle_collisions(game)

# Bad: One huge function doing everything
def update_game(game: Game) -> None:
    # 200 lines of mixed logic
```

### Avoid Premature Abstraction

Don't create abstractions until the pattern is clear from actual usage. If you
only have one use case, keep it simple.

### Clear Separation

Shared code lives in well-defined directories: `config/`, `entities/`, `core/`,
`utils/`

## Layered Configuration Architecture

**Data Flow Pattern**:

```
Configuration values → Logic functions receive Game object → Rendering reads from Game object
```

### Configuration Layer (`src/config/`)

- `configuration.py`: All game settings (screen size, speeds, colors)
  initialized at runtime from screen info
- `actors/`: Entity creation and fleet management
- `logic/`: Pure game logic functions that take the Game object and modify
  sprites
- `rendering/`: Display logic - separates rendering from state
- `controls/`: Input handling
- `statistics/`: Game state (active, paused, score tracking, encrypted high
  score persistence)
- `music/`: Audio effects and background music

**Critical Rule**: Avoid direct pygame calls in logic. Logic modifies state,
rendering displays it.

## Pygame Sprite-Based Entity System

Entities (`Ship`, `Alien`, `Bullet`) inherit from `pygame.sprite.Sprite` and use
groups for batch operations:

```python
# In game.py - sprite groups
self.bullets: Group = Group()
self.aliens: Group = Group()

# In logic - batch update via group
game.bullets.update()  # Calls update() on all sprites
game.aliens.update()   # Calls update() on all sprites

# Collision detection using sprite groups
if pygame.sprite.spritecollideany(game.ship, game.aliens):
    ship_hit(game)  # Handle collision
```

### Entity Position Pattern

**Key pattern**: Entities store position as **float** (`self.x`) and sync to
**int** (`self.rect.x`) for screen coordinates:

```python
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        self.x = 100.0  # Float for precise movement
        self.rect.x = int(self.x)  # Int for rendering

    def update(self):
        self.x += self.speed_x  # Smooth movement
        self.rect.x = int(self.x)  # Sync to rect
```

The `update()` method modifies position; individual `blitme()` in rendering or
group operations handle display.

## Python Type Safety Rules

### Mandatory Type Annotations

All function parameters and returns must be typed:

```python
# Good
def update_bullets(game: Game) -> None:
    game.bullets.update()

# Bad
def update_bullets(game):
    game.bullets.update()
```

### Avoid `Any` and `unknown`

Use specific types or `Union` for multiple types:

```python
# Good
from typing import Optional, Union
def get_score(player: Optional[str]) -> Union[int, None]:
    ...

# Bad
def get_score(player: Any) -> Any:
    ...
```

### Prefer Type Inference

Let mypy infer types when obvious, but annotate function signatures explicitly:

```python
# Inference is fine for local variables
alien_count = len(game.aliens)  # mypy infers int

# But always annotate functions
def count_aliens(game: Game) -> int:
    return len(game.aliens)
```

### Unclear Types = Stop and Clarify

If types aren't clear, pause and discuss before continuing. Don't use `Any` as a
placeholder.

### Generic Types

Use proper generics from `typing` module:

```python
from typing import List, Dict, Optional
from pygame.sprite import Group

def filter_active_bullets(bullets: Group) -> List[Bullet]:
    ...

def get_config() -> Dict[str, Union[int, str]]:
    ...
```

## Strict mypy Configuration

`pyproject.toml` enforces strict type checking:

- All function parameters and returns must be typed
- No `Any` types unless explicitly unavoidable
- Decorators must be typed
- Untyped definitions are rejected

Always add type hints to new code: `def move_ship(dx: float) -> None:`

## Cross-Cutting Concerns

### Asset Loading Pattern

**Always** use `resource_path()` from `src/core/path_utils.py` for all
image/sound files:

```python
from src.core.path_utils import resource_path

# Handles both bundled executables (py2app/pyinstaller) and source execution
icon_path = resource_path("src/assets/icons/icon.png")
icon = pygame.image.load(icon_path)
```

### Configuration Scaling

`Configuration` class scales game assets based on runtime screen resolution
using `scale_factor`. New visual entities should apply this factor when
loading/scaling images (see `Ship` and `Alien` for pattern).

### Statistics & Game State

`src/config/statistics/statistics.py` manages game state with:

- `game_active`, `game_paused`, `game_over`: Game flow control
- `score`, `level`, `ships_remaining`: Game progress
- `high_score`: Persisted to disk with **Fernet encryption** (key derived from
  `_PASSWORD` + `_SALT`) to prevent casual tampering

**Access pattern**: `game.statistics.<attribute>`. Never duplicate state. High
scores are automatically encrypted when saved via `save_high_score()`.

### Localization

`src/config/language/language.py` provides `get_text()` for UI strings. Check
language files in `src/assets/translations/` before hardcoding text.

## Important Notes

### Game Loop Update Order

Review `src/config/logic/game_logic.py` to understand the critical update order
in `src/game.py:run()`:

```python
verify_events(self)      # 1. Input handling
self.ship.update()       # 2. Ship movement
update_bullets(self)     # 3. Bullet physics & collisions
update_aliens(self)      # 4. Alien movement & collisions
update_screen(self)      # 5. Rendering (last!)
```

### Entity Creation Pattern

Use factory functions in `src/config/actors/` (e.g., `create_fleet()`,
`create_alien()`). **Never instantiate entities directly in logic**.

### Collision Detection

- **Ship/Alien**: `pygame.sprite.spritecollideany(game.ship, game.aliens)`
- **Bullet/Alien**: Spatial grid in `update_spatial_grid()` for optimization

### Screen Dimensions

Don't hardcode screen sizes; use `game.ai_configuration.screen_width/height` or
`screen.get_rect()`

### Pygame Group Iteration

Pygame groups are mutated during iteration. Use `game.aliens.copy()` if removing
during iteration (already done in `update_bullets()`).

### Documentation vs. Code

Documentation in `docs/` describes aspirational ECS architecture (Entity,
Component, System classes) **not yet implemented**. Current codebase uses
simpler Pygame Sprite-based pattern with direct Game object injection.
