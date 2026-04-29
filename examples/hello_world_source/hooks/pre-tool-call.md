---
name: pre-tool-call
trigger: Before any tool call that writes files
---

## Purpose

Guard file-write operations in this Flask/pytest repository by validating the target path against known state and session context before any file is modified.

## Actions

1. Load `agent-context.json` to read current session state (including any restricted write paths recorded at runtime) and load `memory/schema.md` to confirm the session state contract is intact before proceeding with the write.
2. Check the target file path against `restricted_write_paths` from the analysis input — this value is **Not determinable from source — fill in `agent-context.json` static.restricted_write_paths after reviewing your repo**; until that field is populated, log a warning and prompt for confirmation before writing to any path outside the known entry point (`app.py`) or test directory (`tests/`), as those are the only paths confirmed present in the file tree.

## Context loaded

- **`agent-context.json`**: Current session state, including any runtime-recorded restricted write paths and domain concept definitions.
- **`memory/schema.md`**: Session state contract used to validate that `agent-context.json` conforms to the expected schema before its values are trusted.

## Skipped when

- `AGENT_SKIP_HOOKS=true` environment variable is set.
- The tool call is a read-only operation (e.g., file read, search, list) that performs no write to the filesystem.
- The target path has already been validated and approved within the same session turn, as recorded in `agent-context.json`.