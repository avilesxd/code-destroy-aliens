# Release Process

This guide explains how to release a new version of Alien Invasion, including
version bumping, changelog updates, and publishing builds.

## Overview

The release process is largely automated through scripts and CI/CD workflows.
The general flow is:

1. **Bump version** using automated script
2. **Update changelog** with release notes
3. **Sync to website**
4. **Create git tag** and push
5. **Automated builds** create release artifacts

## Prerequisites

- Write access to the repository
- Git configured with SSH keys (for signing tags)
- Python virtual environment activated
- All tests passing locally (`npm run verify`)

## Step-by-Step Process

### 1. Run Version Bump Script

The version bump script automates most of the tedious work:

```powershell
# For Windows PowerShell
.\scripts\bump-version.ps1 -Type <patch|minor|major>

# For macOS/Linux bash
./scripts/bump-version.sh <patch|minor|major>
```

**Version type selection:**

- `patch`: Bug fixes and small changes (1.2.0 → 1.2.1)
- `minor`: New features, non-breaking changes (1.2.0 → 1.3.0)
- `major`: Breaking changes, major rewrites (1.2.0 → 2.0.0)

**What the script does automatically:**

- Updates `package.json` and `package-lock.json`
- Updates `tools/generate-version.py` VERSION constant
- Generates platform-specific version files:
    - `versions/windows.txt` (PyInstaller metadata)
    - `versions/macos.txt` (py2app version string)
- Updates version number in `website/index.html`
- Updates download links in `website/index.html` to point to new release
- Creates new entry in `CHANGELOG.md` with template sections

### 2. Edit CHANGELOG.md

The script creates a template entry in `CHANGELOG.md`. Fill in the details:

```markdown
## [v1.3.0] - 2025-12-11

### Added

- List new features
- Include new capabilities
- Mention new components

### Changed

- Document modifications to existing features
- Note behavior changes
- List refactorings that affect usage

### Fixed

- Bug fixes
- Performance improvements
- Correction of issues

### Refactored

- Internal code improvements
- Architecture changes
- Technical debt resolution

### Chore

- Build system updates
- Dependency updates
- CI/CD improvements
```

**Best practices:**

- Use clear, user-facing language
- Link to issues/PRs when relevant
- Group related changes together
- Start items with verbs (Add, Fix, Update, etc.)
- Keep entries concise but descriptive

### 3. Sync Changelog to Website

Once your changelog is complete, sync it to the website:

```bash
python scripts\sync-website-changelog.py
```

This script:

- Parses `CHANGELOG.md` markdown
- Converts entries to HTML with proper styling
- Applies color coding to section headers:
    - 🟢 Added: Green
    - 🔵 Changed: Blue
    - 🟡 Fixed: Yellow
    - 🟣 Refactored: Purple
    - ⚪ Chore: Gray
    - 🔴 Security: Red
- Updates `website/changelog.html`

### 4. Review Changes

Before committing, review all modified files:

```bash
git status
git diff
```

**Files that should be changed:**

- `package.json`, `package-lock.json`
- `tools/generate-version.py`
- `versions/windows.txt`, `versions/macos.txt`
- `website/index.html`
- `website/changelog.html`
- `CHANGELOG.md`

### 5. Commit and Tag

Create a commit and tag for the release:

```bash
# Stage all changes
git add .

# Commit with conventional commit format
git commit -m "chore: bump version to X.X.X"

# Create annotated tag
git tag -a vX.X.X -m "Release vX.X.X"

# Push commit and tags
git push origin main
git push origin --tags
```

**Important:** Tags must follow the format `vX.X.X` (with `v` prefix) to trigger
build workflows.

### 6. Monitor CI/CD Pipeline

Once you push the tag, GitHub Actions workflows begin automatically:

1. **Build Windows** (`build-windows.yml`)

    - Installs dependencies
    - Runs PyInstaller with `.spec` file
    - Creates `.exe` artifact
    - Duration: ~3-5 minutes

2. **Build macOS** (`build-macos.yml`)

    - Installs dependencies
    - Runs py2app
    - Creates `.dmg` artifact
    - Duration: ~1-2 minutes

3. **Create Release** (`release.yml`)

    - Triggers after both builds complete
    - Downloads build artifacts
    - Creates GitHub release
    - Uploads `.exe` and `.dmg` files
    - Duration: ~30 seconds

4. **Deploy Website** (`deploy.yml`)
    - Triggers on push to main
    - Builds MkDocs documentation
    - Deploys to GitHub Pages
    - Duration: ~1 minute

**Monitor progress:**

```bash
# Using GitHub CLI
gh run list -L 5
gh run watch <run-id>

# Or visit: https://github.com/avilesxd/code-destroy-aliens/actions
```

### 7. Verify Release

Once workflows complete, verify the release:

1. **Check GitHub Release:**

    ```bash
    gh release view vX.X.X
    ```

    - Verify `.exe` and `.dmg` assets are attached
    - Check file sizes are reasonable
    - Ensure release notes are present

2. **Test Downloads:**

    - Download Windows executable
    - Download macOS DMG
    - Test installation and launch on respective platforms

3. **Check Website:**
    - Visit <https://avilesxd.github.io/code-destroy-aliens/>
    - Verify version number is updated
    - Test download links work
    - Check changelog page displays correctly

## Troubleshooting

### Build Failures

**Windows build fails with missing .spec:**

```bash
# Ensure .spec file is committed
git add "Alien Invasion.spec"
git commit -m "ci: add PyInstaller spec file"
```

**macOS build fails:**

- Check `setup.py` configuration
- Verify py2app is in requirements.txt
- Review build logs for missing dependencies

### Release Not Created

If builds succeed but release doesn't create:

```bash
# Manually trigger release workflow
gh workflow run release.yml -f tag=vX.X.X
```

### Website Not Updating

```bash
# Manually trigger website deployment
gh workflow run deploy.yml
```

### Download Links 404

If download links return 404:

- Verify release was created successfully
- Check asset names match links in `website/index.html`
- Asset names should be:
    - `Alien.Invasion.exe` (Windows)
    - `Alien.Invasion.dmg` (macOS)

## Version File Details

### package.json

```json
{
    "version": "1.3.0"
}
```

- Source of truth for version number
- Updated by `npm version` command in bump script

### tools/generate-version.py

```python
VERSION = "1.3.0"
```

- Used to generate platform-specific version files
- Must match package.json version

### versions/windows.txt

- PyInstaller version metadata
- Embedded in .exe file properties
- Displays in Windows Explorer file details

### versions/macos.txt

- Simple version string for py2app
- Used in .app bundle Info.plist

### website/index.html

Version display and download links:

```html
<p class="text-sm text-gray-400 mt-4">
    Version 1.3.0 - <a href="changelog.html">View changelog</a>
</p>
<a href="https://github.com/.../releases/download/v1.3.0/Alien.Invasion.exe">
    Download for Windows
</a>
```

## Emergency Rollback

If a release has critical issues:

### 1. Delete Bad Release

```bash
gh release delete vX.X.X --yes
git tag -d vX.X.X
git push origin :refs/tags/vX.X.X
```

### 2. Revert Changes

```bash
git revert <commit-hash>
git push
```

### 3. Create Hotfix

```bash
.\scripts\bump-version.ps1 -Type patch
# Update CHANGELOG.md with hotfix notes
# Follow normal release process
```

## Best Practices

1. **Test thoroughly before releasing**

    - Run full test suite: `npm run verify`
    - Test game functionality locally
    - Check builds work on target platforms

2. **Keep changelog up-to-date**

    - Document changes as you make them
    - Don't wait until release time
    - Be specific but concise

3. **Follow semantic versioning**

    - Patch: backwards compatible bug fixes
    - Minor: backwards compatible new features
    - Major: breaking changes

4. **Communicate releases**

    - Announce on project channels
    - Highlight major features
    - Provide upgrade instructions if needed

5. **Schedule releases strategically**
    - Avoid releasing on Fridays
    - Ensure team availability for hotfixes
    - Consider user time zones

## Related Documentation

- [Workflow Guide](workflow.md) - Git workflow and commit conventions
- [Windows Build Guide](../development/windows-build.md) - Local Windows builds
- [macOS Build Guide](../development/macos-build.md) - Local macOS builds
- [Code Quality](../development/code-quality.md) - Testing and quality checks
