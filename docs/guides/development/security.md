# 🔐 Security & Dependency Management

## Overview

Security checks are handled with `pip-audit` and automated via GitHub Actions.
Dependency updates are managed through Dependabot.

## Local Commands

```bash
# Install Python dependencies
npm run deps:install

# Audit for vulnerabilities
npm run security:audit

# Attempt automatic fixes (when available)
npm run security:audit-fix

# Check for outdated packages
npm run deps:outdated
```

## Automated Audits

The `Security Audit` workflow runs on:

- Every PR that changes `requirements.txt`
- Pushes to `main` that touch `requirements.txt`
- Weekly schedule (Monday 09:00 UTC)

Audit reports are uploaded as artifacts in GitHub Actions.

## Dependabot

Dependabot configuration lives in `.github/dependabot.yml` and covers:

- Python dependencies (`pip`)
- npm dependencies
- GitHub Actions

See the [Dependabot Guide](dependabot.md) for details.

## Best Practices

- Keep dependencies pinned in `requirements.txt`.
- Review Dependabot PRs promptly.
- Run `npm run verify` after updates.

## Resources

- [SECURITY.md](../../SECURITY.md)
- [pip-audit documentation](https://pypi.org/project/pip-audit/)
- [Dependabot documentation](https://docs.github.com/en/code-security/dependabot)
