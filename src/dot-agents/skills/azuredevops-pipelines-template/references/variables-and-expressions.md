# Variables and Expressions

## Timing Model

- `${{ }}` template expression:
  - Compile-time.
  - Use for template structure (`if`, `each`, template insertion).
  - Accesses parameters and static variables.
- `$[ ]` runtime expression:
  - Runtime.
  - Use for `condition:` and runtime-calculated variables.
  - Does not access template parameters.
- `$( )` macro:
  - Runtime before each task.
  - Use inside scripts and task inputs.

## Side-by-Side Example

```yaml
parameters:
  - name: runPerf
    type: boolean
    default: false

variables:
  staticVar: "ci"
  isMain: $[eq(variables['Build.SourceBranch'], 'refs/heads/main')]

jobs:
  - job: build
    steps:
      - script: echo "mode=${{ variables.staticVar }} build=$(Build.BuildId)"

  - ${{ if eq(parameters.runPerf, true) }}:
      - job: perf
        condition: and(succeeded(), eq(variables.isMain, 'True'))
        steps:
          - script: echo "Running perf suite"
```

## Common Failure Modes

- Using `$[ ]` to reference `parameters.*`.
- Using `${{ }}` to read runtime output variables.
- Assuming a variable set in one step is available in the same step.
- Using macro syntax in `trigger` or `resources`.
