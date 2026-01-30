# Python Script Guidance (Pixi Shebang)

## Requirements
- Require self-contained execution via Pixi shebang; do not rely on a global Python.
- Note: shebangs are Unix-only and require `pixi` installed on PATH.
- This guidance is based on Pixi advanced shebang support (pixi.prefix.dev).

## Canonical Shebang
```python
#!/usr/bin/env -S pixi exec --spec python=3.12 --spec requests -- python
```

## Notes
- `pixi exec` creates an isolated environment and runs the script with declared dependencies.
- Make the script executable: `chmod +x script.py`.
- Use `if __name__ == "__main__":` guard.
- Prefer `argparse` (stdlib) or `typer` for CLI parsing.
- Keep dependency specs reasonable; avoid overly strict pinning unless required.

## Minimal Template
```python
#!/usr/bin/env -S pixi exec --spec python=3.12 --spec requests -- python

import argparse

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()
    print(args.url)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

ALWAYS test scripts in a clean environment to ensure it compiles and the '--help' flag works as expected.

## MANDATORY libraries when useful.

- `rich`: always use for pretty console output AND logging.
- `httxp`: modern HTTP client, better than `requests`.
- `typer`: for more complex CLIs, built on `click` with type hints.
- `pydantic`: for robust data validation and settings management.