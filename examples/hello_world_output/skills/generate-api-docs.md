---
name: generate-api-docs
description: Generate or update API documentation from the OpenAPI spec.
---

## When to use this skill

Use this skill whenever the OpenAPI spec has been modified and the generated API documentation needs to be refreshed or created for the first time.

## Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Locate the OpenAPI spec file (`.openapi.yaml`) in the repository root — confirm it is not a swap file (`.openapi.yaml.swp`) left from an interrupted edit, and resolve any in-progress edits before proceeding.
3. Generate or update the API docs from the OpenAPI spec using your doc generation tool (e.g., `redoc-cli`, `swagger-codegen`, or a project-specific script — Command not determinable from source — check your project's documentation).
4. Validate the output by opening the generated documentation and confirming all endpoints, request/response schemas, and descriptions match the current spec.

## Expected output

A successful run produces up-to-date human-readable API documentation (HTML, Markdown, or equivalent) that accurately reflects every path, method, parameter, and schema defined in `.openapi.yaml`. No errors or warnings are emitted during generation, and the output files are written to the expected docs directory.

## Common failures

- **Swap file present (`.openapi.yaml.swp`)**: A prior edit to the OpenAPI spec was interrupted. Remove the swap file (`rm .openapi.yaml.swp`), verify `.openapi.yaml` is complete and valid YAML, then re-run the generation step.
- **Missing dependencies**: If the doc generation tool is not found, run `pip install -r requirements.txt` and confirm the tool is listed there; if it is a separate Node/Ruby tool, install it per that tool's own instructions.
- **Invalid OpenAPI spec**: If the generator reports schema validation errors, lint the spec with a validator (e.g., `swagger-parser` or `redocly lint .openapi.yaml`), fix the reported issues, and re-run.
- **Entry point or source files not found**: The application source (e.g., `app.py`) may not be present in the working tree — confirm the full repository has been checked out and is not showing only scaffolding files before attempting doc generation.