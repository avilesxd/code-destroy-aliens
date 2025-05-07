# Version Control

## Version Files

The project maintains its version information in the following files:

- `version.txt` - Main version file
- `version_macOS.txt` - macOS specific version

## Version Format

We follow the [Semantic Versioning](https://semver.org/) standard (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

## How to Update Version

1. Update the version number in both version files simultaneously:

   ```bash
   echo "X.Y.Z" > version.txt
   echo "X.Y.Z" > version_macOS.txt
   ```

2. Create a new git tag: `git tag vX.Y.Z`
3. Push the tag: `git push origin vX.Y.Z`

## Release Process

1. Update version numbers in both version files
2. Update CHANGELOG.md with new changes
3. Create a new release on GitHub
4. Tag the release with the new version
5. Generate release notes from CHANGELOG.md

## Best Practices

- Maintain detailed change log in CHANGELOG.md
- Strictly follow semantic versioning
- Document important changes in each version
- Ensure git tags match versions in files
- Keep version files synchronized across platforms
- Always update both version files simultaneously to maintain consistency

## Examples

### Minor Version Update

```bash
# Update both version files simultaneously
echo "1.1.0" > version.txt
echo "1.1.0" > version_macOS.txt

# Create and push tag
git tag v1.1.0
git push origin v1.1.0
```

### Patch Version Update

```bash
# Update both version files simultaneously
echo "1.0.1" > version.txt
echo "1.0.1" > version_macOS.txt

# Create and push tag
git tag v1.0.1
git push origin v1.0.1
```

## References

- [Semantic Versioning](https://semver.org/)
- [Git Tags Guide](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
- [Versioning Best Practices](https://keepachangelog.com/)
