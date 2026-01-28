# 🔊 Audio System

## Overview

Audio is managed by the `Music` singleton in `src/config/music/music.py`. It
loads background music and sound effects using `resource_path()` and exposes
simple toggle and playback methods.

## Music and Sound Effects

The `Music` class:

- Initializes the Pygame mixer
- Loads background music and effects
- Starts looping music automatically (except in tests)
- Provides methods to pause/resume music and toggle sound effects

Available sound effects:

- Shooting
- Explosion
- Game over

## Common Controls

The game binds audio controls to keyboard input:

- `M`: Toggle music (pause/resume)
- `S`: Toggle sound effects

## Usage Pattern

The `Game` object owns a `music` instance and passes it to entities that need
audio:

```python
game.music.play_shoot()
game.music.play_explosion()
game.music.play_game_over()
```

## Test Environment Behavior

In automated tests, audio is disabled and `DummySound` is used to avoid
initializing the mixer.

## Best Practices

- Keep audio loading centralized in `Music`.
- Use `resource_path()` for all audio files.
- Avoid direct mixer calls outside the audio module.

## Next Steps

- Read the [Asset Management Guide](assets.md)
- Check out the [Entity System Guide](entity-system.md)
- Learn about [Performance Optimization](performance.md)
