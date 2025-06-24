# app/worker_dummy_api.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def dummy():
    return {"status": "Celery worker is running"}