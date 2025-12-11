#!/usr/bin/env python3
"""
Script to sync CHANGELOG.md to website/changelog.html
Converts markdown changelog entries to HTML format
"""

import re
from pathlib import Path


def parse_changelog(md_content: str) -> list[dict]:
    """Parse CHANGELOG.md and extract version entries"""
    versions = []

    # Find all version sections
    version_pattern = r"## \[v([\d.]+)\] - (\d{4}-\d{2}-\d{2})(.*?)(?=## \[v|\Z)"
    matches = re.finditer(version_pattern, md_content, re.DOTALL)

    for match in matches:
        version = match.group(1)
        date = match.group(2)
        content = match.group(3).strip()

        # Parse sections (Added, Changed, Fixed, etc.)
        sections = {}
        section_pattern = r"### (\w+)\n\n(.*?)(?=### |\Z)"
        section_matches = re.finditer(section_pattern, content, re.DOTALL)

        for section_match in section_matches:
            section_name = section_match.group(1)
            section_content = section_match.group(2).strip()

            # Extract list items
            items = re.findall(r"^- (.+)$", section_content, re.MULTILINE)
            if items:
                sections[section_name] = items

        if sections:
            versions.append({"version": version, "date": date, "sections": sections})

    return versions


def get_section_color(section_name: str) -> str:
    """Get Tailwind color class for section"""
    colors = {
        "Added": "text-green-300",
        "Changed": "text-blue-300",
        "Fixed": "text-yellow-300",
        "Refactored": "text-purple-300",
        "Chore": "text-gray-400",
        "Security": "text-red-300",
        "Documentation": "text-cyan-300",
        "Infrastructure": "text-indigo-300",
    }
    return colors.get(section_name, "text-green-300")


def generate_version_html(version_data: dict) -> str:
    """Generate HTML for a single version entry"""
    version = version_data["version"]
    date = version_data["date"]

    html_parts = [
        '                        <div class="bg-gray-800 rounded-lg p-6">',
        '                            <h3 class="text-2xl font-bold mb-4 text-green-400">',
        f"                                Version {version} - {date}",
        "                            </h3>",
        '                            <div class="space-y-4">',
    ]

    for section_name, items in version_data["sections"].items():
        color = get_section_color(section_name)
        html_parts.extend(
            [
                "                                <div>",
                f'                                    <h4 class="text-xl font-semibold mb-2 {color}">',
                f"                                        {section_name}",
                "                                    </h4>",
                '                                    <ul class="list-disc list-inside space-y-2 text-gray-300">',
            ]
        )

        for item in items:
            html_parts.append(f"                                        <li>{item}</li>")

        html_parts.extend(
            [
                "                                    </ul>",
                "                                </div>",
            ]
        )

    html_parts.extend(
        [
            "                            </div>",
            "                        </div>",
        ]
    )

    return "\n".join(html_parts)


def update_website_changelog() -> bool:
    """Update website/changelog.html from CHANGELOG.md"""
    print("📝 Syncing CHANGELOG.md to website...")

    # Read CHANGELOG.md
    changelog_path = Path("CHANGELOG.md")
    if not changelog_path.exists():
        print("❌ CHANGELOG.md not found")
        return False

    md_content = changelog_path.read_text(encoding="utf-8")
    versions = parse_changelog(md_content)

    if not versions:
        print("❌ No versions found in CHANGELOG.md")
        return False

    print(f"✓ Found {len(versions)} versions")

    # Read current changelog.html
    html_path = Path("website/changelog.html")
    if not html_path.exists():
        print("❌ website/changelog.html not found")
        return False

    html_content = html_path.read_text(encoding="utf-8")

    # Find the changelog content section
    start_marker = '<div class="card rounded-xl p-8 max-w-4xl mx-auto">\n                    <div class="space-y-8">'
    end_marker = "                    </div>\n                </div>\n            </section>"

    start_idx = html_content.find(start_marker)
    end_idx = html_content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("❌ Could not find changelog section in HTML")
        return False

    # Generate new content
    versions_html = []
    for version_data in versions:
        versions_html.append(generate_version_html(version_data))

    new_content = start_marker + "\n" + "\n".join(versions_html) + "\n" + end_marker

    # Replace content
    new_html = html_content[:start_idx] + new_content + html_content[end_idx + len(end_marker) :]

    # Write back
    html_path.write_text(new_html, encoding="utf-8")

    print(f"✓ Updated website/changelog.html with {len(versions)} versions")
    return True


if __name__ == "__main__":
    success = update_website_changelog()
    exit(0 if success else 1)
