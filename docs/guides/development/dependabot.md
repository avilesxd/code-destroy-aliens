# Dependabot Configuration Guide

## What is Dependabot?

Dependabot is GitHub's automated dependency update tool that:

- 🔍 Scans your dependencies for updates
- 🔒 Checks for security vulnerabilities
- 🤖 Automatically creates Pull Requests with updates
- 📊 Groups related updates together

## Configuration Overview

Our Dependabot setup (`.github/dependabot.yml`) monitors:

### 1. Python Dependencies (`pip`)

- **Schedule**: Weekly on Mondays at 09:00 UTC
- **File**: `requirements.txt`
- **Max PRs**: 10 open at once

**Grouped Updates**:

- **Development tools**: pytest, black, isort, flake8, mypy
- **Documentation**: mkdocs, Markdown, Jinja2
- **Build tools**: pyinstaller, py2app, setuptools
- **Security**: cryptography, urllib3, requests, certifi (always separate for
  visibility)

### 2. npm Dependencies

- **Schedule**: Weekly on Mondays at 09:00 UTC
- **File**: `package.json`
- **Max PRs**: 5 open at once
- All updates grouped together

### 3. GitHub Actions

- **Schedule**: Weekly on Mondays at 09:00 UTC
- **Files**: `.github/workflows/*.yml`
- **Max PRs**: 5 open at once
- Automatically updates action versions (e.g., `actions/checkout@v3` → `@v4`)

## How It Works

### 1. Automated Detection

Every Monday at 9 AM, Dependabot:

1. Checks for dependency updates
2. Compares with latest versions
3. Identifies security vulnerabilities
4. Creates PRs for updates

### 2. Pull Request Creation

Each PR includes:

- **Title**: `chore: bump <dependency> from X.Y.Z to A.B.C`
- **Description**: Changelog, commits, release notes
- **Labels**: `dependencies`, `python`/`javascript`/`github-actions`
- **Compatibility**: Passes all CI checks

### 3. Your Action Required

When a PR is created:

1. **Review the changelog** - Check for breaking changes
2. **Wait for CI** - All tests must pass
3. **Test locally** (optional for major updates):

    ```bash
    git fetch origin
    git checkout dependabot/pip/package-name
    npm run verify
    ```

4. **Merge** - Use "Squash and merge"

## Grouping Strategy

### Why Group Updates?

Instead of 10 separate PRs for pytest, pytest-cov, coverage, etc., you get **1
PR** with all testing tools updated together.

**Benefits**:

- ✅ Fewer PRs to review
- ✅ Related updates tested together
- ✅ Cleaner git history

**Example Groups**:

```yaml
development-dependencies:
    # One PR updates: pytest, black, isort, flake8, mypy

documentation:
    # One PR updates: mkdocs, mkdocs-material, Jinja2

build-tools:
    # One PR updates: pyinstaller, py2app, setuptools
```

### Security Updates (Always Separate)

Security-related packages are **never grouped**:

- cryptography
- urllib3
- requests
- certifi

This ensures security updates are highly visible and can be merged immediately.

## Handling Dependabot PRs

### ✅ Safe to Auto-Merge

- Patch updates (1.2.3 → 1.2.4)
- Development dependencies
- GitHub Actions minor updates

### ⚠️ Requires Review

- Minor updates (1.2.3 → 1.3.0)
- Security updates (read advisory)
- Grouped PRs (test together)

### 🚨 Requires Testing

- Major updates (1.2.3 → 2.0.0)
- Core runtime dependencies (pygame, cryptography)
- Breaking changes mentioned in changelog

### Example Workflow

```bash
# 1. Dependabot creates PR "chore: bump pytest from 8.4.1 to 8.5.0"

# 2. CI runs automatically (tests, lint, typecheck)

# 3. Review changelog on PR

# 4. If all green and no breaking changes → Merge

# 5. If unsure, test locally:
git fetch origin
git checkout dependabot/pip/pytest
npm run verify
```

## Ignored Updates

We ignore major version updates for:

- **pygame**: Breaking changes in major versions
- **python**: Requires manual testing

To change this, edit `.github/dependabot.yml`:

```yaml
ignore:
    - dependency-name: 'pygame'
      update-types: ['version-update:semver-major']
```

## Customization

### Change Schedule

```yaml
schedule:
    interval: 'daily' # daily, weekly, monthly
    day: 'monday' # For weekly
    time: '09:00' # UTC
```

### Change PR Limit

```yaml
open-pull-requests-limit: 20 # Default is 5
```

### Disable a Package Ecosystem

Comment out the ecosystem section:

```yaml
# - package-ecosystem: "npm"  # Disabled
```

## Troubleshooting

### "Too many open PRs"

Increase the limit or merge/close existing PRs:

```yaml
open-pull-requests-limit: 15
```

### "Update failed"

Common causes:

- Dependency conflict (check error in PR)
- Package not found (deprecated/renamed)
- Version constraint in requirements.txt too strict

Fix: Update requirements.txt manually or close the PR.

### "Security update not created"

Check:

1. Is the package in your `requirements.txt`?
2. Is it in an `ignore` rule?
3. Check GitHub Security Advisories tab

## Best Practices

### ✅ Do

- Review PRs weekly
- Merge security updates quickly
- Keep open PR count low
- Test major updates locally
- Read changelogs for breaking changes

### ❌ Don't

- Ignore security updates
- Let PRs accumulate
- Auto-merge without CI passing
- Skip testing major version bumps
- Disable Dependabot without good reason

## Monitoring

### View Dependabot Activity

1. Go to **Insights** → **Dependency graph** → **Dependabot**
2. See all open/closed PRs
3. Check update frequency
4. View security alerts

### GitHub Notifications

Configure in GitHub Settings:

- **Watch** → **Custom** → **Dependabot alerts**

## Integration with Our Security Workflow

Dependabot works alongside:

1. **Security Audit Workflow** (`.github/workflows/security-audit.yml`)
    - Runs weekly
    - Scans with `pip-audit`
    - Creates vulnerability reports

2. **Manual Commands**:

    ```bash
    npm run security:audit        # Check vulnerabilities
    npm run deps:outdated         # List outdated packages
    ```

**Flow**:

```
Security Audit detects CVE
    ↓
Dependabot creates PR with fix
    ↓
CI runs automatically
    ↓
You review and merge
    ↓
Next audit shows "No vulnerabilities"
```

## Resources

- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Configuration Options](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file)
- [Security Policy](../../SECURITY.md)
- [Security & Dependency Management](security.md)

---

**Last Updated**: January 15, 2026
