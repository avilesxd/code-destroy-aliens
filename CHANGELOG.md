# Changelog

All notable changes to this project will be documented in this file.

## [v1.4.0] - 2026-02-11

### Added

- Gamepad support with comprehensive controller mapping and configuration
- Linux build support via PyInstaller
- Linux download button on website for direct executable downloads
- Node.js version specification with .nvmrc file (Node 18)
- Security improvements with pip-audit integration
- Dependabot configuration for automated dependency updates

### Changed

- Improved test coverage from 70% to 82%
- Enhanced documentation with professional layout and organization
- Updated multiple GitHub Actions dependencies
- Improved contribution guidelines to enforce feature branch usage

### Fixed

- PyInstaller syntax for Linux build command
- Windows locale detection support for language system
- Fallback language retrieval using getlocale() for better compatibility

### Performance

- Optimized FPS counter rendering with caching and toggle
- Removed redundant test execution from build workflows

### Chore

- Updated npm and Python dependencies via Dependabot
- Added comprehensive CI/CD documentation
- Improved code conventions and workflow documentation

---

## [v1.3.0] - 2025-12-11

### Added

- Support for 38 additional languages (Arabic, Bulgarian, and more)
- Automated version bump system with PowerShell and Bash scripts
- FPS counter display with real-time frame tracking
- Game class for centralized game asset and behavior management
- MockGame class and pytest fixture for improved testing encapsulation
- NumberFormatter support for quintillion, sextillion, and octillion values
- Input validation for NumberFormatter to handle negative numbers and invalid
  types
- Comprehensive tests for path_utils functions
- Translations section to development navigation
- Language checklist for game translations
- AI Copilot instructions for project overview and workflows

### Changed

- Improved system language detection with environment variable fallback and
  macOS support
- Enhanced alien creation functions to use Game object for better encapsulation
- Refactored event handling to use Game object
- Refactored game logic to use Game object for better maintainability
- Refactored game rendering functions with improved gradient surface caching
- Updated ship and alien speed factors for improved gameplay dynamics
- Improved number formatting logic with uppercase suffixes (K, M, B, T)
- Enhanced system requirements documentation for Windows and macOS
- Improved README.md structure and content
- Refactored tests to use MockGame for better clarity
- Updated workflow configurations

### Fixed

- Virtual environment check before command execution
- Alien movement test to use correct x position
- Scope enforcement in commit messages (must be empty)
- Button label from "Play Online" to "Play Now" in README
- Version number synchronization across package files

### Refactored

- Test structure to use MockGame fixture throughout
- Game object usage across all major systems

### Chore

- Updated dependencies (js-yaml from 4.1.0 to 4.1.1)
- Added lint-staged configuration for pre-commit hooks

---

## [v1.2.0] - 2025-05-15

### Added

- Music and sound toggle options (with translations)
- Multilanguage support expansion (German, French, Italian, Portuguese)
- Dynamic screen resolution scaling
- Number formatting for scores (abbreviated form)
- Enhanced versioning system with Windows/macOS version files
- SECURITY.md policy document
- Code of Conduct and contribution guidelines
- System requirements documentation for all platforms
- Recommended VSCode extensions for development
- Live server integration
- Enhanced accessibility features

### Changed

- Modularized game logic and actor management
- Improved translation system architecture
- Enhanced Windows build scripts
- Updated release workflow with enhanced verification
- Refactored path utilities
- Improved documentation navigation
- Enhanced mkdocs.yml configuration

### Fixed

- Missing newline in translation files
- Sound toggle key correction (X→S)
- Documentation URL inconsistencies
- Copyright year updates
- Redundant configuration files
- Typography and UI consistency
- Module docstring improvements

### Refactored

- Resource path handling system
- Game logic structure
- Configuration in mypy.ini → pyproject.toml
- VSCode IDE configuration
- Pytest structure and execution

### Chore

- Enhanced CI/CD workflow steps
- Added Prettier configuration
- Improved release workflow automation
- Enhanced GitHub Actions workflows
- Optimized dependency management

### Security

- Additional security policy documentation
- Enhanced vulnerability reporting process

## [v1.1.0] - 2024-05-01

### Added

- Enhanced macOS compatibility and build process
- Improved documentation and build guides
- Added comprehensive type checking configuration

### Changed

- Refactored code structure for improved readability
- Updated project configuration for better maintainability
- Enhanced resource path handling

### Fixed

- Various bug fixes and improvements
- Type checking issues in setup.py

## [1.0.0] - 2024-04-17

### Added

- Multilingual support for game interface
- Encrypted high score system
- Enhanced sound effects and music control
- Controls screen with detailed instructions
- Game pause and lives display
- Comprehensive unit tests
- Technical documentation with MkDocs
- Build guides for macOS and Windows
- CI/CD configuration with GitHub Actions

### Changed

- Complete game structure refactoring
- Improved resource management
- Performance optimization
- Updated alien descent speed
- Enhanced README and documentation
- Optimized game assets

### Fixed

- Cross-platform resource path handling
- Error handling improvements
- Pygame compatibility issues
- Project dependencies update

### Security

- High score encryption implementation
- Enhanced file and resource management

### Documentation

- Complete project architecture documentation
- Updated contribution guidelines
- Build guides for different platforms

### Infrastructure

- GitHub Actions CI/CD setup
- MkDocs documentation system
- Development environment configuration
