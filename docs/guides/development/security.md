# Security & Dependency Management

This document explains how we handle security and dependency management in the
Alien Invasion project.

## Quick Start

```bash
# Install all dependencies
npm run deps:install
# Or: pip install -r requirements.txt

# Check for security vulnerabilities
npm run security:audit

# Fix vulnerabilities automatically (when possible)
npm run security:audit-fix

# Check for outdated dependencies
npm run deps:outdated
```

## Dependency File

### `requirements.txt` (Unified)

Contains **all** project dependencies in a single file, organized by category:

**Runtime Dependencies** (~10 packages):

- pygame (game engine)
- cryptography (high score encryption)
- Network utilities (requests, urllib3, certifi, etc.)

**Development Dependencies** (~94 packages):

- Testing (pytest, pytest-cov, coverage)
- Code quality (black, isort, flake8, mypy)
- Documentation (mkdocs, mkdocs-material)
- Build tools (pyinstaller, py2app, setuptools)
- Security auditing (pip-audit)

**Total**: ~104 packages **Purpose**: Single source of truth for all
dependencies **Management**: Automated updates via Dependabot

## Security Auditing

### Automated Scans

We run automated security audits:

1. **On Every PR**: Checks dependencies for known vulnerabilities
2. **Weekly Schedule**: Monday at 9:00 AM UTC
3. **Manual Trigger**: Via GitHub Actions workflow

### Viewing Audit Reports

Audit reports are uploaded as artifacts in GitHub Actions:

1. Go to Actions tab
2. Select "Security Audit" workflow
3. Download the audit report artifact

### Local Security Checks

```bash
# Quick audit (recommended)
npm run security:audit

# Audit with detailed descriptions
pip-audit -r requirements.txt --desc

# Attempt automatic fixes
npm run security:audit-fix

# Generate markdown report
pip-audit -r requirements.txt --format markdown > security-report.md
```

## Updating Dependencies

### Security Updates (High Priority)

When vulnerabilities are detected:

1. **Automatic PR**: Dependabot/Renovate creates PR (if configured)
2. **Manual Update**:

    ```bash
    pip install --upgrade <package-name>
    # Update requirements.txt with new version
    npm run security:audit  # Verify fix
    ```

### Regular Updates

Check for outdated packages:

```bash
npm run deps:outdated
```

Update carefully:

1. Review changelog for breaking changes
2. Update version in requirements file
3. Test thoroughly (`npm run verify`)
4. Commit with conventional commit message

## CI/CD Integration

### GitHub Actions Workflows

, manual

- **Actions**:
    - Audits all dependencies in requirements.txt
    - Fails build if vulnerabilities found
    - Uploads detailed report as artifact
    - Comments on PR with vulnerability details

#### Dependency Installation in CI/CD

All workflows use the unified requirements.txt:

```yaml
- name: Install dependencies
  run: |
      python -m pip install --upgrade pip
      pip install -r requirements.txt
      python -m pip install --upgrade pip
      pip install -r requirements.txt
      pip install -r requirements-dev.txt  # Add this for dev workflows
```

## Vulnerability Response Process

### 1. Detection

- Automated: GitHub Actions flags vulnerability
- Manual: Developer runs `npm run security:audit`

### 2. Assessment

- Review vulnerability details (CVE, GHSA)
- Check affected versions
- Determine severity (Critical, High, Medium, Low)

### 3. Remediation

```bash
# Attempt automatic fix
npm run security:audit-fix

# Manual fix if needed
pip install --upgrade <vulnerable-package>
# Update requirements.txt
npm run verify  # Ensure nothing broke
```

### 4. Verification

```bash
npm run security:audit  # Should show "No known vulnerabilities found"
npm run test           # All tests pass
npm run verify         # Complete quality check
```

### 5. Documentation

Update requirements.txt with comments explaining the fix:

```python
# Updated to fix CVE-YYYY-XXXXX (description)
package==X.Y.Z
```

## Best Practices

Dependabot Integration

### Automated Dependency Updates

Dependabot is configured to automatically:

- Check for updates every Monday at 9:00 AM UTC
- Create grouped PRs for related packages
- Separate security updates for high visibility
- Label PRs appropriately (dependencies, python, npm, github-actions)

**Configuration**: `.github/dependabot.yml`

**Grouped Updates**: or Dependabot PRs

- Don't install packages globally
- Don't use `pip install --upgrade` blindly on all packages
- Don't commit untested dependency updates
- Don't disable security workflows
- Don't manually update dependencies that Dependabot manages
- Don't merge Dependabot PRs without CI passing

See [Dependabot Guide](dependabot.md) for detailed configuration guide.

## Best Practices

### ✅ Do's

- Keep dependencies up-to-date via Dependabot
- Review and merge security PRs immediately
- Run security audits before each release
- Document security-related updates in requirements.txt
- Use specific version pinning (`package==X.Y.Z`)
- Review changelogs before major version updates
- Let Dependabot handle routine

### ❌ Don'ts

- Don't ignore security warnings
- Don't install packages globally
- Don't use `pip install --upgrade` blindly on all packages
- Don't commit untested dependency updates
- Don't disable security workflows

## Known Vulnerabilities (Resolved)

### January 15, 2026 - Security Update

**Affected Packages**: redirect/decompression vulnerabilities)

- `requests 2.32.3` → `2.32.5` (fixed .netrc credentials leak)
- `black 24.2.0` → `24.3.0` (fixed security issue)
- `pymdown-extensions 10.15` → `10.16.1` (fixed CVE)
- `setuptools 75.3.0` → `78.1.1` (fixed security issue)

**CVEs Fixed** (11 total):

**Runtime Dependencies**:

- CVE-2024-12797, GHSA-h4gh-qq45-vh27 (cryptography - OpenSSL)
- CVE-2025-50182, CVE-2025-50181, CVE-2025-66418, CVE-2025-66471, CVE-2026-21441
  (urllib3 - 5 CVEs)
- CVE-2024-47081 (requests - netrc leak)

**Development Dependencies**:

- PYSEC-2024-48 (black)
- CVE-2025-68142 (pymdown-extensions)
- PIntegration with Development Workflow

### Daily Development

```bash
# 1. Pull latest changes
git pull origin main

# 2. Install/update dependencies
npm run deps:install

# 3. Check for vulnerabilities
npm run security:audit

# 4. Work on features...

# 5. Before committing
npm run verify  # Includes all quality checks
```

### Handling Dependabot PRs

1. **Review PR description** - Check changelog and breaking changes
2. **Wait for CI** - All checks must pass
3. **Security PRs** - Merge immediately if CI is green
4. **Regular PRs** - Review changelog, merge if no breaking changes
5. **Major updates** - Test locally before merging

## Resources

- [pip-audit documentation](https://pypi.org/project/pip-audit/)
- [Dependabot documentation](https://docs.github.com/en/code-security/dependabot)
- [Python Security Advisories](https://github.com/pypa/advisory-database)
- [GitHub Security Advisories](https://github.com/advisories)
- [NIST NVD](https://nvd.nist.gov/)
- [SECURITY.md](../../SECURITY.md) - Project security policy
- [Dependabot Guide](dependabot.md) - Dependabot configuration

---

**Last Updated**: January 15, 2026
