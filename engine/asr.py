import vosk
import whisper
import webrtcvad
import numpy as np
import os
from typing import Generator, Tuple
import wave

class VoskASR:
    def __init__(self, model_path: str = "models/vosk-model-small-ru-0.22"):
        """Initialize Vosk ASR model for streaming recognition"""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Vosk model not found at {model_path}. Please download it first.")
        
        self.model = vosk.Model(model_path)
        self.vad = webrtcvad.Vad(2)  # Aggressiveness mode 2
        
    def transcribe_stream(self, audio_chunks: Generator[Tuple[bytes, float], None, None]) -> Generator[dict, None, None]:
        """Transcribe streaming audio chunks"""
        rec = vosk.KaldiRecognizer(self.model, 16000)
        
        for chunk, timestamp in audio_chunks:
            # Check if chunk contains speech
            if self.vad.is_speech(chunk, 16000):
                if rec.AcceptWaveform(chunk):
                    result = rec.Result()
                    yield {"event": "final", "text": result, "timestamp": timestamp}
                else:
                    partial = rec.PartialResult()
                    yield {"event": "partial", "text": partial, "timestamp": timestamp}
        
        # Get final result
        final_result = rec.FinalResult()
        yield {"event": "final", "text": final_result, "timestamp": "end"}

class WhisperASR:
    def __init__(self, model_size: str = "base"):
        """Initialize Whisper ASR model for batch processing"""
        self.model = whisper.load_model(model_size)
        
    def transcribe_file(self, file_path: str) -> dict:
        """Transcribe entire WAV file"""
        # Whisper expects 16kHz audio, resample if needed
        with wave.open(file_path, 'rb') as wf:
            if wf.getframerate() != 16000:
                # Would need to resample here - for now assuming correct format
                pass
        
        result = self.model.transcribe(file_path, language="ru", task="transcribe")
        return result

# Model preloading implementation
def preload_models():
    """Preload ASR models at startup for better performance"""
    # Set CPU optimization flags
    os.environ["OMP_NUM_THREADS"] = str(os.cpu_count())
    os.environ["MKL_NUM_THREADS"] = str(os.cpu_count())
    
    # Preload models here if needed
    # For now, models are loaded on demand in the classes above
    pass