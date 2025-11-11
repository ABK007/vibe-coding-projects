"""
Tests for API endpoints
"""

from fastapi.testclient import TestClient


class TestRootEndpoints:
    """Test root and health endpoints"""

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["message"] == "Welcome to Todo API"

    def test_health_check(self, client: TestClient):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "database" in data


class TestCreateTodo:
    """Test creating todos"""

    def test_create_todo_success(self, client: TestClient, sample_todo_data):
        """Test creating a todo successfully"""
        response = client.post("/api/v1/todos/", json=sample_todo_data)
        assert response.status_code == 201

        data = response.json()
        assert data["title"] == sample_todo_data["title"]
        assert data["description"] == sample_todo_data["description"]
        assert data["priority"] == sample_todo_data["priority"]
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data

    def test_create_todo_minimal(self, client: TestClient):
        """Test creating a todo with minimal data"""
        todo_data = {"title": "Minimal Todo"}
        response = client.post("/api/v1/todos/", json=todo_data)
        assert response.status_code == 201

        data = response.json()
        assert data["title"] == "Minimal Todo"
        assert data["priority"] == "medium"  # default value
        assert data["completed"] is False

    def test_create_todo_invalid_priority(self, client: TestClient):
        """Test creating a todo with invalid priority"""
        todo_data = {
            "title": "Invalid Priority Todo",
            "priority": "urgent",  # invalid value
        }
        response = client.post("/api/v1/todos/", json=todo_data)
        assert response.status_code == 422  # Validation error

    def test_create_todo_missing_title(self, client: TestClient):
        """Test creating a todo without title"""
        todo_data = {"description": "No title"}
        response = client.post("/api/v1/todos/", json=todo_data)
        assert response.status_code == 422  # Validation error

    def test_create_todo_empty_title(self, client: TestClient):
        """Test creating a todo with empty title"""
        todo_data = {"title": ""}
        response = client.post("/api/v1/todos/", json=todo_data)
        assert response.status_code == 422  # Validation error


class TestGetTodos:
    """Test getting todos"""

    def test_get_empty_todos(self, client: TestClient):
        """Test getting todos when none exist"""
        response = client.get("/api/v1/todos/")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == 0
        assert data["todos"] == []

    def test_get_todos_list(self, client: TestClient, multiple_todos_data):
        """Test getting list of todos"""
        # Create multiple todos
        for todo_data in multiple_todos_data:
            client.post("/api/v1/todos/", json=todo_data)

        response = client.get("/api/v1/todos/")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == len(multiple_todos_data)
        assert len(data["todos"]) == len(multiple_todos_data)

    def test_get_todos_with_pagination(self, client: TestClient, multiple_todos_data):
        """Test pagination"""
        # Create multiple todos
        for todo_data in multiple_todos_data:
            client.post("/api/v1/todos/", json=todo_data)

        response = client.get("/api/v1/todos/?skip=1&limit=2")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] == len(multiple_todos_data)
        assert len(data["todos"]) == 2

    def test_get_todos_filter_by_completed(
        self, client: TestClient, multiple_todos_data
    ):
        """Test filtering by completion status"""
        # Create todos
        for todo_data in multiple_todos_data:
            client.post("/api/v1/todos/", json=todo_data)

        # Mark first todo as completed
        client.patch("/api/v1/todos/1/toggle")

        # Get only incomplete todos
        response = client.get("/api/v1/todos/?completed=false")
        assert response.status_code == 200

        data = response.json()
        assert all(not todo["completed"] for todo in data["todos"])

        # Get only completed todos
        response = client.get("/api/v1/todos/?completed=true")
        assert response.status_code == 200

        data = response.json()
        assert all(todo["completed"] for todo in data["todos"])

    def test_get_todos_filter_by_priority(
        self, client: TestClient, multiple_todos_data
    ):
        """Test filtering by priority"""
        # Create todos
        for todo_data in multiple_todos_data:
            client.post("/api/v1/todos/", json=todo_data)

        # Get high priority todos
        response = client.get("/api/v1/todos/?priority=high")
        assert response.status_code == 200

        data = response.json()
        assert all(todo["priority"] == "high" for todo in data["todos"])

    def test_get_todos_search(self, client: TestClient, multiple_todos_data):
        """Test searching todos"""
        # Create todos
        for todo_data in multiple_todos_data:
            client.post("/api/v1/todos/", json=todo_data)

        response = client.get("/api/v1/todos/?search=First")
        assert response.status_code == 200

        data = response.json()
        assert data["total"] >= 1
        assert any("First" in todo["title"] for todo in data["todos"])

    def test_get_todos_sort_by_title(self, client: TestClient, multiple_todos_data):
        """Test sorting todos"""
        # Create todos
        for todo_data in multiple_todos_data:
            client.post("/api/v1/todos/", json=todo_data)

        response = client.get("/api/v1/todos/?sort_by=title&sort_order=asc")
        assert response.status_code == 200

        data = response.json()
        titles = [todo["title"] for todo in data["todos"]]
        assert titles == sorted(titles)


class TestGetTodoById:
    """Test getting a specific todo"""

    def test_get_todo_by_id_success(self, client: TestClient, sample_todo_data):
        """Test getting a todo by ID"""
        # Create a todo
        create_response = client.post("/api/v1/todos/", json=sample_todo_data)
        todo_id = create_response.json()["id"]

        # Get the todo
        response = client.get(f"/api/v1/todos/{todo_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == sample_todo_data["title"]

    def test_get_todo_by_id_not_found(self, client: TestClient):
        """Test getting a non-existent todo"""
        response = client.get("/api/v1/todos/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestUpdateTodo:
    """Test updating todos"""

    def test_update_todo_full(self, client: TestClient, sample_todo_data):
        """Test updating all fields of a todo"""
        # Create a todo
        create_response = client.post("/api/v1/todos/", json=sample_todo_data)
        todo_id = create_response.json()["id"]

        # Update the todo
        update_data = {
            "title": "Updated Title",
            "description": "Updated description",
            "priority": "low",
            "completed": True,
        }
        response = client.put(f"/api/v1/todos/{todo_id}", json=update_data)
        assert response.status_code == 200

        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["description"] == update_data["description"]
        assert data["priority"] == update_data["priority"]
        assert data["completed"] == update_data["completed"]

    def test_update_todo_partial(self, client: TestClient, sample_todo_data):
        """Test partial update of a todo"""
        # Create a todo
        create_response = client.post("/api/v1/todos/", json=sample_todo_data)
        todo_id = create_response.json()["id"]
        original_title = create_response.json()["title"]

        # Update only completion status
        update_data = {"completed": True}
        response = client.put(f"/api/v1/todos/{todo_id}", json=update_data)
        assert response.status_code == 200

        data = response.json()
        assert data["completed"] is True
        assert data["title"] == original_title  # unchanged

    def test_update_todo_not_found(self, client: TestClient):
        """Test updating a non-existent todo"""
        update_data = {"title": "Updated"}
        response = client.put("/api/v1/todos/999", json=update_data)
        assert response.status_code == 404


class TestToggleTodo:
    """Test toggling todo completion"""

    def test_toggle_todo_to_completed(self, client: TestClient, sample_todo_data):
        """Test toggling todo from incomplete to complete"""
        # Create a todo
        create_response = client.post("/api/v1/todos/", json=sample_todo_data)
        todo_id = create_response.json()["id"]

        # Toggle completion
        response = client.patch(f"/api/v1/todos/{todo_id}/toggle")
        assert response.status_code == 200

        data = response.json()
        assert data["completed"] is True

    def test_toggle_todo_to_incomplete(self, client: TestClient, sample_todo_data):
        """Test toggling todo from complete to incomplete"""
        # Create and complete a todo
        create_response = client.post("/api/v1/todos/", json=sample_todo_data)
        todo_id = create_response.json()["id"]
        client.patch(f"/api/v1/todos/{todo_id}/toggle")

        # Toggle back
        response = client.patch(f"/api/v1/todos/{todo_id}/toggle")
        assert response.status_code == 200

        data = response.json()
        assert data["completed"] is False

    def test_toggle_todo_not_found(self, client: TestClient):
        """Test toggling a non-existent todo"""
        response = client.patch("/api/v1/todos/999/toggle")
        assert response.status_code == 404


class TestDeleteTodo:
    """Test deleting todos"""

    def test_delete_todo_success(self, client: TestClient, sample_todo_data):
        """Test deleting a todo"""
        # Create a todo
        create_response = client.post("/api/v1/todos/", json=sample_todo_data)
        todo_id = create_response.json()["id"]

        # Delete the todo
        response = client.delete(f"/api/v1/todos/{todo_id}")
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"].lower()

        # Verify it's deleted
        get_response = client.get(f"/api/v1/todos/{todo_id}")
        assert get_response.status_code == 404

    def test_delete_todo_not_found(self, client: TestClient):
        """Test deleting a non-existent todo"""
        response = client.delete("/api/v1/todos/999")
        assert response.status_code == 404


class TestDeleteAllCompleted:
    """Test deleting all completed todos"""

    def test_delete_all_completed_todos(self, client: TestClient, multiple_todos_data):
        """Test deleting all completed todos"""
        # Create todos
        for todo_data in multiple_todos_data:
            client.post("/api/v1/todos/", json=todo_data)

        # Mark some as completed
        client.patch("/api/v1/todos/1/toggle")
        client.patch("/api/v1/todos/2/toggle")

        # Delete all completed
        response = client.delete("/api/v1/todos/completed/all")
        assert response.status_code == 200

        data = response.json()
        assert "2" in data["message"]  # Should delete 2 todos

        # Verify only incomplete todos remain
        get_response = client.get("/api/v1/todos/")
        remaining_todos = get_response.json()["todos"]
        assert all(not todo["completed"] for todo in remaining_todos)

    def test_delete_all_completed_when_none(self, client: TestClient):
        """Test deleting completed todos when none exist"""
        response = client.delete("/api/v1/todos/completed/all")
        assert response.status_code == 200
        assert "0" in response.json()["message"]
