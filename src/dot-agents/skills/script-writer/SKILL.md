---
name: script-writer
description: |
  Write production-ready one-off scripts and automation utilities with proper error handling and safety patterns. Use when developing bash automation, Python CLI tools, shell scripts, system administration scripts, or command-line batch processing—e.g., "write a script to process files", "python one-liner for data conversion", "bash automation for backups", "shell script with error handling".
---

# Script Writer Skill

## Purpose

Provide concise, safe, and reproducible scripting guidance with language-specific references for Bash and Python.

## Core Principles

Scripts without safety measures fail in production. Every time. We write scripts that protect our systems and data.

## General Script Guidelines

**Safety requirements** (Never compromise):
- **YOU MUST default to non-destructive behavior** unless explicitly requested.
- **YOU MUST handle errors explicitly**; fail fast with clear messages.
- **YOU MUST validate all inputs** (types, ranges, required args); never assume valid data.
- **YOU MUST use safe defaults**; require explicit confirmation for destructive operations.
- **YOU MUST NEVER include secrets** in code, logs, or examples; use env vars or files by request.

**Quality standards** (Always follow):
- **Always** make scripts idempotent where practical; avoid repeated side effects.
- **Always** use clear logging: stderr for errors, stdout for normal output.
- **Always** return meaningful exit codes (0 success, non-zero on failure).
- **Always** ensure deterministic behavior (sorted output, fixed locale, stable randomness if used).
- **Always** minimize dependencies; document required tools and versions.
- **Always** document assumptions (OS, dependencies, required files/paths).

## Output Requirements

Before delivering the script, confirm:
1. **YOU MUST** provide complete script contents ready to run.
2. **YOU MUST** include usage notes (how to run, required flags, examples).
3. **YOU MUST** state all assumptions explicitly.

## References (Load on Demand)

- **[references/bash-scripts.md](references/bash-scripts.md)** - Load immediately for Bash/shell scripts, shebang patterns, or strict mode
- **[references/python-scripts.md](references/python-scripts.md)** - Load immediately for Python scripts or Pixi shebang execution

**YOU MUST ask a clarifying question** if the target language is ambiguous before choosing a reference. No exceptions.
