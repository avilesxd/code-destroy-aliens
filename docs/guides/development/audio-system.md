# 🔊 Audio System

## Overview

This guide covers the audio system implementation for Alien Invasion, including
sound effects, music, and audio management.

## Audio Components

### 1. Sound Effects

```python
class SoundEffect:
    def __init__(self, path: str):
        self.sound = pygame.mixer.Sound(path)
        self.volume = 1.0
        self.channel = None

    def play(self, loop: int = 0) -> None:
        self.channel = self.sound.play(loops=loop)
        if self.channel:
            self.channel.set_volume(self.volume)

    def stop(self) -> None:
        if self.channel:
            self.channel.stop()
```

### 2. Music

```python
class Music:
    def __init__(self, path: str):
        self.path = path
        self.volume = 1.0
        self.loaded = False

    def load(self) -> None:
        if not self.loaded:
            pygame.mixer.music.load(self.path)
            self.loaded = True

    def play(self, loop: int = -1) -> None:
        self.load()
        pygame.mixer.music.play(loops=loop)
        pygame.mixer.music.set_volume(self.volume)
```

## Audio Manager

### 1. Basic Implementation

```python
class AudioManager:
    def __init__(self):
        self.sounds = {}
        self.music = {}
        self.master_volume = 1.0
        self.music_volume = 0.5
        self.sfx_volume = 0.7

    def load_sound(self, name: str, path: str) -> None:
        self.sounds[name] = SoundEffect(path)

    def load_music(self, name: str, path: str) -> None:
        self.music[name] = Music(path)

    def play_sound(self, name: str) -> None:
        if name in self.sounds:
            self.sounds[name].play()

    def play_music(self, name: str) -> None:
        if name in self.music:
            self.music[name].play()
```

### 2. Volume Control

```python
class VolumeControl:
    def __init__(self, audio_manager: AudioManager):
        self.audio_manager = audio_manager

    def set_master_volume(self, volume: float) -> None:
        self.audio_manager.master_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def set_music_volume(self, volume: float) -> None:
        self.audio_manager.music_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def _update_volumes(self) -> None:
        pygame.mixer.music.set_volume(
            self.audio_manager.master_volume * self.audio_manager.music_volume
        )
```

## Audio Events

### 1. Event System

```python
class AudioEvent:
    def __init__(self, event_type: str, data: Any):
        self.type = event_type
        self.data = data

class AudioEventManager:
    def __init__(self):
        self.listeners = defaultdict(list)

    def subscribe(self, event_type: str, listener: Callable) -> None:
        self.listeners[event_type].append(listener)

    def dispatch(self, event: AudioEvent) -> None:
        for listener in self.listeners[event.type]:
            listener(event.data)
```

### 2. Event Types

```python
class AudioEventType(Enum):
    SOUND_PLAYED = "sound_played"
    MUSIC_STARTED = "music_started"
    VOLUME_CHANGED = "volume_changed"
    MUTE_TOGGLED = "mute_toggled"
```

## Audio Optimization

### 1. Sound Pooling

```python
class SoundPool:
    def __init__(self, sound: pygame.mixer.Sound, size: int):
        self.sound = sound
        self.channels = [pygame.mixer.Channel(i) for i in range(size)]
        self.next_channel = 0

    def play(self) -> None:
        channel = self.channels[self.next_channel]
        channel.play(self.sound)
        self.next_channel = (self.next_channel + 1) % len(self.channels)
```

### 2. Audio Streaming

```python
class AudioStream:
    def __init__(self, path: str):
        self.path = path
        self.stream = None

    def start(self) -> None:
        self.stream = open(self.path, 'rb')
        pygame.mixer.music.load(self.stream)
        pygame.mixer.music.play()

    def stop(self) -> None:
        if self.stream:
            self.stream.close()
            self.stream = None
```

## Best Practices

### 1. Performance

- Use sound pooling for frequent sounds
- Stream large audio files
- Pre-mix sounds when possible
- Monitor audio memory usage

### 2. Quality

- Use appropriate sample rates
- Normalize audio levels
- Implement proper mixing
- Handle audio formats correctly

### 3. User Experience

- Provide volume controls
- Implement mute functionality
- Handle audio device changes
- Save audio preferences

## Tools

### 1. Audio Processing

- Audacity for editing
- FFmpeg for conversion
- SoX for processing
- Custom tools for optimization

### 2. Testing

- Audio latency testing
- Memory usage monitoring
- Performance profiling
- Cross-platform testing

## Next Steps

- Read the [Asset Management Guide](assets.md)
- Check out the [Entity System Guide](entity-system.md)
- Learn about [Performance Optimization](performance.md)
