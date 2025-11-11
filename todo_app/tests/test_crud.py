"""
Tests for CRUD operations
"""

from sqlalchemy.orm import Session
from app import crud
from app.schemas import TodoCreate, TodoUpdate


class TestCreateTodoCRUD:
    """Test create operations"""

    def test_create_todo(self, db: Session):
        """Test creating a todo in database"""
        todo_data = TodoCreate(
            title="Test Todo", description="Test description", priority="high"
        )

        todo = crud.create_todo(db, todo_data)

        assert todo.id is not None
        assert todo.title == "Test Todo"
        assert todo.description == "Test description"
        assert todo.priority == "high"
        assert todo.completed is False
        assert todo.created_at is not None

    def test_create_todo_default_priority(self, db: Session):
        """Test creating a todo with default priority"""
        todo_data = TodoCreate(title="Test Todo")

        todo = crud.create_todo(db, todo_data)

        assert todo.priority == "medium"


class TestGetTodoCRUD:
    """Test read operations"""

    def test_get_todo_by_id(self, db: Session):
        """Test getting a todo by ID"""
        # Create a todo
        todo_data = TodoCreate(title="Test Todo")
        created_todo = crud.create_todo(db, todo_data)

        # Get the todo
        todo = crud.get_todo(db, created_todo.id)

        assert todo is not None
        assert todo.id == created_todo.id
        assert todo.title == "Test Todo"

    def test_get_todo_not_found(self, db: Session):
        """Test getting a non-existent todo"""
        todo = crud.get_todo(db, 999)
        assert todo is None

    def test_get_todos_empty(self, db: Session):
        """Test getting todos from empty database"""
        todos = crud.get_todos(db)
        assert todos == []

    def test_get_todos_multiple(self, db: Session):
        """Test getting multiple todos"""
        # Create multiple todos
        for i in range(3):
            todo_data = TodoCreate(title=f"Todo {i + 1}")
            crud.create_todo(db, todo_data)

        todos = crud.get_todos(db)
        assert len(todos) == 3

    def test_get_todos_with_pagination(self, db: Session):
        """Test pagination"""
        # Create 5 todos
        for i in range(5):
            todo_data = TodoCreate(title=f"Todo {i + 1}")
            crud.create_todo(db, todo_data)

        # Get first 2
        todos = crud.get_todos(db, skip=0, limit=2)
        assert len(todos) == 2

        # Get next 2
        todos = crud.get_todos(db, skip=2, limit=2)
        assert len(todos) == 2

    def test_get_todos_filter_by_completed(self, db: Session):
        """Test filtering by completion status"""
        # Create completed and incomplete todos
        todo1 = TodoCreate(title="Incomplete Todo")
        crud.create_todo(db, todo1)

        todo2 = TodoCreate(title="Complete Todo")
        created = crud.create_todo(db, todo2)
        crud.toggle_todo_completion(db, created.id)

        # Get incomplete todos
        incomplete = crud.get_todos(db, completed=False)
        assert len(incomplete) == 1
        assert incomplete[0].completed is False

        # Get completed todos
        completed = crud.get_todos(db, completed=True)
        assert len(completed) == 1
        assert completed[0].completed is True

    def test_get_todos_filter_by_priority(self, db: Session):
        """Test filtering by priority"""
        # Create todos with different priorities
        for priority in ["low", "medium", "high"]:
            todo_data = TodoCreate(title=f"{priority} Todo", priority=priority)
            crud.create_todo(db, todo_data)

        # Get high priority todos
        high_priority = crud.get_todos(db, priority="high")
        assert len(high_priority) == 1
        assert high_priority[0].priority == "high"

    def test_get_todos_search(self, db: Session):
        """Test searching todos"""
        # Create todos
        crud.create_todo(db, TodoCreate(title="Project Meeting"))
        crud.create_todo(db, TodoCreate(title="Buy Groceries"))
        crud.create_todo(db, TodoCreate(title="Call", description="Discuss project"))

        # Search for "project"
        results = crud.get_todos(db, search="project")
        assert len(results) == 2

    def test_get_todos_sort_by_title_asc(self, db: Session):
        """Test sorting by title ascending"""
        # Create todos in random order
        for title in ["Zebra", "Apple", "Mango"]:
            crud.create_todo(db, TodoCreate(title=title))

        todos = crud.get_todos(db, sort_by="title", sort_order="asc")
        titles = [t.title for t in todos]
        assert titles == ["Apple", "Mango", "Zebra"]

    def test_get_todos_sort_by_title_desc(self, db: Session):
        """Test sorting by title descending"""
        # Create todos
        for title in ["Apple", "Mango", "Zebra"]:
            crud.create_todo(db, TodoCreate(title=title))

        todos = crud.get_todos(db, sort_by="title", sort_order="desc")
        titles = [t.title for t in todos]
        assert titles == ["Zebra", "Mango", "Apple"]

    def test_get_todos_count(self, db: Session):
        """Test counting todos"""
        # Create todos
        for i in range(5):
            crud.create_todo(db, TodoCreate(title=f"Todo {i + 1}"))

        count = crud.get_todos_count(db)
        assert count == 5

    def test_get_todos_count_with_filter(self, db: Session):
        """Test counting todos with filter"""
        # Create todos with different priorities
        crud.create_todo(db, TodoCreate(title="High 1", priority="high"))
        crud.create_todo(db, TodoCreate(title="High 2", priority="high"))
        crud.create_todo(db, TodoCreate(title="Low 1", priority="low"))

        count = crud.get_todos_count(db, priority="high")
        assert count == 2


class TestUpdateTodoCRUD:
    """Test update operations"""

    def test_update_todo_full(self, db: Session):
        """Test updating all fields"""
        # Create a todo
        todo_data = TodoCreate(title="Original Title")
        created = crud.create_todo(db, todo_data)

        # Update all fields
        update_data = TodoUpdate(
            title="Updated Title",
            description="New description",
            priority="high",
            completed=True,
        )
        updated = crud.update_todo(db, created.id, update_data)

        assert updated is not None
        assert updated.title == "Updated Title"
        assert updated.description == "New description"
        assert updated.priority == "high"
        assert updated.completed is True

    def test_update_todo_partial(self, db: Session):
        """Test partial update"""
        # Create a todo
        todo_data = TodoCreate(title="Original", priority="low")
        created = crud.create_todo(db, todo_data)

        # Update only priority
        update_data = TodoUpdate(priority="high")
        updated = crud.update_todo(db, created.id, update_data)

        assert updated is not None
        assert updated.title == "Original"  # unchanged
        assert updated.priority == "high"  # updated

    def test_update_todo_not_found(self, db: Session):
        """Test updating non-existent todo"""
        update_data = TodoUpdate(title="Updated")
        result = crud.update_todo(db, 999, update_data)
        assert result is None


class TestToggleTodoCRUD:
    """Test toggle completion operations"""

    def test_toggle_to_completed(self, db: Session):
        """Test toggling to completed"""
        # Create incomplete todo
        todo_data = TodoCreate(title="Test Todo")
        created = crud.create_todo(db, todo_data)
        assert created.completed is False

        # Toggle
        toggled = crud.toggle_todo_completion(db, created.id)
        assert toggled is not None
        assert toggled.completed is True

    def test_toggle_to_incomplete(self, db: Session):
        """Test toggling to incomplete"""
        # Create and complete a todo
        todo_data = TodoCreate(title="Test Todo")
        created = crud.create_todo(db, todo_data)
        crud.toggle_todo_completion(db, created.id)

        # Toggle back
        toggled = crud.toggle_todo_completion(db, created.id)
        assert toggled is not None
        assert toggled.completed is False

    def test_toggle_not_found(self, db: Session):
        """Test toggling non-existent todo"""
        result = crud.toggle_todo_completion(db, 999)
        assert result is None


class TestDeleteTodoCRUD:
    """Test delete operations"""

    def test_delete_todo(self, db: Session):
        """Test deleting a todo"""
        # Create a todo
        todo_data = TodoCreate(title="To be deleted")
        created = crud.create_todo(db, todo_data)

        # Delete it
        result = crud.delete_todo(db, created.id)
        assert result is True

        # Verify it's gone
        todo = crud.get_todo(db, created.id)
        assert todo is None

    def test_delete_todo_not_found(self, db: Session):
        """Test deleting non-existent todo"""
        result = crud.delete_todo(db, 999)
        assert result is False

    def test_delete_all_completed_todos(self, db: Session):
        """Test deleting all completed todos"""
        # Create some todos
        for i in range(5):
            todo = crud.create_todo(db, TodoCreate(title=f"Todo {i + 1}"))
            # Complete odd numbered todos
            if i % 2 == 0:
                crud.toggle_todo_completion(db, todo.id)

        # Delete all completed
        deleted_count = crud.delete_all_completed_todos(db)
        assert deleted_count == 3

        # Verify only incomplete remain
        remaining = crud.get_todos(db)
        assert len(remaining) == 2
        assert all(not t.completed for t in remaining)

    def test_delete_all_completed_when_none(self, db: Session):
        """Test deleting completed todos when none exist"""
        # Create only incomplete todos
        crud.create_todo(db, TodoCreate(title="Incomplete 1"))
        crud.create_todo(db, TodoCreate(title="Incomplete 2"))

        deleted_count = crud.delete_all_completed_todos(db)
        assert deleted_count == 0

        # Verify all todos still exist
        remaining = crud.get_todos(db)
        assert len(remaining) == 2


class TestTodoModel:
    """Test Todo model"""

    def test_todo_repr(self, db: Session):
        """Test string representation of Todo"""
        todo_data = TodoCreate(title="Test Todo")
        todo = crud.create_todo(db, todo_data)

        repr_str = repr(todo)
        assert "Todo" in repr_str
        assert str(todo.id) in repr_str
        assert "Test Todo" in repr_str
        assert "False" in repr_str or "completed=False" in repr_str.lower()
