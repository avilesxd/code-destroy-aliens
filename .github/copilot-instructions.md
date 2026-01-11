# AI Copilot Instructions for Alien Invasion

## Quick Start

**Alien Invasion** is a Space Invaders-style arcade game built in Python with
Pygame. The codebase emphasizes type safety, comprehensive testing, and modular
architecture with clear separation of concerns.

**Key Tech Stack**: Python 3.8+, Pygame 2.5.0+, pytest, mypy for type checking

## 📚 Detailed Documentation

For comprehensive guidance, see these specialized files:

- **[conventions.md](copilot-agents/conventions.md)** - Code standards, type
  safety, formatting rules
- **[architecture.md](copilot-agents/architecture.md)** - System design,
  patterns, data flow
- **[workflows.md](copilot-agents/workflows.md)** - Development, testing,
  release processes
- **[ci-cd.md](copilot-agents/ci-cd.md)** - GitHub Actions, automated testing,
  builds, debugging CI failures
- **[agent-behavior.md](copilot-agents/agent-behavior.md)** - When to ask vs.
  act, quality standards

## Essential Quick Reference

### Core Conventions

- **Package management**: Use `npm run` scripts (handles Python venv
  automatically)
- **Type annotations**: Mandatory on all functions - no `Any` types
- **Asset loading**: Always use `resource_path()` from `src/core/path_utils.py`
- **Entity pattern**: Inherit from `pygame.sprite.Sprite`, store position as
  float (`self.x`)
- **Game object injection**: Logic functions receive `Game` object
- **Entity creation**: Use factory functions in `src/config/actors/`

### Quick Commands

```bash
npm run dev          # Run game
npm run test         # Run tests
npm run verify       # Run all quality checks
npm run lint         # Check code style
npm run typecheck    # Check type annotations
npm run format       # Auto-format code
```

### Architecture Overview

**Layered configuration pattern**:

- `src/config/` - Central hub for game behavior (logic, rendering, controls,
  stats)
- `src/entities/` - Pygame Sprite subclasses (Ship, Alien, Bullet)
- `src/core/` - Core utilities (path_utils for asset loading)
- `src/utils/` - Helpers (number_formatter)

**Data Flow**: Configuration → Logic (modifies Game object) → Rendering
(displays state)

See [architecture.md](copilot-agents/architecture.md) for detailed patterns.

### Quality Checklist (Before Every Commit)

1. `npm run lint` - fix all linting issues
2. `npm run typecheck` - fix all type errors
3. `npm run test` - all tests must pass
4. `npm run format` - auto-format code

**Or run all at once**: `npm run verify`

**Non-negotiable**: No code accepted with type errors, lint violations, or
failing tests.

See [workflows.md](copilot-agents/workflows.md) for release process, CI/CD, and
platform builds.

## Common Patterns

**Asset Loading** (handles bundled + source execution):

```python
from src.core.path_utils import resource_path
icon = pygame.image.load(resource_path("src/assets/icons/icon.png"))
```

**Entity Position** (float precision, int rendering):

```python
self.x = 100.0  # Float for smooth movement
self.rect.x = int(self.x)  # Sync to rect each frame
```

**Game Loop Update Order**:

```
verify_events() → ship.update() → update_bullets() → update_aliens() → update_screen()
```

## Critical Rules

- ❌ Never instantiate entities directly - use factory functions in
  `src/config/actors/`
- ❌ Never hardcode screen dimensions - use
  `game.ai_configuration.screen_width/height`
- ❌ Never bypass high score encryption - use
  `game.statistics.save_high_score()`
- ❌ Never use `Any` types without justification
- ✅ Always use `resource_path()` for asset loading
- ✅ Always use `.copy()` when removing from pygame groups during iteration
- ✅ Always test in headless mode (`SDL_VIDEODRIVER=dummy` set in conftest.py)
- ✅ Always add/update tests when changing behavior

## Agent Behavior

### When to Ask vs. Act

- **Execute directly**: Simple tasks ("add bullet color", "fix typo")
- **Confirm first**: Complex changes ("refactor collision", "new game mode")
- **Ask questions**: Unclear requirements (never assume)

### Before Claiming Complete

1. ✅ Read relevant files to understand context
2. ✅ Check dependencies with `list_code_usages` if modifying shared code
3. ✅ Run `npm run verify` - all checks must pass
4. ✅ Update tests (even if not explicitly requested)

See [agent-behavior.md](copilot-agents/agent-behavior.md) for complete
guidelines guidelines
