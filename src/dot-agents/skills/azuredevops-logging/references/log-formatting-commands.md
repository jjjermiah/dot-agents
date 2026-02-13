# Azure DevOps Log-Formatting Commands (`##[...]`)

Use this reference when you only want to improve log readability. These commands
do not change pipeline variables, status, artifacts, or build metadata.

## Commands

- `##[group]...` / `##[endgroup]` - collapsible log group.
- `##[section]...` - visual section label.
- `##[warning]...` - highlighted warning line.
- `##[error]...` - highlighted error line.
- `##[debug]...` - debug line (best with diagnostics enabled).
- `##[command]...` - show command text being executed.

## Brief Example

```bash
echo "##[group]Install dependencies"
echo "##[command]npm ci"
echo "##[warning]Using cached lockfile"
echo "##[endgroup]"
```

## Rule of Thumb

- If removing the line only changes appearance, use `##[...]`.

## Official Source

- `https://learn.microsoft.com/en-us/azure/devops/pipelines/scripts/logging-commands?view=azure-devops&tabs=bash`
