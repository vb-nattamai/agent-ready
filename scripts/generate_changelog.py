#!/usr/bin/env python3
"""
Generate a CHANGELOG entry from conventional commits since the last git tag.
Output is printed to stdout and captured by the release workflow.
"""
import subprocess
import sys


def get_commits():
    try:
        last_tag = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        return subprocess.check_output(
            ["git", "log", f"{last_tag}..HEAD", "--format=%s"],
        ).decode()
    except subprocess.CalledProcessError:
        return subprocess.check_output(
            ["git", "log", "HEAD~20..HEAD", "--format=%s"],
        ).decode()


def main():
    commits_raw = get_commits()
    lines = [l.strip() for l in commits_raw.strip().splitlines() if l.strip()]

    added, fixed, changed, breaking, perf = [], [], [], [], []

    for msg in lines:
        # Skip automated version bump commits
        if msg.startswith("chore: bump version"):
            continue
        if msg.startswith("feat"):
            added.append(msg.removeprefix("feat: ").removeprefix("feat"))
        elif msg.startswith("fix"):
            fixed.append(msg.removeprefix("fix: ").removeprefix("fix"))
        elif msg.startswith("perf"):
            perf.append(msg.removeprefix("perf: ").removeprefix("perf"))
        elif msg.startswith("BREAKING CHANGE"):
            breaking.append(msg)
        elif msg.startswith(("docs:", "refactor:", "style:", "test:", "chore:", "ci:")):
            changed.append(msg)

    sections = []

    if added:
        sections.append("### Added\n")
        sections.extend(f"- {item}" for item in added)

    if breaking:
        sections.append("\n### ⚠️ Breaking Changes\n")
        sections.extend(f"- {item}" for item in breaking)

    if fixed:
        sections.append("\n### Fixed\n")
        sections.extend(f"- {item}" for item in fixed)

    if perf:
        sections.append("\n### Performance\n")
        sections.extend(f"- {item}" for item in perf)

    if changed:
        sections.append("\n### Changed\n")
        sections.extend(f"- {item}" for item in changed)

    if not sections:
        sections = ["### Changed\n", "- Minor internal improvements"]

    print("\n".join(sections))


if __name__ == "__main__":
    main()
