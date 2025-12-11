# Script local para bump de versión (alternativa al workflow)
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('patch', 'minor', 'major')]
    [string]$Type
)

Write-Host "🚀 Bumping version ($Type)..." -ForegroundColor Cyan

# Get current version from package.json
$packageJson = Get-Content "package.json" -Raw | ConvertFrom-Json
$currentVersion = $packageJson.version
Write-Host "Current version: $currentVersion" -ForegroundColor Yellow

# Calculate new version
$versionParts = $currentVersion.Split('.')
$major = [int]$versionParts[0]
$minor = [int]$versionParts[1]
$patch = [int]$versionParts[2]

switch ($Type) {
    'major' {
        $major++
        $minor = 0
        $patch = 0
    }
    'minor' {
        $minor++
        $patch = 0
    }
    'patch' {
        $patch++
    }
}

$newVersion = "$major.$minor.$patch"
Write-Host "New version: $newVersion" -ForegroundColor Green

# Update package.json
npm version $newVersion --no-git-tag-version

# Update generate-version.py
$generateVersionPath = "tools\generate-version.py"
$content = Get-Content $generateVersionPath -Raw
$content = $content -replace 'VERSION = ".*"', "VERSION = `"$newVersion`""
Set-Content $generateVersionPath $content -NoNewline

# Generate version files
Write-Host "`n📝 Generating version files..." -ForegroundColor Cyan
python tools\generate-version.py

# Update CHANGELOG.md
$date = Get-Date -Format "yyyy-MM-dd"
$changelogPath = "CHANGELOG.md"
$oldChangelog = Get-Content $changelogPath -Raw

$newEntry = @"
# Changelog

All notable changes to this project will be documented in this file.

## [v$newVersion] - $date

### Added

- Version bump to $newVersion

### Changed

### Fixed

### Refactored

### Chore

---

"@

# Skip first 6 lines (header) of old changelog
$oldLines = (Get-Content $changelogPath)
$oldContent = $oldLines | Select-Object -Skip 6 | Out-String
$newChangelog = $newEntry + $oldContent.TrimStart()
Set-Content $changelogPath $newChangelog.TrimEnd()

Write-Host "`n✅ Version bumped successfully!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Edit CHANGELOG.md to add detailed release notes"
Write-Host "2. Review changes: git status"
Write-Host "3. Commit: git add . && git commit -m 'chore: bump version to $newVersion'"
Write-Host "4. Create tag: git tag -a v$newVersion -m 'Release v$newVersion'"
Write-Host "5. Push: git push origin main --tags"
Write-Host "`nOr use the GitHub workflow instead: gh workflow run version-bump.yml"
