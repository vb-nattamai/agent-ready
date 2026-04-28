---
name: post-test
trigger: After running the test command
---

## Purpose

After `pytest` completes, this hook captures test results and updates session state so the agent can make informed decisions about next steps in the Flask application development workflow.

## Actions

1. Parse the `pytest` exit code and output to determine pass/fail status, number of tests collected, and any failure summaries; store results in `agent-context.json` under a `last_test_run` key.
2. Cross-reference `memory/schema.md` to validate that the updated `agent-context.json` conforms to the session state contract before persisting, then surface a concise test summary (e.g., `X passed, Y failed, Z errors`) to the agent for immediate decision-making.

## Context loaded

- Current session state from `agent-context.json` (including prior test run history, active task, and any pending flags).
- Session state contract from `memory/schema.md` to ensure the written test result structure matches expected schema fields.
- `pytest` stdout/stderr output and exit code from the completed test run.

## Skipped when

- `AGENT_SKIP_HOOKS=true` environment variable is set.
- The `pytest` command was not the test command that triggered this lifecycle point (e.g., a custom runner was invoked directly outside the standard `test_command` configuration).
- `agent-context.json` is missing or unreadable, preventing state persistence without risking data loss.