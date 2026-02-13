# Template Architecture

## Goal

One core CI template should drive both PR validation and mainline CI.

## File Topology

```text
.
├── azure-pipelines-pr.yml
├── azure-pipelines-main.yml
└── templates/
    ├── ci-core.yml
    ├── deps-typescript.yml
    ├── deps-python.yml
    └── deps-r.yml
```

## Core Template Skeleton

```yaml
# templates/ci-core.yml
parameters:
  - name: runIntegrationTests
    type: boolean
    default: false
  - name: dependencyMode
    type: string
    values: [fast, locked]
    default: locked
  - name: languageMatrix
    type: object
    default:
      typescript: true
      python: true
      r: true

stages:
  - stage: ci
    jobs:
      - job: quality
        steps:
          - checkout: self
          - ${{ if eq(parameters.languageMatrix.typescript, true) }}:
              - template: deps-typescript.yml
                parameters:
                  dependencyMode: ${{ parameters.dependencyMode }}
          - ${{ if eq(parameters.languageMatrix.python, true) }}:
              - template: deps-python.yml
                parameters:
                  dependencyMode: ${{ parameters.dependencyMode }}
          - ${{ if eq(parameters.languageMatrix.r, true) }}:
              - template: deps-r.yml
                parameters:
                  dependencyMode: ${{ parameters.dependencyMode }}
          - script: ./scripts/test-unit.sh

      - ${{ if eq(parameters.runIntegrationTests, true) }}:
          - job: integration
            dependsOn: quality
            steps:
              - script: ./scripts/test-integration.sh
```

## Anti-Patterns

- Duplicating job logic in both entry pipelines.
- Hidden dependency on caller global variables.
- Putting CI trigger logic inside templates.
- Running heavy integration tests by default on PR policy runs.
