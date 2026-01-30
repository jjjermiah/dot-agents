---
name: pixi
description: |
  Base pixi package manager for beginners and essential operations. Use when initializing projects, adding packages, managing environments, or as a conda alternative—e.g., "pixi add numpy", "setup pixi project", "pixi.lock detected", "conda alternative".
---

# Pixi Package Manager

## Purpose

Quick reference for pixi - a cross-platform package manager that unifies conda and PyPI ecosystems. Use docs for any claim about performance.

## Core Concept

Pixi treats your project folder as a **workspace**:
- `pixi.toml` or `pyproject.toml` (manifest)
- `pixi.lock` (reproducible lock file - commit this!)
- `.pixi/` (environment directory - gitignore this)

## Essential Commands

```bash
# Project setup
pixi init                      # New project
pixi init --format pyproject   # Python package

# Dependencies
pixi add numpy pandas          # Conda-forge packages
pixi add --pypi requests       # PyPI packages
pixi remove <package>          # Remove package

# Environment
pixi install                   # Install/sync environment
pixi install --frozen          # Use lock file exactly (CI)
pixi install --locked          # Error if lock outdated
pixi shell                     # Enter environment shell
pixi shell -e <env>            # Specific environment

# Execution
pixi run <command>             # Run in environment
pixi run -e <env> <command>    # Run in specific environment
pixi run <task>                # Run defined task

# Info
pixi info                      # Project/environment info
pixi list                      # Installed packages
```

## Configuration

### pixi.toml (Non-Python projects)

```toml
[workspace]
name = "my-project"
channels = ["conda-forge"]
platforms = ["linux-64", "osx-arm64", "win-64"]

[dependencies]
python = ">=3.10"
numpy = "*"

[pypi-dependencies]
requests = ">=2.28"

[tasks]
start = "python main.py"
test = "pytest"
```

### pyproject.toml (Python packages)

```toml
[project]
name = "my-package"
version = "0.1.0"
dependencies = ["numpy", "pandas"]  # Runtime (PyPI)

[tool.pixi.workspace]
channels = ["conda-forge"]
platforms = ["linux-64"]

[tool.pixi.dependencies]
python = ">=3.10"

[tool.pixi.tasks]
test = "pytest"
```

## Lock File Management

**Always commit `pixi.lock`** to ensure reproducibility.

```bash
pixi install              # Updates lock if manifest changed
pixi install --frozen     # Install from lock without updating it
pixi install --locked     # Error if lock doesn't match manifest
```

## Global Tools

Install CLI tools system-wide (like pipx):

```bash
pixi global install ruff black
pixi global install python=3.11
pixi global list
pixi global update
```

## Environment Variables

Pixi sets automatically:
- `CONDA_PREFIX` - Environment path
- `PIXI_PROJECT_ROOT` - Project directory
- `PIXI_ENVIRONMENT_NAME` - Current environment

## Advanced Topics

For advanced pixi features, consult official docs (or use Context7):
- Multi-environment setup: https://pixi.sh/latest/tutorials/multi_environment/
- Task patterns: https://pixi.sh/latest/workspace/advanced_tasks
- System requirements: https://pixi.sh/latest/workspace/system_requirements/
- Manifest reference: https://pixi.sh/latest/reference/pixi_manifest/

## Quick Patterns

### Docker Integration

```dockerfile
FROM ghcr.io/prefix-dev/pixi:0.41.4 AS build

WORKDIR /app
COPY . .
RUN pixi install --locked -e prod
RUN pixi shell-hook -e prod -s bash > /shell-hook
RUN echo "#!/bin/bash" > /app/entrypoint.sh
RUN cat /shell-hook >> /app/entrypoint.sh
RUN echo 'exec "$@"' >> /app/entrypoint.sh

FROM ubuntu:24.04
WORKDIR /app
COPY --from=build /app/.pixi/envs/prod /app/.pixi/envs/prod
COPY --from=build --chmod=0755 /app/entrypoint.sh /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
```

### GitHub Actions

```yaml
- uses: prefix-dev/setup-pixi@v0.9.2
  with:
    cache: true
- run: pixi run test
```

## Do / Don't

**Do**
- Use pixi docs (or Context7) for exact syntax and versioned behavior.
- Keep `pixi.lock` committed and in sync with the manifest.
- Prefer `pixi run` over manual activation in scripts.

**Don't**
- Claim performance numbers without a source.
- Edit `pixi.lock` by hand.
- Assume undocumented options exist (check docs first).

## Troubleshooting

```bash
pixi info                    # Check environment
pixi install                 # Sync environment
rm -r .pixi && pixi install  # Clean reinstall
```
