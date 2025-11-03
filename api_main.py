from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/jobs/add")
def queue_add(x: int, y: int):
    from workers.tasks import add
    job = add.delay(x, y)
    return {"job_id": job.id}

@app.get("/jobs/{job_id}")
def job_status(job_id: str):
    from workers.tasks import app as celery_app
    res = celery_app.AsyncResult(job_id)
    return {"status": res.status, "result": res.result}
