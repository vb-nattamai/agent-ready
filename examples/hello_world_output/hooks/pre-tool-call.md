---
name: pre-tool-call
trigger: Before any tool call that writes files
---

## Purpose

Validate write targets and load current session state before any file-writing operation to prevent unintended modifications in this Flask/Python repository.

## Actions

1. Load `agent-context.json` to verify current session state and confirm the intended write target aligns with the active task scope before proceeding.
2. Check `memory/schema.md` to enforce the session state contract and confirm no restricted write paths are being violated — note that `restricted_write_paths` is currently empty for this repo, but any `.openapi.yaml.swp` swap file conflicts should be flagged before writes to OpenAPI-related files proceed.

## Context loaded

- `agent-context.json`: Current agent session state, active task, and file scope boundaries.
- `memory/schema.md`: Session state contract defining valid write patterns and memory constraints.

## Skipped when

- `AGENT_SKIP_HOOKS=true` environment variable is set.
- The tool call is read-only (e.g., `read_file`, `list_directory`, `search`) and performs no write operation.
- The write target is a temporary file within a system temp directory unrelated to the repository source tree.