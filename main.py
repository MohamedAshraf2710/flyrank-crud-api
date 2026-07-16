from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Response
from pydantic import BaseModel

app = FastAPI()

class TaskCreate(BaseModel):
    title: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None
        
# In-memory list (Our Database)
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Master Git", "done": True}
]

# --- Stage 1 Endpoints ---
@app.get("/")
def read_root():
    """Returns a JSON description of the API."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health_check():
    """Checks if the server is alive and running."""
    return {"status": "ok"}

# --- Stage 2 Endpoints ---
# 1. Get all tasks
@app.get("/tasks")
def get_all_tasks(done: bool | None = None, search: str | None = None):
    """Returns the list of tasks, optionally filtered by 'done' status or 'search' term."""
    result = tasks
    if done is not None:
        result = [t for t in result if t["done"] == done]
    if search is not None:
        result = [t for t in result if search.lower() in t["title"].lower()]
    return result

# 2. Get a single task by ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Returns a single task by its ID, or a 404 error if not found."""
    # Search for the task
    for task in tasks:
        if task["id"] == task_id:
            return task
    
    # If not found, return 404 with the exact required JSON error
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

# --- Stage 3 Endpoints ---
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    """Creates a new task and adds it to the list."""
    # Validate the input: return 400 if title is missing or empty
    if not task.title or not task.title.strip():
        return JSONResponse(status_code=400, content={"error": "Title is required and cannot be empty"})
    
    # Give it the next free id and set done to false
    new_id = max(t["id"] for t in tasks) + 1 if tasks else 1
    new_task = {
        "id": new_id,
        "title": task.title,
        "done": False
    }
    
    # Add to the list and return the created task
    tasks.append(new_task)
    return new_task

# --- Stage 4 Endpoints ---

# Update a task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    """Updates an existing task's title or completion status."""
    # Validate: Empty/invalid body -> 400
    if task_update.title is None and task_update.done is None:
        return JSONResponse(status_code=400, content={"error": "Empty or invalid body"})
    
    for task in tasks:
        if task["id"] == task_id:
            if task_update.title is not None:
                if not task_update.title.strip():
                    return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
                task["title"] = task_update.title
            if task_update.done is not None:
                task["done"] = task_update.done
            return task
            
    # Unknown id -> 404
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

# Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Deletes a task by its ID."""
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            # Return 204 No Content with an empty body
            return Response(status_code=204)
            
    # Unknown id -> 404
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

# --- Extras Endpoints ---

@app.get("/stats")
def get_stats():
    """Returns statistics about the tasks."""
    total = len(tasks)
    done_count = sum(1 for t in tasks if t["done"])
    open_count = total - done_count
    return {"total": total, "done": done_count, "open": open_count}

@app.post("/reset")
def reset_tasks():
    """Restores the 3 example tasks."""
    global tasks
    tasks.clear()
    tasks.extend([
        {"id": 1, "title": "Learn FastAPI", "done": False},
        {"id": 2, "title": "Build CRUD API", "done": False},
        {"id": 3, "title": "Master Git", "done": True}
    ])
    return {"message": "Tasks reset to default examples"}