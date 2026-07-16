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

## Stage 7: AI vs Me

**The Prompt I Used:**
I wrote a highly detailed "Ultimate Prompt" specifying the framework, strictly enforcing 400/404/201/204 status codes, requesting specific JSON error messages, and demanding all stretch goals (Pagination, Filtering, Searching, Stats, and Reset) in one go.

**1. What did the AI do better?**
The AI wrote extremely pythonic and robust code. To enforce my rule of returning a `400 Bad Request` instead of FastAPI's default `422 Unprocessable Entity` for missing fields, it brilliantly made the Pydantic model fields `Optional` (e.g., `title: Optional[str] = None`) and intercepted the payload inside the function to manually return the 400 JSONResponse. It also used advanced generator expressions for the ID creation `max((t["id"] for t in tasks), default=0) + 1`.

**2. What did it get wrong or quietly ignore?**
The AI followed the prompt almost flawlessly. However, because it was so focused on the logic, it didn't create the standard "Buy milk" tasks. Instead, it hallucinated software engineering tasks like "Review system architecture".

**3. What did my prompt forget to specify?**
I forgot to specify the default values for the pagination feature. I only asked for `?limit=int&offset=int`. The AI silently and smartly decided to set defaults `limit: int = 100, offset: int = 0` to prevent the API from breaking if a user didn't provide those parameters.