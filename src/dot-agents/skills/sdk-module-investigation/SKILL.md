---
name: sdk-module-investigation
description: |
  Investigate and integrate weakly documented SDK/library modules (especially Azure SDKs) into code. Use when asked to "investigate module", "SDK", "client class", or when docs are missing/weak and you need to discover APIs, models, or usage patterns to implement integration.
---

# Sdk Module Investigation

## Purpose

Rapidly discover SDK/module behavior from official docs, examples, and source, then integrate with minimal reimplementation and a runnable __main__ example.

## Workflow

1. Scope the target module and client
2. Pull an official SDK example (Context7 + official docs)
3. Inspect module source and API surface (introspection + code search)
4. Implement integration using SDK clients/models
5. Add a __main__ runnable example for validation
6. Verify behavior and document gaps

## Fundamental Requirements

YOU WILL ALWAYS look through SDK codebases to find the right classes/methods/functionalities.
YOU WILL NEVER guess or assume SDK behavior without confirming through official docs or source code.
ALWAYS take note of any utility functions/classes that we can reuse instead of reimplementing functionality. This includes credential handling, client construction patterns, and common models.
For example, you might think to implement kubernetes data parsing yourself, but the python-kubernetes library already has `kubernetes.utils` functions like
`format_quantity`, `parse_quantity`, `parse_duration`, `format_duration` that we can reuse. Always check for existing utilities before implementing new ones or.

## Step 1 - Scope the target module and client

- Identify package name, module path, and primary client class (ex: `azure.mgmt.resource` + `ResourceManagementClient`).
- Define the smallest required capability (ex: create resource group, list items, update resource).

## Step 2 - Pull official SDK examples first

Use Context7 to gather at least one authoritative SDK example.

Use fetch to capture authoritative docs/README for cross-checking.

Prefer official docs and README examples over your pretrained knowledge.
Look through blogs or StackOverflow for community examples.
If examples are outdated, extract patterns (credential setup, client construction, key operations) and confirm against the installed SDK.

## Step 3 - Inspect module source and API surface

Use pixi for any Python execution and keep commands small.

```bash
# Locate module file path
pixi run python -c "import azure.mgmt.resource as m; print(m.__file__)"

# Quick surface scan
pixi run python -c "import inspect, azure.mgmt.resource as m; print([n for n in dir(m) if 'Client' in n])"

# Inspect a client class signature and methods
pixi run python -c "import inspect; from azure.mgmt.resource import ResourceManagementClient; print(inspect.signature(ResourceManagementClient.__init__)); print([m for m in dir(ResourceManagementClient) if 'resource_groups' in m])"
```

Use repo tools for deeper inspection:

- `Read` the module file returned by `__file__` for imports, models, and client wiring.
- `Grep` for class names, operation groups, or method names to find usage patterns and versioned API modules.

Only reimplement behavior if the SDK does not expose it and you verified via source that no suitable client/model exists.

## Step 4 - Implement using SDK clients and models

- Construct clients using official credentials (ex: `AzureCliCredential`, `DefaultAzureCredential`).
- Use operation groups already exposed on the client (ex: `resource_client.resource_groups`).
- Prefer SDK model types over raw dicts unless docs show dict usage is expected.
- Keep integration minimal and aligned with example patterns.

## Step 5 - Add a __main__ runnable example

- Add a small `if __name__ == "__main__":` example to validate integration.
- Keep it side-effect safe where possible (read/list calls). If write operations are required, use a clear dry-run or explicit flag.

## Step 6 - Verify and record gaps

- Cross-check behavior against official example output or expected fields.
- If docs are missing, record inferred behavior and the source (docs URL or source file path).
