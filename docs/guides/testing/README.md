# 🧪 Testing Guide

## Overview

Tests are written with `pytest` and mirror the `src/` layout. The suite runs in
headless mode to avoid opening a Pygame window and focuses on deterministic
behavior.

## Test Organization

```
tests/
├── config/
├── core/
├── entities/
└── utils/
```

## Running Tests

Use the npm scripts (they handle the virtual environment automatically):

```bash
# Run the full test suite
npm run test

# Run a single file
npm run test tests/entities/test_ship.py

# Run a single test
npm run test tests/entities/test_ship.py::test_ship_movement

# Run with coverage
npm run test:coverage
```

## Fixtures and Headless Mode

The `MockGame` fixture and the `SDL_VIDEODRIVER=dummy` setup live in
`tests/conftest.py`. This keeps tests fast and avoids graphical dependencies.

## What to Test

- Entity movement and collision behavior
- Game logic updates (scoring, level progression)
- Rendering helpers that produce deterministic outputs
- Statistics and persistence routines

## Best Practices

- Add tests for new behavior or bug fixes.
- Keep tests independent and deterministic.
- Prefer the `MockGame` fixture over real game initialization.

## Continuous Integration

CI runs formatting, linting, type checking, and tests on every PR. Run
`npm run verify` locally before submitting changes.

## Next Steps

- Read the [Development Guide](../development/core-concepts.md)
- Check out the [Architecture Guide](../development/architecture.md)
- Learn about [Contributing](../contributing/README.md)
