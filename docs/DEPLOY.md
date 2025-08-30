# Deployment Guide

## Docker Compose Deployment

The application can be deployed using Docker Compose which will set up all required services:

```bash
docker-compose up -d --build
```

This will start the following services:
- API server (FastAPI)
- Worker process (Celery)
- Database (PostgreSQL)
- Redis (for queues and caching)
- Frontend (React application)
- Nginx (reverse proxy)

## Environment Configuration

Before deploying, copy the `.env.example` file to `.env` and adjust the values as needed:

```bash
cp .env.example .env
```

Key environment variables:
- `DATABASE_URL`: Connection string for PostgreSQL
- `REDIS_URL`: Connection string for Redis
- `VOSK_MODEL_PATH`: Path to the Vosk model files
- `WHISPER_MODEL_SIZE`: Size of the Whisper model (tiny or base)
- `JWT_SECRET_KEY`: Secret key for JWT token signing
- `OMP_NUM_THREADS` and `MKL_NUM_THREADS`: CPU optimization settings

## CPU Optimization

To optimize performance on CPU:
1. Set `OMP_NUM_THREADS` and `MKL_NUM_THREADS` to the number of CPU cores
2. Adjust `WORKER_CONCURRENCY` in the Celery worker configuration
3. Use the Whisper `tiny` model instead of `base` for faster processing
4. Ensure VAD (Voice Activity Detection) is properly configured to skip silent chunks

## Model Installation

For the ASR models to work, you need to download them:

### Vosk Model
```bash
mkdir -p models
cd models
wget https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip
unzip vosk-model-small-ru-0.22.zip
```

### Whisper Model
Whisper models are automatically downloaded when first used, but you can pre-download them:
```bash
# This will download the base model
python -c "import whisper; whisper.load_model('base')"
```

## Database Migrations

Run database migrations after deployment:

```bash
alembic upgrade head
```

## Initial Data Seeding

Run the seed script to populate the database with initial data:

```bash
python scripts/seed.py
```

## Scaling Considerations

To scale the application:
1. Increase the number of Celery workers:
   ```bash
   docker-compose up -d --scale worker=4
   ```
2. Adjust CPU thread settings in environment variables
3. Monitor performance metrics to determine optimal scaling parameters