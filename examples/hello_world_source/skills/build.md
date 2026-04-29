---
name: build
description: Build the project artifacts.
---

## When to use this skill

Use this skill when you need to install the project and its dependencies so the application and tests are ready to run.

## Steps

1. Install the project and its dependencies:
   ```
   pip install -e '.[dev]' 2>/dev/null || pip install -r requirements.txt
   ```
2. Confirm the entry point is present: verify `app.py` exists in the repository root.
3. Validate the installation succeeded by running the test suite:
   ```
   pytest
   ```

## Expected output

- The install step completes without errors, reporting successful installation of Flask and all listed dependencies (including `httpx`).
- `pytest` discovers and runs tests from the `tests/` directory with no collection errors, indicating the installed package is importable and the environment is correctly set up.

## Common failures

- **`pip install -e '.[dev]'` fails with "No such file or directory" or missing `pyproject.toml`/`setup.py`**: The editable install target is not available; the fallback `pip install -r requirements.txt` will run automatically due to the `||` in the build command. Confirm `requirements.txt` exists in the repository root.
- **`AttributeError` on `@app.get()`**: This shorthand requires Flask 2.x or newer. The installed Flask version is older than required. Upgrade with `pip install --upgrade flask` and confirm the installed version meets the `>=3.11` Python requirement noted for this project.
- **State leakage between tests**: The `_greetings` list is module-level global state and persists across test functions within the same process. If tests fail intermittently due to unexpected list contents, ensure each test function resets or isolates this state before asserting.
- **`httpx` missing causes test fixture errors**: `requirements.txt` includes `httpx` as a dependency intended for integration tests. If `httpx` is removed or not installed, test fixtures may fail. Re-run the install command to restore it.