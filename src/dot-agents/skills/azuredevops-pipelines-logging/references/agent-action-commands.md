# Azure DevOps Agent-Action Commands (`##vso[...]`)

Use this reference when commands must change pipeline behavior or state.

## Task Commands (with brief examples)

- `task.logissue`
  - Required: `type=error|warning`
  - Example:
    ```bash
    echo "##vso[task.logissue type=warning;code=LINT001;]Lint warning found"
    ```

- `task.setprogress`
  - Required: `value=<0-100>`
  - Example:
    ```bash
    echo "##vso[task.setprogress value=40;]Running integration tests"
    ```

- `task.complete`
  - Optional: `result=Succeeded|SucceededWithIssues|Failed`
  - Example:
    ```bash
    echo "##vso[task.complete result=Failed;]Validation failed"
    ```

- `task.setvariable`
  - Required: `variable=<name>`
  - Optional: `isSecret`, `isOutput`, `isReadOnly`
  - Example:
    ```bash
    echo "##vso[task.setvariable variable=ImageTag;isOutput=true]v1.2.3"
    ```

- `task.setsecret`
  - No properties; message is secret value
  - Example:
    ```bash
    echo "##vso[task.setsecret]$ENCODED_TOKEN"
    ```

- `task.prependpath`
  - Message is absolute path
  - Example:
    ```bash
    echo "##vso[task.prependpath]/opt/mytool/bin"
    ```

- `task.uploadfile`
  - Message is absolute file path
  - Example:
    ```bash
    echo "##vso[task.uploadfile]$PWD/test-output/raw.log"
    ```

- `task.uploadsummary`
  - Message is absolute Markdown file path
  - Example:
    ```bash
    echo "##vso[task.uploadsummary]$PWD/reports/summary.md"
    ```

- `task.addattachment`
  - Required: `type`, `name`; message is absolute path
  - Example:
    ```bash
    echo "##vso[task.addattachment type=my.report;name=lint-json;]$PWD/reports/lint.json"
    ```

## Artifact Commands

- `artifact.associate` - link existing artifact location.
- `artifact.upload` - upload/publish local artifact file.

## Build Commands

- `build.uploadlog` - upload extra log file to build container.
- `build.updatebuildnumber` - override build number.
- `build.addbuildtag` - add a build tag (do not use colon in tag).

## Release Command

- `release.updatereleasename` - rename current release.

## Rule of Thumb

- If removing the line changes pipeline behavior/data, use `##vso[...]`.

## Official Sources

- `https://learn.microsoft.com/en-us/azure/devops/pipelines/scripts/logging-commands?view=azure-devops&tabs=bash`
- `https://learn.microsoft.com/en-us/azure/devops/pipelines/process/set-variables-scripts?view=azure-devops`
