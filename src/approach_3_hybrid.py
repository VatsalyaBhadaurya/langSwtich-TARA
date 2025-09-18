"""
Approach 3: Hybrid System - Combines multiple approaches
This approach uses the best available components for each task
"""
import os
import time
import numpy as np
import torch
import soundfile as sf
from typing import Optional, Dict, Any

class HybridLanguageSwitch:
    def __init__(self):
        self.language_detector = None
        self.speech_recognizer = None
        self.text_to_speech = None
        self.current_language = "en"
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize the best available components"""
        print("🔄 Initializing Hybrid Language Switch System...")
        
        # Initialize language detection
        self._init_language_detection()
        
        # Initialize speech recognition
        self._init_speech_recognition()
        
        # Initialize text-to-speech
        self._init_text_to_speech()
        
        print("✓ Hybrid system initialized")
    
    def _init_language_detection(self):
        """Initialize language detection (try multiple options)"""
        # Try SpeechBrain first
        try:
            from speechbrain.pretrained import EncoderClassifier
            self.language_detector = EncoderClassifier.from_hparams(
                source="speechbrain/lang-id-voxlingua107-ecapa",
                savedir="models/lang-id",
                run_opts={"device": "cpu"}
            )
            print("✓ SpeechBrain language detection loaded")
            return
        except:
            pass
        
        # Try Whisper for language detection
        try:
            import whisper
            self.language_detector = whisper.load_model("base")
            print("✓ Whisper language detection loaded")
            return
        except:
            pass
        
        # Fallback to simple detection
        from language_detector_simple import SimpleLanguageDetector
        self.language_detector = SimpleLanguageDetector()
        print("✓ Simple language detection loaded")
    
    def _init_speech_recognition(self):
        """Initialize speech recognition (try multiple options)"""
        # Try Vosk first
        try:
            from vosk import Model, KaldiRecognizer
            if os.path.exists("models/vosk"):
                model = Model("models/vosk")
                self.speech_recognizer = KaldiRecognizer(model, 16000)
                print("✓ Vosk speech recognition loaded")
                return
        except:
            pass
        
        # Try Whisper
        try:
            import whisper
            if self.language_detector and hasattr(self.language_detector, 'transcribe'):
                # Whisper is already loaded for language detection
                print("✓ Whisper speech recognition loaded")
                return
        except:
            pass
        
        # Fallback to simple recognition
        from speech_recognizer_simple import SimpleSpeechRecognizer
        self.speech_recognizer = SimpleSpeechRecognizer()
        print("✓ Simple speech recognition loaded")
    
    def _init_text_to_speech(self):
        """Initialize text-to-speech (try multiple options)"""
        # Try Coqui TTS
        try:
            from TTS.api import TTS
            self.text_to_speech = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", 
                                    progress_bar=False, gpu=False)
            print("✓ Coqui TTS loaded")
            return
        except:
            pass
        
        # Try pyttsx3
        try:
            import pyttsx3
            self.text_to_speech = pyttsx3.init()
            print("✓ pyttsx3 TTS loaded")
            return
        except:
            pass
        
        # Fallback to simple TTS
        from text_to_speech_simple import SimpleTextToSpeech
        self.text_to_speech = SimpleTextToSpeech()
        print("✓ Simple TTS loaded")
    
    def detect_language(self, audio_data: np.ndarray) -> tuple:
        """Detect language from audio"""
        if self.language_detector is None:
            return "en", 0.5
        
        try:
            # Check if it's SpeechBrain
            if hasattr(self.language_detector, 'classify_batch'):
                audio_tensor = torch.tensor(audio_data, dtype=torch.float32)
                if audio_tensor.dim() == 1:
                    audio_tensor = audio_tensor.unsqueeze(0)
                prediction = self.language_detector.classify_batch(audio_tensor)
                language = prediction[3][0]
                confidence = float(prediction[1][0])
                return language, confidence
            
            # Check if it's Whisper
            elif hasattr(self.language_detector, 'transcribe'):
                # Save temporary file for Whisper
                temp_path = "temp_detect.wav"
                sf.write(temp_path, audio_data, 16000)
                result = self.language_detector.transcribe(temp_path, language=None)
                os.remove(temp_path)
                return result.get("language", "en"), 0.8
            
            # Fallback to simple detection
            else:
                return self.language_detector.detect_language_simple(audio_tensor=torch.tensor(audio_data))
        
        except Exception as e:
            print(f"Language detection error: {e}")
            return "en", 0.5
    
    def transcribe_audio(self, audio_data: np.ndarray, language: str = "en") -> str:
        """Transcribe audio to text"""
        if self.speech_recognizer is None:
            return ""
        
        try:
            # Check if it's Vosk
            if hasattr(self.speech_recognizer, 'AcceptWaveform'):
                audio_bytes = (audio_data * 32768.0).astype(np.int16).tobytes()
                if self.speech_recognizer.AcceptWaveform(audio_bytes):
                    import json
                    result = json.loads(self.speech_recognizer.Result())
                    return result.get('text', '').strip()
                else:
                    result = json.loads(self.speech_recognizer.PartialResult())
                    return result.get('partial', '').strip()
            
            # Check if it's Whisper
            elif hasattr(self.speech_recognizer, 'transcribe'):
                temp_path = "temp_transcribe.wav"
                sf.write(temp_path, audio_data, 16000)
                result = self.speech_recognizer.transcribe(temp_path, language=language)
                os.remove(temp_path)
                return result.get("text", "").strip()
            
            # Fallback
            else:
                return self.speech_recognizer.transcribe_text_input("")
        
        except Exception as e:
            print(f"Speech recognition error: {e}")
            return ""
    
    def synthesize_speech(self, text: str, language: str = "en", output_path: str = None) -> bool:
        """Synthesize speech from text"""
        if self.text_to_speech is None or not text.strip():
            return False
        
        try:
            # Check if it's Coqui TTS
            if hasattr(self.text_to_speech, 'tts_to_file'):
                if output_path:
                    self.text_to_speech.tts_to_file(text=text, file_path=output_path, language=language)
                else:
                    self.text_to_speech.tts_to_file(text=text, file_path="temp_output.wav", language=language)
                return True
            
            # Check if it's pyttsx3
            elif hasattr(self.text_to_speech, 'save_to_file'):
                if output_path:
                    self.text_to_speech.save_to_file(text, output_path)
                else:
                    self.text_to_speech.say(text)
                self.text_to_speech.runAndWait()
                return True
            
            # Fallback
            else:
                return self.text_to_speech.synthesize_speech(text, language, output_path)
        
        except Exception as e:
            print(f"TTS synthesis error: {e}")
            return False
    
    def process_audio_file(self, input_path: str, output_path: str = None) -> Dict[str, Any]:
        """Process audio file through the complete pipeline"""
        try:
            # Load audio
            audio_data, sample_rate = sf.read(input_path)
            
            # Detect language
            language, confidence = self.detect_language(audio_data)
            print(f"Detected language: {language} (confidence: {confidence:.2f})")
            
            # Transcribe
            transcription = self.transcribe_audio(audio_data, language)
            print(f"Transcription: {transcription}")
            
            # Synthesize response
            if output_path and transcription:
                success = self.synthesize_speech(transcription, language, output_path)
                if success:
                    print(f"✓ Output saved to: {output_path}")
            
            return {
                "language": language,
                "confidence": confidence,
                "transcription": transcription,
                "success": True
            }
        
        except Exception as e:
            return {"error": str(e), "success": False}

def main():
    """Test hybrid approach"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Hybrid Language Switch")
    parser.add_argument("--input", type=str, help="Input audio file")
    parser.add_argument("--output", type=str, help="Output audio file")
    
    args = parser.parse_args()
    
    # Create system
    system = HybridLanguageSwitch()
    
    if args.input:
        result = system.process_audio_file(args.input, args.output)
        if result["success"]:
            print("✓ Processing completed successfully")
        else:
            print(f"✗ Processing failed: {result.get('error', 'Unknown error')}")
    else:
        print("Please provide --input audio file")

if __name__ == "__main__":
    main()
