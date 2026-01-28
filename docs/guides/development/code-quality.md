# 📝 Code Quality Guide

## Overview

This guide summarizes the quality standards enforced in the Alien Invasion
codebase. The tooling and rules are strict by design to keep the project
maintainable and safe to evolve.

## Formatting and Linting

- **black** and **isort** handle formatting
- **flake8** enforces style rules
- **Line length**: 125 characters

Use the npm scripts:

| Script                 | Purpose                                  |
| ---------------------- | ---------------------------------------- |
| `npm run format`       | Format Python code with black and isort  |
| `npm run format:check` | Check formatting without modifying files |
| `npm run lint`         | Run flake8                               |

## Type Safety

Type annotations are mandatory for all functions. The project runs `mypy` in
strict mode and rejects untyped definitions.

```python
def update_bullets(game: Game) -> None:
    """Update bullet positions and resolve collisions."""
    game.bullets.update()
```

Use explicit types instead of `Any` wherever possible.

Run type checks with:

```bash
npm run typecheck
```

## Documentation Standards

Docstrings are required for:

- Classes
- Public methods
- Complex functions

Example:

```python
class Ship(Sprite):
    """Represents the player's ship.

    Handles movement, rendering, and shoot actions.
    """
```

## Testing Standards

Tests use `pytest` and run in headless mode. New behavior requires new or
updated tests.

```bash
npm run test
```

## Review Checklist

- [ ] Code formatted and linted
- [ ] All functions have type hints
- [ ] Tests updated and passing
- [ ] Public APIs documented
- [ ] No debug prints or dead code

## Next Steps

- Read the [Architecture Guide](architecture.md)
- Check out the [Performance Guide](performance.md)
- Learn about [Testing](../testing/README.md)
