# Security Policy

## Supported Versions

We release security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.3.x   | :white_check_mark: |
| < 1.3   | :x:                |

## Reporting a Vulnerability

We take the security of Alien Invasion seriously. If you discover a security
vulnerability, please follow these steps:

### 1. **Do Not** Publicly Disclose

Please do not open a public issue for security vulnerabilities. Instead, report
them privately.

### 2. Report Via Email

Send details to: **<nacho72001@gmail.com>**

Include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes (optional)

### 3. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Varies by severity (critical issues prioritized)

## Security Measures

### Automated Security Audits

We use automated tools to scan for vulnerabilities:

- **pip-audit**: Weekly scans of Python dependencies
- **GitHub Security Advisories**: Automated alerts for known vulnerabilities
- **Dependabot**: Automatic dependency update PRs

### Running Security Checks Locally

```bash
# Check for known vulnerabilities in dependencies
npm run security:audit

# Attempt automatic fixes
npm run security:audit-fix

# Check for outdated packages
npm run deps:outdated
```

### CI/CD Security

Our CI/CD pipeline includes:

- Security audits on every PR
- Weekly scheduled vulnerability scans
- Automated reports for detected issues

## Dependency Management

### Production Dependencies

Only essential runtime dependencies are included in `requirements.txt`:

- pygame (game engine)
- cryptography (high score encryption)
- Minimal HTTP utilities

### Development Dependencies

Build, test, and documentation tools are separated in `requirements-dev.txt`.

### Update Policy

- **Security patches**: Applied immediately
- **Minor updates**: Reviewed and applied weekly
- **Major updates**: Tested thoroughly before adoption

## High Score Encryption

Player high scores are encrypted using Fernet (symmetric encryption) to prevent
casual tampering:

- Uses `cryptography` library (regularly updated)
- Key derived from password + salt
- Encrypted file stored locally

**Note**: This is not intended as strong security for sensitive data, only to
prevent casual score manipulation.

## Known Limitations

1. **Local Storage**: High scores are stored locally (not cloud-synced)
2. **No Authentication**: Single-player game, no user accounts
3. **No Network Features**: Game runs entirely offline (no multiplayer)

## Security Best Practices for Contributors

### Before Committing

1. Run security audit: `npm run security:audit`
2. Check for hardcoded secrets (API keys, passwords)
3. Validate input data in new features
4. Follow type safety guidelines (mypy strict mode)

### Code Review Checklist

- [ ] No hardcoded credentials
- [ ] No unencrypted sensitive data
- [ ] Dependencies are up-to-date
- [ ] Security audit passes
- [ ] Input validation for user data

## Credits

We acknowledge security researchers who responsibly disclose vulnerabilities:

- (None yet - be the first!)

## Additional Resources

- [Python Security Guide](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Pygame Security Considerations](https://www.pygame.org/docs/)

---

**Last Updated**: January 15, 2026
