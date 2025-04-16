# Technical Documentation

## Project Structure

```
code-destroy-aliens/
├── main.py                 # Main game entry point
├── requirements.txt        # Project dependencies
├── src/
│   ├── config/            # Configuration files
│   │   ├── configuration.py  # Game settings
│   │   ├── game_functions.py # Core game functions
│   │   ├── music.py      # Music and sound settings
│   │   └── statistics.py # Game statistics
│   │   └── language.py    # Language system implementation
│   ├── entities/          # Game entities
│   │   ├── ship.py       # Player's spaceship
│   │   ├── alien.py      # Alien invaders
│   │   ├── bullet.py     # Projectiles
│   │   ├── heart.py      # Life indicators
│   │   ├── scoreboard.py # Score display
│   │   └── controls_screen.py # Controls information
│   └── assets/           # Game assets
│       └── translations/ # Language files
│           ├── en.json   # English translations
│           └── es.json   # Spanish translations
└── docs/                 # Documentation
    └── README.md         # This file
```

## Core Components

### Game Engine

- Built with Pygame
- Main game loop in `main.py`
- Handles game states: menu, playing, paused, game over

### Entity System

- `Ship`: Player-controlled spaceship
  - Movement controls
  - Shooting mechanics
  - Collision detection
- `Alien`: Enemy entities
  - Movement patterns
  - Different types and behaviors
  - Spawning system
- `Bullet`: Projectile system
  - Speed and damage properties
  - Collision detection
- `Heart`: Life indicator
  - Visual representation of remaining lives
  - Position management

### Scoring System

- `Scoreboard` class handles:
  - Current score display
  - High score tracking
  - Level progression
  - Lives remaining
  - Pause screen overlay

### Internationalization System

- `Language` class in `config/language.py`
- Features:
  - Automatic language detection
  - JSON-based translation files
  - Fallback to English
  - Easy addition of new languages
- Supported languages:
  - English (default)
  - Spanish
  - Extensible for more languages

### Visual Improvements

- Text rendering:
  - High contrast white text
  - Semi-transparent black backgrounds
  - Alpha value: 180/255 for optimal visibility
- UI elements:
  - Consistent padding and margins
  - Clear visual hierarchy
  - Responsive positioning

## Technical Details

### Performance Considerations

- Sprite groups for efficient rendering
- Object pooling for bullets
- Optimized collision detection
- Memory management for game objects

### Code Architecture

- Object-oriented design
- Separation of concerns
- Modular components
- Easy to extend and maintain

### Dependencies

```
pygame==2.5.2
```

## Development Guidelines

### Adding New Features

1. Create new entity class in `src/entities/`
2. Update main game loop if necessary
3. Add configuration in `settings.py`
4. Update documentation

### Adding New Languages

1. Create new JSON file in `src/assets/translations/`
2. Follow existing translation structure
3. Add language code to detection system
4. Test translations

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to classes and methods
- Keep methods focused and concise

## Testing

- Manual testing for gameplay mechanics
- Performance testing for frame rate
- Language system testing
- Cross-platform compatibility

## Known Issues

- None currently reported

## Future Improvements

- Additional language support
- More alien types
- Power-up system
- Sound effects and music
- Level progression system
