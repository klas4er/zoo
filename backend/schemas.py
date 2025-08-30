from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime

# Entity configuration schemas
class EntityField(BaseModel):
    name: str
    fields: List[str]
    required: Optional[List[str]] = []
    validators: Optional[Dict[str, str]] = {}

class EntityConfig(BaseModel):
    entities: List[EntityField]
    rules: Dict[str, str]

# Response schemas
class TranscriptionResponse(BaseModel):
    id: str
    status: str
    duration_sec: float
    wer: Optional[float] = None
    text: str
    entities: Dict[str, Dict[str, Any]]
    timeline: List[Dict[str, Any]]

class WebSocketStats(BaseModel):
    rtf: float
    cpu_load: float

class AnimalCreate(BaseModel):
    species: str
    name: Optional[str] = None
    tags: Optional[Dict] = {}

class ObservationCreate(BaseModel):
    animal_id: int
    watcher_id: int
    raw_text: str
    confidence: float

class ObservationEntityCreate(BaseModel):
    observation_id: int
    type: str
    payload_json: Dict[str, Any]