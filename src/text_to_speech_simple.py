"""
Simple Text-to-Speech Module - Lightweight alternative
"""
import os
from typing import Optional

class SimpleTextToSpeech:
    def __init__(self, model_name="simple"):
        self.model_name = model_name
        self.tts_engine = None
        self._try_load_tts()
    
    def _try_load_tts(self):
        """Try to load TTS engine, fallback to simple mode if not available"""
        # Try Coqui TTS first
        try:
            from TTS.api import TTS
            self.tts_engine = TTS(model_name=self.model_name, progress_bar=False, gpu=False)
            print("✓ Coqui TTS loaded successfully")
            return
        except ImportError:
            print("⚠️ Coqui TTS not available")
        except Exception as e:
            print(f"⚠️ Coqui TTS loading failed: {e}")
        
        # Try pyttsx3 as fallback
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            print("✓ pyttsx3 TTS loaded successfully")
        except ImportError:
            print("⚠️ pyttsx3 not available")
        except Exception as e:
            print(f"⚠️ pyttsx3 loading failed: {e}")
            self.tts_engine = None
    
    def synthesize_speech(self, text: str, language: str = "en", output_path: str = "output.wav") -> bool:
        """
        Synthesize speech from text
        Args:
            text: str - text to synthesize
            language: str - language code
            output_path: str - output file path
        Returns:
            bool - success status
        """
        if not text.strip():
            return False
        
        if self.tts_engine is None:
            print(f"[TTS] Would synthesize: '{text}' in {language}")
            return False
        
        try:
            # Check if it's Coqui TTS
            if hasattr(self.tts_engine, 'tts_to_file'):
                self.tts_engine.tts_to_file(
                    text=text,
                    file_path=output_path,
                    language=language
                )
            # Check if it's pyttsx3
            elif hasattr(self.tts_engine, 'save_to_file'):
                self.tts_engine.save_to_file(text, output_path)
                self.tts_engine.runAndWait()
            else:
                print(f"[TTS] Would synthesize: '{text}' in {language}")
                return False
            
            print(f"✓ Speech synthesized: {output_path}")
            return True
        except Exception as e:
            print(f"TTS synthesis error: {e}")
            return False
    
    def speak_text(self, text: str, language: str = "en") -> bool:
        """
        Speak text directly (for real-time mode)
        """
        if not text.strip():
            return False
        
        if self.tts_engine is None:
            print(f"[TTS] Would speak: '{text}' in {language}")
            return False
        
        try:
            # Check if it's pyttsx3
            if hasattr(self.tts_engine, 'say'):
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                return True
            else:
                print(f"[TTS] Would speak: '{text}' in {language}")
                return False
        except Exception as e:
            print(f"TTS speak error: {e}")
            return False
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return ["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh", "hi"]
