# Changelog

## Project Structure
- Created backend, engine, frontend, infra, docs, scripts, and tests directories
- Set up proper directory structure for all components

## Backend Implementation
- Implemented FastAPI application with health check endpoint
- Created SQLAlchemy models for animals, observations, observation_entities, and relations
- Set up Alembic for database migrations
- Created Pydantic schemas for API requests and responses
- Implemented API routers for all required endpoints

## Engine Implementation
- Implemented VoskASR class for streaming speech recognition
- Implemented WhisperASR class for batch WAV file processing
- Created EntityExtractor class using Natasha and spaCy for named entity recognition
- Added regex rules for extracting temperatures, weights, food amounts, and dates
- Implemented EntityNormalizer class for entity normalization and validation

## Frontend Implementation
- Set up React + TypeScript + Vite project
- Created pages for Upload & History, Live Transcription, Animal Profile, and Reports
- Implemented basic UI components with Tailwind CSS
- Added Recharts for data visualization

## Containerization
- Created Dockerfiles for backend API, worker, and frontend
- Implemented docker-compose.yml for multi-service deployment
- Added nginx.conf for reverse proxy configuration
- Created .env.example for environment configuration

## Testing
- Added unit tests for NER and normalization functionality
- Created test fixtures for entity extraction evaluation
- Implemented WER evaluation script

## Documentation
- Created README.md with project overview and quick start guide
- Created DEPLOY.md with deployment instructions
- Created API.md with detailed API documentation
- Created ENTITIES.md with entity extraction rules and examples

## Security Implementation
- Added JWT authentication
- Implemented role-based access control
- Added file size and MIME type validation
- Configured CORS policy

## Performance Optimization
- Implemented model preloading
- Added CPU optimization settings
- Implemented VAD for silence detection
- Added chunking for Whisper processing
- Added caching for repeated segments

All required components have been implemented according to the specifications.