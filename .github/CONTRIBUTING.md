# 🤝 Contributor Guide

Thank you for your interest in contributing to **Alien Invasion**! Your help is
welcome, whether it's fixing bugs, improving the code, or adding new features.

---

## 🧑‍💻 How to contribute?

### 1. Fork the Repository

Click the "Fork" button in the top right corner of this repository.

### 2. Clone Your Fork

```bash
git clone https://github.com/your-username/code-destroy-aliens.git

cd code-destroy-aliens
```

### 3. Create a Branch

```bash
git checkout -b improve-or-fix-descriptive
```

### 4. Make Your Changes

Make sure you follow good coding practices and maintain a clear structure.

### 5. Test Your Code

- Run the game to verify that everything works correctly.
- Make sure you don't break anything existing.
- Run tests.

### 6. Commit

```bash
# Stage your changes
git add .

# Create a commit following the conventional commit format
# The commit will be validated by commitlint and husky
# Example: git commit -m "feat: add new player movement system"
# Example: git commit -m "fix: resolve collision detection bug"
# Example: git commit -m "docs: update README with new features"
```

The commit message must follow the
[Conventional Commits](https://www.conventionalcommits.org/) format:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding or fixing tests
- `chore:` for maintenance tasks
- `perf:` for performance improvements
- `ci:` for CI/CD related changes
- `build:` for build system changes
- `revert:` for reverting previous changes
- `wip:` for work in progress

If your commit doesn't follow this format, husky will prevent the commit from
being created.

### 7. Push your changes

```bash
git push origin descriptive-fix-or-improve
```

### 8. Create a Pull Request

Go to your fork on GitHub and click "Compare & pull request".

---

## 📝 Recommendations

- Keep your changes focused on a single goal per PR.
- If you're proposing a major new feature, open an issue to discuss it first.
- Add comments in the code if you need to explain why something is happening.

---

## 🧪 Tests

### Testing Guidelines

1. **Test Coverage**

    - Write tests for all new features and bug fixes
    - Aim for at least 80% test coverage for new code
    - Include both unit tests and integration tests where appropriate

2. **Test Structure**

    - Place test files in the `tests` directory
    - Name test files with the pattern `test_*.py`
    - Use clear and descriptive test function names

3. **Running Tests**

    ```bash
    # Run all tests
    python -m pytest

    # Run specific test file
    python -m pytest tests/test_specific.py
    ```

4. **Test Best Practices**

    - Follow the AAA pattern (Arrange, Act, Assert)
    - Keep tests independent and isolated
    - Use meaningful test data
    - Document complex test scenarios
    - Mock external dependencies when necessary

5. **Continuous Integration**
    - All tests must pass before merging
    - Pull requests will be automatically tested
    - Fix any failing tests before requesting review

---

## 💬 Contact

If you have any questions, please open an issue or contact us directly through
[Discussions](https://github.com/avilesxd/code-destroy-aliens/discussions).

---

Thanks for helping improve this project! 🚀
