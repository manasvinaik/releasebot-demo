import subprocess
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHANGELOG_FILE = ROOT / "CHANGELOG.md"


def run_git_command(command):
    """Run a Git command and return its output."""
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True
    )

    return result.stdout.strip()


def get_last_tag():
    """Return the most recent Git tag."""
    try:
        return run_git_command(
            ["git", "describe", "--tags", "--abbrev=0"]
        )
    except subprocess.CalledProcessError:
        return None


def get_commits_since_last_tag():
    """Get commits made since the last release tag."""

    last_tag = get_last_tag()

    if last_tag:
        command = [
            "git",
            "log",
            f"{last_tag}..HEAD",
            "--pretty=format:%s"
        ]
    else:
        command = [
            "git",
            "log",
            "--pretty=format:%s"
        ]

    try:
        output = run_git_command(command)

        if not output:
            return []

        return output.splitlines()

    except subprocess.CalledProcessError:
        return []


def categorize_commits(commits):
    """Categorize Conventional Commits."""

    categories = {
        "Features": [],
        "Bug Fixes": [],
        "Documentation": [],
        "Tests": [],
        "Refactoring": [],
        "Maintenance": []
    }

    for commit in commits:

        match = re.match(
            r"^(feat|fix|docs|test|refactor|chore):\s*(.+)",
            commit
        )

        if not match:
            continue

        commit_type = match.group(1)
        message = match.group(2)

        category_map = {
            "feat": "Features",
            "fix": "Bug Fixes",
            "docs": "Documentation",
            "test": "Tests",
            "refactor": "Refactoring",
            "chore": "Maintenance"
        }

        category = category_map[commit_type]

        categories[category].append(message)

    return categories


def generate_section(version, categories):
    """Generate a Markdown section for the new release."""

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
    """Insert the new release at the top of CHANGELOG.md."""

    existing = CHANGELOG_FILE.read_text(encoding="utf-8")

    marker = (
        "All notable changes to this project "
        "will be documented in this file."
    )

    if marker not in existing:
        raise ValueError(
            "Could not find the changelog header."
        )

    parts = existing.split(marker, 1)

    updated = (
        parts[0]
        + marker
        + "\n\n"
        + new_section
        + "\n"
        + parts[1].lstrip()
    )

    CHANGELOG_FILE.write_text(
        updated,
        encoding="utf-8"
    )


def main():

    if len(sys.argv) != 2:
        print("Usage: python scripts/generate_changelog.py VERSION")
        return

    version = sys.argv[1]

    commits = get_commits_since_last_tag()

    if not commits:
        print("No new commits found.")
        return

    categories = categorize_commits(commits)

    new_section = generate_section(
        version,
        categories
    )

    update_changelog(new_section)

    print("CHANGELOG.md updated successfully.")


if __name__ == "__main__":
    main()