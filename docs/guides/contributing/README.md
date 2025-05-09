# 🤝 Contributing Guide

## Overview

Thank you for your interest in contributing to Alien Invasion! This guide will
help you get started with contributing to the project.

## Getting Started

### 1. Fork the Repository

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment

```bash
git clone https://github.com/your-username/code-destroy-aliens.git

cd code-destroy-aliens
```

### 2. Development Setup

Follow the [Installation Guide](../getting-started/installation.md) to set up
your development environment.

## Contribution Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Follow the [Code Style Guide](#code-style)
- Write tests for new features
- Update documentation

### 3. Commit Changes

```bash
git add .
git commit -m "feat: add new feature"
```

### 4. Push Changes

```bash
git push origin feature/your-feature-name
```

### 5. Create Pull Request

1. Go to GitHub
2. Create a new Pull Request
3. Fill in the PR template
4. Wait for review

## Code Style

### Python Code

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings

```python
def move_ship(x: int, y: int) -> None:
    """Move the ship to the specified coordinates.

    Args:
        x: The x-coordinate
        y: The y-coordinate
    """
    ship.position = (x, y)
```

### Documentation

- Use Markdown for documentation
- Follow the existing style
- Include examples

## Testing

### Before Submitting

1. Run all tests
2. Check code coverage
3. Verify documentation

```bash
pytest
pytest --cov=src
mkdocs serve
```

## Pull Request Guidelines

### PR Template

```markdown
## Description

Brief description of the changes

## Related Issues

Fixes #123

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist

- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code follows style guide
- [ ] All tests pass
```

### Review Process

1. Automated checks run
2. Code review by maintainers
3. Address feedback
4. Merge when approved

## Issue Guidelines

### Creating Issues

1. Use the issue template
2. Provide detailed information
3. Include reproduction steps

### Issue Labels

- `bug`: Something is broken
- `enhancement`: New feature request
- `documentation`: Documentation updates
- `help wanted`: Looking for contributors

## Communication

### GitHub Discussions

Use GitHub Discussions for:

- Feature proposals
- Questions
- General discussion

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Recognition

Contributors will be:

- Listed in the README
- Given credit in release notes
- Invited to join the team

## Next Steps

- Read the [Development Guide](../development/core-concepts.md)
- Check out the [Testing Guide](../testing/README.md)
