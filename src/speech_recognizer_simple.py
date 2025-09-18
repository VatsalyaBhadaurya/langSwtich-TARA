"""
Simple Speech Recognition Module - Lightweight alternative
"""
import os
import json
from typing import Optional

class SimpleSpeechRecognizer:
    def __init__(self, model_path="models/vosk"):
        self.model_path = model_path
        self.model = None
        self.recognizer = None
        self.current_language = "en"
        self._try_load_vosk()
    
    def _try_load_vosk(self):
        """Try to load Vosk model, fallback to simple mode if not available"""
        try:
            from vosk import Model, KaldiRecognizer
            if os.path.exists(self.model_path):
                self.model = Model(self.model_path)
                self.recognizer = KaldiRecognizer(self.model, 16000)
                print("✓ Vosk model loaded successfully")
            else:
                print(f"⚠️ Vosk model not found at {self.model_path}")
                print("💡 To download Vosk model:")
                print("   1. Go to: https://alphacephei.com/vosk/models")
                print("   2. Download 'vosk-model-small-en-us-0.15.zip'")
                print("   3. Extract to models/vosk/")
                print("   4. Or run: python download_models.py")
                print("Running in simple mode (text input only)")
        except ImportError:
            print("⚠️ Vosk not available, running in simple mode")
            print("💡 Install Vosk: pip install vosk")
        except Exception as e:
            print(f"⚠️ Vosk loading failed: {e}, running in simple mode")
    
    def transcribe_audio(self, audio_data: bytes, language: str = "en") -> str:
        """
        Transcribe audio data to text
        Args:
            audio_data: bytes - raw audio data
            language: str - language code
        Returns:
            str - transcribed text
        """
        if self.recognizer is None:
            # Fallback: return placeholder text
            return "[Audio transcription not available - Vosk model needed]"
        
        try:
            if self.recognizer.AcceptWaveform(audio_data):
                result = json.loads(self.recognizer.Result())
                return result.get('text', '').strip()
            else:
                result = json.loads(self.recognizer.PartialResult())
                return result.get('partial', '').strip()
        except Exception as e:
            print(f"Speech recognition error: {e}")
            return ""
    
    def transcribe_text_input(self, text: str) -> str:
        """
        For testing purposes - transcribe text input directly
        """
        return text
    
    def finalize_transcription(self) -> str:
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
        if self.recognizer and self.model:
            from vosk import KaldiRecognizer
            self.recognizer = KaldiRecognizer(self.model, 16000)
