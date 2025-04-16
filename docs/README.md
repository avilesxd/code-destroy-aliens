# 📚 Technical Documentation - Alien Invasion

Welcome to the technical documentation for **Alien Invasion**, an arcade shooter in which you must defend Earth from waves of aliens.

## 🎮 Game Images

| Start | Game | End |
|-------|------|-----|
| ![Start][game_start_url] | ![Game][game_score_url] | ![End][game_over_url] |

## 🏗️ Project Structure

```
code-destroy-aliens/
├── src/                  # Source code
│   ├── assets/           # Game resources
│   │   ├── images/       # Sprites
│   │   ├── music/        # Music
│   │   └── icons/        # Application icons
│   ├── config/           # Configuration files
│   │   ├── configuration.py  # Game settings
│   │   ├── game_functions.py # Core game functions
│   │   ├── music.py      # Music and sound settings
│   │   └── statistics.py # Game statistics
│   ├── core/             # Core game logic
│   │   └── utils.py      # Utility functions
│   └── entities/         # Game entities
│       ├── alien.py      # Alien enemies
│       ├── bullet.py     # Projectiles
│       ├── button.py     # UI buttons
│       ├── heart.py      # Life indicators
│       ├── scoreboard.py # Score display
│       └── ship.py       # Player ship
├── docs/                 # Documentation
├── website/              # Website files
├── main.py               # Entry point
├── setup.py              # Installation script to compile the game for MacOS
├── requirements.txt      # Dependencies
└── version.txt           # Version information
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
```

## 🎮 Running the Game

Start the game with:

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

The executable will be created in the `dist` directory.

## 🔧 Configuration

The game can be configured through various files:

- `src/config/configuration.py`: Game settings, screen size, FPS, etc.
- `src/config/statistics.py`: Game statistics and scoring system
- `src/config/game_functions.py`: Core game mechanics
- `src/assets/`: Customize sprites, sounds, and other assets

## 📄 License

This project is licensed under the [MIT License](../LICENSE)

<!-- IMAGES -->
[game_start_url]: https://raw.githubusercontent.com/avilesxd/code-destroy-aliens/refs/heads/main/docs/images/game_start.PNG
[game_over_url]: https://raw.githubusercontent.com/avilesxd/code-destroy-aliens/refs/heads/main/docs/images/game_over.PNG
[game_score_url]: https://raw.githubusercontent.com/avilesxd/code-destroy-aliens/refs/heads/main/docs/images/game_score.PNG
