# Todo API - Documentation

**Base URL:** `http://localhost:8000/api/v1`

**Interactive Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Endpoints

| Method | Endpoint               | Description          |
| ------ | ---------------------- | -------------------- |
| GET    | `/`                    | Welcome message      |
| GET    | `/health`              | Health check         |
| POST   | `/todos/`              | Create todo          |
| GET    | `/todos/`              | List todos           |
| GET    | `/todos/{id}`          | Get todo             |
| PUT    | `/todos/{id}`          | Update todo          |
| PATCH  | `/todos/{id}/toggle`   | Toggle completion    |
| DELETE | `/todos/{id}`          | Delete todo          |
| DELETE | `/todos/completed/all` | Delete all completed |

---

## 1. Create Todo

`POST /api/v1/todos/`

**Request:**

```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "priority": "low | medium | high (optional, default: medium)"
}
```

**Response:** `201 Created`

```json
{
  "id": 1,
  "title": "Complete documentation",
  "description": "Write API docs",
  "priority": "high",
  "completed": false,
  "created_at": "2025-11-11T10:30:00Z",
  "updated_at": null
}
```

---

## 2. Get All Todos

`GET /api/v1/todos/`

**Query Parameters:**

- `skip` - Pagination offset (default: 0)
- `limit` - Max results (default: 100, max: 1000)
- `completed` - Filter by status (true/false)
- `priority` - Filter by priority (low/medium/high)
- `search` - Search in title/description
- `sort_by` - Sort field (created_at/updated_at/title/priority)
- `sort_order` - asc or desc (default: desc)

**Example:** `/api/v1/todos/?completed=false&priority=high&limit=10`

**Response:** `200 OK`

```json
{
  "total": 2,
  "todos": [
    {
      "id": 1,
      "title": "Complete documentation",
      "description": "Write API docs",
      "priority": "high",
      "completed": false,
      "created_at": "2025-11-11T10:30:00Z",
      "updated_at": null
    }
  ]
}
```

---

## 3. Get Todo by ID

`GET /api/v1/todos/{id}`

**Response:** `200 OK` or `404 Not Found`

```json
{
  "id": 1,
  "title": "Complete documentation",
  "description": "Write API docs",
  "priority": "high",
  "completed": false,
  "created_at": "2025-11-11T10:30:00Z",
  "updated_at": null
}
```

---

## 4. Update Todo

`PUT /api/v1/todos/{id}`

**Request:** (all fields optional)

```json
{
  "title": "string",
  "description": "string",
  "completed": true,
  "priority": "low | medium | high"
}
```

**Response:** `200 OK` or `404 Not Found`

---

## 5. Toggle Completion

`PATCH /api/v1/todos/{id}/toggle`

**Description:** Toggles completed status (true ↔ false)

**Response:** `200 OK` or `404 Not Found`

---

## 6. Delete Todo

`DELETE /api/v1/todos/{id}`

**Response:** `200 OK` or `404 Not Found`

```json
{
  "message": "Todo deleted successfully"
}
```

---

## 7. Delete All Completed

`DELETE /api/v1/todos/completed/all`

**Response:** `200 OK`

```json
{
  "message": "Deleted 5 completed todo(s)"
}
```

---

## Data Models

**TodoCreate:**

```typescript
{
  title: string;        // Required, 1-200 chars
  description?: string;
  priority?: "low" | "medium" | "high";
}
```

**TodoUpdate:**

```typescript
{
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: "low" | "medium" | "high";
}
```

**TodoResponse:**

```typescript
{
  id: number;
  title: string;
  description: string | null;
  priority: "low" | "medium" | "high";
  completed: boolean;
  created_at: string; // ISO 8601
  updated_at: string | null;
}
```

---

## Error Responses

**404 Not Found:**

```json
{ "detail": "Todo not found" }
```

**422 Validation Error:**

```json
{
  "detail": [
    {
      "type": "string",
      "loc": ["body", "title"],
      "msg": "Field required"
    }
  ]
}
```

---

## Quick Examples

```bash
# Create
curl -X POST http://localhost:8000/api/v1/todos/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries","priority":"high"}'

# List all
curl http://localhost:8000/api/v1/todos/

# Filter
curl "http://localhost:8000/api/v1/todos/?completed=false&priority=high"

# Update
curl -X PUT http://localhost:8000/api/v1/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'

# Toggle
curl -X PATCH http://localhost:8000/api/v1/todos/1/toggle

# Delete
curl -X DELETE http://localhost:8000/api/v1/todos/1
```
