# 🚀 Performance Guide

## Overview

This guide covers performance optimization techniques and best practices for
Alien Invasion.

## Performance Metrics

### 1. Frame Rate

Target: 60 FPS (16.67ms per frame)

```python
def measure_frame_rate():
    clock = pygame.time.Clock()
    fps = 60
    while running:
        # Game logic
        clock.tick(fps)
```

### 2. Memory Usage

Monitor memory consumption:

```python
import psutil
import os

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss
```

### 3. CPU Usage

Track CPU utilization:

```python
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)
```

## Optimization Techniques

### 1. Rendering Optimization

```python
# Use sprite groups efficiently
all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()

# Batch rendering
def render_sprites(screen, sprites):
    screen.blits([(sprite.image, sprite.rect) for sprite in sprites])
```

### 2. Collision Detection

```python
# Spatial partitioning
class SpatialHash:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.cells = {}

    def add(self, entity):
        cell = self.get_cell(entity.position)
        if cell not in self.cells:
            self.cells[cell] = []
        self.cells[cell].append(entity)
```

### 3. Memory Management

```python
# Object pooling
class BulletPool:
    def __init__(self, size):
        self.pool = [Bullet() for _ in range(size)]
        self.next = 0

    def get(self):
        bullet = self.pool[self.next]
        self.next = (self.next + 1) % len(self.pool)
        return bullet
```

## Performance Profiling

### 1. Using cProfile

```python
import cProfile
import pstats

def profile_game():
    profiler = cProfile.Profile()
    profiler.enable()
    # Game code
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats()
```

### 2. Memory Profiling

```python
from memory_profiler import profile

@profile
def memory_intensive_function():
    # Function code
    pass
```

## Best Practices

### 1. Rendering

- Use sprite groups
- Minimize surface creation
- Batch draw calls
- Use dirty rectangles
- Optimize blit operations

### 2. Physics

- Implement spatial partitioning
- Use efficient collision detection
- Cache calculations
- Limit physics updates

### 3. Memory

- Use object pooling
- Implement proper cleanup
- Monitor memory usage
- Handle resource loading

### 4. CPU

- Profile regularly
- Optimize hot paths
- Use efficient algorithms
- Cache calculations

## Performance Testing

### 1. Frame Rate Testing

```python
def test_frame_rate():
    game = Game()
    start_time = time.time()
    for _ in range(60):
        game.update(1/60)
    end_time = time.time()
    assert end_time - start_time < 1.0
```

### 2. Memory Testing

```python
def test_memory_usage():
    game = Game()
    initial_memory = get_memory_usage()
    game.load_level("large_level")
    final_memory = get_memory_usage()
    assert final_memory - initial_memory < 1000000  # 1MB
```

## Tools

### 1. Profiling Tools

- cProfile
- memory_profiler
- line_profiler
- py-spy

### 2. Monitoring Tools

- psutil
- pygame.time.Clock
- tracemalloc

## Common Issues

### 1. Frame Drops

Causes:

- Too many sprites
- Inefficient collision detection
- Heavy calculations

Solutions:

- Implement culling
- Optimize collision detection
- Cache calculations

### 2. Memory Leaks

Causes:

- Unreleased resources
- Circular references
- Large asset loading

Solutions:

- Implement proper cleanup
- Use weak references
- Optimize asset loading

### 3. CPU Spikes

Causes:

- Complex calculations
- Inefficient algorithms
- Too many updates

Solutions:

- Profile and optimize
- Use efficient algorithms
- Limit update frequency

## Next Steps

- Read the [Architecture Guide](architecture.md)
- Check out the [Testing Guide](../testing/README.md)
- Learn about [Code Quality](code-quality.md)
