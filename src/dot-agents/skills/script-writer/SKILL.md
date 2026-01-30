---
name: script-writer
description: |
  Write production-ready one-off scripts and automation utilities with proper error handling and safety patterns. Use when developing bash automation, Python CLI tools, shell scripts, system administration scripts, or command-line batch processing—e.g., "write a script to process files", "python one-liner for data conversion", "bash automation for backups", "shell script with error handling".
---

# Script Writer Skill

## Purpose

Provide concise, safe, and reproducible scripting guidance with language-specific references for Bash and Python.

## General Script Guidelines
- Favor safety: default to non-destructive behavior unless explicitly requested.
- Make scripts idempotent where practical; avoid repeated side effects.
- Handle errors explicitly; fail fast with clear messages.
- Use clear logging to stderr for errors, stdout for normal output.
- Return meaningful exit codes (0 success, non-zero on failure).
- Ensure deterministic behavior (sorted output, fixed locale, stable randomness if used).
- Validate inputs (types, ranges, required args) and handle missing/invalid values.
- Minimize dependencies; document required tools and versions.
- Use safe defaults; require explicit confirmation for destructive operations.
- Avoid secrets in code, logs, or examples; use env vars or files by request.
- Aim for reproducible execution environments (pin major versions; document toolchain).

## Output
- Provide the script contents.
- Include usage notes (how to run, required flags, examples).
- State assumptions (OS, dependencies, required files/paths).

## References (Load on Demand)

- **[references/bash-scripts.md](references/bash-scripts.md)** - Load for Bash/shell scripts, shebang patterns, or strict mode
- **[references/python-scripts.md](references/python-scripts.md)** - Load for Python scripts or Pixi shebang execution

If language is ambiguous, ask a clarifying question before choosing a reference.
