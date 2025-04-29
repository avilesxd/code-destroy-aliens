# Project Architecture

This document describes the structure and architecture of the "Alien Invasion" project.

## Directory Structure

```
code-destroy-aliens/
├── .github/            # GitHub configuration
│   ├── ISSUE_TEMPLATE/ # Issue templates
│   │   ├── bug_report.md      # Template for bug reports
│   │   └── feature_request.md # Template for feature requests
│   ├── FUNDING.yml    # GitHub Sponsors configuration
│   ├── pull_request_template.md # Pull request template
│   └── workflows/     # GitHub Actions workflows
│       ├── deploy.yml    # Deployment workflow
│       ├── release.yml   # Release workflow
│       └── tests.yml     # Testing workflow
├── .husky/              # Git hooks configuration
│   └── pre-commit      # Pre-commit hook script
├── .vscode/            # VS Code configuration
│   ├── extensions.json  # Recommended VS Code extensions
│   ├── settings.json   # VS Code workspace settings
│   └── tasks.json      # VS Code task configurations
├── docs/             # Documentation
│   ├── README.md    # Technical documentation
│   └── images/      # Documentation images
├── scripts/         # Utility scripts
│   └── run-with-env.js  # Script to run Python with environment setup
├── src/                # Source code
│   ├── config/        # Configuration files
│   │   ├── configuration.py  # Game settings and constants
│   │   ├── game_functions.py # Core game logic and functions
│   │   ├── music.py      # Audio system implementation
│   │   ├── statistics.py # Game statistics and persistence
│   │   └── language.py   # Internationalization system
│   ├── core/          # Core utilities
│   │   ├── path_utils.py # Path handling utilities
│   │   └── __init__.py
│   ├── entities/      # Game entities
│   │   ├── ship.py      # Player's spaceship implementation
│   │   ├── alien.py     # Alien behavior and types
│   │   ├── bullet.py    # Projectile system
│   │   ├── heart.py     # Life indicator system
│   │   ├── controls_screen.py # Controls information display
│   │   ├── scoreboard.py # Score display and UI
│   │   ├── button.py    # UI button implementation
│   │   └── __init__.py
│   └── assets/        # Game assets
│       ├── images/    # Image resources
│       ├── sounds/    # Sound effects
│       ├── music/     # Background music
│       ├── icons/     # Application icons
│       └── translations/ # Language files
│           ├── en.json  # English translations
│           └── es.json  # Spanish translations
├── tests/                 # Project tests
│   ├── entities/         # Entity tests
│   │   ├── test_alien.py        # Tests for alien behavior
│   │   ├── test_bullet.py       # Tests for bullet mechanics
│   │   ├── test_button.py       # Tests for UI buttons
│   │   ├── test_controls_screen.py  # Tests for controls screen
│   │   ├── test_heart.py        # Tests for heart/life display
│   │   ├── test_scoreboard.py   # Tests for scoreboard functionality
│   │   └── test_ship.py         # Tests for player ship
│   ├── core/             # Core functionality tests
│   │   ├── test_game.py         # Tests for main game functionality
│   │   └── test_game_functions.py  # Tests for game core functions
│   └── config/           # Configuration tests
│       ├── test_language.py     # Tests for language system
│       └── test_security.py     # Tests for security features and input validation
└── website/        # Project website
    ├── index.html
    └── styles.css
├── .editorconfig          # Editor configuration
├── .flake8               # Flake8 linting configuration
├── .gitignore           # Git ignore rules
├── CHANGELOG.md         # Project changelog
├── CODE_OF_CONDUCT.md   # Code of conduct for the project
├── commitlint.config.js  # Commit message linting configuration
├── CONTRIBUTING.md      # Contributing guidelines
├── LICENSE             # Project license
├── main.py                 # Main game entry point
├── mypy.ini             # MyPy type checking configuration
├── package.json          # Node.js dependencies
├── pyproject.toml        # Black and isort configuration
├── pytest.ini            # Pytest configuration
├── README.md             # Main project documentation
├── requirements.txt        # Python dependencies
├── setup.py               # Project setup configuration
└── version.txt          # Version information
```

## Main Components

### src/config/

Contains game configuration and utilities:

- `configuration.py`: General game configuration
- `music.py`: Audio management
- `statistics.py`: Game statistics
- `language.py`: Internationalization system

### src/core/

Core game functionalities:

- `path_utils.py`: Path handling utilities
- Other core utilities

### src/entities/

Game entities:

- `alien.py`: Alien class
- `bullet.py`: Bullet class
- `ship.py`: Player ship class
- `button.py`: UI button class
- `heart.py`: Life indicator system
- `controls_screen.py`: Controls information display
- `scoreboard.py`: Scoreboard

### tests/

Project tests organized by components:

- `entities/`: Entity tests
  - `test_alien.py`: Tests for alien behavior
  - `test_bullet.py`: Tests for bullet mechanics
  - `test_button.py`: Tests for UI buttons
  - `test_controls_screen.py`: Tests for controls screen
  - `test_heart.py`: Tests for heart/life display
  - `test_scoreboard.py`: Tests for scoreboard functionality
  - `test_ship.py`: Tests for player ship
- `core/`: Core functionality tests
  - `test_game.py`: Tests for main game functionality
  - `test_game_functions.py`: Tests for game core functions
- `config/`: Configuration tests
  - `test_language.py`: Tests for language system
  - `test_security.py`: Tests for security features and input validation

## Game Flow

1. Initialization:
   - Configuration loading
   - Pygame initialization
   - Resource loading

2. Main Menu:
   - Display start buttons
   - Menu event handling

3. Main Game:
   - Ship control
   - Alien generation
   - Collision system
   - Scoring system

4. Game Over:
   - Statistics saving
   - Transition to main menu

## Development Tools

- **Formatting**: Black and isort
- **Linting**: Flake8
- **Type Checking**: MyPy
- **Testing**: Pytest
- **Version Control**: Git with Husky for pre-commits
- **Build**: PyInstaller

## NPM Scripts

- `dev`: Runs the game in development mode
- `format`: Formats the code
- `format:check`: Checks code format
- `lint`: Runs the linter
- `typecheck`: Checks types
- `test`: Runs the tests
- `verify`: Runs all verifications
- `build`: Builds the executable

## Pre-commit Hooks

Pre-commit hooks verify:

1. Code formatting
2. Linting
3. Type checking
4. Tests

Each verification must pass to allow the commit.
