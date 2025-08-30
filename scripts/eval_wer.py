#!/usr/bin/env python3

"""
Script to evaluate Word Error Rate (WER) for the ASR system.
"""

import jiwer
from engine.asr import WhisperASR
import os
import json

def evaluate_wer(audio_dir: str, reference_file: str):
    """Evaluate WER for all WAV files in a directory"""
    # Load reference transcriptions
    with open(reference_file, 'r') as f:
        references = json.load(f)
    
    # Initialize Whisper ASR
    asr = WhisperASR("base")  # or "tiny" for faster processing
    
    # Process each WAV file
    total_wer = 0.0
    file_count = 0
    
    for filename in os.listdir(audio_dir):
        if filename.endswith(".wav"):
            file_path = os.path.join(audio_dir, filename)
            
            # Get reference transcription
            reference = references.get(filename)
            if not reference:
                print(f"No reference transcription for {filename}")
                continue
            
            # Transcribe file
            result = asr.transcribe_file(file_path)
            hypothesis = result["text"]
            
            # Calculate WER
            wer = jiwer.wer(reference, hypothesis)
            total_wer += wer
            file_count += 1
            
            print(f"WER for {filename}: {wer:.4f}")
    
    # Calculate average WER
    if file_count > 0:
        avg_wer = total_wer / file_count
        print(f"Average WER: {avg_wer:.4f}")
        return avg_wer
    else:
        print("No files processed")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python eval_wer.py <audio_dir> <reference_file>")
        sys.exit(1)
    
    audio_dir = sys.argv[1]
    reference_file = sys.argv[2]
    
    evaluate_wer(audio_dir, reference_file)