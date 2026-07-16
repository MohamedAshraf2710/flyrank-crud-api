# FlyRank CRUD API

A simple in-memory CRUD API for managing a to-do list, built with FastAPI. This is the Week 2 (A1) assignment for the FlyRank Backend AI Engineering Internship.

## How to Install & Run

1. Install the required dependencies:
   ```bash
   pip install fastapi uvicorn pydantic
   ```
2. Start the server on localhost:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

## Endpoints Table

| CRUD Operation | HTTP Method | Endpoint | Meaning |
|---|---|---|---|
| - | GET | `/` | API Information |
| - | GET | `/health` | Health Check |
| Read | GET | `/tasks` | List all tasks (supports `?done=true` and `?search=term` filters) |
| Read | GET | `/tasks/{id}` | Get a single task by ID |
| Create | POST | `/tasks` | Add a new task |
| Update | PUT | `/tasks/{id}` | Update a task's title or status |
| Delete | DELETE | `/tasks/{id}` | Remove a task |
| - | GET | `/stats` | **Extra:** Get statistics about tasks |
| - | POST | `/reset` | **Extra:** Reset tasks to default |

## Example curl Output

**Request:**
```bash
curl -i http://localhost:8000/tasks/1
```

**Response:**
```http
HTTP/1.1 200 OK
date: Wed, 15 Jul 2026 21:59:43 GMT
server: uvicorn
content-length: 45
content-type: application/json

{"id":1,"title":"Learn FastAPI","done":false}
```

## Swagger UI Screenshot
*(Please refer to the Swagger UI at `http://localhost:8000/docs` to see the generated interactive documentation).*

## AI vs Me (Stage 7 - Optional)
**Prompt used:** 
> "Write a FastAPI CRUD application for a to-do list. It should use an in-memory list (no database). Support GET, POST, PUT, DELETE operations with correct status codes (200, 201, 204, 400, 404). Add validation for empty titles on creation and update."

**Differences found:**
1. **Validation Details:** The AI handled validation slightly differently, using Pydantic's built-in validation instead of manual checks in the route handler.
2. **Missing Endpoints:** The AI forgot to add the `/health` and root `/` API description endpoints which were specified in Stage 1, because the prompt forgot to explicitly request them.
3. **Data Structure:** The AI used a dictionary for in-memory storage mapping ID to tasks, instead of a list.