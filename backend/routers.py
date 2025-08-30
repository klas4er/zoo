from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from services import TranscriptionService
from database import get_db
from schemas import TranscriptionResponse, EntityConfig
from sqlalchemy.orm import Session
from typing import Optional
import os
import uuid

router = APIRouter()

@router.post("/api/audio/process", response_model=TranscriptionResponse)
async def process_audio(
    file: UploadFile = File(...), 
    watcher_id: int = Form(1),
    animal_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    """Process uploaded WAV file"""
    # Validate file type
    if not file.content_type.startswith("audio/wav"):
        raise HTTPException(status_code=400, detail="Only WAV files are supported")
    
    # Save uploaded file temporarily
    file_id = str(uuid.uuid4())
    file_path = f"/tmp/{file_id}.wav"
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Process the file
    service = TranscriptionService(db)
    metadata = {}
    if animal_id:
        metadata["animal_id"] = animal_id
    
    try:
        result = service.process_wav_file(file_path, watcher_id, metadata)
        # Clean up temporary file
        os.remove(file_path)
        return result
    except Exception as e:
        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/transcriptions", response_model=list[TranscriptionResponse])
async def list_transcriptions(
    animal_id: Optional[int] = None, 
    watcher_id: Optional[int] = None,
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List transcriptions with optional filtering"""
    service = TranscriptionService(db)
    return service.get_transcriptions(animal_id, watcher_id, start_date, end_date)

@router.get("/api/transcriptions/{id}", response_model=TranscriptionResponse)
async def get_transcription(id: int, db: Session = Depends(get_db)):
    """Get detailed transcription result"""
    service = TranscriptionService(db)
    try:
        return service.get_transcription(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/api/entities/config", response_model=EntityConfig)
async def configure_entities(config: EntityConfig):
    """Configure entity extraction rules"""
    # In a real implementation, we would save these rules to a database or file
    # For now, we'll just return the config as received
    return config

@router.get("/api/animals/{id}/log", response_model=list[TranscriptionResponse])
async def get_animal_log(id: int, db: Session = Depends(get_db)):
    """Get animal observation log"""
    service = TranscriptionService(db)
    return service.get_transcriptions(animal_id=id)

@router.get("/api/reports/daily")
async def get_daily_report(date: Optional[str] = None, db: Session = Depends(get_db)):
    """Get daily report"""
    # In a real implementation, we would aggregate data for the specified date
    # For now, we'll return a placeholder response
    return {"date": date or "today", "report": "Daily report placeholder"}

# WebSocket endpoint would be implemented separately