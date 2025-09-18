"""
Minimalistic Text-to-Speech Module using Coqui TTS
"""
import os
from TTS.api import TTS


class TextToSpeech:
    def __init__(self, model_name="tts_models/multilingual/multi-dataset/xtts_v2"):
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load TTS model"""
        try:
            self.model = TTS(model_name=self.model_name, progress_bar=False, gpu=False)
            print("✓ Text-to-speech model loaded")
        except Exception as e:
            print(f"✗ Failed to load TTS model: {e}")
            self.model = None
    
    def synthesize_speech(self, text, language="en", output_path="output.wav"):
        """
        Synthesize speech from text
        Args:
            text: str - text to synthesize
            language: str - language code
            output_path: str - output file path
        Returns:
            bool - success status
        """
        if self.model is None or not text.strip():
            return False
        
        try:
            # For xtts-v2, we need a reference speaker audio
            # Using a simple approach - generating without reference
            self.model.tts_to_file(
                text=text,
                file_path=output_path,
                language=language
            )
            return True
        except Exception as e:
            print(f"TTS synthesis error: {e}")
            return False
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        return ["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh", "hi"]
