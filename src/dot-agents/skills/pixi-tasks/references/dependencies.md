# Dependencies Reference

Task chains, dependency graphs, workflow orchestration.

## Contents

- [Basic Dependencies](#basic-dependencies)
- [Dependency Patterns](#dependency-patterns)
- [Feature-Based Dependencies](#feature-based-dependencies)
- [Complex Workflows](#complex-workflows)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)
- [Common Issues](#common-issues)

## Basic Dependencies

```toml
[tasks]
setup = "mkdir -p build"
build = { cmd = "make", depends-on = ["setup"] }
```

## Dependency Patterns

### Linear Chain

```toml
[tasks]
fetch = "git submodule update --init"
configure = { cmd = "./configure", depends-on = ["fetch"] }
build = { cmd = "make", depends-on = ["configure"] }
test = { cmd = "make test", depends-on = ["build"] }
```

### Diamond Pattern

```toml
[tasks]
setup = "mkdir -p build"
fetch-data = { cmd = "curl -o data.csv ...", depends-on = ["setup"] }
fetch-model = { cmd = "curl -o model.pkl ...", depends-on = ["setup"] }
train = { cmd = "python train.py", depends-on = ["fetch-data", "fetch-model"] }
```

Execution: setup → fetch-data/fetch-model → train (order by dependencies)

### Fan-Out / Fan-In

```toml
[tasks]
setup = "echo 'Starting'"

lint = { cmd = "ruff check .", depends-on = ["setup"] }
typecheck = { cmd = "mypy src/", depends-on = ["setup"] }
format = { cmd = "ruff format --check .", depends-on = ["setup"] }

test = { cmd = "pytest", depends-on = ["lint", "typecheck", "format"] }
deploy = { cmd = "./deploy.sh", depends-on = ["test"] }
```

## Feature-Based Dependencies

```toml
[feature.build.dependencies]
cmake = "*"

[feature.build.tasks]
configure = "cmake -B build"
compile = { cmd = "cmake --build build", depends-on = ["configure"] }

[environments]
build = ["build"]

[tasks]
ci-build = { depends-on = [{ task = "compile", environment = "build" }] }
```

## Complex Workflows

### CI/CD Pipeline

```toml
[tasks]
install = "pixi install --frozen"

lint = { cmd = "ruff check .", depends-on = ["install"] }
format = { cmd = "ruff format --check .", depends-on = ["install"] }
types = { cmd = "mypy src/", depends-on = ["install"] }

unit-test = { cmd = "pytest tests/unit", depends-on = ["lint", "format", "types"] }
int-test = { cmd = "pytest tests/integration", depends-on = ["unit-test"] }

build = { cmd = "python -m build", depends-on = ["int-test"] }

ci = { depends-on = ["build"] }
```

### Data Pipeline

```toml
[tasks]
fetch = "python fetch_data.py"
clean = { cmd = "python clean.py", depends-on = ["fetch"] }
validate = { cmd = "python validate.py", depends-on = ["clean"] }
features = { cmd = "python features.py", depends-on = ["validate"] }
train = { cmd = "python train.py", depends-on = ["features"] }
evaluate = { cmd = "python eval.py", depends-on = ["train"] }

pipeline = { depends-on = ["evaluate"] }
```

## Error Handling

### Fail-Fast

```toml
[tasks]
lint = "ruff check ."
test = { cmd = "pytest", depends-on = ["lint"] }  # Won't run if lint fails
```

### Continue-On-Error

```toml
[tasks]
lint = "ruff check . || echo 'Lint warnings'"
test = { cmd = "pytest", depends-on = ["lint"] }  # Runs even with warnings
```

## Best Practices

1. **Keep dependencies explicit** - Clear chain
2. **Name tasks by action** - `install-deps`, `compile-sass`
3. **Group related tasks** - Setup, build, quality
4. **Use aggregator tasks** - `ci`, `lint`, `test-all`

### Aggregator Pattern

```toml
[tasks]
lint-py = "ruff check ."
lint-js = "eslint src/"
lint-md = "markdownlint docs/"

lint = { depends-on = ["lint-py", "lint-js", "lint-md"] }

ci = { depends-on = ["lint", "test", "build"] }
```

## Common Issues

**Circular Dependencies**:
```toml
# Bad
a = { cmd = "...", depends-on = ["b"] }
b = { cmd = "...", depends-on = ["a"] }  # Error!
```

**Missing Dependencies**:
```toml
# Bad: implicit dependency
configure = "cmake -B build"
build = "cmake --build build"  # May fail!

# Good: explicit
build = { cmd = "cmake --build build", depends-on = ["configure"] }
```

**Redundant Dependencies**:
```toml
# Bad: "a" is redundant (transitive via "b")
c = { cmd = "...", depends-on = ["a", "b"] }

# Good: only direct dependencies
c = { cmd = "...", depends-on = ["b"] }
```
