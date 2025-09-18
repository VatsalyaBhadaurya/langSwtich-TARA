"""
Simple Whisper-based Speech Recognition
This uses Whisper which is more reliable for speech detection
"""
import time
import os
import whisper
import pyaudio
import numpy as np
import threading
import queue

class WhisperSpeechSystem:
    def __init__(self):
        self.audio = None
        self.stream = None
        self.is_recording = False
        self.whisper_model = None
        self.tts_engine = None
        
        # Audio parameters
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.channels = 1
        self.format = pyaudio.paInt16
        
        # Audio buffer
        self.audio_buffer = []
        self.buffer_size = self.sample_rate * 5  # 5 seconds
        
        self._init_components()
    
    def _init_components(self):
        """Initialize all components"""
        print("🔄 Initializing components...")
        
        # Initialize audio
        try:
            self.audio = pyaudio.PyAudio()
            print("✓ Audio system initialized")
        except Exception as e:
            print(f"✗ Audio initialization failed: {e}")
            return
        
        # Initialize Whisper
        try:
            print("🔄 Loading Whisper model (this may take a moment)...")
            self.whisper_model = whisper.load_model("base")
            print("✓ Whisper model loaded")
        except Exception as e:
            print(f"⚠️ Whisper initialization failed: {e}")
        
        # Initialize TTS
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            print("✓ TTS engine loaded")
        except Exception as e:
            print(f"⚠️ TTS initialization failed: {e}")
    
    def speak(self, text):
        """Speak text"""
        if self.tts_engine and text:
            try:
                print(f"🔊 Speaking: {text}")
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"TTS error: {e}")
    
    def process_audio_buffer(self):
        """Process accumulated audio buffer"""
        if not self.whisper_model or len(self.audio_buffer) < self.sample_rate:
            return ""
        
        try:
            # Convert buffer to numpy array
            audio_array = np.array(self.audio_buffer, dtype=np.float32)
            
            # Transcribe with Whisper
            result = self.whisper_model.transcribe(
                audio_array,
                language=None,  # Auto-detect language
                task="transcribe"
            )
            
            transcription = result.get("text", "").strip()
            language = result.get("language", "en")
            
            if transcription:
                print(f"🎯 [{language.upper()}] {transcription}")
                return transcription, language
            
            return "", language
            
        except Exception as e:
            print(f"Whisper processing error: {e}")
            return "", "en"
    
    def run(self):
        """Run the real-time system"""
        if not self.audio or not self.whisper_model:
            print("❌ System not properly initialized")
            return
        
        print("🎤 Starting Whisper Speech Recognition")
        print("=" * 50)
        print("Press Ctrl+C to stop")
        print("💡 Speak clearly into your microphone")
        print("📊 Processing every 5 seconds")
        print()
        
        try:
            # Start audio stream
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            self.is_recording = True
            print("✓ Recording started")
            print("🎯 Listening for speech...")
            print()
            
            chunk_count = 0
            last_transcription = ""
            
            # Process audio in real-time
            while self.is_recording:
                try:
                    # Read audio data
                    audio_data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                    chunk_count += 1
                    
                    # Convert to float and add to buffer
                    audio_array = np.frombuffer(audio_data, dtype=np.int16)
                    audio_array = audio_array.astype(np.float32) / 32768.0
                    self.audio_buffer.extend(audio_array)
                    
                    # Show progress
                    if chunk_count % 50 == 0:
                        buffer_seconds = len(self.audio_buffer) / self.sample_rate
                        print(f"📊 Buffer: {buffer_seconds:.1f}s, Chunks: {chunk_count}")
                    
                    # Process when buffer is full
                    if len(self.audio_buffer) >= self.buffer_size:
                        print("🔄 Processing audio buffer...")
                        
                        transcription, language = self.process_audio_buffer()
                        
                        if transcription and transcription != last_transcription:
                            print(f"🎯 SPEECH DETECTED: {transcription}")
                            
                            # Speak response
                            response = f"I heard: {transcription}"
                            self.speak(response)
                            
                            last_transcription = transcription
                        else:
                            print("📝 No speech detected in this segment")
                        
                        # Clear buffer
                        self.audio_buffer = []
                        print("🔄 Buffer cleared, listening again...")
                        print()
                
                except Exception as e:
                    print(f"Audio processing error: {e}")
                    time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\n🛑 Stopping system...")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.is_recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()
        print("✓ System cleaned up")

def main():
    """Main function"""
    print("🚀 Whisper Speech Recognition System")
    print("=" * 40)
    print("This uses OpenAI Whisper for better accuracy")
    print("Speak clearly and wait for processing")
    print()
    
    system = WhisperSpeechSystem()
    system.run()

if __name__ == "__main__":
    main()
