# 🤖 legacy-to-agentic-ready

**A toolkit you drop onto any existing repository to generate all scaffolding files that make it understandable and operable by AI agents — without hallucinations, without invented paths, without breaking existing code.**

> **Supports:** Claude · OpenAI · Gemini · Any LLM

---

## Why This Exists

AI coding agents (Copilot, Claude Code, Cursor, Aider, etc.) work **dramatically better** when a repository contains structured context files that describe:

- What the repo does and how it's organized
- Where key files live and what they contain
- What tools, APIs, and conventions are available
- How to build, test, and deploy

Without these files, agents hallucinate paths, invent APIs, and produce code that doesn't compile. **This toolkit fixes that.**

---

## What It Generates

When you run the transformer on your repository, it produces:

| File | Purpose | Platform |
|------|---------|----------|
| `AGENTS.md` | Agent instruction file | GitHub Copilot / OpenAI |
| `CLAUDE.md` | Agent instruction file | Claude Code / Anthropic |
| `system_prompt.md` | Universal system prompt | Any LLM |
| `agent-context.json` | Machine-readable repo map | All platforms |
| `mcp.json` | MCP server configuration | Claude / MCP-compatible |
| `tool.*.template.*` | Tool scaffolds (Python, TS, Java, Go) | All platforms |

---

## Quick Start

### 1. Clone this toolkit

```bash
git clone https://github.com/YOUR_ORG/legacy-to-agentic-ready.git
cd legacy-to-agentic-ready
```

### 2. Run the transformer against your target repo

```bash
python scripts/run_transformer.py --target /path/to/your/repo
```

### 3. Review and commit the generated files

The transformer will:
1. **Scan** your repository structure, languages, and frameworks
2. **Generate** platform-specific agent instruction files
3. **Create** a machine-readable context map (`agent-context.json`)
4. **Scaffold** tool templates matching your repo's languages
5. **Output** all files into your target repo (no existing files are modified)

---

## Repository Structure

```
legacy-to-agentic-ready/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── .github/
│   └── agents/
│       └── repo-to-agentic.agent.md   # GitHub Copilot agent definition
├── .claude/
│   └── agents/
│       └── repo-to-agentic.agent.md   # Claude Code agent definition
├── prompts/
│   └── repo-to-agentic-universal.md   # Universal LLM prompt
├── templates/
│   ├── agent-context.template.json    # Repo context map template
│   ├── AGENTS.template.md             # GitHub/OpenAI agent instructions
│   ├── CLAUDE.template.md             # Claude agent instructions
│   ├── system_prompt.template.md      # Universal system prompt
│   ├── mcp.template.json              # MCP server config template
│   ├── tool.python.template.py        # Python tool scaffold
│   ├── tool.typescript.template.ts    # TypeScript tool scaffold
│   ├── tool.java.template.java        # Java tool scaffold
│   └── tool.go.template.go            # Go tool scaffold
└── scripts/
    └── run_transformer.py             # Main transformer script
```

---

## Usage Modes

### Mode 1: Full Automation (Recommended)

```bash
python scripts/run_transformer.py --target /path/to/repo
```

Scans the repo and generates all applicable files.

### Mode 2: Selective Generation

```bash
# Only generate AGENTS.md and CLAUDE.md
python scripts/run_transformer.py --target /path/to/repo --only agents

# Only generate tool templates
python scripts/run_transformer.py --target /path/to/repo --only tools

# Only generate the context map
python scripts/run_transformer.py --target /path/to/repo --only context
```

### Mode 3: Dry Run

```bash
python scripts/run_transformer.py --target /path/to/repo --dry-run
```

Shows what would be generated without writing any files.

### Mode 4: Use as an AI Agent

Copy `.github/agents/repo-to-agentic.agent.md` or `.claude/agents/repo-to-agentic.agent.md` into your repo and let your AI agent run the transformation interactively.

---

## Supported Languages & Frameworks

The transformer auto-detects:

- **Python** (Django, Flask, FastAPI, scripts)
- **TypeScript / JavaScript** (React, Next.js, Node.js, Express)
- **Java** (Spring Boot, Maven, Gradle)
- **Go** (standard library, Gin, Echo)
- **Rust** (Cargo-based projects)
- **C# / .NET** (ASP.NET, console apps)
- **Ruby** (Rails, gems)
- And more via generic fallback templates

---

## Philosophy

1. **Never modify existing code** — only add new files
2. **Never hallucinate** — all generated content is derived from actual repo analysis
3. **Platform-agnostic** — generates files for every major AI agent platform
4. **Idempotent** — safe to run multiple times; existing generated files are updated, not duplicated
5. **Transparent** — every generated file includes a header explaining what it is and why it exists

---

## Contributing

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/my-improvement`)
3. Commit your changes (`git commit -am 'Add new template for X'`)
4. Push to the branch (`git push origin feature/my-improvement`)
5. Open a Pull Request

---

## License

MIT — see [LICENSE](LICENSE) for details.
