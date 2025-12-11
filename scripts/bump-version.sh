#!/bin/bash
# Script local para bump de versión (alternativa al workflow)

set -e

# Colors
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Check arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 {patch|minor|major}"
    exit 1
fi

TYPE=$1
if [[ ! "$TYPE" =~ ^(patch|minor|major)$ ]]; then
    echo "Error: Invalid version type. Use: patch, minor, or major"
    exit 1
fi

echo -e "${CYAN}🚀 Bumping version ($TYPE)...${NC}"

# Get current version from package.json
CURRENT_VERSION=$(node -p "require('./package.json').version")
echo -e "${YELLOW}Current version: $CURRENT_VERSION${NC}"

# Calculate new version
IFS='.' read -r -a version_parts <<< "$CURRENT_VERSION"
major="${version_parts[0]}"
minor="${version_parts[1]}"
patch="${version_parts[2]}"

case $TYPE in
    major)
        major=$((major + 1))
        minor=0
        patch=0
        ;;
    minor)
        minor=$((minor + 1))
        patch=0
        ;;
    patch)
        patch=$((patch + 1))
        ;;
esac

NEW_VERSION="$major.$minor.$patch"
echo -e "${GREEN}New version: $NEW_VERSION${NC}"

# Update package.json
npm version $NEW_VERSION --no-git-tag-version

# Update generate-version.py
sed -i "s/VERSION = \".*\"/VERSION = \"$NEW_VERSION\"/" tools/generate-version.py

# Generate version files
echo -e "\n${CYAN}📝 Generating version files...${NC}"
python tools/generate-version.py

# Update CHANGELOG.md
DATE=$(date +%Y-%m-%d)
TEMP_FILE=$(mktemp)

cat > $TEMP_FILE << EOF
# Changelog

All notable changes to this project will be documented in this file.

## [v$NEW_VERSION] - $DATE

### Added

- Version bump to $NEW_VERSION

### Changed

### Fixed

### Refactored

### Chore

---

EOF

# Skip first 6 lines (header) of old changelog
tail -n +7 CHANGELOG.md >> $TEMP_FILE
mv $TEMP_FILE CHANGELOG.md

echo -e "\n${GREEN}✅ Version bumped successfully!${NC}"
echo -e "\n${CYAN}Next steps:${NC}"
echo "1. Edit CHANGELOG.md to add detailed release notes"
echo "2. Review changes: git status"
echo "3. Commit: git add . && git commit -m 'chore: bump version to $NEW_VERSION'"
echo "4. Create tag: git tag -a v$NEW_VERSION -m 'Release v$NEW_VERSION'"
echo "5. Push: git push origin main --tags"
echo ""
echo "Or use the GitHub workflow instead: gh workflow run version-bump.yml"
