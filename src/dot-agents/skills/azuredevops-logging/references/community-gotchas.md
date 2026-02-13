# Azure DevOps Logging: Community Gotchas

Use this reference when behavior is confusing, inconsistent, or appears to
ignore valid commands.

## 1) Escaping and Parser Boundaries

- Reserved sequences (`;`, `]`, CR, LF) are parser-sensitive in `##vso[...]`.
- `%` itself needs dedicated escaping in many variable payload scenarios.
- Practical escape recipe:
  - `%` -> `%AZP25`
  - `\n` -> `%0A`
  - `\r` -> `%0D`

Source:
`https://raw.githubusercontent.com/microsoft/azure-pipelines-agent/master/docs/design/percentEncoding.md`

## 2) Multiline Variables Truncated to First Line

- Unescaped multiline values may appear as first-line only when read later.
- Encode newline/carriage return before `task.setvariable`.
- Confirm decoded value in downstream step.

Sources:
- `https://learn.microsoft.com/en-us/azure/devops/pipelines/process/set-variables-scripts?view=azure-devops`
- `https://blog.paulaxon.co.uk/azure-devops/multiline-variables/`
- `https://techcommunity.microsoft.com/discussions/azure/passing-a-here-string-as-adhoc-output-variable/3929484`

## 3) `set -x` Breaks or Corrupts Logging Commands

- Bash xtrace can prefix/alter emitted command lines and break parser handling.
- Disable xtrace around command emission.

Sources:
- `https://learn.microsoft.com/en-us/azure/devops/pipelines/scripts/logging-commands?view=azure-devops`
- `https://github.com/microsoft/azure-pipelines-tasks/issues/17578`

## 4) Secret Masking Is Not Substring-Aware

- Azure DevOps does not mask secret substrings; avoid structured secrets.
- Some logs may over-mask unrelated values, reducing diagnosability.

Sources:
- `https://learn.microsoft.com/en-us/azure/devops/pipelines/scripts/logging-commands?view=azure-devops`
- `https://github.com/microsoft/azure-pipelines-agent/issues/1207`

## 5) Output Variable Scope and Name Pitfalls

- Values set in a step are unavailable in that same step.
- `isOutput=true` changes reference syntax and requires task naming.
- Matrix/deployment strategies can alter output variable names.

Sources:
- `https://learn.microsoft.com/en-us/azure/devops/pipelines/process/set-variables-scripts?view=azure-devops`
- `https://stackoverflow.com/questions/61588762/azure-pipeline-output-variables-task-setvariable-is-not-assigning-any-value-to-v`
- `https://stackoverflow.com/questions/70010567/azure-devops-yaml-passing-variable-using-vsotask-setvariable-not-working`

## 6) `task.complete` vs Script Exit Code Ambiguity

- Mixed success/failure signals can produce confusing outcomes.
- Prefer one clear failure path: log issue + complete failed + non-zero exit.

Source:
`https://github.com/microsoft/azure-pipelines-tasks/issues/14939`

## 7) Summary Publishing Quirks

- `task.uploadsummary` may show duplicate effects in some rerun scenarios.
- Keep summary generation idempotent and include run identifiers in content.

Source:
`https://github.com/microsoft/azure-pipelines-tasks/issues/21550`

## Troubleshooting Sequence

1. Reproduce with a minimal single-step script.
2. Disable `set -x` near every logging command.
3. Escape payloads and retry.
4. Print `env` in downstream step to inspect variable materialization.
5. Verify job/stage `dependsOn` and output expression syntax.
6. Enable diagnostics for missing debug visibility.

Diagnostics source:
`https://learn.microsoft.com/en-us/azure/devops/pipelines/troubleshooting/review-logs?view=azure-devops`
