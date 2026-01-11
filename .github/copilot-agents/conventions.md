# Code Conventions & Standards

## Core Conventions

### Package Management

- Use `npm` for Node tooling
- Python virtual environment (`env/`) for Python dependencies
- **Never** install Python packages globally
- Use `npm run` scripts which handle venv activation via
  `scripts/run-with-env.js`

### Python Execution

Always use `npm run` scripts:

```bash
npm run dev          # python main.py
npm run test         # pytest
npm run lint         # flake8
npm run typecheck    # mypy
```

**Never** run Python commands directly. The scripts ensure virtual environment
activation.

### Type Annotations

**Mandatory** on all functions - no `Any` types unless unavoidable:

```python
# ✅ Good
def update_bullets(game: Game) -> None:
    game.bullets.update()

# ❌ Bad
def update_bullets(game):
    game.bullets.update()
```

### Asset Loading

**Always** use `resource_path()` from `src/core/path_utils.py` for
images/sounds:

```python
from src.core.path_utils import resource_path

# Handles bundled executables AND source execution
icon_path = resource_path("src/assets/icons/icon.png")
icon = pygame.image.load(icon_path)
```

### Entity Pattern

Entities inherit from `pygame.sprite.Sprite`:

- Store position as **float** (`self.x`, `self.y`)
- Sync to **int** rect for rendering (`self.rect.x = int(self.x)`)
- Update position in `update()` method

```python
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 100.0  # Float for precision

    def update(self):
        self.x += self.speed
        self.rect.x = int(self.x)  # Sync to rect
```

### Game Object Injection

Logic functions receive `Game` object, never access pygame globals directly:

```python
# ✅ Good
def update_aliens(game: Game) -> None:
    game.aliens.update()

# ❌ Bad
def update_aliens():
    ALIENS.update()  # Global variable
```

### Entity Creation

**No direct instantiation**. Use factory functions in `src/config/actors/`:

```python
# ✅ Good
from src.config.actors.game_actors import create_alien
alien = create_alien(game, x, y)

# ❌ Bad
from src.entities.alien import Alien
alien = Alien(game.ai_configuration, game.screen, x, y)
```

## Code Quality Standards

### Line Length

**125 characters** maximum (configured in `pyproject.toml` for black + isort)

### Formatting Tools

- **black**: Code formatter
- **isort**: Import sorter
- **flake8**: Linter (125 char line limit)
- **mypy**: Type checker (strict mode)
- **prettier**: For JS/JSON/MD/YML files

### Pre-commit Hooks (Husky + lint-staged)

Automatically runs before each commit:

- Python files → `black`, `isort`, `flake8`
- Other files → `prettier`

Commits are **rejected** if checks fail.

### Documentation

Docstrings **required** for:

- All classes
- All public methods
- Complex functions

Style example from `Ship` class:

```python
class Ship(pygame.sprite.Sprite):
    """Represents the player's ship.

    Manages ship movement, rendering, and state. The ship can move
    left/right and fire bullets.

    Attributes:
        screen (pygame.Surface): The game screen
        x (float): Horizontal position (float for smooth movement)
        rect (pygame.Rect): Position rectangle for rendering
    """
```

## Type Safety Requirements

### Strict mypy Configuration

`pyproject.toml` enforces:

- `check_untyped_defs = true`
- `disallow_untyped_defs = true`
- `disallow_incomplete_defs = true`
- `disallow_untyped_decorators = true`
- `warn_return_any = true`

### Type Hints Patterns

```python
from typing import Optional, List, Dict, Union
from pygame.sprite import Group

# Simple types
def get_score() -> int:
    return 0

# Optional types
def get_player_name() -> Optional[str]:
    return None

# Collections
def get_aliens() -> List[Alien]:
    return []

# Union types
def get_value() -> Union[int, str]:
    return 42

# Complex types
def process_config() -> Dict[str, Union[int, float, str]]:
    return {}
```

### Generic Types from `typing`

- `List[Type]` for lists
- `Dict[Key, Value]` for dictionaries
- `Optional[Type]` for nullable values
- `Union[Type1, Type2]` for multiple types
- `Tuple[Type1, Type2]` for tuples

## File Organization

### Directory Structure Rules

- `src/config/`: Configuration and behavioral functions (pure or Game-object
  modifying)
- `src/entities/`: Pygame Sprite subclasses with visual/interactive behavior
- `src/core/`: Utilities (`path_utils.py` for assets, `__init__.py` for package
  setup)
- `src/utils/`: Helpers (`number_formatter.py` for UI text)
- `tests/`: Mirror `src/` structure; use `conftest.py` fixtures

### Import Organization (isort)

1. Standard library imports
2. Third-party imports (pygame, pytest, etc.)
3. Local imports (src.\*)

```python
import os
from typing import List

import pygame
from pygame.sprite import Group

from src.config.configuration import Configuration
from src.entities.ship import Ship
```

## Critical Rules

### Screen Dimensions

Don't hardcode screen sizes:

```python
# ✅ Good
width = game.ai_configuration.screen_width
height = game.ai_configuration.screen_height
# or
rect = screen.get_rect()

# ❌ Bad
width = 1200  # Hardcoded
height = 800
```

### Pygame Group Mutation

Groups are mutated during iteration. Use `.copy()` when removing:

```python
# ✅ Good
for bullet in game.bullets.copy():
    if not bullet.active:
        game.bullets.remove(bullet)

# ❌ Bad (can skip elements)
for bullet in game.bullets:
    if not bullet.active:
        game.bullets.remove(bullet)
```

### High Score Security

Stats module handles encryption automatically:

```python
# ✅ Good
game.statistics.high_score = 1000
game.statistics.save_high_score()

# ❌ Bad (bypasses encryption)
with open('high_score.txt', 'w') as f:
    f.write('1000')
```

### Test Environment

Always test Pygame code in headless mode. `conftest.py` sets
`SDL_VIDEODRIVER=dummy`.

## Documenting New Constraints

If introducing a new "always X" or "never Y" rule, **document it** in:

- This file (conventions.md)
- Or the relevant section in other agent files
- Update main copilot-instructions.md with cross-reference
