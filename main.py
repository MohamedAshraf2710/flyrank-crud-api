from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

app = FastAPI(
    title="To-Do List API",
    description="A complete, highly professional CRUD API for a To-Do List.",
    version="1.0"
)

class TaskCreate(BaseModel):
    title: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

# 1. Data Storage: In-memory list pre-filled with 3 sample tasks
initial_tasks = [
    {"id": 1, "title": "Review system architecture", "done": False},
    {"id": 2, "title": "Write unit tests for authentication", "done": False},
    {"id": 3, "title": "Deploy to staging environment", "done": True}
]

tasks: List[Dict[str, Any]] = [dict(t) for t in initial_tasks]

# 2. Base Endpoints
@app.get("/")
def read_root():
    """Returns the API metadata and available base endpoints."""
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks", "/stats", "/reset"]}

@app.get("/health")
def health_check():
    """Health check endpoint to verify the server is running."""
    return {"status": "ok"}

# 4. Stretch Goals & Extras (GET /tasks)
@app.get("/tasks")
def list_tasks(done: Optional[bool] = None, search: Optional[str] = None, limit: int = 100, offset: int = 0):
    """
    List all tasks with optional filtering, searching, and pagination.
    - `done`: Filter by completion status (true/false).
    - `search`: Case-insensitive keyword search in the task title.
    - `limit` & `offset`: Pagination parameters.
    """
    filtered_tasks = tasks
    
    # Filtering
    if done is not None:
        filtered_tasks = [t for t in filtered_tasks if t["done"] == done]
        
    # Searching
    if search is not None:
        keyword = search.lower()
        filtered_tasks = [t for t in filtered_tasks if keyword in t["title"].lower()]
        
    # Pagination
    return filtered_tasks[offset:offset + limit]

# 3. Core CRUD Endpoints
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Retrieve a specific task by its ID."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

@app.post("/tasks", status_code=201)
def create_task(task_in: Optional[TaskCreate] = None):
    """Create a new task. Generates a sequential ID and defaults 'done' to false."""
    if not task_in or not task_in.title or not task_in.title.strip():
        return JSONResponse(status_code=400, content={"error": "Title is required and cannot be empty"})
        
    new_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {
        "id": new_id,
        "title": task_in.title,
        "done": False
    }
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_in: Optional[TaskUpdate] = None):
    """Update an existing task's title and/or completion status."""
    if not task_in or (task_in.title is None and task_in.done is None):
        return JSONResponse(status_code=400, content={"error": "Empty or invalid body"})
        
    if task_in.title is not None and not str(task_in.title).strip():
         return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})

    for task in tasks:
        if task["id"] == task_id:
            if task_in.title is not None:
                task["title"] = task_in.title
            if task_in.done is not None:
                task["done"] = task_in.done
            return task
            
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Delete a task by its ID."""
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return Response(status_code=204)
            
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

# 4. Stretch Goals & Extras (stats & reset)
@app.get("/stats")
def get_stats():
    """Return dynamic statistics about the tasks."""
    total = len(tasks)
    done_count = sum(1 for t in tasks if t["done"])
    open_count = total - done_count
    return {"total": total, "done": done_count, "open": open_count}

@app.post("/reset")
def reset_tasks():
    """Reset the tasks list to its original sample state."""
    global tasks
    tasks.clear()
    tasks.extend([dict(t) for t in initial_tasks])
    return {"message": "Tasks successfully reset to the original sample state"}