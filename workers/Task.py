import os
from celery import Celery

broker = os.getenv("CELERY_BROKER_URL")
backend = os.getenv("CELERY_RESULT_BACKEND")

app = Celery("pollylab", broker=broker, backend=backend)

@app.task
def add(x: int, y: int) -> int:
    return x + y
