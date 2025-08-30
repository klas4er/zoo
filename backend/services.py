from repositories import AnimalRepository, ObservationRepository, ObservationEntityRepository
from engine.asr import VoskASR, WhisperASR
from engine.ner import EntityExtractor
from engine.normalization import EntityNormalizer
from models import Observation
from schemas import TranscriptionResponse
import os
import uuid
from typing import Dict, Any, List
import time
from sqlalchemy.orm import Session

class TranscriptionService:
    def __init__(self, db: Session):
        self.db = db
        self.animal_repo = AnimalRepository(db)
        self.observation_repo = ObservationRepository(db)
        self.entity_repo = ObservationEntityRepository(db)
        
        # Initialize ASR models
        vosk_model_path = os.getenv("VOSK_MODEL_PATH", "models/vosk-model-small-ru-0.22")
        self.vosk_asr = VoskASR(vosk_model_path)
        whisper_model_size = os.getenv("WHISPER_MODEL_SIZE", "base")
        self.whisper_asr = WhisperASR(whisper_model_size)
        
        # Initialize NER and normalization
        self.entity_extractor = EntityExtractor()
        self.entity_normalizer = EntityNormalizer()
    
    def process_wav_file(self, file_path: str, watcher_id: int, metadata: Dict[Any, Any] = {}) -> TranscriptionResponse:
        """Process WAV file with Whisper ASR and extract entities"""
        start_time = time.time()
        
        # Transcribe with Whisper
        transcription_result = self.whisper_asr.transcribe_file(file_path)
        duration = time.time() - start_time
        
        # Extract text and confidence
        text = transcription_result["text"]
        confidence = 0.0  # Whisper doesn't provide segment-level confidence in this simple implementation
        
        # Extract entities
        entities = self.entity_extractor.extract_entities(text)
        
        # Normalize entities
        normalized_entities = self.entity_normalizer.normalize_entities(entities)
        validated_entities = self.entity_normalizer.validate_entities(normalized_entities)
        
        # Create observation in database
        animal_id = metadata.get("animal_id", 1)  # Default to 1 if not provided
        observation = self.observation_repo.create_observation({
            "animal_id": animal_id,
            "watcher_id": watcher_id,
            "raw_text": text,
            "confidence": confidence
        })
        
        # Create observation entities in database
        for entity_type, entity_data in validated_entities.items():
            self.entity_repo.create_observation_entity({
                "observation_id": observation.id,
                "type": entity_type,
                "payload_json": entity_data
            })
        
        # Calculate WER if reference text is provided (simplified)
        wer = 0.0
        if "reference_text" in metadata:
            # In a real implementation, we would calculate WER using a library like jiwer
            # This is a placeholder implementation
            reference = metadata["reference_text"]
            wer = self._calculate_wer(reference, text)
        
        return TranscriptionResponse(
            id=f"obs_{observation.id}",
            status="done",
            duration_sec=duration,
            wer=wer,
            text=text,
            entities=validated_entities,
            timeline=[]
        )
    
    def _calculate_wer(self, reference: str, hypothesis: str) -> float:
        """Calculate Word Error Rate between reference and hypothesis text"""
        # This is a simplified implementation
        # In a real implementation, we would use a library like jiwer
        reference_words = reference.split()
        hypothesis_words = hypothesis.split()
        
        if len(reference_words) == 0:
            return 0.0
            
        # This is not a real WER calculation, just a placeholder
        # that compares the number of words
        word_diff = abs(len(reference_words) - len(hypothesis_words))
        wer = word_diff / len(reference_words)
        
        return min(wer, 1.0)  # Cap at 1.0
    
    def get_transcriptions(self, animal_id: int = None, watcher_id: int = None, 
                          start_date: str = None, end_date: str = None) -> List[TranscriptionResponse]:
        """Get list of transcriptions with optional filtering"""
        # Convert string dates to datetime objects if provided
        from datetime import datetime
        start_dt = datetime.fromisoformat(start_date) if start_date else None
        end_dt = datetime.fromisoformat(end_date) if end_date else None
        
        observations = self.observation_repo.get_observations(
            animal_id=animal_id,
            watcher_id=watcher_id,
            start_date=start_dt,
            end_date=end_dt
        )
        
        transcriptions = []
        for obs in observations:
            entities = self.entity_repo.get_entities_by_observation(obs.id)
            entity_dict = {e.type: e.payload_json for e in entities}
            
            transcriptions.append(TranscriptionResponse(
                id=f"obs_{obs.id}",
                status="done",
                duration_sec=0.0,  # Not applicable for listing
                text=obs.raw_text,
                entities=entity_dict,
                timeline=[]
            ))
            
        return transcriptions
    
    def get_transcription(self, observation_id: int) -> TranscriptionResponse:
        """Get detailed transcription result"""
        observation = self.observation_repo.get_observation(observation_id)
        if not observation:
            raise ValueError(f"Observation with id {observation_id} not found")
            
        entities = self.entity_repo.get_entities_by_observation(observation_id)
        entity_dict = {e.type: e.payload_json for e in entities}
        
        return TranscriptionResponse(
            id=f"obs_{observation.id}",
            status="done",
            duration_sec=0.0,
            text=observation.raw_text,
            entities=entity_dict,
            timeline=[]
        )