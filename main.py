from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

class TaskCreate(BaseModel):
    title: str | None = None
    
# In-memory list (Our Database)
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Master Git", "done": True}
]

# --- Stage 1 Endpoints ---
@app.get("/")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

# --- Stage 2 Endpoints ---
# 1. Get all tasks
@app.get("/tasks")
def get_all_tasks():
    return tasks

# 2. Get a single task by ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    # Search for the task
    for task in tasks:
        if task["id"] == task_id:
            return task
    
    # If not found, return 404 with the exact required JSON error
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

# --- Stage 3 Endpoints ---
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
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