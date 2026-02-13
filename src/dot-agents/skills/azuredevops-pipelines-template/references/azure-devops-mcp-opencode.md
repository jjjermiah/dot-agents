# Azure DevOps MCP Setup for OpenCode

## Objective

Enable local OpenCode sessions to query Azure DevOps repos, pipelines, and work
data via MCP tools.

## Recommended Baseline

Use Microsoft's Azure DevOps MCP server (`@azure-devops/mcp`) with local
transport.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "ado": {
      "type": "local",
      "command": ["npx", "-y", "@azure-devops/mcp", "contoso", "--authentication", "azcli"],
      "enabled": true
    }
  }
}
```

Environment token mode:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "ado": {
      "type": "local",
      "command": ["npx", "-y", "@azure-devops/mcp", "contoso", "--authentication", "envvar"],
      "environment": {
        "ADO_MCP_AUTH_TOKEN": "{env:ADO_MCP_AUTH_TOKEN}"
      }
    }
  }
}
```

## Security Rules

- Prefer Entra or `azcli` auth over PAT when possible.
- If using PAT-like token flows, use least privilege and short expiry.
- Keep tokens in env or secret stores, never in repo files.
- Scope MCP tools to required domains only.

## Notes

- Azure DevOps OAuth legacy flow is being deprecated; prefer modern auth models.
- Verify current server auth behavior before standardizing org-wide.
