# 📚 Technical Documentation - Alien Invasion

Welcome to the technical documentation for **Alien Invasion**, an arcade shooter in which you must defend Earth from waves of aliens.

## 🎮 Game Images

 | Start | Game | End |
 |-------|------|-----|
 | ![Start][game_start_url] | ![Game][game_score_url] | ![End][game_over_url] |

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

## 🧰 Requirements

- Python 3.8+
- pygame 2.5.0+
- Additional dependencies listed in `requirements.txt`

## ⚙️ Installation

1. Clone the repository:

```bash
 git clone https://github.com/avilesxd/code-destroy-aliens.git
 cd code-destroy-aliens
```

2. Create and activate a virtual environment:

```bash
 # Windows
 python -m venv venv
 venv\Scripts\activate
 
 # Linux/MacOS
 python3 -m venv venv
 source venv/bin/activate
 ```

 3. Install dependencies:

 ```bash
 pip install -r requirements.txt
 pygame==2.5.2
 ```

4. Start the game with:

 ```bash
 python main.py
 ```

## 🧱 Building the Game

### Windows Build

1. Create the spec file:

```bash
 pyi-makespec main.py --name="Alien Invasion" --icon="src/assets/icons/icon.ico" --onefile --noconsole --add-data="src;src" --version-file="version.txt"
 ```

 2. Build the executable:

 ```bash
 pyinstaller ".\Alien Invasion.spec"
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

## Future Improvements

- Additional language support
- More alien types
- Power-up system

## 📄 License

This project is licensed under the [MIT License](../LICENSE)

<!-- IMAGES -->
 [game_start_url]: https://raw.githubusercontent.com/avilesxd/code-destroy-aliens/refs/heads/main/docs/images/game_start.png
 [game_over_url]: https://raw.githubusercontent.com/avilesxd/code-destroy-aliens/refs/heads/main/docs/images/game_over.png
 [game_score_url]: https://raw.githubusercontent.com/avilesxd/code-destroy-aliens/refs/heads/main/docs/images/game_score.png
