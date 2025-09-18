"""
Approach 4: Fixed Real-time System
This approach fixes the real-time audio processing issues
"""
import time
import numpy as np
import pyaudio
import threading
import queue
from typing import Optional, Callable

class RealTimeLanguageSwitch:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.is_recording = False
        self.audio_stream = None
        self.audio = None
        self.callback = None
        self.current_language = "en"
        
        # Audio parameters
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.channels = 1
        self.format = pyaudio.paInt16
        
        # Initialize audio
        self._init_audio()
    
    def _init_audio(self):
        """Initialize audio system"""
        try:
            self.audio = pyaudio.PyAudio()
            print("✓ Audio system initialized")
        except Exception as e:
            print(f"✗ Audio initialization failed: {e}")
            self.audio = None
    
    def set_callback(self, callback: Callable[[np.ndarray, str], None]):
        """Set callback function for processed audio"""
        self.callback = callback
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Audio callback function"""
        if self.is_recording:
            # Convert bytes to numpy array
            audio_data = np.frombuffer(in_data, dtype=np.int16)
            audio_data = audio_data.astype(np.float32) / 32768.0
            
            # Add to queue for processing
            self.audio_queue.put(audio_data)
        
        return (in_data, pyaudio.paContinue)
    
    def start_recording(self) -> bool:
        """Start real-time recording"""
        if self.audio is None:
            print("✗ Audio system not initialized")
            return False
        
        try:
            self.audio_stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=self._audio_callback
            )
            
            self.is_recording = True
            self.audio_stream.start_stream()
            print("✓ Recording started")
            return True
        
        except Exception as e:
            print(f"✗ Failed to start recording: {e}")
            return False
    
    def stop_recording(self):
        """Stop recording"""
        self.is_recording = False
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.audio_stream = None
        print("✓ Recording stopped")
    
    def process_audio_queue(self):
        """Process audio from queue"""
        buffer = []
        buffer_size = self.sample_rate * 2  # 2 seconds of audio
        
        while self.is_recording:
            try:
                # Get audio data from queue
                audio_chunk = self.audio_queue.get(timeout=0.1)
                buffer.extend(audio_chunk)
                
                # Process when buffer is full
                if len(buffer) >= buffer_size:
                    audio_array = np.array(buffer[:buffer_size])
                    buffer = buffer[buffer_size//2:]  # Keep overlap
                    
                    # Call callback if set
                    if self.callback:
                        self.callback(audio_array, self.current_language)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Audio processing error: {e}")
    
    def run_realtime(self):
        """Run real-time processing"""
        if not self.start_recording():
            return
        
        # Start processing thread
        process_thread = threading.Thread(target=self.process_audio_queue)
        process_thread.daemon = True
        process_thread.start()
        
        try:
            print("🎤 Real-time processing started")
            print("Press Ctrl+C to stop")
            
            while self.is_recording:
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\n🛑 Stopping...")
        finally:
            self.stop_recording()
    
    def cleanup(self):
        """Clean up resources"""
        self.stop_recording()
        if self.audio:
            self.audio.terminate()

class SimpleRealTimeProcessor:
    """Simple real-time processor with basic functionality"""
    
    def __init__(self):
        self.rt_system = RealTimeLanguageSwitch()
        self.language_detector = None
        self.speech_recognizer = None
        self.text_to_speech = None
        
        # Initialize components
        self._init_components()
        
        # Set up callback
        self.rt_system.set_callback(self.process_audio)
    
    def _init_components(self):
        """Initialize processing components"""
        # Simple language detection
        from language_detector_simple import SimpleLanguageDetector
        self.language_detector = SimpleLanguageDetector()
        
        # Simple speech recognition
        from speech_recognizer_simple import SimpleSpeechRecognizer
        self.speech_recognizer = SimpleSpeechRecognizer()
        
        # Simple TTS
        from text_to_speech_simple import SimpleTextToSpeech
        self.text_to_speech = SimpleTextToSpeech()
        
        print("✓ Components initialized")
    
    def process_audio(self, audio_data: np.ndarray, language: str):
        """Process audio data"""
        try:
            # Detect language
            detected_lang, confidence = self.language_detector.detect_language_simple(
                audio_tensor=torch.tensor(audio_data)
            )
            
            # Only process if confidence is high
            if confidence > 0.6:
                if detected_lang != self.rt_system.current_language:
                    print(f"🔄 Language switched: {self.rt_system.current_language} → {detected_lang}")
                    self.rt_system.current_language = detected_lang
                
                # Transcribe
                audio_bytes = (audio_data * 32768.0).astype(np.int16).tobytes()
                transcription = self.speech_recognizer.transcribe_audio(audio_bytes, detected_lang)
                
                if transcription and len(transcription.strip()) > 3:
                    print(f"[{detected_lang.upper()}] {transcription}")
                    
                    # Simple response
                    response = f"I heard: {transcription}"
                    self.text_to_speech.speak_text(response, detected_lang)
        
        except Exception as e:
            print(f"Processing error: {e}")
    
    def run(self):
        """Run the real-time system"""
        self.rt_system.run_realtime()
    
    def cleanup(self):
        """Clean up"""
        self.rt_system.cleanup()

def main():
    """Main function"""
    import torch
    
    print("🚀 Real-time Language Switch - Fixed Version")
    print("=" * 50)
    
    processor = SimpleRealTimeProcessor()
    
    try:
        processor.run()
    finally:
        processor.cleanup()

if __name__ == "__main__":
    main()
