# Typed Parameters and Template APIs

## Principle

Treat templates as strict APIs. Every expected input must be declared and typed.

## Preferred Types

- `stepList`: controlled caller step injection.
- `jobList`: reusable job packs and test suites.
- `stageList`: environment progression templates.
- `object`: nested config payloads.

In templates, use `object` where `stringList` would otherwise be tempting.

## jobList with templateContext

```yaml
# templates/test-suites.yml
parameters:
  - name: suites
    type: jobList

jobs:
  - ${{ each suite in parameters.suites }}:
      - job: ${{ suite.job }}
        displayName: ${{ suite.templateContext.displayName }}
        steps:
          - script: echo "tier=${{ suite.templateContext.tier }}"
          - ${{ suite.steps }}
```

```yaml
# caller
extends:
  template: templates/test-suites.yml
  parameters:
    suites:
      - job: smoke
        templateContext:
          displayName: Smoke tests
          tier: quick
        steps:
          - script: ./scripts/test-smoke.sh
      - job: integration
        templateContext:
          displayName: Integration tests
          tier: heavy
        steps:
          - script: ./scripts/test-integration.sh
```

## Contract Checklist

- Parameter name, type, default, and constraints are explicit.
- No undeclared global variable dependencies.
- Optional extension points are typed and bounded.
