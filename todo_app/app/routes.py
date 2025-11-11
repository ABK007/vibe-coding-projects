"""
API routes for todo operations
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas import (
    TodoCreate,
    TodoUpdate,
    TodoResponse,
    TodoListResponse,
    MessageResponse,
)
from app import crud

router = APIRouter(prefix="/api/v1/todos", tags=["todos"])


@router.post("/", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """
    Create a new todo item
    """
    return crud.create_todo(db=db, todo=todo)


@router.get("/", response_model=TodoListResponse)
def get_todos(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of items to return"
    ),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    priority: Optional[str] = Query(
        None, pattern="^(low|medium|high)$", description="Filter by priority"
    ),
    search: Optional[str] = Query(None, description="Search in title and description"),
    sort_by: str = Query(
        "created_at",
        pattern="^(created_at|updated_at|title|priority)$",
        description="Field to sort by",
    ),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db),
):
    """
    Get all todos with optional filtering, searching, and sorting
    """
    todos = crud.get_todos(
        db=db,
        skip=skip,
        limit=limit,
        completed=completed,
        priority=priority,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    total = crud.get_todos_count(
        db=db, completed=completed, priority=priority, search=search
    )

    return TodoListResponse(total=total, todos=todos)


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Get a specific todo by ID
    """
    db_todo = crud.get_todo(db=db, todo_id=todo_id)

    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    return db_todo


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    """
    Update an existing todo
    """
    db_todo = crud.update_todo(db=db, todo_id=todo_id, todo_update=todo)

    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    return db_todo


@router.delete("/{todo_id}", response_model=MessageResponse)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Delete a todo by ID
    """
    success = crud.delete_todo(db=db, todo_id=todo_id)

    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")

    return MessageResponse(message="Todo deleted successfully")


@router.patch("/{todo_id}/toggle", response_model=TodoResponse)
def toggle_todo_completion(todo_id: int, db: Session = Depends(get_db)):
    """
    Toggle the completion status of a todo
    """
    db_todo = crud.toggle_todo_completion(db=db, todo_id=todo_id)

    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    return db_todo


@router.delete("/completed/all", response_model=MessageResponse)
def delete_all_completed_todos(db: Session = Depends(get_db)):
    """
    Delete all completed todos
    """
    deleted_count = crud.delete_all_completed_todos(db=db)

    return MessageResponse(message=f"Deleted {deleted_count} completed todo(s)")
