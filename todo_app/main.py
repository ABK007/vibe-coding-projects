"""
FastAPI Todo Application
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.database import init_db
from app.routes import router as todo_router

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    """
    # Startup: Initialize database tables
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")
    yield
    # Shutdown: Cleanup if needed
    print("Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title=os.getenv("APP_NAME", "Todo API"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="A complete Todo API built with FastAPI and PostgreSQL",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(todo_router)


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint
    """
    return {
        "message": "Welcome to Todo API",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "database": "connected"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=debug)
