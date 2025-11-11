# Testing Guide for Todo App

## Overview

This project includes comprehensive test coverage using **pytest** for both API endpoints and CRUD operations.

## Test Statistics

- **Total Tests**: 51
- **API Endpoint Tests**: 26
- **CRUD Operation Tests**: 25
- **Test Coverage**: All major functionality

## Running Tests

### Run All Tests

```cmd
uv run pytest
```

### Run with Verbose Output

```cmd
uv run pytest -v
```

### Run Specific Test File

```cmd
uv run pytest tests/test_api_endpoints.py -v
uv run pytest tests/test_crud.py -v
```

### Run Specific Test Class

```cmd
uv run pytest tests/test_api_endpoints.py::TestCreateTodo -v
```

### Run Specific Test

```cmd
uv run pytest tests/test_api_endpoints.py::TestCreateTodo::test_create_todo_success -v
```

### Run with Coverage (if pytest-cov installed)

```cmd
uv add pytest-cov
uv run pytest --cov=app --cov-report=html
```

## Test Structure

### Test Files

- **`tests/test_api_endpoints.py`** - Tests for all REST API endpoints
- **`tests/test_crud.py`** - Tests for database CRUD operations
- **`tests/conftest.py`** - Pytest fixtures and configuration
- **`pytest.ini`** - Pytest configuration file

### Test Organization

#### API Endpoint Tests (`test_api_endpoints.py`)

1. **TestRootEndpoints** - Root and health check endpoints
2. **TestCreateTodo** - Creating todos (success, validation, errors)
3. **TestGetTodos** - Listing todos (pagination, filtering, sorting, search)
4. **TestGetTodoById** - Getting specific todo
5. **TestUpdateTodo** - Updating todos (full and partial)
6. **TestToggleTodo** - Toggling completion status
7. **TestDeleteTodo** - Deleting single todo
8. **TestDeleteAllCompleted** - Bulk delete completed todos

#### CRUD Operation Tests (`test_crud.py`)

1. **TestCreateTodoCRUD** - Database create operations
2. **TestGetTodoCRUD** - Database read operations (with filters, search, sorting)
3. **TestUpdateTodoCRUD** - Database update operations
4. **TestToggleTodoCRUD** - Toggle completion operations
5. **TestDeleteTodoCRUD** - Database delete operations
6. **TestTodoModel** - Model representation tests

## Test Database

Tests use an **in-memory SQLite database** that is:

- Created fresh for each test
- Automatically cleaned up after each test
- Isolated from production PostgreSQL database
- Fast and doesn't require external setup

## Fixtures

### Available Fixtures (from `conftest.py`)

- **`db`** - Provides a fresh database session for each test
- **`client`** - Provides FastAPI TestClient with database override
- **`sample_todo_data`** - Sample todo data dictionary
- **`multiple_todos_data`** - List of multiple sample todos
- **`create_todo`** - Helper function to create todos in tests

## Test Coverage Details

### API Endpoint Tests (26 tests)

- ✅ Root endpoint
- ✅ Health check
- ✅ Create todo (success, minimal, invalid priority, missing/empty title)
- ✅ Get all todos (empty, list, pagination, filters, search, sorting)
- ✅ Get todo by ID (success, not found)
- ✅ Update todo (full, partial, not found)
- ✅ Toggle completion (to completed, to incomplete, not found)
- ✅ Delete todo (success, not found)
- ✅ Delete all completed (with todos, when none)

### CRUD Operation Tests (25 tests)

- ✅ Create todo (with all fields, with defaults)
- ✅ Get todo by ID (success, not found)
- ✅ Get todos (empty, multiple, pagination)
- ✅ Filter todos (by completed, by priority)
- ✅ Search todos in title/description
- ✅ Sort todos (ascending, descending)
- ✅ Count todos (all, filtered)
- ✅ Update todo (full, partial, not found)
- ✅ Toggle completion (both directions, not found)
- ✅ Delete todo (success, not found)
- ✅ Delete all completed (with todos, when none)
- ✅ Model representation

## Test Examples

### Example 1: Testing Create Endpoint

```python
def test_create_todo_success(self, client: TestClient, sample_todo_data):
    response = client.post("/api/v1/todos/", json=sample_todo_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_todo_data["title"]
```

### Example 2: Testing with Filters

```python
def test_get_todos_filter_by_priority(self, client: TestClient):
    # Create todos with different priorities
    client.post("/api/v1/todos/", json={"title": "High", "priority": "high"})
    client.post("/api/v1/todos/", json={"title": "Low", "priority": "low"})

    # Get high priority only
    response = client.get("/api/v1/todos/?priority=high")
    data = response.json()
    assert all(todo["priority"] == "high" for todo in data["todos"])
```

### Example 3: Testing CRUD Operations

```python
def test_update_todo_partial(self, db: Session):
    # Create todo
    todo_data = TodoCreate(title="Original", priority="low")
    created = crud.create_todo(db, todo_data)

    # Update only priority
    update_data = TodoUpdate(priority="high")
    updated = crud.update_todo(db, created.id, update_data)

    assert updated.title == "Original"  # unchanged
    assert updated.priority == "high"  # updated
```

## Continuous Integration

To integrate tests into CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    uv sync
    uv run pytest -v --tb=short
```

## Best Practices

1. **Test Isolation** - Each test is independent and doesn't affect others
2. **Clear Naming** - Test names clearly describe what they test
3. **Arrange-Act-Assert** - Tests follow AAA pattern
4. **Edge Cases** - Tests cover both success and error scenarios
5. **Fast Execution** - In-memory database makes tests run quickly

## Adding New Tests

When adding new features, follow this pattern:

1. Add test fixtures to `conftest.py` if needed
2. Create test class with descriptive name
3. Write tests for success cases
4. Write tests for error cases
5. Write tests for edge cases
6. Run tests to verify: `uv run pytest -v`

## Troubleshooting

### Tests Fail with Import Errors

```cmd
uv sync
```

### Tests Pass Locally but Fail in CI

Check database dependencies and environment variables

### Specific Test Fails

Run with verbose output to see details:

```cmd
uv run pytest tests/test_api_endpoints.py::TestCreateTodo::test_create_todo_success -vvs
```

## Summary

✅ **51 tests** covering all functionality  
✅ **API endpoints** fully tested  
✅ **CRUD operations** fully tested  
✅ **Fast execution** with in-memory database  
✅ **Easy to run** with simple commands  
✅ **Well organized** with clear structure  
✅ **Production ready** test suite

Run `uv run pytest -v` to verify everything works!
