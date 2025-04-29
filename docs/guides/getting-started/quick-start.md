# 🚀 Quick Start Guide

This guide will help you get started with Alien Invasion quickly.

## Prerequisites

- Python 3.8 or higher
- Pygame 2.5.0 or higher
- Node.js (for development tools)
- Git

## Installation

1. **Clone the Repository**:

```bash
git clone https://github.com/avilesxd/code-destroy-aliens.git
cd code-destroy-aliens
```

2. **Install Dependencies**:

```bash
# Install Node.js dependencies
npm install

# Create and activate virtual environment
python -m venv env
env\Scripts\activate  # Windows
source env/bin/activate  # Linux/MacOS

# Install Python dependencies
pip install -r requirements.txt
```

3. **Run the Game**:

```bash
# Development mode
npm run dev

# Or directly
python main.py
```

## Basic Controls

- **Arrow Keys**: Move the ship
- **Spacebar**: Shoot
- **P**: Pause game
- **ESC**: Return to main menu
- **M**: Toggle music
- **S**: Toggle sound effects

## Development Tools

The project includes several npm scripts for development:

| Script | Description |
|--------|-------------|
| `npm run dev` | Run the game in development mode |
| `npm run format` | Format code using black and isort |
| `npm run format:check` | Check code formatting |
| `npm run lint` | Run flake8 linter |
| `npm run typecheck` | Run mypy type checker |
| `npm run test` | Run all tests |
| `npm run build` | Build the game executable |

## Next Steps

- Read the [Installation Guide](installation.md) for detailed setup instructions
- Check out the [Configuration Guide](configuration.md) to customize the game
- Explore the [Development Guide](../development/core-concepts.md) to start contributing

## Need Help?

- Check the [Troubleshooting Guide](reference/troubleshooting/README.md)
- Open an [issue](https://github.com/avilesxd/code-destroy-aliens/issues)
