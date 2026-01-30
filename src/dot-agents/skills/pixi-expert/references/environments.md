# Environments Reference

Deep dive into multi-environment composition with features and solve groups.

## Contents

- [Feature Definition Patterns](#feature-definition-patterns)
- [Environment Composition Patterns](#environment-composition-patterns)
- [Solve Group Strategies](#solve-group-strategies)
- [Common Environment Setups](#common-environment-setups)
- [CLI Commands](#cli-commands)

## Feature Definition Patterns

### Basic Feature

```toml
[feature.test.dependencies]
pytest = "*"
pytest-cov = "*"

[feature.test.tasks]
test = "pytest -v"
```

### Feature with PyPI Dependencies

```toml
[feature.dev.pypi-dependencies]
black = "*"
isort = "*"
```

### Feature with Platform Restrictions

```toml
[feature.gpu]
platforms = ["linux-64"]
channels = ["nvidia", "conda-forge"]
dependencies = { cuda = "12.*" }
```

## Environment Composition Patterns

### Development Stack

```toml
[environments]
minimal = { features = [] }
dev = { features = ["test"] }
full = { features = ["test", "dev", "docs"] }
lint = { features = ["dev"], no-default-feature = true }
```

### Production Testing

```toml
[environments]
prod = { features = [], solve-group = "production" }
test-prod = { features = ["test"], solve-group = "production" }
staging = { features = ["monitoring"], solve-group = "production" }
```

### GPU/CPU Split

```toml
[feature.cuda]
platforms = ["linux-64"]
dependencies = { pytorch = "*", cuda = "*" }
system-requirements = { cuda = "12" }

[feature.cpu]
dependencies = { pytorch = "*" }

[environments]
gpu = ["cuda"]
cpu = ["cpu"]
```

## Solve Group Strategies

### Single Solve Group (Recommended)

All environments share same dependency versions:

```toml
[environments]
dev = { features = ["test", "dev"], solve-group = "main" }
prod = { features = [], solve-group = "main" }
test-prod = { features = ["test"], solve-group = "main" }
```

### Multiple Solve Groups

Different environments can have different versions:

```toml
[environments]
bleeding = { features = ["test"], solve-group = "latest" }
stable = { features = ["test"], solve-group = "stable" }
```

## Common Environment Setups

### Data Science Project

```toml
[dependencies]
python = ">=3.10"
numpy = "*"
pandas = "*"

[feature.jupyter.dependencies]
jupyterlab = "*"

[feature.viz.dependencies]
matplotlib = "*"
seaborn = "*"

[feature.ml.dependencies]
scikit-learn = "*"

[feature.gpu.dependencies]
tensorflow = "*"

[environments]
default = ["jupyter", "viz"]
ml = ["jupyter", "viz", "ml"]
ml-gpu = ["jupyter", "viz", "ml", "gpu"]
```

### Web Application

```toml
[dependencies]
python = ">=3.11"
fastapi = "*"
uvicorn = "*"

[feature.dev.dependencies]
pytest = "*"
httpx = "*"

[feature.dev.tasks]
dev = "uvicorn main:app --reload"

[feature.prod.tasks]
serve = "gunicorn main:app"

[environments]
dev = ["dev"]
prod = ["prod"]
```

### Library Development

```toml
[feature.test.dependencies]
pytest = "*"
pytest-cov = "*"

[feature.lint.dependencies]
ruff = "*"
mypy = "*"

[feature.docs.dependencies]
mkdocs = "*"

[feature.build.dependencies]
build = "*"
twine = "*"

[environments]
ci = ["test", "lint"]
dev = ["test", "lint", "docs"]
release = ["build", "test"]
```

## CLI Commands

```bash
pixi info                    # List environments
pixi run -e <env> <cmd>      # Run in environment
pixi shell -e <env>          # Enter shell
pixi install -e <env>        # Install specific
pixi install --all           # Install all
```
