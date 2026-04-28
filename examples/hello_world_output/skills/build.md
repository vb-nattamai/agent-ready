---
name: build
description: Build the project artifacts.
---

## When to use this skill

Use this skill when you need to install dependencies and prepare the Flask project for local development or deployment.

## Steps

1. Install all project dependencies: `pip install -r requirements.txt`
2. Verify the entry point exists — check for `app.py` or another Flask application file in the repository root (entry point was not confirmed in analysis; inspect the directory if uncertain).
3. Confirm installation succeeded by running `pip list` and checking that Flask and all expected packages appear without errors.

## Expected output

A successful run looks like:

```
Collecting flask
  Downloading flask-x.x.x-py3-none-any.whl
...
Successfully installed flask-x.x.x <other packages>
```

`pip list` will show Flask and all dependencies listed in `requirements.txt` as installed in the current environment.

## Common failures

- **`requirements.txt` not found**: The application source files may not be present — the repository may contain only scaffolding. Verify that `requirements.txt` exists in the working directory before running the install command.
- **`.openapi.yaml` corruption**: A swap file (`.openapi.yaml.swp`) was detected, indicating the OpenAPI spec may have been left in an unsaved edit state. Resolve or remove the swap file before relying on any spec-driven tooling.
- **Dependency conflicts or version errors**: Create and activate a virtual environment first (`python -m venv .venv && source .venv/bin/activate`) then re-run `pip install -r requirements.txt` to isolate the environment.