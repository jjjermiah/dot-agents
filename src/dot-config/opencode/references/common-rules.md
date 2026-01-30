# Common Rules Reference

Load on demand when agents/skills need detailed guidance on shared patterns.

## Delegation Patterns
YOU WILL ALWAYS USE SUBAGENTS FOR SPECIALIZED TASKS WHENEVER POSSIBLE.
- `docs` - Markdown/MDX documentation
- `python-dev` - Python code and tooling
- `r-dev` - R code, packages, data workflows
- `plan` - Research and design before implementation

## Code Style Defaults

**Python**: PEP 8/257, type hints for public APIs, Ruff/Black formatting, 88-char lines.
**R**: Tidyverse style (snake_case, ~80 chars), roxygen2 docs, explicit `package::function()`.
**Markdown**: Clear headings, bullet lists, code blocks with language tags.

## Error Handling

- Fail fast with clear messages
- Use structured errors with custom classes (packages)
- Chain errors to preserve context
- Never swallow errors silently

## Testing

- Test behavior, not implementation
- Use fakes over mocks for business logic
- Keep unit tests fast (<2s)
- Use temp directories for file operations

## Safety Rails

- No destructive/irreversible actions without explicit instruction
- No secrets in code, logs, or examples
- Prefer reversible changes and feature flags
- Check for uncommitted changes before major work
