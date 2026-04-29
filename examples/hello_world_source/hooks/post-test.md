---
name: post-test
trigger: After running the test command
---

## Purpose

After `pytest` completes, capture the outcome and update session state so the agent can decide whether to proceed with commits, surface failures, or flag state-isolation issues specific to this repo's module-level `_greetings` global.

## Actions

1. Read `agent-context.json` and `memory/schema.md` to load current session state and the session state contract, then record the test run result (pass/fail, exit code) into the session state under the schema defined in `memory/schema.md`.
2. If `pytest` exited non-zero, surface the failure to the agent and flag the known pitfall: the module-level `_greetings` list in `app.py` is global state that persists across requests within a process — tests may be leaking state between test functions if isolation fixtures are not in place; the agent should inspect the `tests/` directory for missing teardown or fixture resets before re-running `pytest`.

## Context loaded

- Current session state and history from `agent-context.json`.
- Session state contract (field names, types, allowed values) from `memory/schema.md`.
- Test run exit code and whether the failure is new or recurring within this session.

## Skipped when

- `AGENT_SKIP_HOOKS=true` environment variable is set.
- The test command was not `pytest` (i.e., a different test runner was invoked directly, bypassing the verified test command from `pyproject.toml`).
- `agent-context.json` is absent or unreadable, as session state cannot be updated without a valid context file.