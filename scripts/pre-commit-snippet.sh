#!/bin/sh
# Snippet for manual pre-commit hook installation
# If you already have a pre-commit hook, append the contents of this file

# Installed by AgentReady (https://github.com/vb-nattamai/agent-ready)
# Keeps agent-context.json fresh — re-scans only if source files changed.

CHANGED=$(git diff --cached --name-only | grep -E '\.(py|ts|js|java|go|rs|cs|rb)$')
if [ -z "$CHANGED" ]; then
  exit 0
fi

TOOLKIT=$(git config --get agentic.toolkit-path)
if [ -z "$TOOLKIT" ]; then
  echo "[agentic-ready] Skipping context refresh — agentic.toolkit-path not set."
  echo "  Run: git config agentic.toolkit-path /path/to/agent-ready"
  exit 0
fi

echo "[agentic-ready] Source files changed — refreshing agent-context.json..."
python "$TOOLKIT/scripts/run_transformer.py" --target . --only context --force --quiet

if ! git diff --quiet agent-context.json; then
  git add agent-context.json
  echo "[agentic-ready] agent-context.json updated and staged."
fi
