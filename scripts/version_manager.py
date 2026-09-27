import subprocess
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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


def get_current_version():
    """Get the latest release version from Git tags."""

    try:
        tag = run_git_command(
            ["git", "describe", "--tags", "--abbrev=0"]
        )

        return tag.lstrip("v")

    except subprocess.CalledProcessError:
        return "1.0.0"


def get_commits_since_last_tag():

    try:

        last_tag = run_git_command(
            ["git", "describe", "--tags", "--abbrev=0"]
        )

        output = run_git_command(
            [
                "git",
                "log",
                f"{last_tag}..HEAD",
                "--pretty=format:%s"
            ]
        )

    except subprocess.CalledProcessError:

        output = run_git_command(
            ["git", "log", "--pretty=format:%s"]
        )

    if not output:
        return []

    return output.splitlines()


def calculate_next_version():

    current = get_current_version()

    major, minor, patch = map(
        int,
        current.split(".")
    )

    commits = get_commits_since_last_tag()

    has_feature = False
    has_fix = False

    for commit in commits:

        if re.match(r"^feat(\(.+\))?:", commit):
            has_feature = True

        elif re.match(r"^fix(\(.+\))?:", commit):
            has_fix = True

    if has_feature:
        minor += 1
        patch = 0

    elif has_fix:
        patch += 1

    else:
        patch += 1

    return f"{major}.{minor}.{patch}"


if __name__ == "__main__":

    version = calculate_next_version()

    print(version)