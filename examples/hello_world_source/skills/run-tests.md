---
name: run-tests
description: Run the full test suite with project-configured settings.
---

## When to use this skill

Use this skill whenever you need to execute the full test suite to verify correctness of the codebase.

## Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Run the test suite: `pytest`
3. Confirm success by reviewing the terminal summary line — all tests should show as passed with zero errors or failures.

## Expected output

A successful run produces a pytest summary line such as:

```
============================= N passed in X.XXs ==============================
```

No `FAILED`, `ERROR`, or `WARNING` lines should appear for test items.

## Common failures

- **Missing dependencies**: If imports fail or `ModuleNotFoundError` is raised, re-run `pip install -r requirements.txt` and confirm `httpx` is present — it may be required by test fixtures even though the app itself does not use it.
- **State leakage between tests**: The `_greetings` list is module-level global state and persists across test functions within the same process. If tests fail intermittently or produce unexpected data, check that each test function resets or isolates this list before making assertions.
- **Flask version incompatibility**: The app uses `@app.get()` shorthand, which requires Flask 2.x or later. If `AttributeError` is raised on import, upgrade Flask: `pip install --upgrade flask`.
- **Wrong test client usage**: Tests must obtain the Flask test client via `app.test_client()`. Importing `app` directly gives the Flask instance, not a running server — ensure fixtures use `app.test_client()`.