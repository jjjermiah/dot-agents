# Dependency Management: TypeScript, Python, R

## Intent

Keep dependency resolution deterministic, cache-friendly, and explicit across
TypeScript, Python, and R workloads.

## TypeScript

```yaml
parameters:
  - name: jsPackageManager
    type: string
    values: [bun, npm]
    default: bun

steps:
  - ${{ if eq(parameters.jsPackageManager, 'bun') }}:
      - script: bun install --frozen-lockfile
        displayName: Install dependencies (bun)
  - ${{ if eq(parameters.jsPackageManager, 'npm') }}:
      - script: npm ci
        displayName: Install dependencies (npm)
```

## Python (pixi)

```yaml
steps:
  - script: pixi install
    displayName: Resolve Python environment
  - script: pixi run test
    displayName: Run Python tests
```

## R (pixi)

```yaml
steps:
  - script: pixi install
    displayName: Resolve R environment
  - script: pixi run r-test
    displayName: Run R tests
```

## Mode Switch

Use one explicit pipeline parameter such as `dependencyMode`:

- `fast`: faster PR feedback where policy allows.
- `locked`: strict reproducibility for post-merge main runs.

Never make dependency mode an implicit global variable.
