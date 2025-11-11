"""
CRUD operations for Todo items
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from typing import Optional
from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate


def create_todo(db: Session, todo: TodoCreate) -> Todo:
    """
    Create a new todo item
    """
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        completed=False,
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todo(db: Session, todo_id: int) -> Optional[Todo]:
    """
    Get a single todo by ID
    """
    return db.query(Todo).filter(Todo.id == todo_id).first()


def get_todos(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> list[Todo]:
    """
    Get all todos with optional filtering and sorting
    """
    query = db.query(Todo)

    # Apply filters
    if completed is not None:
        query = query.filter(Todo.completed == completed)

    if priority:
        query = query.filter(Todo.priority == priority)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Todo.title.ilike(search_pattern))
            | (Todo.description.ilike(search_pattern))
        )

    # Apply sorting
    if sort_order.lower() == "asc":
        query = query.order_by(asc(getattr(Todo, sort_by)))
    else:
        query = query.order_by(desc(getattr(Todo, sort_by)))

    return query.offset(skip).limit(limit).all()


def get_todos_count(
    db: Session,
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
) -> int:
    """
    Get count of todos with optional filtering
    """
    query = db.query(Todo)

    if completed is not None:
        query = query.filter(Todo.completed == completed)

    if priority:
        query = query.filter(Todo.priority == priority)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Todo.title.ilike(search_pattern))
            | (Todo.description.ilike(search_pattern))
        )

    return query.count()


def update_todo(db: Session, todo_id: int, todo_update: TodoUpdate) -> Optional[Todo]:
    """
    Update an existing todo
    """
    db_todo = get_todo(db, todo_id)

    if not db_todo:
        return None

    # Update only provided fields
    update_data = todo_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_todo, field, value)

    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int) -> bool:
    """
    Delete a todo by ID
    """
    db_todo = get_todo(db, todo_id)

    if not db_todo:
        return False

    db.delete(db_todo)
    db.commit()
    return True


def toggle_todo_completion(db: Session, todo_id: int) -> Optional[Todo]:
    """
    Toggle the completion status of a todo
    """
    db_todo = get_todo(db, todo_id)

    if not db_todo:
        return None

    db_todo.completed = not db_todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_all_completed_todos(db: Session) -> int:
    """
    Delete all completed todos and return the count of deleted items
    """
    deleted_count = db.query(Todo).filter(Todo.completed.is_(True)).delete()
    db.commit()
    return deleted_count
