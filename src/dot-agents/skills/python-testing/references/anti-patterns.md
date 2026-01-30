# Testing Anti-Patterns

**Sources**: [dagster fake-driven-testing](https://github.com/dagster-io/erk), [awesome-cursor-rules](https://github.com/sanjeed5/awesome-cursor-rules-mdc)

## Speculative Tests

**NEVER write tests for code that doesn't exist** (unless TDD right now).

```python
# BAD: Placeholder for "maybe later"
# def test_feature_we_might_add():
#     pass

# GOOD: TDD for feature being implemented NOW
def test_payment_processing():  # Writing this, then implementing
    result = process_payment(amount=100)
    assert result.status == "success"
```

## Wrong Test Categorization

**Unit tests with subprocess = integration tests**. Misclassification kills CI speed.

```python
# BAD: "Unit test" with subprocess (should be integration)
def test_cli_command():
    result = subprocess.run(["myapp", "process"], capture_output=True)

# GOOD: Real unit test with CliRunner
def test_cli_command():
    runner = CliRunner()
    result = runner.invoke(cli, ["process"])
    assert result.exit_code == 0
```

## Hardcoded Paths (Catastrophic)

```python
# BAD: Can write to real filesystem
def test_config():
    config = load_config(Path("/Users/dev/config.yaml"))

# GOOD: Isolated
def test_config(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text("debug: true")
    config = load_config(config_file)
```

## Complex Logic in Adapters

**Adapters should be thin wrappers**. Push logic to service layer.

```python
# BAD: Business logic in adapter
class RealDatabaseAdapter:
    def get_premium_expired_users(self):
        users = self.query("SELECT * FROM users")
        # 50 lines of filtering logic...

# GOOD: Thin adapter, logic in service
class RealDatabaseAdapter:
    def query(self, sql: str) -> list[dict]:
        return self._conn.execute(sql).fetchall()

class SubscriptionService:
    def get_premium_expired_users(self):
        users = self.db.query("SELECT * FROM users WHERE premium")
        return [u for u in users if self._is_expired(u)]
```

## Fakes with I/O

**Fakes must be in-memory only**.

```python
# BAD: Fake does real I/O
class FakeDatabase:
    def query(self, sql):
        conn = sqlite3.connect(":memory:")  # Still I/O!

# GOOD: Pure in-memory
class FakeDatabase:
    def __init__(self):
        self._data = {}
    def query(self, sql):
        return self._data.get(self._parse_table(sql), [])
```

## Testing Implementation, Not Behavior

```python
# BAD: Tests internal method calls
def test_user_creation(mocker):
    mock_validate = mocker.patch.object(UserService, "_validate_email")
    service.create_user("test@example.com")
    mock_validate.assert_called_once()  # Breaks on refactor

# GOOD: Tests observable behavior
def test_user_creation():
    user = service.create_user("test@example.com")
    assert user.email == "test@example.com"
    assert user.id is not None
```
