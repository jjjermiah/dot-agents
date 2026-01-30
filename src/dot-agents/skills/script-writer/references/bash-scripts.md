# Bash Script Guidance

## Core Practices
- Start with strict mode: `set -euo pipefail` and set `IFS=$'\n\t'`.
- Use `#!/usr/bin/env bash` shebang.
- Quote all variable expansions unless you explicitly want word splitting.
- Prefer arrays for lists; avoid `for x in $(...)`.
- Be explicit about globbing; use `shopt -s nullglob` when needed.
- Parse flags with `getopts` for portability.
- Use `trap` for cleanup and to report failures.
- Create temp files/dirs with `mktemp` and clean them up.
- Check dependencies with `command -v tool >/dev/null`.
- Avoid `sudo` unless explicitly requested.
- Write errors to stderr; use meaningful exit codes.
- Run `shellcheck` during development.
- Use safe file ops (no `rm -rf` without explicit user request).

## Portability Notes
- macOS ships Bash 3.x by default; avoid Bash 4+ features unless user confirms newer Bash.

## Minimal Template
```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

cleanup() { :; }
trap cleanup EXIT

main() {
  if ! command -v jq >/dev/null; then
    echo "jq is required" >&2
    exit 1
  fi
  echo "ok"
}

main "$@"
```
