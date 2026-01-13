# 🤝 Contributor Guide

Thank you for your interest in contributing to **Alien Invasion**! Your help is
welcome, whether it's fixing bugs, improving the code, or adding new features.

---

## ⚠️ Important: Branch Policy

**CRITICAL**: All development work must be done in feature branches. **Direct
commits to `main` are prohibited.**

All changes must be submitted via Pull Request and pass all automated checks
before merging.

---

## 🧑‍💻 How to contribute?

### 1. Fork the Repository

Click the "Fork" button in the top right corner of this repository.

### 2. Clone Your Fork

```bash
git clone https://github.com/your-username/code-destroy-aliens.git

cd code-destroy-aliens
```

### 3. Create a Feature Branch

**Branch Naming Conventions:**

- `feature/descriptive-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/what-changed` - Documentation updates
- `refactor/what-refactored` - Code refactoring
- `test/what-tested` - Test additions/improvements
- `chore/task-description` - Maintenance tasks

```bash
# Ensure you're on main and up to date
git checkout main
git pull origin main

# Create and switch to your feature branch
git checkout -b feature/your-feature-name
# Or: fix/your-bug-fix, docs/your-doc-update, etc.
```

### 4. Make Your Changes

Make sure you follow good coding practices and maintain a clear structure.

### 5. Test Your Code

- **Run all quality checks**: `npm run verify`
    - This runs: format → prettier → lint → typecheck → test
- Make sure all tests pass
- Ensure code follows style guidelines
- Verify type annotations are correct

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

### 7. Push Your Branch

```bash
git push origin feature/your-feature-name
```

### 8. Create a Pull Request

Go to your fork on GitHub and click "Compare & pull request".

**Pull Request Requirements:**

- ✅ Descriptive title following commit conventions (`feat:`, `fix:`, etc.)
- ✅ Clear description of what changed and why
- ✅ All CI checks must pass (tests, linting, type checking)
- ✅ No merge conflicts with `main`
- ✅ Tests added/updated for your changes
- ✅ Documentation updated if needed

**PR will be merged using:**

- **Squash and merge** for feature branches
- Branch will be deleted after merging

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
    # Run all quality checks (includes tests)
    npm run verify

    # Run only tests
    npm run test

    # Run tests with coverage
    npm run test:coverage

    # Run specific test file
    npm run test tests/test_specific.py

    # Run with verbose output
    npm run test -v
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
