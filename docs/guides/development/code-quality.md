# 📝 Code Quality Guide

## Overview

This guide outlines the code quality standards and practices for Alien Invasion.

## Code Style

### 1. Python Style Guide

Follow PEP 8 with these additional rules:

```python
# Use type hints
def move_ship(x: int, y: int) -> None:
    """Move the ship to specified coordinates."""
    ship.position = (x, y)

# Use dataclasses for data structures
@dataclass
class Position:
    x: float
    y: float

# Use enums for constants
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
```

### 2. Documentation

```python
def fire_bullet(position: Position, direction: Vector2) -> Bullet:
    """Fire a bullet from the specified position.
    
    Args:
        position: Starting position of the bullet
        direction: Direction vector for bullet movement
        
    Returns:
        Bullet: The created bullet entity
        
    Raises:
        ValueError: If position is invalid
    """
    # Implementation
```

## Code Organization

### 1. Directory Structure

```
src/
├── config/        # Configuration
├── core/          # Core systems
├── entities/      # Game entities
├── systems/       # Game systems
└── utils/         # Utilities
```

### 2. Module Organization

```python
# module.py
"""Module docstring."""

# Imports
import pygame
from typing import List, Optional

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Classes
class Game:
    """Game class docstring."""
    
    def __init__(self):
        """Initialize game."""
        pass

# Functions
def helper_function():
    """Helper function docstring."""
    pass
```

## Best Practices

### 1. SOLID Principles

```python
# Single Responsibility
class RenderSystem:
    def render(self, screen, entities):
        pass

# Open/Closed
class Weapon(ABC):
    @abstractmethod
    def fire(self):
        pass

class LaserWeapon(Weapon):
    def fire(self):
        pass

# Liskov Substitution
class Entity:
    def update(self):
        pass

class Ship(Entity):
    def update(self):
        pass

# Interface Segregation
class Movable(ABC):
    @abstractmethod
    def move(self):
        pass

class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass

# Dependency Inversion
class Game:
    def __init__(self, renderer: Renderer):
        self.renderer = renderer
```

### 2. Design Patterns

```python
# Observer Pattern
class EventManager:
    def __init__(self):
        self.listeners = defaultdict(list)

    def subscribe(self, event_type, listener):
        self.listeners[event_type].append(listener)

# Factory Pattern
class EntityFactory:
    def create_ship(self, position):
        return Ship(position)

# Strategy Pattern
class MovementStrategy(ABC):
    @abstractmethod
    def move(self, entity):
        pass
```

## Code Quality Tools

### 1. Static Analysis

```yaml
# .flake8
[flake8]
max-line-length = 88
extend-ignore = E203
exclude = .git,__pycache__,build,dist
```

### 2. Type Checking

```python
# mypy.ini
[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

### 3. Formatting

```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'
```

## Testing Standards

### 1. Unit Tests

```python
def test_ship_movement():
    ship = Ship()
    ship.move_right()
    assert ship.position.x == 5

def test_collision_detection():
    bullet = Bullet()
    alien = Alien()
    assert not check_collision(bullet, alien)
```

### 2. Integration Tests

```python
def test_game_loop():
    game = Game()
    game.initialize()
    game.update(1.0)
    assert game.state == GameState.PLAYING
```

## Code Review Checklist

### 1. General

- [ ] Follows style guide
- [ ] Has proper documentation
- [ ] Uses type hints
- [ ] No commented-out code
- [ ] No debug prints

### 2. Functionality

- [ ] Works as intended
- [ ] Handles edge cases
- [ ] No side effects
- [ ] Proper error handling

### 3. Performance

- [ ] Efficient algorithms
- [ ] No memory leaks
- [ ] Reasonable complexity
- [ ] Proper resource management

## Common Issues

### 1. Code Smells

- Long functions
- Duplicate code
- Magic numbers
- Complex conditionals

### 2. Anti-patterns

- God objects
- Spaghetti code
- Premature optimization
- Over-engineering

## Tools and Resources

### 1. Development Tools

- Black: Code formatting
- isort: Import sorting
- flake8: Linting
- mypy: Type checking
- pytest: Testing

### 2. IDE Configuration

- VS Code settings
- PyCharm settings
- Sublime Text settings

## Next Steps

- Read the [Architecture Guide](architecture.md)
- Check out the [Performance Guide](performance.md)
- Learn about [Testing](../testing/README.md)
