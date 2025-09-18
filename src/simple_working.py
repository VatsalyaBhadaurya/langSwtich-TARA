"""
Simple Working Real-time Speech Recognition
This version focuses on getting basic speech detection working
"""
import time
import os
import pyaudio
import json
import threading
import queue

class SimpleWorkingSystem:
    def __init__(self):
        self.audio = None
        self.stream = None
        self.is_recording = False
        self.vosk_model = None
        self.vosk_recognizer = None
        self.tts_engine = None
        
        # Audio parameters
        self.sample_rate = 16000
        self.chunk_size = 4000
        self.channels = 1
        self.format = pyaudio.paInt16
        
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
        
        # Initialize Vosk
        try:
            from vosk import Model, KaldiRecognizer
            if os.path.exists("models/vosk"):
                print("🔄 Loading Vosk model...")
                self.vosk_model = Model("models/vosk")
                self.vosk_recognizer = KaldiRecognizer(self.vosk_model, self.sample_rate)
                print("✓ Vosk model loaded")
            else:
                print("⚠️ Vosk model not found")
        except Exception as e:
            print(f"⚠️ Vosk initialization failed: {e}")
        
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
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"TTS error: {e}")
    
    def process_audio_chunk(self, audio_data):
        """Process a chunk of audio data"""
        if not self.vosk_recognizer:
            return ""
        
        try:
            if self.vosk_recognizer.AcceptWaveform(audio_data):
                result = json.loads(self.vosk_recognizer.Result())
                return result.get('text', '').strip()
            else:
                result = json.loads(self.vosk_recognizer.PartialResult())
                return result.get('partial', '').strip()
        except Exception as e:
            print(f"Processing error: {e}")
            return ""
    
    def run(self):
        """Run the real-time system"""
        if not self.audio or not self.vosk_recognizer:
            print("❌ System not properly initialized")
            return
        
        print("🎤 Starting Simple Real-time Speech Recognition")
        print("=" * 50)
        print("Press Ctrl+C to stop")
        print("💡 Speak clearly into your microphone")
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
            
            # Process audio in real-time
            while self.is_recording:
                try:
                    # Read audio data
                    audio_data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                    
                    # Process the audio
                    transcription = self.process_audio_chunk(audio_data)
                    
                    if transcription and len(transcription) > 2:
                        print(f"🎯 Speech detected: {transcription}")
                        
                        # Speak response
                        response = f"I heard: {transcription}"
                        self.speak(response)
                        
                        # Reset recognizer for next phrase
                        from vosk import KaldiRecognizer
                        self.vosk_recognizer = KaldiRecognizer(self.vosk_model, self.sample_rate)
                
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
    print("🚀 Simple Working Speech Recognition")
    print("=" * 40)
    
    system = SimpleWorkingSystem()
    system.run()

if __name__ == "__main__":
    main()
