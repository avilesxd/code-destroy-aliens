# 🧪 Testing Guide

## Overview

This guide covers the testing strategy and practices for Alien Invasion. We use a comprehensive testing approach to ensure game quality and reliability.

## Testing Types

### 1. Unit Testing

Test individual components and systems:

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

### 2. Integration Testing

Test interactions between systems:

```python
def test_game_loop_integration():
    game = Game()
    game.initialize()
    game.update(1.0)
    assert game.state == GameState.PLAYING
```

### 3. System Testing

Test complete game systems:

```python
def test_physics_system():
    system = PhysicsSystem()
    entity = create_test_entity()
    system.add_entity(entity)
    system.update(1.0)
    assert entity.position.x == 100
```

## Test Organization

### Directory Structure

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── system/         # System tests
└── fixtures/       # Test fixtures
```

### Test Naming

- Use `test_` prefix for test functions
- Group related tests in classes
- Use descriptive test names

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_ship.py

# Run with coverage
pytest --cov=src
```

### Test Configuration

```python
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

## Test Fixtures

### Common Fixtures

```python
@pytest.fixture
def game():
    game = Game()
    game.initialize()
    return game

@pytest.fixture
def ship():
    return Ship(position=(100, 100))
```

### Using Fixtures

```python
def test_ship_movement(ship):
    ship.move_right()
    assert ship.position.x == 105
```

## Mocking

### Mocking External Dependencies

```python
def test_audio_system(mocker):
    mock_sound = mocker.Mock()
    audio_system = AudioSystem(mock_sound)
    audio_system.play_sound("shoot")
    mock_sound.play.assert_called_once()
```

### Mocking Game State

```python
def test_game_state_transition(mocker):
    game = Game()
    mocker.patch.object(game, 'change_state')
    game.handle_game_over()
    game.change_state.assert_called_with(GameState.GAME_OVER)
```

## Performance Testing

### Frame Rate Testing

```python
def test_frame_rate():
    game = Game()
    start_time = time.time()
    for _ in range(60):
        game.update(1/60)
    end_time = time.time()
    assert end_time - start_time < 1.0
```

### Memory Usage Testing

```python
def test_memory_usage():
    game = Game()
    initial_memory = get_memory_usage()
    game.load_level("large_level")
    final_memory = get_memory_usage()
    assert final_memory - initial_memory < 1000000  # 1MB
```

## Continuous Integration

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest
```

## Best Practices

### 1. Test Coverage

- Aim for 80%+ coverage
- Focus on critical paths
- Test edge cases

### 2. Test Organization

- Group related tests
- Use descriptive names
- Keep tests independent

### 3. Performance

- Run tests in parallel
- Use efficient fixtures
- Monitor test duration

## Next Steps

- Read the [Development Guide](../development/core-concepts.md)
- Check out the [Architecture Guide](../development/architecture.md)
- Learn about [Contributing](../contributing/README.md)
