"""Basic smoke tests for agent_ready.cli.

Run with:
    python3 -m pytest tests/ -v
or after pip install:
    pytest
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure the package is importable when running tests from the repo root
# (no pip install needed)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import agent_ready  # noqa: E402
from agent_ready.cli import (  # noqa: E402
    RepoAnalyzer,
    score,
    TOOLKIT_ROOT,
    TEMPLATES_DIR,
)


# ── Package metadata ───────────────────────────────────────────────────────

def test_version_format():
    """version string must be semver (x.y.z)."""
    parts = agent_ready.__version__.split(".")
    assert len(parts) == 3
    assert all(p.isdigit() for p in parts)


# ── Path resolution ────────────────────────────────────────────────────────

def test_toolkit_root_exists():
    """TOOLKIT_ROOT must resolve to the repo root (contains pyproject.toml)."""
    assert (TOOLKIT_ROOT / "pyproject.toml").exists(), (
        f"TOOLKIT_ROOT ({TOOLKIT_ROOT}) does not contain pyproject.toml"
    )


def test_templates_dir_exists():
    """TEMPLATES_DIR must exist and contain core template files."""
    assert TEMPLATES_DIR.is_dir()
    required = [
        "agent-context.template.json",
        "AGENTS.template.md",
        "CLAUDE.template.md",
        "mcp.template.json",
        "system_prompt.template.md",
    ]
    for name in required:
        assert (TEMPLATES_DIR / name).exists(), f"Missing template: {name}"


# ── RepoAnalyzer — language detection ─────────────────────────────────────

def test_detect_languages_python(tmp_path):
    (tmp_path / "main.py").write_text("print('hello')")
    (tmp_path / "requirements.txt").touch()
    analyzer = RepoAnalyzer(tmp_path)
    metadata = analyzer.analyze()
    assert "Python" in metadata.get("primary_languages", []) or \
           "Python" in metadata.get("languages", {})


def test_detect_languages_java(tmp_path):
    java_dir = tmp_path / "src" / "main" / "java"
    java_dir.mkdir(parents=True)
    (java_dir / "App.java").write_text("public class App {}")
    (tmp_path / "pom.xml").write_text("<project/>")
    analyzer = RepoAnalyzer(tmp_path)
    metadata = analyzer.analyze()
    langs = metadata.get("primary_languages", []) or list(metadata.get("languages", {}).keys())
    assert "Java" in langs


def test_analyzer_empty_dir(tmp_path):
    """Analyzer must not crash on an empty directory."""
    metadata = RepoAnalyzer(tmp_path).analyze()
    assert isinstance(metadata, dict)


# ── RepoAnalyzer — framework detection ────────────────────────────────────

def test_detect_frameworks_fastapi(tmp_path):
    (tmp_path / "requirements.txt").write_text("fastapi==0.110.0\nuvicorn")
    metadata = RepoAnalyzer(tmp_path).analyze()
    assert "FastAPI" in metadata.get("frameworks", [])


def test_detect_frameworks_spring(tmp_path):
    pom = """<project>
  <parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
  </parent>
</project>"""
    (tmp_path / "pom.xml").write_text(pom)
    metadata = RepoAnalyzer(tmp_path).analyze()
    assert "Spring Boot" in metadata.get("frameworks", [])


# ── Scoring ────────────────────────────────────────────────────────────────

def test_score_returns_dict(tmp_path):
    result = score(tmp_path)
    assert "score" in result
    assert "max" in result
    assert "rows" in result
    assert isinstance(result["score"], int)
    assert result["score"] <= result["max"]


def test_score_improves_with_context(tmp_path):
    """A repo with agent-context.json scores higher than one without."""
    base = score(tmp_path)
    context = {
        "project_name": "test-project",
        "primary_languages": ["Python"],
        "frameworks": ["FastAPI"],
        "entry_point": "main.py",
        "test_command": "pytest",
        "build_system": "pip",
        "environment_variables": [{"name": "PORT", "required": True}],
        "last_scanned": "2026-01-01T00:00:00Z",
    }
    (tmp_path / "agent-context.json").write_text(json.dumps(context))
    with_context = score(tmp_path)
    assert with_context["score"] > base["score"]


# ── Shim backward compatibility ────────────────────────────────────────────

def test_shim_is_runnable():
    """scripts/run_transformer.py must be a thin shim delegating to the package."""
    shim = TOOLKIT_ROOT / "scripts" / "run_transformer.py"
    assert shim.exists()
    src = shim.read_text()
    assert "from agent_ready.cli import main" in src
