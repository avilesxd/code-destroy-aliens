# 📚 Technical Documentation - Alien Invasion

<div align="center">
  <img src="https://raw.githubusercontent.com/avilesxd/code-destroy-aliens/refs/heads/main/docs/images/game_start.png" alt="Alien Invasion Game" width="600"/>
  
  [![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
  [![Pygame Version](https://img.shields.io/badge/pygame-2.5.0%2B-green.svg)](https://www.pygame.org/)
  [![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
</div>

## Table of Contents

- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Available Scripts](#available-scripts)
- [Building](#building-the-game)
- [Core Components](#core-components)
- [Game Architecture](#game-architecture)
- [Development Guidelines](#development-guidelines)
- [Testing](#testing)
- [Performance Optimization](#performance-optimization)
- [Code Quality Tools](#code-quality-tools)

## Project Structure

The project follows a well-organized structure to maintain code clarity and scalability. For a detailed breakdown of the architecture and how different components interact, please refer to the [ARCHITECTURE.md](ARCHITECTURE.md) document.

Here's a high-level overview of the main directories:

```
code-destroy-aliens/
├── src/                    # Source code directory
│   ├── core/              # Core game engine components
│   ├── entities/          # Game entities and sprites
│   ├── states/            # Game state management
│   ├── utils/             # Utility functions and helpers
│   └── assets/            # Game assets (images, sounds, etc.)
├── tests/                 # Test files
├── docs/                  # Documentation
│   ├── images/           # Documentation images
│   ├── ARCHITECTURE.md   # Detailed architecture documentation
│   └── README.md         # This file
├── requirements.txt      # Python dependencies
├── package.json         # Node.js dependencies and scripts
└── main.py             # Game entry point
```

For a comprehensive understanding of the project's architecture, including detailed explanations of each component and their interactions, please visit [ARCHITECTURE.md](ARCHITECTURE.md).

## Requirements

### System Requirements

- Python 3.8 or higher
- Pygame 2.5.0 or higher
- Operating System: Windows, macOS, or Linux

### Dependencies

All required packages are listed in `requirements.txt`.

## Installation

### Development Setup

1. **Clone the Repository**:

```bash
git clone https://github.com/avilesxd/code-destroy-aliens.git
cd code-destroy-aliens
```

2. **Install Node.js Dependencies**:

```bash
npm install
```

3. **Create Virtual Environment**:

```bash
# Windows
python -m venv env
env\Scripts\activate

# Linux/MacOS
python3 -m venv env
source env/bin/activate
```

4. **Install Python Dependencies**:

```bash
pip install -r requirements.txt
```

5. **Run the Game**:

```bash
# Using npm script (recommended)
npm run dev

# Or directly with Python
python main.py
```

### Available Scripts

The project includes several npm scripts to help with development and maintenance:

| Script | Description | Command |
|--------|-------------|---------|
| Development | Run the game in development mode | `npm run dev` |
| Code Formatting | Format all Python code using black and isort | `npm run format` |
| Format Check | Check if code formatting is correct | `npm run format:check` |
| Linting | Run flake8 linter to check code style | `npm run lint` |
| Type Checking | Run mypy to check type hints | `npm run typecheck` |
| Testing | Run all tests using pytest | `npm run test` |
| Building | Build the game executable using PyInstaller | `npm run build` |

### Building the Game

To create a distributable executable:

```bash
npm run build
```

This will create a single executable file using PyInstaller with all necessary assets included.

## Core Components

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

## Game Architecture

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

## Development Guidelines

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

## Performance Optimization

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

## Additional Resources

- [Pygame Documentation](https://www.pygame.org/docs/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Game Development Best Practices](https://realpython.com/pygame-a-primer/)

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
