# AgentReady

AI coding agents fail in predictable ways.

They hallucinate file paths. They invent APIs. They write code that doesn't compile.

Not because the models are bad.

Because they have no context about your repo.

AgentReady fixes that. It reads your codebase, generates structured context files, and measures whether those files actually improve AI agent behaviour.

> Supports: Claude · OpenAI · Gemini · Groq · Mistral · Together · Ollama

---

## What it generates

| File | Purpose |
|---|---|
| `AGENTS.md` | Operating contract for GitHub Copilot and OpenAI agents |
| `CLAUDE.md` | Auto-loaded by Claude Code at every session start |
| `system_prompt.md` | Universal system prompt for any LLM |
| `agent-context.json` | Machine-readable repo map (static + dynamic sections) |
| `mcp.json` | MCP server configuration |
| `memory/schema.md` | Agent working memory schema |
| `AGENTIC_EVAL.md` | Eval report showing baseline vs with-context scores |

---

## How it works

Three models work in sequence:

1. **Analysis** — reads your codebase. Source files, config, CI, README. Extracts domain concepts, entry points, env vars, known pitfalls.
2. **Generation** — writes all scaffolding files from scratch based on the analysis.
3. **Evaluation** — runs 15 questions against your repo with and without the generated context. Measures whether the context actually helps.

The result is a PR in your repo with all generated files and an eval report showing the improvement.

---

## Quick start

The fastest path is the one-click installer.

1. Go to [Actions → Install AgentReady to Target Repository](https://github.com/vb-nattamai/agent-ready/actions/workflows/install-to-target-repo.yml)
2. Click **Run workflow**
3. Enter your target repo (`owner/repo`), choose your LLM provider
4. Done

The installer pushes a trigger workflow into your repo, opens an issue, adds the `agentic-ready` label, and the transformation starts automatically. A PR appears with all generated files.

---

## Requirements

- Python 3.9+
- An API key for your chosen provider

```bash
# Anthropic (default)
export ANTHROPIC_API_KEY="sk-ant-..."

# OpenAI
export OPENAI_API_KEY="sk-..."

# Google
export GOOGLE_API_KEY="..."

# Groq
export GROQ_API_KEY="..."

# Mistral
export MISTRAL_API_KEY="..."

# Together
export TOGETHER_API_KEY="..."

# Ollama (local, no key needed)
# just have Ollama running
```

---

## Model strategy

AgentReady uses a tiered model strategy. Analysis uses the most capable model. Evaluation uses the cheapest.

| Provider | Analysis | Generation | Evaluation |
|---|---|---|---|
| `anthropic` | claude-opus-4-6 | claude-sonnet-4-6 | claude-haiku-4-5 |
| `openai` | gpt-5.4 | gpt-5.4-mini | gpt-5.4-nano |
| `google` | gemini-2.5-pro | gemini-2.5-pro | gemini-2.5-flash-lite |
| `groq` | llama-3.3-70b | llama-3.3-70b | llama-3.1-8b-instant |
| `mistral` | mistral-large | mistral-large | mistral-small |
| `together` | Qwen3.5-397B | Llama-3.3-70B | Qwen3.5-9B |
| `ollama` | llama3.3 | llama3.3 | llama3.2 |

---

## CLI usage

```bash
git clone https://github.com/vb-nattamai/agent-ready.git
cd agent-ready
pip install -r requirements.txt

# Full transformation
agent-ready --target /path/to/your/repo --provider anthropic

# Preview without writing files
agent-ready --target /path/to/your/repo --dry-run

# Regenerate context only
agent-ready --target /path/to/your/repo --only context --force

# Skip eval
agent-ready --target /path/to/your/repo --eval false

# Quiet mode for CI
agent-ready --target /path/to/your/repo --quiet
```

---

## GitHub Actions

### How the trigger works

The installer pushes a workflow into your target repo that listens for the `agentic-ready` label:

```yaml
on:
  issues:
    types: [labeled]
```

Label-only trigger prevents duplicate runs. When the installer creates an issue and adds the label in one step, GitHub fires both `opened` and `labeled`. Using `labeled` only, the transformation runs exactly once.

**To retrigger**: add the `agentic-ready` label to any issue in your repo.

### What happens when it runs

```
Label added to issue
    |
    +-- 1. Checks actor has write access
    +-- 2. Analysis model reads your codebase (~60s)
    +-- 3. Generation model writes all scaffolding files
    +-- 4. Evaluation model runs 15 questions
    +-- 5. Opens PR: "Add agentic-ready scaffolding"
    +-- 6. Comments on the issue with the PR link
    +-- 7. Closes the issue
```

### Eval as a CI gate

Set `fail_level` in your `agentic-ready.yml` to block PRs below a quality threshold:

```yaml
fail_level: '0.8'  # fail if fewer than 80% of eval questions pass
```

### Required secrets

Add these in your target repo under Settings → Secrets → Actions:

| Secret | When needed |
|---|---|
| `ANTHROPIC_API_KEY` | provider: anthropic (default) |
| `OPENAI_API_KEY` | provider: openai |
| `GOOGLE_API_KEY` | provider: google |
| `GROQ_API_KEY` | provider: groq |
| `MISTRAL_API_KEY` | provider: mistral |
| `TOGETHER_API_KEY` | provider: together |
| `INSTALL_TOKEN` | always — PAT with `repo` + `workflow` scopes |

---

## Keeping context fresh

Repos change. Context goes stale. Two ways to handle it.

**Weekly drift detection** — installed automatically into your target repo. Runs every Monday at 09:00 UTC. Detects structural drift in `agent-context.json` and opens a PR if updates are needed.

**Manual refresh**

```bash
agent-ready --target /path/to/repo --only context --force
```

---

## PR Review Agent

AgentReady includes an LLM-powered PR review agent grounded in your `agent-context.json`.

```bash
agent-ready --target /path/to/repo --review-pr 42
```

Posts APPROVE or REQUEST\_CHANGES directly to GitHub. Available as a workflow template that runs automatically on every pull request in your repo.

---

## The eval report

Every transformation produces `AGENTIC_EVAL.md`. It shows how much the generated context improves AI responses across 15 questions in five categories.

```
AGENTIC EVAL REPORT
--------------------
Category              Baseline    With Context    Delta
Architecture              0.4          0.9        +0.5
Entry points              0.3          1.0        +0.7
Domain concepts           0.2          0.8        +0.6
Potential pitfalls        0.1          0.7        +0.6
Conventions               0.5          0.9        +0.4
--------------------
Overall pass rate:    0.30 -> 0.86   (+0.56)
```

This is the number that tells you whether the context files are actually doing anything.

---

## The agent-context.json split

The generated context map has two sections:

**Static** — you edit this once. Repo name, entry point, restricted paths, environment variables, domain concepts. Never overwritten by the tool.

**Dynamic** — auto-refreshed on every scan. Module layout, last scanned timestamp, agent capabilities.

Your manual edits stay safe. The context stays current.

---

## Supported languages and frameworks

Python (Django, Flask, FastAPI), TypeScript/JavaScript (React, Next.js, Node.js, Express), Java (Spring Boot, Maven, Gradle), Go (Gin, Echo), Rust (Cargo), C#/.NET (ASP.NET), Ruby (Rails).

Generic fallback templates for everything else.

---

## Gitea

Replace `.github/` with `.gitea/`. Identical YAML syntax. The reusable workflow reference becomes:

```yaml
uses: your-gitea.com/vb-nattamai/agent-ready/.gitea/workflows/reusable-transformer.yml@main
```

See [docs/automation.md](docs/automation.md) for full Gitea setup.

---

## Philosophy

- Never modify existing code
- Generate from analysis of what is actually there
- Measure whether the output works, not just whether it exists
- Idempotent: safe to run multiple times
- Every generated file explains what it is and why it exists

---

## Troubleshooting

**Two PRs are created** — your `agentic-ready.yml` uses both `opened` and `labeled`. Change to `labeled` only.

**Workflow not triggering** — confirm the `agentic-ready` label exists in your repo and Actions are enabled under Settings → Actions.

**403 on push** — `INSTALL_TOKEN` has expired or lacks `repo` + `workflow` scopes.

**529 API overloaded** — the transformer retries up to 5 times with increasing waits. If all retries fail, wait 10-15 minutes and retrigger.

---

## Contributing

```bash
git checkout -b feature/your-improvement
git commit -m "feat: description"
git push origin feature/your-improvement
# open a PR
```

Commit prefixes: `feat:` (minor bump), `fix:` (patch bump), `BREAKING CHANGE:` (major bump), `docs:/chore:/style:/test:/refactor:` (no bump).

---

## License

MIT — see [LICENSE](LICENSE) for details.
