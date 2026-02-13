---
name: azuredevops-pipelines-template
description: |
  Azure DevOps Repos-first template architecture for reusable CI pipelines. Use when designing or debugging Azure Pipelines YAML templates, splitting PR validation from post-merge main workflows while reusing one core CI template, enforcing strict compile-time/runtime variable rules, building typed template APIs (`stepList`, `jobList`, `stageList`, `templateContext`), or creating self-contained dependency-management templates for TypeScript/Python/R using bun, npm, and pixi—e.g., "one CI template for PR and main", "fix expression timing bug", "design jobList template contract".
---

# Azure DevOps Pipelines Template

## Purpose

Build production-grade Azure Pipelines template systems for Azure Repos. Reuse
one CI core across PR and main, keep templates self-contained, and make
variable timing explicit so behavior is predictable.

## Non-Negotiable Rules

- Target Azure DevOps Repos and Azure Pipelines YAML only.
- Never rely on YAML `pr:` for Azure Repos PR validation.
- Always treat templates as APIs: declare all required inputs explicitly.
- Never assume caller-defined variables exist unless passed or declared.
- Prefer typed parameters over implicit string variables for control flow.

## Pairing Contract with `azuredevops-pipelines-logging`

Use both skills when template design and script signaling intersect:

- This skill owns template topology, trigger strategy, parameter contracts,
  compile-time shape, and runtime conditions.
- `azuredevops-pipelines-logging` owns `##vso[...]` and `##[...]` command
  correctness, escaping, masking, and output-variable propagation details.
- Keep responsibilities explicit: this skill chooses the variable flow model;
  logging skill defines the exact command lines that implement it.

## Standard Topology

Use three files as a baseline:

1. `azure-pipelines-pr.yml` - branch-policy validation pipeline for PRs.
2. `azure-pipelines-main.yml` - post-merge `main` CI pipeline.
3. `templates/ci-core.yml` - shared implementation logic.

The two entry pipelines should only set triggers and template parameters. Keep
all jobs, stages, and steps in the shared template.

## PR vs Main Pattern (Azure Repos)

- `azure-pipelines-pr.yml` should use `trigger: none` and `pr: none`; connect
  this pipeline to target branches via Build Validation branch policy.
- `azure-pipelines-main.yml` should use CI `trigger` on `main` and `pr: none`.
- Reuse the same core template with different parameters:
  - PR: fast checks, no heavy integration suite.
  - Main: same core checks plus heavy integration jobs or stages.

## Variable and Expression Contract

Choose syntax by evaluation phase:

- `${{ }}` compile-time template expression:
  - Use for template structure (`if`, `each`, template insertion).
  - Has access to parameters and static variables only.
- `$[ ]` runtime expression:
  - Use for runtime conditions and computed variable values.
  - Does not access template parameters.
- `$( )` macro syntax:
  - Use inside task inputs and scripts.
  - Expands before each task.

Never mix these syntaxes casually. Most template bugs are timing bugs.

## Self-Contained Template API Pattern

For each template:

1. Declare all parameters with `type` and sensible defaults.
2. Constrain string parameters using `values:` when practical.
3. Define template-owned variables locally in the template.
4. Pass caller data via `parameters`, not hidden globals.
5. Use typed extension points (`stepList`, `jobList`, `stageList`) where needed.

## Typed Extension Points

- Use `stepList` to inject controlled step hooks.
- Use `jobList` with `templateContext` for suite metadata and fan-out jobs.
- Use `stageList` for environment promotion templates.
- In templates, use `object` instead of `stringList`.

## Dependency Management (TypeScript, Python, R)

Design dependency installation as dedicated step templates and include them from
`ci-core.yml` based on typed parameters.

- TypeScript: `bun install --frozen-lockfile` or `npm ci`.
- Python: `pixi install`, `pixi run <task>`.
- R: `pixi install`, `pixi run <task>`.

Use one explicit parameter (for example `dependencyMode: fast|locked`) to alter
install strictness between PR and main.

## Workflow

1. Pick topology (`pr/main/core`) and draft template API.
2. Define a parameter table (name, type, default, allowed values).
3. Implement compile-time structure with `${{ }}` only.
4. Add runtime `condition:` logic with `$[ ]` where required.
5. Delegate script-level signaling and `##vso[...]` command details to
   `azuredevops-pipelines-logging` when needed.
6. Wire TS/Python/R dependency templates via explicit parameters.
7. Validate PR and main paths execute expected job sets.

## Output Contract

When this skill is used, return:

1. Concrete pipeline topology (`pr/main/core`) and file map.
2. Copy-paste YAML snippets for entry pipelines and shared template sections.
3. Variable and expression timing rationale for each decision.
4. Parameter contract table and validation checklist.
5. Azure Repos branch-policy guidance for PR validation.

## Companion Skill

- `azuredevops-pipelines-logging`: load when the template design requires
  concrete `##vso[...]` command snippets, output variable propagation, secret
  masking, or rich log formatting semantics.

## References (Load on Demand)

- **[references/azure-repos-pr-validation.md](references/azure-repos-pr-validation.md)**
  - Load when implementing PR validation behavior in Azure Repos.
- **[references/template-architecture.md](references/template-architecture.md)**
  - Load when implementing shared core templates for PR/main reuse.
- **[references/variables-and-expressions.md](references/variables-and-expressions.md)**
  - Load when debugging compile-time versus runtime behavior.
- **[references/typed-parameters.md](references/typed-parameters.md)**
  - Load when designing `stepList`, `jobList`, and `stageList` APIs.
- **[references/dependency-management-ts-python-r.md](references/dependency-management-ts-python-r.md)**
  - Load when implementing bun/npm/pixi dependency install patterns.
- **[references/azure-devops-mcp-opencode.md](references/azure-devops-mcp-opencode.md)**
  - Load when configuring Azure DevOps MCP in OpenCode.
- **[references/sources-and-slugs.md](references/sources-and-slugs.md)**
  - Load when source traceability is required.
