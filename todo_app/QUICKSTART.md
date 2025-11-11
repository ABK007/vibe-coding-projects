# Todo App Backend - Quick Start Guide

## ⚡ Quick Start (Windows)

### 1. Update Database Configuration

Edit the `.env` file and replace the placeholder with your actual PostgreSQL credentials:

```env
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/your_database
```

### 2. Verify Setup

```cmd
uv run python test_setup.py
```

This will check if all dependencies are installed and the .env file is configured correctly.

### 3. Run the Application

```cmd
uv run python main.py
```

Or with uvicorn directly:

```cmd
uv run uvicorn main:app --reload
```

### 4. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📝 API Quick Reference

### Create a Todo

```bash
curl -X POST "http://localhost:8000/api/v1/todos/" -H "Content-Type: application/json" -d "{\"title\":\"My First Todo\",\"priority\":\"high\"}"
```

### Get All Todos

```bash
curl "http://localhost:8000/api/v1/todos/"
```

### Get Todo by ID

```bash
curl "http://localhost:8000/api/v1/todos/1"
```

### Update Todo

```bash
curl -X PUT "http://localhost:8000/api/v1/todos/1" -H "Content-Type: application/json" -d "{\"completed\":true}"
```

### Toggle Completion

```bash
curl -X PATCH "http://localhost:8000/api/v1/todos/1/toggle"
```

### Delete Todo

```bash
curl -X DELETE "http://localhost:8000/api/v1/todos/1"
```

### Search Todos

```bash
curl "http://localhost:8000/api/v1/todos/?search=project&priority=high&completed=false"
```

## 🔧 Common Issues

### Database Connection Error

If you see "could not connect to server":

1. Make sure PostgreSQL is running
2. Check your DATABASE_URL in .env
3. Verify database exists: `psql -U postgres -c "CREATE DATABASE todo_db;"`

### Import Errors

If you see import errors:

```cmd
uv sync
```

### Port Already in Use

Change the port in .env:

```env
PORT=8080
```

## 📁 Project Files Overview

- **main.py** - Application entry point, FastAPI setup
- **app/database.py** - Database configuration and session management
- **app/models.py** - SQLAlchemy Todo model
- **app/schemas.py** - Pydantic validation schemas
- **app/crud.py** - Database CRUD operations
- **app/routes.py** - API endpoints and route handlers
- **.env** - Environment variables (not in git)
- **test_setup.py** - Setup verification script

## 🚀 Features Implemented

✅ Create, Read, Update, Delete todos
✅ Filter by completion status
✅ Filter by priority (low/medium/high)
✅ Search in title and description
✅ Sort by multiple fields
✅ Toggle completion status
✅ Bulk delete completed todos
✅ Automatic timestamps
✅ Full API documentation
✅ CORS enabled
✅ Health check endpoint
✅ Request validation with Pydantic
✅ PostgreSQL database with SQLAlchemy

## 📞 Need Help?

- Check the full README.md for detailed documentation
- Visit /docs endpoint for interactive API documentation
- Run test_setup.py to verify your installation
