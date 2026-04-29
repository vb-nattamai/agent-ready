---
name: add-dependency
description: Add a new dependency to the project.
---

## When to use this skill

Use this skill whenever a new third-party package needs to be added to the project and recorded so other contributors and environments can install it.

## Steps

1. Install the new package and add it to `requirements.txt` manually, or install it directly:
   ```
   pip install <package-name>
   ```
2. Add the package (with a pinned or minimum version) to `requirements.txt` so it is tracked:
   ```
   echo "<package-name>==<version>" >> requirements.txt
   ```
3. If the project uses `pyproject.toml` for metadata (confirmed present), also add the dependency under the appropriate `[project] dependencies` or `[project.optional-dependencies]` section in `pyproject.toml`.
4. Re-run the install step to verify the environment is consistent:
   ```
   pip install -r requirements.txt
   ```
   (Install command detected as likely: `pip install -e .` — verify before use against your `pyproject.toml`.)
5. Run the test suite to confirm nothing is broken:
   ```
   pytest
   ```

## Expected output

- `pip install <package-name>` completes without errors and reports the installed version.
- `pip install -r requirements.txt` exits cleanly with no conflicts or resolution errors.
- `pytest` exits with all tests passing and no import errors related to the new or existing packages.

## Common failures

- **Version conflict**: A newly added package conflicts with an existing dependency (e.g., `httpx` is already present in `requirements.txt` for test fixtures — adding a package that pins a conflicting version of `httpx` will cause resolver errors). Run `pip check` after installation to surface conflicts, then adjust version constraints.
- **Package added to `requirements.txt` but not `pyproject.toml`**: If the project is installed in editable mode (`pip install -e .`), packages listed only in `requirements.txt` may not be included in the package's declared metadata. Verify both files are updated if `pyproject.toml` declares dependencies.
- **Tests pass locally but fail in CI**: The new package may not be pinned, leading to a different version being resolved in a clean environment. Pin the version explicitly in `requirements.txt` after confirming the correct version locally.
- **`pytest` reports `ModuleNotFoundError`**: The package was not installed into the active virtual environment. Confirm the correct environment is active and re-run `pip install -r requirements.txt`.

## Notes

- `requirements.txt` includes `httpx`, which is noted as likely intended for integration tests rather than the application itself. Do not remove it when editing the file, as doing so may break test fixtures.
- The project requires Python `>=3.11` (from `pyproject.toml`). Ensure any new dependency supports this version range before adding it.