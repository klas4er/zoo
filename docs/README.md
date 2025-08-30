# Zoo Keeper AI Assistant

AI assistant for zoo keepers that converts voice observations to structured data.

## Features

- Batch processing of WAV files
- Real-time streaming transcription via WebSocket
- Named entity recognition for animal behaviors, vitals, feeding, etc.
- Dashboard for managers to view reports and trends
- Role-based access control (zoo keeper, manager, admin)

## Quick Start

1. Clone the repository
2. Set up environment variables (see `.env.example`)
3. Run with Docker:
   ```bash
   docker-compose up -d --build
   ```

## Local Development

1. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   npm install
   ```

2. Set up database:
   ```bash
   alembic upgrade head
   ```

3. Start services:
   ```bash
   # Terminal 1: API
   uvicorn backend.main:app --reload
   
   # Terminal 2: Worker
   celery -A backend.worker.app worker -l info -c $(nproc)
   
   # Terminal 3: Frontend
   npm run dev
   ```

## API Endpoints

- `POST /api/audio/process` - Process WAV file
- `GET /api/transcriptions` - List transcriptions
- `GET /api/transcriptions/{id}` - Get detailed transcription
- `POST /api/entities/config` - Configure entity extraction rules
- `GET /api/animals/{id}/log` - Get animal observation log
- `GET /api/reports/daily` - Get daily report
- `GET /api/health` - Health check
- `GET /api/metrics` - Performance metrics
- `GET /ws/transcribe` - WebSocket streaming endpoint

## Performance

- WER < 20% on CPU
- Entity extraction accuracy > 75%
- Processing time < 90 seconds for 5-minute audio

## License

All models and libraries used have permissive licenses (Apache/MIT/BSD).