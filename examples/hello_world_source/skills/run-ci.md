---
name: run-ci
description: Trigger or simulate the CI pipeline.
---

## When to use this skill

Use this skill when you need to simulate or verify the full CI pipeline locally before pushing changes.

## Steps

1. Install dependencies: `pip install -e '.[dev]' 2>/dev/null || pip install -r requirements.txt`
2. Run the test suite: `pytest`
3. Confirm all tests pass with no errors or unexpected skips reported in the output.

## Expected output

A successful run shows pytest collecting tests from the `tests` directory, all tests passing, and a final summary line such as `X passed` with no failures, errors, or warnings that indicate broken state.

## Common failures

- **Stale global state between tests**: The `_greetings` list is module-level global state and persists across test functions within the same process. If tests are leaking state into each other, add explicit teardown or reset logic in your test fixtures to clear this list between tests.
- **Wrong Flask version**: The app uses `@app.get()` shorthand which requires Flask 2.x or newer. If you see `AttributeError` on startup or during tests, run `pip show flask` and upgrade if the installed version is older than 2.0.
- **Missing httpx**: `requirements.txt` includes `httpx`, which may be required by test fixtures. Do not remove it without verifying no test depends on it, or tests may fail with `ModuleNotFoundError`.
- **Install command fails**: The editable install (`pip install -e .`) is detected as likely — verify before use. If it fails, fall back to `pip install -r requirements.txt`.
- **Python version mismatch**: This project requires Python `>=3.11`. If pytest fails to collect or import, confirm your active Python version with `python --version`.