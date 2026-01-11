# Development Workflows

## Running the Game

```bash
npm run dev          # Runs: python main.py via virtual environment
npm run build:windows  # Creates .exe with pyinstaller
npm run build:macos    # Creates .app with py2app
```

**Important**: Always use `npm run` scripts. They handle virtual environment
activation automatically via `scripts/run-with-env.js`.

## Quality Checks (Before Every Commit)

Run these commands in order:

```bash
# 1. Fix linting issues
npm run lint

# 2. Fix type errors
npm run typecheck

# 3. Verify tests pass
npm run test

# 4. Auto-format code
npm run format
```

Or run all at once:

```bash
npm run verify  # Runs: format → prettier → lint → typecheck → test
```

**Non-Negotiable**: No code is accepted with type errors, lint violations, or
failing tests.

## Testing

### Running Tests

```bash
npm run test              # pytest with pytest.ini defaults
npm run test:coverage     # pytest --cov=src tests/
```

### Test Structure

- `tests/` mirrors `src/` layout
- Use `MockGame` fixture from `conftest.py` to avoid pygame display
  initialization
- Headless mode set via `SDL_VIDEODRIVER=dummy` in conftest
- Platform-specific tests: Use `@pytest.mark.windows` or `@pytest.mark.macos`
  markers (see `pytest.ini`)

### Test Pattern Example

```python
def test_bullet_movement(mock_game):
    """Test bullet moves upward when updated."""
    from src.entities.bullet import Bullet

    bullet = Bullet(mock_game.ai_configuration, mock_game.screen, mock_game.ship)
    initial_y = bullet.y

    bullet.update()

    assert bullet.y < initial_y  # Bullet moved up
```

### Running Specific Tests

```bash
# Run single test file
npm run test tests/entities/test_bullet.py

# Run specific test function
npm run test tests/entities/test_bullet.py::test_bullet_movement

# Run tests matching pattern
npm run test -k "bullet"

# Run with verbose output
npm run test -v

# Run and stop at first failure
npm run test -x
```

### Understanding Test Output

**Test passed**:

```
tests/entities/test_bullet.py::test_bullet_movement PASSED [100%]
```

**Test failed**:

```
tests/entities/test_bullet.py::test_bullet_movement FAILED [100%]
AssertionError: assert 100.0 < 100.0
```

**Common test issues**:

- **AssertionError**: Expected vs actual values don't match
- **AttributeError**: Object doesn't have expected attribute (check mock setup)
- **ImportError**: Module not found (check imports and conftest.py)
- **TypeError**: Type mismatch (check type annotations)

**Important**: Add/update tests when changing behavior, even if not explicitly
requested.

### Test Coverage

View detailed coverage report:

```bash
npm run test:coverage
# Generates HTML report in htmlcov/index.html
```

**Coverage requirements**:

- Aim for 80%+ overall coverage
- 100% coverage for critical paths (game logic, collision detection)
- Lower coverage acceptable for UI code (buttons, rendering)

**Uncovered lines strategy**:

1. Check `htmlcov/index.html` for uncovered lines
2. Add tests for important logic paths
3. Use `# pragma: no cover` sparingly for impossible-to-test code

## Releasing a New Version

### Automated Version Bump Process

```bash
# 1. Bump version (patch/minor/major)
.\scripts\bump-version.ps1 -Type minor

# This automatically:
# - Updates package.json, package-lock.json
# - Updates tools/generate-version.py
# - Generates version files for Windows/macOS
# - Updates website/index.html version and download links
# - Creates new CHANGELOG.md entry with template

# 2. Edit CHANGELOG.md with actual release notes
# Add details under Added, Changed, Fixed, etc.

# 3. Sync changelog to website
python scripts\sync-website-changelog.py

# 4. Commit and tag
git add .
git commit -m "chore: bump version to X.X.X"
git tag -a vX.X.X -m "Release vX.X.X"
git push --tags

# 5. Builds trigger automatically on tag push
# - Windows build (~3-5 min)
# - macOS build (~1-2 min)
# - Release creation (automatic after builds complete)
```

### Version Files

- `package.json`: npm version (source of truth)
- `tools/generate-version.py`: Python VERSION constant
- `versions/windows.txt`: PyInstaller version metadata
- `versions/macos.txt`: py2app version string
- `website/index.html`: Displayed version and download links
- `website/changelog.html`: HTML changelog (synced from CHANGELOG.md)

### CI/CD Pipeline

1. Push tag → triggers `build-windows.yml` and `build-macos.yml`
2. Both builds complete → triggers `release.yml`
3. Release created with .exe and .dmg artifacts
4. Website auto-deploys on main branch push

## Platform-Specific Builds

### Windows

- Use `npm run build:windows` (pyinstaller)
- Requires `.version-file` from `versions/windows.txt`
- Creates standalone `.exe` in `dist/`

### macOS

- Use `npm run build:macos` (py2app)
- Configuration in `setup.py`
- Requires signing setup for distribution
- Creates `.app` bundle in `dist/`

### Linux

- No official build; runs from source
- Users run `npm install && npm run dev`

## Git Workflow

### Pre-commit Hooks (Automated via Husky)

`.husky/pre-commit` runs `npx lint-staged` which:

- **Python files**: Applies `black`, `isort`, `flake8`
- **JS/JSON/MD/YML**: Applies `prettier`

Commits are **rejected** if formatters/linters fail.

### Commit Message Standards (via commitlint)

Must follow Conventional Commits format: `<type>: <subject>`

**Valid types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`,
`perf`, `ci`, `build`, `revert`, `wip`

**Rules**:

- Scopes are **REJECTED** by rule `'scope-empty': [2, 'always']`
- Subject line max 150 chars
- No period at end of subject
- Case-insensitive
- Body/footer max 250 chars per line

**Examples**:

```bash
# ✅ Good
git commit -m "feat: add shield ability to player ship"
git commit -m "fix: prevent aliens from overlapping bullets"
git commit -m "docs: update game controls documentation"

# ❌ Bad
git commit -m "feat(entities): add shield to ship"  # Scope not supported
git commit -m "Add shield."                         # No type prefix
```

## Common Development Tasks

### Adding a New Game Entity

1. Create class inheriting `pygame.sprite.Sprite` in `src/entities/`
2. Implement `__init__()`, `update()`, `blitme()` (or use group `.draw()`)
3. Add type hints to all methods
4. Load assets using `resource_path()` from `src/core/path_utils.py`
5. Create test file `tests/entities/test_*.py` using `MockGame` fixture
6. Update `Game.__init__()` to instantiate and add to appropriate group

**Pattern**: Position stored as float (`self.x`), sync to rect each frame for
pixel-perfect rendering.

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

- `update_aliens()`: Checks fleet edges, calls `game.aliens.update()`, detects
  collisions
- `update_bullets()`: Calls `game.bullets.update()`, removes inactive bullets,
  checks collisions via spatial grid

### Handling Asset Loading

Use `resource_path()` from `src/core/path_utils.py` for all image/sound files:

```python
from src.core.path_utils import resource_path

icon_path = resource_path("src/assets/icons/icon.png")
icon = pygame.image.load(icon_path)
```

This function handles bundled executables (py2app/pyinstaller) and source
execution correctly.

## Debugging Failures

### When Tests Fail Locally

1. **Read the error message**: Don't skip past it
2. **Run the specific test**: `npm run test path/to/test.py::test_name`
3. **Use verbose mode**: `npm run test -v` for detailed output
4. **Check test isolation**: Run test alone, then with others
5. **Inspect fixtures**: Verify `MockGame` is set up correctly

### When CI Fails but Local Passes

**Common causes**:

- Platform differences (Windows/Linux/macOS)
- Environment variables not set
- Cached dependencies out of sync
- Random test order exposing test interdependence

**Solutions**:

```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Reinstall dependencies
rm -rf env/
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows
pip install -r requirements.txt
npm install

# Test with random order
npm run test --random-order
```

See [ci-cd.md](ci-cd.md) for detailed CI troubleshooting.

## Performance & Profiling

### Don't Guess - Measure

- Don't assume performance bottlenecks
- Add instrumentation before optimizing (timing decorators, frame rate counters)
- Use actual profiling tools

### Test in Isolation

- Validate changes in small scope before applying project-wide
- Check FPS counter after modifications
- Profile with `cProfile` if suspicious of performance issues

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()
# ... code to profile ...
profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumtime')
stats.print_stats(10)
```

### Performance Testing

```bash
# Run game with profiling
python -m cProfile -o profile.stats main.py

# Analyze profile
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumtime'); p.print_stats(20)"
```

**Focus areas**:

- `update_bullets()` - Spatial grid efficiency
- `update_aliens()` - Fleet movement optimization
- `update_screen()` - Rendering performance
- Sprite group operations - Collision detection
