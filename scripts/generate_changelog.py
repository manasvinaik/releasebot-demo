import subprocess
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHANGELOG_FILE = ROOT / "CHANGELOG.md"
VERSION_FILE = ROOT / "VERSION"


def get_current_version():
    """Read the current version from VERSION."""
    return VERSION_FILE.read_text(encoding="utf-8").strip()


def get_commits():
    """Get commit messages since the latest version tag."""
    try:
        result = subprocess.run(
            ["git", "log", "--pretty=format:%s", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout.splitlines()

    except subprocess.CalledProcessError:
        return []


def categorize_commits(commits):
    """Categorize commits according to Conventional Commits."""
    categories = {
        "Features": [],
        "Bug Fixes": [],
        "Documentation": [],
        "Tests": [],
        "Refactoring": [],
        "Maintenance": []
    }

    for commit in commits:
        match = re.match(r"(\w+):\s*(.+)", commit)

        if not match:
            continue

        commit_type = match.group(1)
        message = match.group(2)

        if commit_type == "feat":
            categories["Features"].append(message)

        elif commit_type == "fix":
            categories["Bug Fixes"].append(message)

        elif commit_type == "docs":
            categories["Documentation"].append(message)

        elif commit_type == "test":
            categories["Tests"].append(message)

        elif commit_type == "refactor":
            categories["Refactoring"].append(message)

        elif commit_type == "chore":
            categories["Maintenance"].append(message)

    return categories


def generate_section(version, categories):
    """Generate the Markdown section for a release."""
    lines = [
        f"## [{version}]",
        ""
    ]

    for category, commits in categories.items():

        if not commits:
            continue

        lines.append(f"### {category}")
        lines.append("")

        for commit in commits:
            lines.append(f"- {commit}")

        lines.append("")

    return "\n".join(lines)


def update_changelog(new_section):
    """Add the new release section below the changelog title."""
    existing = CHANGELOG_FILE.read_text(encoding="utf-8")

    marker = "All notable changes to this project will be documented in this file."

    if marker in existing:
        parts = existing.split(marker, 1)

        updated = (
            parts[0]
            + marker
            + "\n\n"
            + new_section
            + "\n"
            + parts[1].lstrip()
        )

        CHANGELOG_FILE.write_text(updated, encoding="utf-8")


def main():
    version = get_current_version()

    print(f"Current version: {version}")

    commits = get_commits()

    print(f"Found {len(commits)} commits.")

    categories = categorize_commits(commits)

    new_section = generate_section(version, categories)

    update_changelog(new_section)

    print("CHANGELOG.md updated successfully.")


if __name__ == "__main__":
    main()