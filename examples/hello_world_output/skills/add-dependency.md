---
name: add-dependency
description: Add a new dependency to the project.
---

## When to use this skill

Use this skill when you need to introduce a new Python package dependency to the Flask project.

## Steps

1. Add the new package (with an optional version pin) to `requirements.txt`, one package per line (e.g., `requests==2.31.0`).
2. Install all dependencies, including the newly added one, by running: `pip install -r requirements.txt`
3. Verify the dependency installed correctly by running `pytest` and confirming the package is importable (e.g., `python -c "import <package_name>"`).

## Expected output

- `pip install -r requirements.txt` completes with no errors and prints a line such as `Successfully installed <package-name>-<version>`.
- `pytest` passes with the same results as before the addition (no new failures introduced by the dependency).
- The new package name appears when running `pip show <package_name>`.

## Common failures

- **Package not found on PyPI**: Double-check the package name spelling in `requirements.txt`; use `pip search <name>` or browse [pypi.org](https://pypi.org) to confirm the correct name.
- **Version conflict with existing dependencies**: Review the conflict message printed by pip, adjust the version pin in `requirements.txt` to a compatible range, and re-run `pip install -r requirements.txt`.
- **`requirements.txt` not found**: The repository scaffolding may not yet include the original Flask application files — verify the file exists at the repo root before editing; see the note about missing source files in the project analysis.

## Notes

The repository as analyzed contains only generated AgentReady scaffolding and documentation — the actual `requirements.txt` and Flask application source files may not be present in the visible file tree. Confirm that `requirements.txt` exists at the project root before proceeding, and check the project's documentation if it is missing.