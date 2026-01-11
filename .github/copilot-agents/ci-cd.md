# CI/CD & GitHub Actions

## Overview

The project uses GitHub Actions for automated testing, building, and deployment.
All workflows are in `.github/workflows/`.

## Workflows

### 1. Code Quality & Tests (`tests.yml`)

**Triggers**: Push to `main`, Pull Requests to `main`

**What it does**:

1. Checks Python formatting (black, isort)
2. Checks Prettier formatting (JS/JSON/MD/YML)
3. Runs linting (flake8)
4. Runs type checking (mypy)
5. Runs tests with coverage
6. Validates commit message format

**Environment**: Ubuntu, Python 3.13, Node 18

```yaml
Sequence:
format:check → prettier:check → lint → typecheck → test:coverage → commitlint
```

**Common Failures**:

| Error                     | Cause                  | Fix                                             |
| ------------------------- | ---------------------- | ----------------------------------------------- |
| `Formatting check failed` | Code not formatted     | Run `npm run format` locally                    |
| `Lint errors found`       | Flake8 violations      | Run `npm run lint`, fix issues                  |
| `Type checking failed`    | mypy errors            | Run `npm run typecheck`, add type hints         |
| `Tests failed`            | Test assertions failed | Run `npm run test`, fix failing tests           |
| `Commit message invalid`  | Wrong format           | Use `type: subject` (e.g., `feat: add feature`) |

**How to debug locally**:

```bash
# Run exactly what CI runs
npm run format:check
npm run format:prettier-check
npm run lint
npm run typecheck
npm run test:coverage

# Or all at once
npm run verify
```

### 2. Build Windows (`build-windows.yml`)

**Triggers**:

- Tag push matching `v*` (e.g., `v1.3.0`)
- Manual trigger via `workflow_dispatch`
- Repository dispatch event

**What it does**:

1. Sets up Python 3.13 on Windows
2. Caches pip packages and PyInstaller build
3. Installs dependencies
4. Builds `.exe` with PyInstaller using `Alien Invasion.spec`
5. Verifies executable was created
6. Uploads artifact (`.exe` file)

**Build time**: ~3-5 minutes

**Artifact**: `Alien Invasion.exe` (~50MB)

**How to test locally** (Windows only):

```bash
npm run build:windows
# Check dist/Alien Invasion.exe
```

**Common issues**:

- **Missing version file**: Ensure `versions/windows.txt` exists (run
  `python tools/generate-version.py`)
- **Import errors**: Check all modules are in `requirements.txt`
- **PyInstaller cache**: Clear with `pyinstaller --clean 'Alien Invasion.spec'`

### 3. Build macOS (`build-macos.yml`)

**Triggers**:

- Tag push matching `v*`
- Manual trigger
- Repository dispatch event

**What it does**:

1. Sets up Python 3.13 on macOS
2. Caches pip packages
3. Installs dependencies
4. Builds `.app` bundle with py2app
5. Creates `.dmg` file for distribution
6. Verifies app bundle structure
7. Uploads both `.app` and `.dmg` artifacts

**Build time**: ~1-2 minutes

**Artifacts**:

- `Alien Invasion.app` (app bundle)
- `Alien Invasion.dmg` (~50MB, distributable)

**How to test locally** (macOS only):

```bash
npm run build:macos
# Check dist/Alien Invasion.app
```

**Common issues**:

- **py2app config**: Check `setup.py` configuration
- **Signing issues**: May need to disable Gatekeeper locally for testing
- **Missing resources**: Ensure `src/` directory is included in `DATA_FILES`

### 4. Release (`release.yml`)

**Triggers**: After both Windows and macOS builds complete successfully

**What it does**:

1. Waits for both build workflows to finish
2. Downloads `.exe` and `.dmg` artifacts
3. Creates GitHub Release with tag version
4. Attaches both executables to the release

**Release includes**:

- Windows: `Alien Invasion.exe`
- macOS: `Alien Invasion.dmg`
- Changelog from `CHANGELOG.md`

### 5. Deploy Website (`deploy.yml`)

**Triggers**: Push to `main` branch

**What it does**:

1. Builds MkDocs documentation
2. Deploys to GitHub Pages
3. Updates project website

**Deployment URL**: `https://avilesxd.github.io/code-destroy-aliens/`

### 6. Version Bump (`version-bump.yml`)

**Triggers**: Manual workflow dispatch with version type input

**What it does**:

1. Runs `scripts/bump-version.ps1` (or `.sh` on Unix)
2. Updates all version files
3. Commits changes
4. Creates and pushes git tag

**Usage**: Prefer local version bumping with
`.\scripts\bump-version.ps1 -Type [patch|minor|major]`

## CI/CD Best Practices

### Before Pushing Code

Always run locally first:

```bash
npm run verify  # Ensures CI will pass
```

### When CI Fails

1. **Read the logs**: Click the failed workflow in GitHub Actions
2. **Identify the step**: Check which step failed (format, lint, test, etc.)
3. **Reproduce locally**: Run the same npm script that failed
4. **Fix and verify**: Fix the issue, run `npm run verify`
5. **Push again**: CI should pass now

### Common CI Patterns

**Format check failed**:

```bash
npm run format          # Auto-fix formatting
npm run format:check    # Verify it passes
```

**Type errors**:

```bash
npm run typecheck       # See all errors
# Fix type annotations
npm run typecheck       # Verify clean
```

**Tests failing**:

```bash
npm run test            # Run all tests
npm run test -k "test_name"  # Run specific test
# Fix the test or code
npm run test            # Verify all pass
```

### Release Process (Automated)

```bash
# 1. Bump version locally
.\scripts\bump-version.ps1 -Type minor

# 2. Edit CHANGELOG.md with release notes

# 3. Sync changelog to website
python scripts\sync-website-changelog.py

# 4. Commit and tag
git add .
git commit -m "chore: bump version to X.X.X"
git tag -a vX.X.X -m "Release vX.X.X"
git push origin main
git push --tags

# CI takes over:
# - build-windows.yml runs (~3-5 min)
# - build-macos.yml runs (~1-2 min)
# - release.yml creates release with artifacts
# - deploy.yml updates website
```

## Debugging Failed Builds

### Windows Build Issues

**Check the build log for**:

- PyInstaller warnings/errors
- Missing modules
- Import errors at runtime

**Local debugging**:

```powershell
# Clean build
Remove-Item -Recurse -Force build, dist
pyinstaller --clean 'Alien Invasion.spec'

# Test the executable
.\dist\Alien Invasion.exe
```

### macOS Build Issues

**Check the build log for**:

- py2app errors
- Missing frameworks
- Code signing issues (if enabled)

**Local debugging**:

```bash
# Clean build
rm -rf build dist
python3 setup.py py2app

# Test the app
open dist/Alien\ Invasion.app
```

### Test Coverage Failures

**View coverage report locally**:

```bash
npm run test:coverage
# Opens browser with coverage report
# Look for uncovered lines
```

**Common low coverage areas**:

- Error handling paths
- Platform-specific code
- GUI event handlers

## CI Environment Variables

Workflows have access to:

- `${{ github.event.head_commit.message }}` - Commit message
- `${{ github.ref }}` - Branch or tag reference
- `${{ runner.os }}` - OS (Windows, Linux, macOS)
- `${{ github.event_name }}` - Event type (push, pull_request, etc.)

## Caching Strategy

**pip packages**: Cached by OS + `requirements.txt` hash

- Speeds up dependency installation
- Invalidates when requirements change

**PyInstaller build**: Cached by OS + `requirements.txt` hash

- Reuses compiled modules
- Reduces build time significantly

**Node modules**: Cached by lock file hash

- Fast npm install

## Workflow Dependencies

```
Tag Push (v*)
    ├─> build-windows.yml (parallel)
    └─> build-macos.yml (parallel)
            └─> release.yml (waits for both)

Main Push
    ├─> tests.yml (quality checks)
    └─> deploy.yml (website deployment)

Pull Request
    └─> tests.yml (quality checks only)
```

## Tips for AI Agents

### When CI fails for your changes

1. **Check the workflow tab**: Identify which job failed
2. **Read the error**: Don't assume - read the actual error message
3. **Test locally first**: Always run `npm run verify` before pushing
4. **Platform-specific**: If Windows/macOS build fails, note it may not be
   testable on your platform
5. **Don't ignore warnings**: PyInstaller/py2app warnings often indicate runtime
   issues

### When modifying workflows

1. **Test with workflow_dispatch**: Most workflows support manual triggering
2. **Check syntax**: Use GitHub's workflow editor or VS Code extensions
3. **Validate YAML**: Ensure proper indentation and structure
4. **Document changes**: Update this file if adding new workflows

### When debugging build failures

1. **Check artifacts**: Failed builds may still upload partial artifacts
2. **Review recent changes**: Compare with last successful build
3. **Check version files**: Ensure `generate-version.py` was run
4. **Verify dependencies**: Ensure all imports are in `requirements.txt`
