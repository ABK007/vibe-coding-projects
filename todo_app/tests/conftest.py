"""
Pytest configuration and fixtures for testing
"""

import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from main import app


# Use in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """
    Create a fresh database for each test
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create a new session for the test
    db_session = TestingSessionLocal()

    try:
        yield db_session
    finally:
        db_session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    Create a test client with overridden database dependency
    """

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_todo_data():
    """
    Sample todo data for testing
    """
    return {
        "title": "Test Todo",
        "description": "This is a test todo",
        "priority": "high",
    }


@pytest.fixture
def multiple_todos_data():
    """
    Multiple sample todos for testing
    """
    return [
        {"title": "First Todo", "description": "First test todo", "priority": "high"},
        {
            "title": "Second Todo",
            "description": "Second test todo",
            "priority": "medium",
        },
        {"title": "Third Todo", "description": "Third test todo", "priority": "low"},
    ]


@pytest.fixture
def create_todo(client: TestClient):
    """
    Helper fixture to create a todo
    """

    def _create_todo(todo_data: dict):
        response = client.post("/api/v1/todos/", json=todo_data)
        return response.json()

    return _create_todo
