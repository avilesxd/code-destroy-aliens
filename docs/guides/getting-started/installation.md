# 📥 Installation Guide

## Prerequisites

Before installing Alien Invasion, make sure you have the following installed:

- Python 3.8 or higher
- Pygame 2.5.0 or higher
- Node.js (for development tools)
- Git

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/avilesxd/code-destroy-aliens.git
cd code-destroy-aliens
```

### 2. Install Dependencies

#### Windows

```bash
# Install Node.js dependencies
npm install

# Create and activate virtual environment
python -m venv env
env\Scripts\activate

# Install Python dependencies (via npm script)
npm run deps:install
```

#### Linux/macOS

```bash
# Install Node.js dependencies
npm install

# Create and activate virtual environment
python3 -m venv env
source env/bin/activate

# Install Python dependencies (via npm script)
npm run deps:install
```

### 3. Verify Installation

```bash
# Run the game in development mode
npm run dev
```

## Troubleshooting

### Common Issues

1. **Python not found**
    - Make sure Python is installed and added to your PATH
    - Verify installation with `python --version`

2. **Pygame installation fails**
    - Make sure you have the required build tools
    - On Windows, you might need Visual C++ Build Tools
    - On Linux, install development libraries:
      `sudo apt-get install python3-dev`

3. **Virtual environment issues**
    - If activation fails, try using the full path to the activation script
    - Make sure you're using the correct activation command for your OS

### Getting Help

If you encounter any issues not covered here:

1. Check the [Troubleshooting Guide](./reference/troubleshooting/README.md)
2. Open an [issue](https://github.com/avilesxd/code-destroy-aliens/issues)

## Next Steps

- Read the [Quick Start Guide](quick-start.md) to start playing
- Check out the [Configuration Guide](configuration.md) to customize the game
- Explore the [Development Guide](../development/core-concepts.md) to start
  contributing
