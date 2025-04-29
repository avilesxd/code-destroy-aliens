# 🎨 Asset Management System

## Overview

This guide covers the asset management system for Alien Invasion, including loading, caching, and optimization of game assets.

## Asset Types

### 1. Images

```python
class ImageAsset:
    def __init__(self, path: str):
        self.path = path
        self.surface = None
        self.loaded = False

    def load(self):
        if not self.loaded:
            self.surface = pygame.image.load(self.path).convert_alpha()
            self.loaded = True
```

### 2. Sounds

```python
class SoundAsset:
    def __init__(self, path: str):
        self.path = path
        self.sound = None
        self.loaded = False

    def load(self):
        if not self.loaded:
            self.sound = pygame.mixer.Sound(self.path)
            self.loaded = True
```

### 3. Music

```python
class MusicAsset:
    def __init__(self, path: str):
        self.path = path
        self.loaded = False

    def load(self):
        if not self.loaded:
            pygame.mixer.music.load(self.path)
            self.loaded = True
```

## Asset Manager

### 1. Basic Implementation

```python
class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.music = {}
        self.fonts = {}

    def load_image(self, name: str, path: str) -> None:
        self.images[name] = ImageAsset(path)

    def get_image(self, name: str) -> pygame.Surface:
        if name not in self.images:
            raise KeyError(f"Image {name} not found")
        asset = self.images[name]
        if not asset.loaded:
            asset.load()
        return asset.surface
```

### 2. Asset Caching

```python
class AssetCache:
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.cache = {}
        self.usage = {}

    def get(self, key: str, loader: Callable) -> Any:
        if key in self.cache:
            self.usage[key] = time.time()
            return self.cache[key]
        
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        
        value = loader()
        self.cache[key] = value
        self.usage[key] = time.time()
        return value
```

## Asset Loading

### 1. Preloading

```python
def preload_assets(asset_manager: AssetManager) -> None:
    # Load essential assets
    asset_manager.load_image("ship", "assets/images/ship.png")
    asset_manager.load_image("alien", "assets/images/alien.png")
    asset_manager.load_sound("shoot", "assets/sounds/shoot.wav")
```

### 2. Lazy Loading

```python
def lazy_load_asset(asset_manager: AssetManager, name: str) -> None:
    if name not in asset_manager.assets:
        asset_manager.load_asset(name)
```

## Asset Optimization

### 1. Image Optimization

```python
def optimize_image(surface: pygame.Surface) -> pygame.Surface:
    # Convert to optimal format
    return surface.convert_alpha()

def create_sprite_sheet(images: List[pygame.Surface]) -> pygame.Surface:
    # Combine multiple images into a sprite sheet
    width = max(img.get_width() for img in images)
    height = sum(img.get_height() for img in images)
    sheet = pygame.Surface((width, height), pygame.SRCALPHA)
    y = 0
    for img in images:
        sheet.blit(img, (0, y))
        y += img.get_height()
    return sheet
```

### 2. Sound Optimization

```python
def optimize_sound(sound: pygame.mixer.Sound) -> None:
    # Set optimal volume
    sound.set_volume(0.5)
    # Pre-mix for better performance
    sound.play()
    sound.stop()
```

## Asset Organization

### 1. Directory Structure

```
assets/
├── images/
│   ├── sprites/
│   ├── backgrounds/
│   └── ui/
├── sounds/
│   ├── effects/
│   └── music/
└── fonts/
```

### 2. Naming Conventions

- Use lowercase with underscores
- Prefix with type (e.g., `spr_`, `bg_`, `sfx_`)
- Include size/resolution where relevant

## Best Practices

### 1. Loading

- Preload essential assets
- Use lazy loading for non-essential assets
- Implement progress indicators
- Handle loading failures gracefully

### 2. Memory Management

- Monitor memory usage
- Implement asset unloading
- Use appropriate cache sizes
- Clean up unused assets

### 3. Performance

- Optimize asset sizes
- Use sprite sheets
- Compress audio files
- Cache frequently used assets

## Tools

### 1. Asset Creation

- Aseprite for sprites
- Audacity for audio
- TexturePacker for sprite sheets

### 2. Asset Optimization

- ImageMagick for image processing
- FFmpeg for audio processing
- Custom tools for asset management

## Next Steps

- Read the [Audio System Guide](audio-system.md)
- Check out the [Entity System Guide](entity-system.md)
- Learn about [Performance Optimization](performance.md)
