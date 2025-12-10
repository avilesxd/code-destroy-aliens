# AI Copilot Instructions for Alien Invasion

## Project Overview

**Alien Invasion** is a Space Invaders-style arcade game built in Python with
Pygame. The codebase emphasizes type safety, comprehensive testing, and modular
architecture with clear separation of concerns.

**Key Tech Stack**: Python 3.8+, Pygame 2.5.0+, pytest, mypy for type checking

## Architecture Patterns

### Layered Configuration Architecture

The game uses `src/config/` as a central hub for game behavior. Each
subdirectory contains specialized logic:

- `configuration.py`: All game settings (screen size, speeds, colors)
  initialized at runtime from screen info
- `actors/`: Entity creation and fleet management (`create_fleet()`,
  `ship_hit()`, `check_aliens_bottom()`)
- `logic/`: Pure game logic functions (`update_aliens()`, `update_bullets()`,
  `update_spatial_grid()`) that take the Game object and modify sprites
- `rendering/`: Display logic (`update_screen()`, `update_stars()`) - separates
  rendering from state
- `controls/`: Input handling (`verify_events()`)
- `statistics/`: Game state (active, paused, score tracking, high score
  persistence with encryption)
- `music/`: Audio effects and background music

**Pattern**: Configuration values → Logic functions receive Game object →
Rendering reads from Game object. Avoid direct pygame calls in logic.

### Pygame Sprite-Based Entity System

Entities (`Ship`, `Alien`, `Bullet`) inherit from `pygame.sprite.Sprite` and use
groups for batch operations:

```python
# In game.py
self.bullets: Group = Group()
self.aliens: Group = Group()

# In logic - batch update via group
game.bullets.update()  # Calls update() on all sprites
game.aliens.update()   # Calls update() on all sprites

# Collision detection using sprite groups
if pygame.sprite.spritecollideany(game.ship, game.aliens):
    ship_hit(game)  # Handle collision
```

**Key pattern**: Entities store position in `self.x` (float) and sync to
`self.rect.x` (int) for screen coordinates. The `update()` method modifies
position; individual `blitme()` in rendering or group operations handle display.
Use `pygame.sprite.spritecollideany()` for collision detection.

### Type Safety & Validation

Strict mypy configuration enforces type annotations throughout
(`pyproject.toml`):

- All function parameters and returns must be typed
- No `Any` types unless explicitly unavoidable
- Decorators must be typed

Always add type hints to new code: `def move_ship(dx: float) -> None:`

## Critical Workflows

### Running the Game

```bash
npm run dev          # Runs: python main.py via virtual environment
npm run build:windows  # Creates .exe with pyinstaller
npm run build:macos    # Creates .app with py2app
```

### Testing & Quality

```bash
npm run test              # pytest with pytest.ini defaults
npm run test:coverage     # pytest --cov=src tests/
npm run typecheck         # mypy with strict config
npm run lint             # flake8 (125 char line limit)
npm run format           # black + isort (enforced on CI)
npm run verify           # Runs all checks above sequentially
```

**Test Structure**: `tests/` mirrors `src/` layout. Use `MockGame` fixture from
`conftest.py` to avoid pygame display initialization in tests. Headless mode set
via `SDL_VIDEODRIVER=dummy`.

### Code Quality Standards

- **Line length**: 125 characters (black + isort config in `pyproject.toml`)
- **Pre-commit hooks**: Automatically run via Husky + lint-staged before commits
    - Python files: `black`, `isort`, `flake8`
    - JS/JSON/MD/YML: `prettier`
- **Type checking**: mypy runs on CI; must pass for merge
- **Documentation**: Docstrings required for classes and public methods (see
  `Ship` class for style)

### Git Workflow & Commit Standards

**Pre-commit hooks** (via Husky):

- `.husky/pre-commit`: Runs `npx lint-staged` to validate staged files
    - Python files: applies `black`, `isort`, `flake8`
    - Other files: applies `prettier`
- Commits are rejected if formatters/linters fail

**Commit messages** (via commitlint):

- Must follow Conventional Commits format: `<type>: <subject>` (scope NOT
  supported)
- Valid types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`,
  `perf`, `ci`, `build`, `revert`, `wip`
- **All commits MUST be in English** (rule `'subject-lang'` rejects non-English
  characters)
- Scopes are REJECTED by rule `'scope-empty': [2, 'always']`
- Subject line max 150 chars, must be lowercase, no period at end
- Body/footer max 250 chars per line
- Examples:
    - `feat: add shield ability to player ship` ✅
    - `fix: prevent aliens from overlapping bullets` ✅
    - `docs: update game controls documentation` ✅
    - `feat(entities): add shield to ship` ❌ (scope not supported)
    - `feat: agregar escudo al barco` ❌ (Spanish - not English)

**Full verification workflow** (run before pushing):

```bash
npm run verify  # Runs: format → prettier → lint → typecheck → test
```

All checks must pass before CI will accept a PR.

## Common Development Tasks

### Adding a New Game Entity

1. Create class inheriting `pygame.sprite.Sprite` in `src/entities/`
2. Implement `__init__()`, `update()`, `blitme()` (or add to group with
   `.draw()`)
3. Add type hints to all methods
4. Load assets using `resource_path()` from `src/core/path_utils.py` (handles
   bundled/source execution)
5. Create test file `tests/entities/test_*.py` using `MockGame` fixture
6. Update `Game.__init__()` to instantiate and add to appropriate group

**Example pattern** (from `Ship`, `Alien`): Position stored as float (`self.x`),
sync to rect each frame for pixel-perfect rendering.

### Modifying Game Logic

1. Core game loop in `src/game.py:run()` calls functions from
   `src/config/logic/game_logic.py`
2. Logic functions receive `Game` object, modify sprite groups/statistics
3. Keep rendering separate: update sprite positions in logic, render in
   `config/rendering/`
4. Use `src/config/actors/` for entity creation (e.g., `create_fleet()`,
   `create_alien()`)
5. Test logic functions with `MockGame` — they take game object and produce side
   effects

**Example patterns**:

- `update_aliens()`: Checks fleet edges with `check_fleet_edges()`, calls
  `game.aliens.update()`, detects ship collisions with
  `pygame.sprite.spritecollideany(game.ship, game.aliens)`
- `update_bullets()`: Calls `game.bullets.update()`, removes inactive bullets,
  checks bullet-alien collisions via spatial grid

### Handling Asset Loading

Use `resource_path()` from `src/core/path_utils.py` for all image/sound files:

```python
icon_path = resource_path("src/assets/icons/icon.png")
icon = pygame.image.load(icon_path)
```

This function handles bundled executables (py2app/pyinstaller) and source
execution correctly.

## Platform-Specific Considerations

- **Windows builds**: Use `build:windows` task (pyinstaller, requires
  .version-file)
- **macOS builds**: Use `build:macos` task (py2app in `setup.py`, requires
  signing setup)
- **Linux**: No official build; runs from source
- **Tests with platform markers**: Use `@pytest.mark.windows` or
  `@pytest.mark.macos` for OS-specific tests (see `pytest.ini`)

## Cross-Cutting Concerns

### Localization

`src/config/language/language.py` provides `get_text()` for UI strings. Check
language files in `src/assets/translations/` before hardcoding text.

### Configuration Scaling

`Configuration` class scales game assets based on runtime screen resolution
using `scale_factor`. New visual entities should apply this factor when
loading/scaling images (see `Ship` and `Alien` for pattern).

### Statistics & Game State

`src/config/statistics/statistics.py` manages game state with:

- `game_active`, `game_paused`, `game_over`: Game flow control
- `score`, `level`, `ships_remaining`: Game progress
- `high_score`: Persisted to disk with Fernet encryption (key derived from
  `_PASSWORD` + `_SALT`) to prevent casual tampering

Access via `game.statistics.<attribute>`. Never duplicate state. High scores are
automatically encrypted when saved via `save_high_score()`.

## File Organization Rules

- `src/config/`: Configuration and behavioral functions (pure or Game-object
  modifying)
- `src/entities/`: Pygame Sprite subclasses with visual/interactive behavior
- `src/core/`: Utilities (`path_utils.py` for assets, `__init__.py` for package
  setup)
- `src/utils/`: Helpers (`number_formatter.py` for UI text)
- `tests/`: Mirror `src/` structure; use `conftest.py` fixtures; run with
  `npm run test`

## Notes for AI Agents

- **Before modifying logic**: Review `src/config/logic/game_logic.py` to
  understand update order: `verify_events()` → `ship.update()` →
  `update_bullets()` → `update_aliens()` → `update_screen()`
- **Entity creation pattern**: Use functions in `src/config/actors/` (e.g.,
  `create_fleet()`, `create_alien()`). Never instantiate entities directly in
  logic
- **Collision detection**: Use `pygame.sprite.spritecollideany()` for ship/alien
  collisions, spatial grid in `update_spatial_grid()` for bullet/alien
  optimization
- **Type errors block CI**: Always run `npm run typecheck` locally before
  pushing
- **Screen dimensions are dynamic**: Don't hardcode screen sizes; use
  `game.ai_configuration.screen_width/height` or `screen.get_rect()`
- **Pygame groups are mutated during iteration**: Use `game.aliens.copy()` if
  removing during iteration (already done in `update_bullets()`)
- **Test pygame code in headless mode**: conftest.py sets
  `SDL_VIDEODRIVER=dummy` so tests run without display
- **High score encryption**: Stats module automatically handles encryption;
  never read/write high score directly to disk outside `Statistics` class
- **Docs vs. code discrepancy**: Documentation in `docs/` describes aspirational
  ECS architecture (Entity, Component, System classes) not yet implemented.
  Current codebase uses simpler Pygame Sprite-based pattern with direct Game
  object injection
