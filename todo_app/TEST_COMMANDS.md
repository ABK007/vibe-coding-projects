# Quick Testing Commands

## Run All Tests

```cmd
uv run pytest
```

## Run with Verbose Output

```cmd
uv run pytest -v
```

## Run Specific Test File

```cmd
uv run pytest tests/test_api_endpoints.py
uv run pytest tests/test_crud.py
```

## Run Specific Test Class

```cmd
uv run pytest tests/test_api_endpoints.py::TestCreateTodo -v
```

## Run Specific Test

```cmd
uv run pytest tests/test_api_endpoints.py::TestCreateTodo::test_create_todo_success -v
```

## Run Tests with Output

```cmd
uv run pytest -v -s
```

## Run Tests and Show Local Variables on Failure

```cmd
uv run pytest -v -l
```

## Run Only Failed Tests from Last Run

```cmd
uv run pytest --lf
```

## Stop on First Failure

```cmd
uv run pytest -x
```

## Run Tests in Parallel (requires pytest-xdist)

```cmd
uv add pytest-xdist
uv run pytest -n auto
```

## Generate HTML Coverage Report (requires pytest-cov)

```cmd
uv add pytest-cov
uv run pytest --cov=app --cov-report=html
```

## Test Summary

- Total Tests: 51
- API Endpoint Tests: 26
- CRUD Operation Tests: 25
- All tests use in-memory SQLite database
- Tests are isolated and run independently
