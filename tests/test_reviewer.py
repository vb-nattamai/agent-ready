from __future__ import annotations

import json

from agent_ready import reviewer

# ── load_context ──────────────────────────────────────────────────────────────


def test_load_context_returns_none_when_file_missing(tmp_path):
    assert reviewer.load_context(tmp_path) is None


def test_load_context_parses_valid_json(tmp_path):
    ctx = {"static": {"project_name": "X"}, "dynamic": {}}
    (tmp_path / "agent-context.json").write_text(json.dumps(ctx))
    assert reviewer.load_context(tmp_path) == ctx


def test_load_context_returns_none_on_malformed_json(tmp_path):
    (tmp_path / "agent-context.json").write_text("{broken")
    assert reviewer.load_context(tmp_path) is None


# ── truncate_diff ─────────────────────────────────────────────────────────────


def test_truncate_diff_leaves_short_diff_unchanged():
    d = "a" * 100
    assert reviewer.truncate_diff(d, max_chars=200) == d


def test_truncate_diff_truncates_at_limit():
    d = "x" * 5000
    result = reviewer.truncate_diff(d, max_chars=1000)
    assert len(result) < 5000
    assert "truncated" in result


def test_truncate_diff_exact_boundary():
    d = "z" * 1000
    assert reviewer.truncate_diff(d, max_chars=1000) == d


# ── build_review_prompt ───────────────────────────────────────────────────────


def test_build_review_prompt_includes_pr_title():
    meta = {"title": "My unique PR", "body": "", "author": "bob", "files": [], "checks": ""}
    assert "My unique PR" in reviewer.build_review_prompt(None, meta, "")


def test_build_review_prompt_without_context_still_works():
    meta = {"title": "T", "body": "B", "author": "a", "files": ["x.py"], "checks": "SUCCESS"}
    prompt = reviewer.build_review_prompt(None, meta, "diff content")
    assert "diff content" in prompt
    assert "x.py" in prompt


def test_build_review_prompt_includes_restricted_paths():
    ctx = {
        "static": {
            "project_name": "App",
            "description": "",
            "primary_language": "Go",
            "frameworks": [],
            "restricted_write_paths": ["go.sum", ".env"],
            "domain_concepts": [],
        },
        "dynamic": {
            "agent_safe_operations": [],
            "agent_forbidden_operations": [],
            "potential_pitfalls": [],
            "architecture_summary": "",
            "test_command": "",
            "build_command": "",
        },
    }
    meta = {"title": "T", "body": "", "author": "a", "files": [], "checks": ""}
    prompt = reviewer.build_review_prompt(ctx, meta, "")
    assert "go.sum" in prompt
    assert ".env" in prompt


# ── parse_review_response ─────────────────────────────────────────────────────


def test_parse_review_response_approve():
    raw = json.dumps({"decision": "APPROVE", "summary": "ok", "issues": [], "body": "LGTM"})
    r = reviewer.parse_review_response(raw)
    assert r["decision"] == "APPROVE"
    assert r["body"] == "LGTM"


def test_parse_review_response_request_changes():
    raw = json.dumps(
        {
            "decision": "REQUEST_CHANGES",
            "summary": "bugs",
            "issues": [{"severity": "BLOCKER", "file": "a.py", "line": "10", "comment": "bad"}],
            "body": "Fix it.",
        }
    )
    r = reviewer.parse_review_response(raw)
    assert r["decision"] == "REQUEST_CHANGES"
    assert len(r["issues"]) == 1


def test_parse_review_response_strips_markdown_fences():
    inner = json.dumps({"decision": "APPROVE", "summary": "ok", "issues": [], "body": "ok"})
    raw = f"```json\n{inner}\n```"
    r = reviewer.parse_review_response(raw)
    assert r["decision"] == "APPROVE"


def test_parse_review_response_fallback_on_invalid_json():
    r = reviewer.parse_review_response("Not JSON at all.")
    assert r["decision"] == "REQUEST_CHANGES"
    assert r["body"] == "Not JSON at all."


def test_parse_review_response_fixes_invalid_decision():
    raw = json.dumps({"decision": "MAYBE", "body": "hmm"})
    r = reviewer.parse_review_response(raw)
    assert r["decision"] == "REQUEST_CHANGES"


def test_parse_review_response_adds_missing_issues_key():
    raw = json.dumps({"decision": "APPROVE", "summary": "ok", "body": "ok"})
    r = reviewer.parse_review_response(raw)
    assert r["issues"] == []
