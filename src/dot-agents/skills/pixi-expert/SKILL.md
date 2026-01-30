---
name: pixi-expert
description: |
  Advanced pixi for multi-environment and workspace composition. Use when configuring features, solve groups, system requirements, monorepo workspaces, or rattler-build—e.g., "pixi workspace", "multi-environment setup", "CUDA system requirements".
---

# Pixi Expert

## Purpose

Advanced pixi patterns for multi-environment composition, system requirements, and workspace management.

## Multi-Environment Composition

Define multiple environments in one file using **features**.

### Core Concepts

- **Features**: Named sets of dependencies/tasks
- **Environments**: Composed from features
- **Solve Groups**: Ensure consistent versions across environments

### Basic Pattern

```toml
[workspace]
name = "myproject"
channels = ["conda-forge"]
platforms = ["linux-64", "osx-arm64"]

[dependencies]
python = ">=3.10"
numpy = "*"

# Define features
[feature.test.dependencies]
pytest = "*"
pytest-cov = "*"

[feature.test.tasks]
test = "pytest -v --cov"

[feature.dev.dependencies]
ruff = "*"
mypy = "*"

[feature.dev.tasks]
lint = "ruff check ."

# Compose environments
[environments]
default = ["test"]                              # default + test
dev = ["test", "dev"]                           # default + test + dev
prod = { features = [], solve-group = "prod" }  # minimal
test-prod = { features = ["test"], solve-group = "prod" }  # same versions as prod
lint = { features = ["dev"], no-default-feature = true }   # only dev tools
```

### Solve Groups

Use solve groups to keep dependency versions consistent across environments.

```toml
[environments]
prod = { features = [], solve-group = "production" }
test-prod = { features = ["test"], solve-group = "production" }
# Both environments have identical dependency versions
```

### Platform-Specific Features

```toml
[feature.cuda]
platforms = ["linux-64"]
channels = ["nvidia", "conda-forge"]
dependencies = { cuda = "12.*" }

[feature.cuda.system-requirements]
cuda = "12"

[environments]
gpu = ["cuda"]
cpu = []
```

### Usage

```bash
pixi run -e dev test      # Run in dev environment
pixi shell -e prod        # Enter prod shell
pixi install -e gpu       # Install GPU environment
pixi install --all        # Install all environments
```

## System Requirements

Virtual packages (`__linux`, `__cuda`, `__glibc`) declare system capabilities.

### CUDA Configuration

```toml
[system-requirements]
cuda = "12"  # Expected host CUDA driver API version

[feature.gpu.dependencies]
pytorch = "*"
```

### glibc / Linux Version

```toml
[system-requirements]
linux = "4.18"
libc = { family = "glibc", version = "2.28" }
```

### Override via Environment Variables

```bash
export CONDA_OVERRIDE_CUDA=11.8
export CONDA_OVERRIDE_GLIBC=2.17
pixi install
```

### Feature-Specific Requirements

```toml
[feature.gpu]
system-requirements = { cuda = "12" }

[feature.legacy]
system-requirements = { linux = "4.12", libc = { family = "glibc", version = "2.17" } }
```

## Multi-Package Repo

Use separate manifests per package and run commands via `--manifest-path`.

```
repo/
├── packages/
│   ├── core/
│   │   └── pixi.toml
│   └── app/
│       └── pixi.toml
```

### Package Manifest

```toml
[package]
name = "core"
version = "0.1.0"

[dependencies]
requests = "*"
utils = { path = "../utils" }

[tasks]
build = "python -m build"
```

### Commands

```bash
pixi run --manifest-path packages/core/pixi.toml test
pixi install --manifest-path packages/app/pixi.toml
```

## References

- **[references/environments.md](references/environments.md)** - Load when defining features, solve groups, or environment composition.
- **[references/system-requirements.md](references/system-requirements.md)** - Load when dealing with CUDA, glibc, or virtual packages.
- **[references/workspace.md](references/workspace.md)** - Load when structuring multi-package repos or path dependencies.

## Do / Don't

**Do**
- Use Context7 or pixi docs for exact syntax when unsure.
- Keep examples minimal and correct; put deep details in references.

**Don't**
- Use undocumented keys (check docs first).
- Assume parallel task execution without documentation.
