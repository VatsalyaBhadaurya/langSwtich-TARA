"""
Minimalistic Real-time Language Switch System
"""
import time
import yaml
import os
import numpy as np
import torch
import soundfile as sf
from typing import Optional

from language_detector import LanguageDetector
from speech_recognizer import SpeechRecognizer
from text_to_speech import TextToSpeech
from audio_handler import AudioHandler


class LanguageSwitchSystem:
    def __init__(self, config_path="config.yaml"):
        self.config = self._load_config(config_path)
        self.language_detector = LanguageDetector(
            confidence_threshold=self.config['models']['language_detection']['confidence_threshold']
        )
        self.speech_recognizer = SpeechRecognizer(
            model_path=self.config['models']['speech_recognition']['model_path']
        )
        self.text_to_speech = TextToSpeech(
            model_name=self.config['models']['text_to_speech']['model_name']
        )
        self.audio_handler = AudioHandler(
            sample_rate=self.config['audio']['sample_rate'],
            chunk_size=self.config['audio']['chunk_size']
        )
        self.current_language = "en"
        self.is_running = False
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"Config load error: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """Get default configuration"""
        return {
            'audio': {'sample_rate': 16000, 'chunk_size': 4000},
            'models': {
                'language_detection': {'confidence_threshold': 0.8},
                'speech_recognition': {'model_path': 'models/vosk'},
                'text_to_speech': {'model_name': 'tts_models/multilingual/multi-dataset/xtts_v2'}
            }
        }
    
    def process_audio_chunk(self, audio_bytes: bytes) -> Optional[str]:
        """
        Process a single audio chunk through the pipeline
        Returns transcribed text if language is detected with high confidence
        """
        # Convert to tensor for language detection
        audio_tensor = self.audio_handler.bytes_to_tensor(audio_bytes)
        
        if audio_tensor.numel() == 0:
            return None
        
        # Detect language
        detected_lang, confidence = self.language_detector.detect_language(audio_tensor)
        
        # Only process if confidence is high enough
        if self.language_detector.is_confidence_high(confidence):
            if detected_lang != self.current_language:
                print(f"Language switched: {self.current_language} → {detected_lang} (confidence: {confidence:.2f})")
                self.current_language = detected_lang
            
            # Transcribe speech
            transcription = self.speech_recognizer.transcribe_audio(audio_bytes, detected_lang)
            return transcription
        
        return None
    
    def run_realtime(self):
        """Run real-time language switching"""
        print("🎤 Starting real-time language switch system...")
        print("Press Ctrl+C to stop")
        
        if not self.audio_handler.start_recording():
            print("✗ Failed to start audio recording")
            return
        
        self.is_running = True
        audio_buffer = b""
        
        try:
            while self.is_running:
                # Read audio chunk
                chunk = self.audio_handler.read_audio_chunk()
                if chunk is None:
                    continue
                
                audio_buffer += chunk
                
                # Process when buffer is full enough
                if len(audio_buffer) >= self.config['audio']['chunk_size'] * 4:  # Process every 4 chunks
                    transcription = self.process_audio_chunk(audio_buffer)
                    
                    if transcription and transcription.strip():
                        print(f"[{self.current_language.upper()}] {transcription}")
                        
                        # Synthesize response (optional)
                        # self.text_to_speech.synthesize_speech(
                        #     f"I heard: {transcription}",
                        #     self.current_language,
                        #     f"response_{int(time.time())}.wav"
                        # )
                    
                    audio_buffer = b""  # Reset buffer
                
                time.sleep(0.01)  # Small delay to prevent CPU overload
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping system...")
        finally:
            self.cleanup()
    
    def process_file(self, input_file: str, output_file: str = None):
        """Process an audio file"""
        print(f"📁 Processing file: {input_file}")
        
        try:
            # Load audio file
            audio_data, sample_rate = sf.read(input_file)
            audio_tensor = torch.tensor(audio_data, dtype=torch.float32)
            
            # Detect language
            detected_lang, confidence = self.language_detector.detect_language(audio_tensor)
            print(f"Detected language: {detected_lang} (confidence: {confidence:.2f})")
            
            if not self.language_detector.is_confidence_high(confidence):
                print("⚠️ Low confidence in language detection")
                return
            
            # Convert to bytes for Vosk
            audio_bytes = (audio_tensor * 32768.0).numpy().astype(np.int16).tobytes()
            
            # Transcribe
            transcription = self.speech_recognizer.transcribe_audio(audio_bytes, detected_lang)
            print(f"Transcription: {transcription}")
            
            # Synthesize
            if output_file:
                success = self.text_to_speech.synthesize_speech(
                    transcription, detected_lang, output_file
                )
                if success:
                    print(f"✓ Output saved to: {output_file}")
                else:
                    print("✗ TTS synthesis failed")
            
        except Exception as e:
            print(f"File processing error: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        self.is_running = False
        self.audio_handler.cleanup()
        print("✓ System cleaned up")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Real-time Language Switch System")
    parser.add_argument("--mode", choices=["realtime", "file"], default="realtime",
                       help="Run mode: realtime or file processing")
    parser.add_argument("--input", type=str, help="Input audio file (for file mode)")
    parser.add_argument("--output", type=str, help="Output audio file (for file mode)")
    
    args = parser.parse_args()
    
    # Create system
    system = LanguageSwitchSystem()
    
    if args.mode == "realtime":
        system.run_realtime()
    elif args.mode == "file" and args.input:
        system.process_file(args.input, args.output)
    else:
        print("Please specify --input file for file mode")


if __name__ == "__main__":
    main()
