from fastapi import FastAPI

app = FastAPI()

# 1. Root Endpoint (API Description)
@app.get("/")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

# 2. Health Check Endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}