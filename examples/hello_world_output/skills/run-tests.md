---
name: run-tests
description: Run the full test suite with project-configured settings.
---

## When to use this skill

Use this skill whenever you need to execute the full test suite to verify correctness after making changes to the codebase.

## Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Run the test suite: `pytest`
3. Review the output in the terminal — confirm all tests pass with no errors or failures reported.

## Expected output

A successful run produces output similar to:

```
collected N items

... (test results) ...

======= N passed in X.XXs =======
```

All tests should show as `passed` with zero `failed`, `error`, or `warning` entries in the summary line.

## Common failures

- **Missing dependencies**: If `pytest` or Flask-related imports fail, re-run `pip install -r requirements.txt` to ensure all packages are installed, then retry `pytest`.
- **Test directory not found / no tests collected**: The test directory location is not confirmed in the current scaffolding — check your project documentation or search for `test_*.py` or `*_test.py` files and ensure they exist under the expected path before running.
- **Swap file conflict (`.openapi.yaml.swp`)**: A swap file indicates the OpenAPI spec may have been mid-edit. Close any open editor sessions holding that file and remove the swap file (`rm .openapi.yaml.swp`) if it is stale, then re-run tests.
- **`requirements.txt` not found**: The source files may not be fully present — verify the repository checkout is complete and that `requirements.txt` exists at the project root before running the install command.