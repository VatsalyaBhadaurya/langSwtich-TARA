"""
Approach 2: Simple Text-to-Speech with Multiple Engines
This approach provides multiple TTS options for better compatibility
"""
import os
import subprocess
import tempfile
from typing import Optional, List

class MultiTTSEngine:
    def __init__(self):
        self.engines = []
        self._detect_engines()
    
    def _detect_engines(self):
        """Detect available TTS engines"""
        # Try pyttsx3
        try:
            import pyttsx3
            engine = pyttsx3.init()
            self.engines.append(("pyttsx3", engine))
            print("✓ pyttsx3 TTS available")
        except:
            pass
        
        # Try espeak (if available)
        try:
            result = subprocess.run(["espeak", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.engines.append(("espeak", None))
                print("✓ espeak TTS available")
        except:
            pass
        
        # Try Windows SAPI
        try:
            import win32com.client
            engine = win32com.client.Dispatch("SAPI.SpVoice")
            self.engines.append(("sapi", engine))
            print("✓ Windows SAPI TTS available")
        except:
            pass
        
        if not self.engines:
            print("⚠️ No TTS engines available")
    
    def speak_text(self, text: str, language: str = "en") -> bool:
        """Speak text using available engines"""
        if not text.strip():
            return False
        
        for engine_name, engine in self.engines:
            try:
                if engine_name == "pyttsx3":
                    engine.say(text)
                    engine.runAndWait()
                    return True
                elif engine_name == "espeak":
                    # Use espeak command
                    cmd = ["espeak", "-v", language, text]
                    subprocess.run(cmd, check=True)
                    return True
                elif engine_name == "sapi":
                    engine.Speak(text)
                    return True
            except Exception as e:
                print(f"TTS engine {engine_name} failed: {e}")
                continue
        
        print(f"[TTS] Would speak: '{text}' in {language}")
        return False
    
    def save_audio(self, text: str, output_path: str, language: str = "en") -> bool:
        """Save speech to audio file"""
        if not text.strip():
            return False
        
        for engine_name, engine in self.engines:
            try:
                if engine_name == "pyttsx3":
                    engine.save_to_file(text, output_path)
                    engine.runAndWait()
                    return True
                elif engine_name == "espeak":
                    cmd = ["espeak", "-v", language, "-w", output_path, text]
                    subprocess.run(cmd, check=True)
                    return True
                elif engine_name == "sapi":
                    # SAPI doesn't directly support file output
                    continue
            except Exception as e:
                print(f"TTS engine {engine_name} failed: {e}")
                continue
        
        print(f"[TTS] Would save: '{text}' to {output_path}")
        return False
    
    def get_available_voices(self) -> List[str]:
        """Get list of available voices"""
        voices = []
        for engine_name, engine in self.engines:
            if engine_name == "pyttsx3":
                try:
                    voices.extend([v.name for v in engine.getProperty('voices')])
                except:
                    pass
        return voices

def main():
    """Test Multi-TTS approach"""
    tts = MultiTTSEngine()
    
    print("🎤 Multi-TTS Engine Test")
    print("=" * 30)
    
    while True:
        text = input("Enter text to speak (or 'quit'): ").strip()
        if text.lower() == 'quit':
            break
        
        if text:
            tts.speak_text(text)
            print("✓ Speech completed")

if __name__ == "__main__":
    main()
