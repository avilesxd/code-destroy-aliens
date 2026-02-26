# 🤝 Contributing Guide

## Overview

Thanks for your interest in contributing to Alien Invasion. This guide outlines
the expected workflow and quality standards for contributions.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Follow the [Installation Guide](../getting-started/installation.md)

```bash
git clone https://github.com/your-username/code-destroy-aliens.git
cd code-destroy-aliens
```

## Branch Workflow

All work must be done in a feature branch (do not commit directly to `main`).

```bash
git checkout -b feature/your-feature-name
```

Accepted prefixes: `feature/`, `fix/`, `docs/`, `refactor/`, `test/`, `chore/`.

## Commit Messages

Use Conventional Commits (no scope):

```
feat: add new feature
fix: resolve collision bug
docs: update setup instructions
```

## Quality Checklist

Before opening a PR, run:

```bash
npm run qa:verify
```

Equivalent alias: `npm run verify`.

This runs formatting, linting, type checks, and tests.

## Pull Request Guidelines

Include:

- A clear description of the change
- Tests for new behavior
- Documentation updates if needed

## Code Style

- Use type hints for all functions
- Add docstrings for classes and public methods
- Follow existing formatting and naming conventions

## Communication

Use GitHub issues for bugs and feature requests, and Discussions for general
questions.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Next Steps

- Read the [Development Guide](../development/core-concepts.md)
- Check out the [Testing Guide](../testing/README.md)
