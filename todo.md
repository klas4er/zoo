## MVP Development Tasks

### Initial Setup
- [x] Create project directory structure
- [x] Set up backend with FastAPI
- [x] Implement database models and migrations
- [x] Set up frontend with React + TypeScript + Vite

### Core Engine Implementation
- [x] Implement Vosk streaming ASR
- [x] Implement Whisper batch ASR (tiny/base models)
- [x] Implement NER with Natasha and spaCy
- [x] Add regex parsing for dates, temperatures, weights
- [x] Implement data normalization and entity merging

### API Implementation
- [x] Create audio processing endpoint
- [x] Create transcriptions listing endpoint
- [x] Create single transcriptions endpoint
- [x] Create entity configuration endpoint
- [x] Create animal observation log endpoint
- [x] Create daily reports endpoint
- [x] Create health check endpoint
- [x] Create metrics endpoint
- [x] Implement WebSocket streaming endpoint

### Performance Optimization
- [x] Implement model preloading
- [x] Add CPU optimization settings
- [x] Implement VAD for silence detection
- [x] Add chunking for Whisper processing
- [x] Add caching for repeated segments

### Security Implementation
- [x] Add JWT authentication
- [x] Implement role-based access control
- [x] Add file size and MIME type validation
- [x] Configure CORS policy

### Testing
- [x] Add unit tests for NER and normalization
- [x] Add integration tests for WAV processing
- [x] Implement WER evaluation script
- [x] Add entity extraction evaluation

### Documentation
- [x] Create README with setup and usage instructions
- [x] Create DEPLOY.md with Docker deployment guide
- [x] Create API.md with OpenAPI specification
- [x] Create ENTITIES.md with entity rules and examples

### Containerization
- [x] Create Dockerfiles for all services
- [x] Create docker-compose.yml
- [x] Add environment file templates
- [x] Implement seed script for initial data

### Finalization
- [x] Verify all endpoints work correctly
- [x] Test both batch and streaming modes
- [x] Validate performance metrics (WER < 20%, processing time < 90s)
- [x] Package complete solution for delivery