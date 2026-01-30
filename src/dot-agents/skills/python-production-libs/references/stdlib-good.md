# When Stdlib IS the Right Choice

## pathlib - Path handling

```python
from pathlib import Path
config = Path.home() / ".config" / "app.toml"
config.read_text()
config.write_text("content")
list(Path("src").rglob("*.py"))
```

## zoneinfo - Timezones (3.9+)

```python
from datetime import datetime
from zoneinfo import ZoneInfo
now = datetime.now(ZoneInfo("America/New_York"))
```

## subprocess - Running commands

```python
import subprocess
result = subprocess.run(
    ["ls", "-la"],
    capture_output=True, text=True, check=True
)
```

## tempfile - Temporary files

```python
from tempfile import TemporaryDirectory
with TemporaryDirectory() as tmpdir:
    # Auto-deleted after block
    ...
```

## functools - Caching, partials

```python
from functools import lru_cache, cached_property
@lru_cache(maxsize=128)
def expensive(n): ...
```

## itertools - Iteration

```python
from itertools import chain, islice, groupby, batched  # batched 3.12+
```

## contextlib - Context managers

```python
from contextlib import contextmanager, suppress
with suppress(FileNotFoundError):
    Path("x").unlink()
```

## collections - Data structures

```python
from collections import defaultdict, Counter, deque
```

## dataclasses - Simple containers (no validation)

```python
from dataclasses import dataclass
@dataclass
class Point:
    x: float
    y: float
```

Use pydantic when validation needed.

## tomllib - TOML (3.11+)

```python
import tomllib
with open("config.toml", "rb") as f:
    config = tomllib.load(f)
```

## secrets - Crypto randomness

```python
import secrets
token = secrets.token_urlsafe(32)
```
