"""
Approach 1: Using OpenAI Whisper for Speech Recognition
This approach uses Whisper which has built-in language detection
"""
import os
import whisper
import torch
import soundfile as sf
from typing import Optional, Tuple

class WhisperLanguageSwitch:
    def __init__(self, model_size="base"):
        """
        Initialize Whisper-based language switch
        model_size: tiny, base, small, medium, large
        """
        self.model_size = model_size
        self.model = None
        self.current_language = "en"
        self._load_model()
    
    def _load_model(self):
        """Load Whisper model"""
        try:
            print(f"🔄 Loading Whisper model ({self.model_size})...")
            self.model = whisper.load_model(self.model_size)
            print("✓ Whisper model loaded successfully")
        except Exception as e:
            print(f"✗ Failed to load Whisper model: {e}")
            self.model = None
    
    def process_audio_file(self, audio_path: str, output_path: str = None) -> dict:
        """
        Process audio file with Whisper
        Returns: dict with transcription, language, and confidence
        """
        if self.model is None:
            return {"error": "Model not loaded"}
        
        try:
            # Transcribe with language detection
            result = self.model.transcribe(
                audio_path,
                language=None,  # Auto-detect language
                task="transcribe"
            )
            
            detected_lang = result.get("language", "en")
            transcription = result.get("text", "").strip()
            segments = result.get("segments", [])
            
            # Calculate average confidence
            confidences = [seg.get("no_speech_prob", 0) for seg in segments if "no_speech_prob" in seg]
            avg_confidence = 1 - (sum(confidences) / len(confidences)) if confidences else 0.8
            
            return {
                "transcription": transcription,
                "language": detected_lang,
                "confidence": avg_confidence,
                "segments": segments
            }
            
        except Exception as e:
            return {"error": f"Processing failed: {e}"}
    
    def process_audio_data(self, audio_data: np.ndarray, sample_rate: int = 16000) -> dict:
        """
        Process audio data directly
        """
        if self.model is None:
            return {"error": "Model not loaded"}
        
        try:
            # Save temporary file
            temp_path = "temp_audio.wav"
            sf.write(temp_path, audio_data, sample_rate)
            
            result = self.process_audio_file(temp_path)
            
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return result
            
        except Exception as e:
            return {"error": f"Processing failed: {e}"}
    
    def switch_language(self, new_language: str):
        """Manually switch language"""
        self.current_language = new_language
        print(f"Language switched to: {new_language}")

def main():
    """Test Whisper approach"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Whisper Language Switch")
    parser.add_argument("--input", type=str, help="Input audio file")
    parser.add_argument("--output", type=str, help="Output text file")
    parser.add_argument("--model", type=str, default="base", help="Whisper model size")
    
    args = parser.parse_args()
    
    # Create system
    system = WhisperLanguageSwitch(model_size=args.model)
    
    if args.input:
        # Process file
        result = system.process_audio_file(args.input)
        
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Language: {result['language']}")
            print(f"Confidence: {result['confidence']:.2f}")
            print(f"Transcription: {result['transcription']}")
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(f"Language: {result['language']}\n")
                    f.write(f"Confidence: {result['confidence']:.2f}\n")
                    f.write(f"Transcription: {result['transcription']}\n")
                print(f"Results saved to: {args.output}")
    else:
        print("Please provide --input audio file")

if __name__ == "__main__":
    main()
