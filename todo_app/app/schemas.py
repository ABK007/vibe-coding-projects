"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class TodoBase(BaseModel):
    """Base schema for Todo with common attributes"""

    title: str = Field(
        ..., min_length=1, max_length=200, description="Title of the todo item"
    )
    description: Optional[str] = Field(
        None, description="Detailed description of the todo item"
    )
    priority: str = Field(
        default="medium", pattern="^(low|medium|high)$", description="Priority level"
    )


class TodoCreate(TodoBase):
    """Schema for creating a new todo"""

    pass


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo"""

    title: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Title of the todo item"
    )
    description: Optional[str] = Field(
        None, description="Detailed description of the todo item"
    )
    completed: Optional[bool] = Field(None, description="Completion status")
    priority: Optional[str] = Field(
        None, pattern="^(low|medium|high)$", description="Priority level"
    )


class TodoResponse(TodoBase):
    """Schema for todo response"""

    id: int
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class TodoListResponse(BaseModel):
    """Schema for list of todos"""

    total: int
    todos: list[TodoResponse]


class MessageResponse(BaseModel):
    """Schema for message responses"""

    message: str
