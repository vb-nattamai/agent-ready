#!/usr/bin/env python3
"""
MCP-compatible tool: refresh agent-context.json for a target repository.

Usage (standalone):
    python tools/refresh_context.py --target /path/to/repo

Usage (via MCP host):
    Configured in mcp.json — receives JSON-RPC calls from Claude Code / VS Code.
"""

import argparse
import json
import subprocess
import sys


def refresh(target: str, provider: str = "anthropic", dry_run: bool = False) -> dict:
    """Run agent-ready context-only refresh on a target repo."""
    cmd = [
        sys.executable,
        "-m",
        "agent_ready.cli",
        "--target",
        target,
        "--only",
        "context",
        "--force",
    ]
    if provider != "anthropic":
        cmd += ["--provider", provider]
    if dry_run:
        cmd += ["--dry-run"]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "target": target,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh agent-context.json for a repo")
    parser.add_argument("--target", "-t", required=True, help="Path to target repository")
    parser.add_argument(
        "--provider",
        default="anthropic",
        choices=["anthropic", "openai", "google", "groq", "mistral", "together", "ollama"],
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    result = refresh(args.target, provider=args.provider, dry_run=args.dry_run)
    if result["stdout"]:
        print(result["stdout"], end="")
    if not result["success"]:
        print(result["stderr"], file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # MCP JSON-RPC mode: if stdin has JSON, handle as tool call
    if not sys.stdin.isatty():
        try:
            request = json.loads(sys.stdin.read())
            params = request.get("params", {})
            result = refresh(
                target=params.get("target", "."),
                provider=params.get("provider", "anthropic"),
                dry_run=params.get("dry_run", False),
            )
            print(json.dumps({"result": result}))
            sys.exit(0 if result["success"] else 1)
        except (json.JSONDecodeError, KeyError):
            pass
    main()
