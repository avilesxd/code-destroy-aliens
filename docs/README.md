# 📚 Technical Documentation - Alien Invasion

<div align="center">
  <img src="https://raw.githubusercontent.com/avilesxd/code-destroy-aliens/refs/heads/main/docs/images/game_start.png" alt="Alien Invasion Game" width="600"/>
  
  [![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
  [![Pygame Version](https://img.shields.io/badge/pygame-2.5.0%2B-green.svg)](https://www.pygame.org/)
  [![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
</div>

## 📋 Table of Contents

- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Building](#-building)
- [Core Components](#-core-components)
- [Game Architecture](#-game-architecture)
- [Development Guidelines](#-development-guidelines)
- [Testing](#-testing)
- [Performance Optimization](#-performance-optimization)
- [Code Quality Tools](#-code-quality-tools)

## 🗂️ Project Structure

```
code-destroy-aliens/
├── main.py                 # Main game entry point
├── requirements.txt        # Project dependencies
├── setup.py               # Project setup configuration
├── pytest.ini            # Pytest configuration
├── .flake8               # Flake8 linting configuration
├── pyproject.toml        # Black and isort configuration
├── .gitignore           # Git ignore rules
├── .husky/              # Git hooks configuration
│   ├── pre-commit      # Pre-commit hook script
│   └── _/             # Husky internal files
├── src/
│   ├── config/            # Configuration files
│   │   ├── configuration.py  # Game settings and constants
│   │   ├── game_functions.py # Core game logic and functions
│   │   ├── music.py      # Audio system implementation
│   │   ├── statistics.py # Game statistics and persistence
│   │   └── language.py   # Internationalization system
│   ├── entities/         # Game entities
│   │   ├── ship.py      # Player's spaceship implementation
│   │   ├── alien.py     # Alien behavior and types
│   │   ├── bullet.py    # Projectile system
│   │   ├── heart.py     # Life indicator system
│   │   ├── scoreboard.py # Score display and UI
│   │   └── controls_screen.py # Controls information display
│   └── assets/          # Game assets
│       ├── images/      # Image resources
│       ├── sounds/      # Audio resources
│       └── translations/ # Language files
│           ├── en.json  # English translations
│           └── es.json  # Spanish translations
├── tests/               # Test files
│   ├── __init__.py
│   ├── test_ship.py
│   ├── test_alien.py
│   └── test_bullet.py
├── docs/               # Documentation
│   ├── README.md      # Technical documentation
│   └── images/        # Documentation images
└── website/           # Project website
    ├── index.html
    └── styles.css
```

## 🧰 Requirements

### System Requirements

- Python 3.8 or higher
- Pygame 2.5.0 or higher
- Operating System: Windows, macOS, or Linux

### Dependencies

All required packages are listed in `requirements.txt`:

```
pygame>=2.5.0
cryptography>=3.4.7
```

## ⚙️ Installation

### Development Setup

1. **Clone the Repository**:

```bash
git clone https://github.com/avilesxd/code-destroy-aliens.git
cd code-destroy-aliens
```

2. **Create Virtual Environment**:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**:

```bash
pip install -r requirements.txt
```

4. **Run the Game**:

```bash
python main.py
```

## 🧱 Building

### Windows Build

1. **Create Spec File**:

```bash
pyi-makespec main.py \
  --name="Alien Invasion" \
  --icon="src/assets/icons/icon.ico" \
  --onefile \
  --noconsole \
  --add-data="src;src" \
  --version-file="version.txt"
```

2. **Build Executable**:

```bash
pyinstaller ".\Alien Invasion.spec"
```

### Build Options

- `--onefile`: Creates a single executable
- `--noconsole`: Hides the console window
- `--add-data`: Includes game assets
- `--version-file`: Adds version information

## 🎮 Core Components

### Game Engine

- Built with Pygame for graphics and input handling
- Main game loop in `main.py`
- State management system for different game screens

### Entity System

- Sprite-based collision detection
- Custom entity classes for game objects
- Particle effects system

### Audio System

- Background music management
- Sound effect system
- Volume control and mute options

### Localization System

- JSON-based translation files
- Automatic language detection
- Dynamic text rendering

## 🏗️ Game Architecture

### Main Loop

```python
while running:
    # Handle events
    # Update game state
    # Render frame
    # Control frame rate
```

### State Management

- Menu State
- Game State
- Pause State
- Game Over State

### Collision System

- Spatial partitioning for performance
- Custom collision detection
- Particle effects on collisions

## 📝 Development Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Document all public methods
- Keep functions focused and small

### Git Workflow

1. Create feature branch
2. Make changes
3. Run tests
4. Submit pull request

### Testing

- Unit tests for core functionality
- Integration tests for game systems
- Performance testing for optimization

## 🚀 Performance Optimization

### Techniques Used

- Spatial partitioning for collision detection
- Surface caching for gradients
- Efficient sprite rendering
- Memory management for particles

### Best Practices

- Minimize surface creation
- Use sprite groups efficiently
- Optimize collision detection
- Manage memory usage

## 🔍 Debugging

### Common Issues

1. Memory leaks
2. Performance bottlenecks
3. Collision detection problems
4. Audio synchronization

### Debug Tools

- Pygame debug mode
- Performance profiler
- Memory usage monitor

## Code Quality Tools

The project uses several tools to maintain code quality and consistency:

### Linting and Formatting

- **Flake8**: Python linter that checks for:
  - Syntax errors (E)
  - Style violations (F)
  - Warnings (W)
  - Code complexity (C)
  - Maximum line length: 88 characters
  - Maximum complexity: 10

- **Black**: Automatic code formatter that:
  - Applies consistent style
  - Line length: 88 characters
  - Python 3.9+ compatible

- **isort**: Import sorter that:
  - Automatically sorts imports
  - Compatible with black
  - Adds trailing commas
  - Uses parentheses for multi-line imports

### Configuration Files

1. `.flake8`:

```ini
[flake8]
max-line-length = 88
extend-ignore = E203
exclude =
    .git,
    __pycache__,
    build,
    dist,
    .venv,
    venv,
    env,
    .pytest_cache,
    .tox
per-file-ignores =
    __init__.py:F401
max-complexity = 10
select = E,F,W,C
```

2. `pyproject.toml`:

```toml
[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'

[tool.isort]
profile = "black"
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
line_length = 88
```

### Usage

To manually run the code quality tools:

```bash
# Format code automatically
black .
isort .

# Check code without formatting
flake8 .
```

### Pre-commit Hooks

The project uses pre-commit hooks to automatically run these tools before each commit. The hooks will:

1. Check import ordering with isort
2. Verify code formatting with black
3. Run flake8 for linting
4. Execute tests
5. Only allow the commit if all checks pass

## 📚 Additional Resources

- [Pygame Documentation](https://www.pygame.org/docs/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Game Development Best Practices](https://realpython.com/pygame-a-primer/)

## 🤝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines on how to contribute to this project.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
