"""
Minimalistic Speech Recognition Module using Vosk
"""
import json
import os
from vosk import Model, KaldiRecognizer


class SpeechRecognizer:
    def __init__(self, model_path="models/vosk"):
        self.model_path = model_path
        self.model = None
        self.recognizer = None
        self.current_language = None
        self._load_model()
    
    def _load_model(self):
        """Load Vosk model"""
        try:
            if os.path.exists(self.model_path):
                self.model = Model(self.model_path)
                self.recognizer = KaldiRecognizer(self.model, 16000)
                print("✓ Speech recognition model loaded")
            else:
                print(f"✗ Vosk model not found at {self.model_path}")
                print("Please download a Vosk model from: https://alphacephei.com/vosk/models")
        except Exception as e:
            print(f"✗ Failed to load Vosk model: {e}")
            self.model = None
    
    def transcribe_audio(self, audio_data, language="en"):
        """
        Transcribe audio data to text
        Args:
            audio_data: bytes - raw audio data
            language: str - language code (for future multi-model support)
        Returns:
            str - transcribed text
        """
        if self.recognizer is None:
            return ""
        
        try:
            # Process audio in chunks
            if self.recognizer.AcceptWaveform(audio_data):
                result = json.loads(self.recognizer.Result())
                return result.get('text', '').strip()
            else:
                # Get partial result
                result = json.loads(self.recognizer.PartialResult())
                return result.get('partial', '').strip()
        except Exception as e:
            print(f"Speech recognition error: {e}")
            return ""
    
    def finalize_transcription(self):
        """Get final transcription result"""
        if self.recognizer is None:
            return ""
        
        try:
            result = json.loads(self.recognizer.FinalResult())
            return result.get('text', '').strip()
        except Exception as e:
            print(f"Final transcription error: {e}")
            return ""
    
    def reset(self):
        """Reset recognizer for new audio"""
        if self.recognizer:
            self.recognizer = KaldiRecognizer(self.model, 16000)
