---
name: session-start
trigger: At the start of every Claude Code session
---

## Purpose

Initializes session state for the Flask application by loading persisted agent context and verifying the Python environment is ready for development and testing.

## Actions

1. Load `agent-context.json` to restore the previous session's state, including any in-progress tasks, known issues (such as the `.openapi.yaml.swp` swap file indicating an interrupted edit), and notes about unverified configuration fields (`entry_point`, `test_directory`, `run_command`).
2. Check `memory/schema.md` to confirm the session state contract, then verify the Python environment by confirming `pip install -r requirements.txt` has been run and that `pytest` is available for testing.

## Context loaded

- Current agent state and task continuity from `agent-context.json`
- Session state schema and field contracts from `memory/schema.md`
- Known repository gaps: `entry_point`, `test_directory`, and `run_command` are marked `TODO: verify` and should be resolved early in the session
- Swap file alert: `.openapi.yaml.swp` may indicate the OpenAPI spec was left in an unsaved state and requires inspection

## Skipped when

- `AGENT_SKIP_HOOKS=true` environment variable is set
- `agent-context.json` does not exist yet (first-time repository setup, no prior session to restore)
- The Python virtual environment is already confirmed active and `requirements.txt` has not changed since the last session