---
name: session-start
trigger: At the start of every Claude Code session
---

## Purpose

Load persisted session state and surface key project facts so the agent begins each session with accurate, grounded context for this Flask/pytest Python repository.

## Actions

1. Read `agent-context.json` and validate it against the contract defined in `memory/schema.md`; surface any schema violations as warnings before proceeding.
2. Display the following verified project facts to establish a shared baseline:
   - **Entry point:** `app.py`
   - **Run command:** `python app.py`
   - **Install command:** `pip install -e .` (detected as likely — verify before use)
   - **Test command:** `pytest` (high confidence, sourced from `pyproject.toml [tool.pytest]`)
   - **Python version:** `>=3.11` (sourced from `pyproject.toml requires-python`)
   - **Restricted write paths:** Not determinable from source — fill in `agent-context.json static.restricted_write_paths` after reviewing your repo
3. Emit the following known pitfalls as session-start reminders:
   - The `_greetings` list is module-level global state; it persists across requests within a process but resets on restart, and tests may leak state between test functions if not isolated.
   - Flask's test client must be obtained via `app.test_client()`; importing `app` directly gives you the Flask instance, not a running server.
   - The app uses `@app.get()` shorthand (Flask 2.x+); older Flask versions will raise `AttributeError`.
   - `requirements.txt` includes `httpx` but the app only uses Flask; removing it could break test fixtures.

## Context loaded

- **`agent-context.json`:** Current persisted session state (task progress, open decisions, working notes).
- **`memory/schema.md`:** The session state contract used to validate `agent-context.json` on load.
- **Verified project facts:** entry point, run/install/test commands, Python version requirement, and known pitfalls as listed in Actions above.

## Skipped when

- `AGENT_SKIP_HOOKS=true` environment variable is set.
- `agent-context.json` does not exist yet (first-time setup); in this case the agent should create it in accordance with `memory/schema.md` before proceeding.