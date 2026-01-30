---
name: python-testing
description: |
  Pytest-first Python testing with emphasis on fakes over mocks. Covers unit, integration, and async tests; fixture design; coverage setup; and debugging test failures. Use when writing tests, reviewing test quality, designing fixtures, setting up pytest, or debugging failures—e.g., "write unit tests for new feature", "fixture design patterns", "fakes vs mocks comparison", "fix failing tests".
---

# Python Testing Skill

## Purpose

Pytest-first testing emphasizing **fakes over mocks** and behavior-driven assertions.

## Core Philosophy

Bias toward business logic tests over fakes (Layer 4). Fakes track mutations without coupling to implementation. See `references/test-doubles.md` for details.

## Required Tools

`pytest`, `pytest-cov`, `pytest-asyncio`, `pytest-mock`, `hypothesis`

## Directory Structure

```
project/
├── src/mypackage/
└── tests/
    ├── conftest.py
    ├── unit/
    │   ├── fakes/          # Layer 1: Fake tests
    │   └── services/       # Layer 4: Business logic
    ├── integration/        # Layer 2: Sanity tests
    └── e2e/                # Layer 5: Real systems
```

See `references/test-layers.md` for layer distribution and decision tree.

## Quick Patterns

### Prefer Fakes Over Mocks

```python
# GOOD: Fake tests behavior
def test_user_creation():
    fake_db = FakeDatabaseAdapter()
    service = UserService(database=fake_db)
    user = service.create_user("alice@example.com")
    assert user.id == 1
    assert "INSERT" in fake_db.executed_queries[0]

# AVOID: Mock couples to implementation
def test_user_creation(mocker):
    mock_db = mocker.patch("myapp.service.database")
    # Breaks on refactor
```

### Factory Fixtures

```python
@pytest.fixture
def make_user():
    def _make(name="test", **kwargs):
        return User(name=name, email=f"{name}@example.com", **kwargs)
    return _make
```

### Capture Side Effects

```python
@pytest.fixture
def capture_emails(monkeypatch):
    sent = []
    monkeypatch.setattr("myapp.email.send", lambda **kw: sent.append(kw))
    return sent
```

## DO

- Test behavior, not implementation
- Use fakes for business logic
- Descriptive names: `test_<what>_<condition>_<expected>`
- Use `tmp_path` for file operations

## DON'T

- Use subprocess in unit tests (use CliRunner)
- Hardcode paths
- Test private methods directly
- Use `time.sleep()` in unit tests

## References (Load on Demand)

- **[references/test-doubles.md](references/test-doubles.md)** - Fakes vs mocks, when to use each
- **[references/anti-patterns.md](references/anti-patterns.md)** - Common mistakes
- **[references/test-layers.md](references/test-layers.md)** - Five-layer strategy, distribution
- **[references/fixture-patterns.md](references/fixture-patterns.md)** - Factory fixtures, scope, teardown
- **[references/agentic-testing.md](references/agentic-testing.md)** - AI-assisted test writing
