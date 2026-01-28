# 🚀 Performance Guide

## Overview

Alien Invasion uses a few focused optimizations to keep gameplay smooth. This
document highlights what is already in place and how to extend it safely.

## Current Optimizations

### Spatial Grid Collision Detection

Bullet–alien collisions are accelerated using a spatial grid in
`src/config/logic/game_logic.py`. This reduces collision checks by only
comparing objects in nearby cells.

### Bullet Pooling

`Bullet` uses a small object pool to reduce allocations during gameplay. Use
`Bullet.get_bullet()` and let the class recycle inactive bullets.

### Gradient Background Caching

The gradient background surface is cached in
`src/config/rendering/game_rendering.py` and only rebuilt when the screen size
changes.

## Best Practices

- Avoid per-frame allocations in tight loops.
- Use sprite groups for batch updates.
- Keep collision checks localized.
- Prefer configuration-driven values over hard-coded constants.

## Profiling

If you need to investigate performance, use standard Python tools such as
`cProfile` or `tracemalloc` and focus on the update loop hotspots:

- `update_bullets()`
- `update_aliens()`
- `update_screen()`

## Next Steps

- Read the [Architecture Guide](architecture.md)
- Check out the [Testing Guide](../testing/README.md)
- Learn about [Code Quality](code-quality.md)
