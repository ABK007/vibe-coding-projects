# Todo App - FastAPI Backend

A complete, production-ready Todo application backend built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- ✅ **Full CRUD Operations** - Create, Read, Update, Delete todos
- 🔍 **Advanced Filtering** - Filter by completion status, priority, and search
- 📊 **Sorting** - Sort by created date, updated date, title, or priority
- 🎯 **Priority Levels** - Low, Medium, High priority todos
- 🔄 **Toggle Completion** - Quickly toggle todo completion status
- 🗑️ **Bulk Delete** - Delete all completed todos at once
- 📝 **Detailed Descriptions** - Add rich descriptions to todos
- 🕒 **Timestamps** - Automatic created_at and updated_at tracking
- 🔒 **Type Safety** - Full Pydantic validation
- 📚 **Auto Documentation** - OpenAPI/Swagger docs at `/docs`

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic v2
- **Package Manager**: UV
- **Server**: Uvicorn

## Project Structure

```
todo_app/
├── app/
│   ├── __init__.py
│   ├── database.py      # Database configuration
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py          # Database operations
│   └── routes.py        # API endpoints
├── main.py              # Application entry point
├── .env                 # Environment variables
├── pyproject.toml       # Project dependencies
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.13+
- PostgreSQL database instance
- UV package manager

### Installation

1. **Clone or navigate to the project directory**:

   ```cmd
   cd e:\PIAIC\vibe-coding-projects\todo_app
   ```

2. **Install dependencies using UV**:

   ```cmd
   uv sync
   ```

3. **Configure environment variables**:

   Edit the `.env` file and update the `DATABASE_URL` with your PostgreSQL credentials:

   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
   ```

4. **Initialize the database**:

   The database tables will be created automatically when you start the application.

### Running the Application

#### Using Python directly:

```cmd
uv run python main.py
```

#### Using Uvicorn:

```cmd
uv run uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Root & Health

- `GET /` - Welcome message
- `GET /health` - Health check

### Todo Operations

| Method | Endpoint                      | Description                  |
| ------ | ----------------------------- | ---------------------------- |
| POST   | `/api/v1/todos/`              | Create a new todo            |
| GET    | `/api/v1/todos/`              | Get all todos (with filters) |
| GET    | `/api/v1/todos/{id}`          | Get a specific todo          |
| PUT    | `/api/v1/todos/{id}`          | Update a todo                |
| DELETE | `/api/v1/todos/{id}`          | Delete a todo                |
| PATCH  | `/api/v1/todos/{id}/toggle`   | Toggle completion status     |
| DELETE | `/api/v1/todos/completed/all` | Delete all completed todos   |

### Query Parameters for GET /api/v1/todos/

- `skip` (int): Number of items to skip (default: 0)
- `limit` (int): Maximum items to return (default: 100)
- `completed` (bool): Filter by completion status
- `priority` (string): Filter by priority (low, medium, high)
- `search` (string): Search in title and description
- `sort_by` (string): Field to sort by (created_at, updated_at, title, priority)
- `sort_order` (string): Sort order (asc, desc)

## Example Requests

### Create a Todo

```bash
curl -X POST "http://localhost:8000/api/v1/todos/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project",
    "description": "Finish the FastAPI todo app",
    "priority": "high"
  }'
```

### Get All Todos

```bash
curl "http://localhost:8000/api/v1/todos/"
```

### Get Filtered Todos

```bash
curl "http://localhost:8000/api/v1/todos/?completed=false&priority=high&sort_by=created_at&sort_order=desc"
```

### Update a Todo

```bash
curl -X PUT "http://localhost:8000/api/v1/todos/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated title",
    "completed": true
  }'
```

### Delete a Todo

```bash
curl -X DELETE "http://localhost:8000/api/v1/todos/1"
```

## Database Schema

### Todo Model

| Field       | Type        | Description                        |
| ----------- | ----------- | ---------------------------------- |
| id          | Integer     | Primary key (auto-increment)       |
| title       | String(200) | Todo title (required)              |
| description | Text        | Detailed description (optional)    |
| completed   | Boolean     | Completion status (default: false) |
| priority    | String(20)  | Priority level (default: medium)   |
| created_at  | DateTime    | Creation timestamp (auto)          |
| updated_at  | DateTime    | Last update timestamp (auto)       |

## Development

### Running in Development Mode

The application runs in reload mode by default when `DEBUG=True` in `.env`:

```cmd
uv run python main.py
```

### Database Migrations

For production, consider using Alembic for database migrations:

```cmd
uv add alembic
uv run alembic init alembic
```

## Environment Variables

| Variable     | Description                  | Default    |
| ------------ | ---------------------------- | ---------- |
| DATABASE_URL | PostgreSQL connection string | Required   |
| APP_NAME     | Application name             | "Todo API" |
| APP_VERSION  | API version                  | "1.0.0"    |
| DEBUG        | Debug mode                   | True       |
| PORT         | Server port                  | 8000       |

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `201` - Created
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

## CORS Configuration

CORS is enabled for all origins by default. For production, update the `allow_origins` in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Support

For issues and questions, please open an issue on the repository.
