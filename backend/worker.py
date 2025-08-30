import os
import redis
from celery import Celery
from database import SessionLocal
from services import TranscriptionService

# Initialize Celery
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
app = Celery("zoo_keeper_ai", broker=redis_url, backend=redis_url)

@app.task
def process_audio_task(file_path: str, watcher_id: int, metadata: dict = {}):
    """Celery task for processing audio files"""
    db = SessionLocal()
    try:
        service = TranscriptionService(db)
        result = service.process_wav_file(file_path, watcher_id, metadata)
        return result.dict()
    finally:
        db.close()

# Configure Celery
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_concurrency=int(os.getenv("WORKER_CONCURRENCY", "1")),
    worker_prefetch_multiplier=1,
)