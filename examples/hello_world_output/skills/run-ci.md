---
name: run-ci
description: Trigger or simulate the CI pipeline.
---

## When to use this skill

Use this skill when you need to validate the project locally by running the full install, build, and test sequence as it would execute in CI.

## Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Run the test suite: `pytest`
3. Confirm all tests pass by reviewing the final pytest summary line (e.g., `X passed in Xs`)

## Expected output

A successful run produces output similar to:

```
collected X items

tests/test_*.py ....                          [100%]

============================== X passed in 0.XXs ==============================
```

No errors, no failures, and no warnings that halt execution.

## Common failures

- **Missing `requirements.txt`**: The file tree did not confirm the presence of `requirements.txt` — if `pip install -r requirements.txt` fails, verify the file exists at the repository root and check the project's documentation for the correct dependency file name.
- **No tests discovered by pytest**: If pytest reports `no tests ran`, the test directory location is unconfirmed (`TODO: verify` in analysis) — locate the test files manually and run `pytest <test_directory>` explicitly.
- **Swap file conflict on `.openapi.yaml`**: A `.openapi.yaml.swp` file exists, indicating an interrupted edit — resolve or remove the swap file before running any step that parses the OpenAPI spec to avoid stale or corrupt data.
- **`app.py` or entry point not found**: The application source files were not confirmed in the file tree — if tests import the Flask app and fail with `ModuleNotFoundError`, verify the entry point location before re-running `pytest`.