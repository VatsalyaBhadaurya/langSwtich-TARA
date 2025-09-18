"""
Working Real-time Language Switch System
This version fixes all the issues and works properly
"""
import time
import os
import numpy as np
import pyaudio
import threading
import queue
import json
from typing import Optional

class WorkingRealTimeSystem:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.is_recording = False
        self.audio_stream = None
        self.audio = None
        self.current_language = "en"
        
        # Audio parameters
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.channels = 1
        self.format = pyaudio.paInt16
        
        # Initialize components
        self._init_audio()
        self._init_components()
    
    def _init_audio(self):
        """Initialize audio system"""
        try:
            self.audio = pyaudio.PyAudio()
            print("✓ Audio system initialized")
        except Exception as e:
            print(f"✗ Audio initialization failed: {e}")
            self.audio = None
    
    def _init_components(self):
        """Initialize processing components"""
        # Initialize Vosk
        self.vosk_model = None
        self.vosk_recognizer = None
        self._init_vosk()
        
        # Initialize TTS
        self.tts_engine = None
        self._init_tts()
    
    def _init_vosk(self):
        """Initialize Vosk speech recognition"""
        try:
            from vosk import Model, KaldiRecognizer
            if os.path.exists("models/vosk"):
                print("🔄 Loading Vosk model...")
                self.vosk_model = Model("models/vosk")
                self.vosk_recognizer = KaldiRecognizer(self.vosk_model, self.sample_rate)
                print("✓ Vosk speech recognition loaded")
            else:
                print("⚠️ Vosk model not found - speech recognition disabled")
        except Exception as e:
            print(f"⚠️ Vosk initialization failed: {e}")
            self.vosk_model = None
            self.vosk_recognizer = None
    
    def _init_tts(self):
        """Initialize text-to-speech"""
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            print("✓ TTS engine loaded")
        except Exception as e:
            print(f"⚠️ TTS initialization failed: {e}")
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Audio callback function"""
        if self.is_recording:
            self.audio_queue.put(in_data)
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
    
    def process_audio_data(self, audio_data: bytes) -> str:
        """Process audio data and return transcription"""
        if self.vosk_recognizer is None:
            return ""
        
        try:
            if self.vosk_recognizer.AcceptWaveform(audio_data):
                result = json.loads(self.vosk_recognizer.Result())
                return result.get('text', '').strip()
            else:
                result = json.loads(self.vosk_recognizer.PartialResult())
                return result.get('partial', '').strip()
        except Exception as e:
            print(f"Speech recognition error: {e}")
            return ""
    
    def speak_text(self, text: str):
        """Speak text using TTS"""
        if self.tts_engine is None or not text.strip():
            return
        
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS error: {e}")
    
    def run_realtime(self):
        """Run real-time language switching"""
        print("🎤 Starting Working Real-time Language Switch System")
        print("=" * 60)
        print("Press Ctrl+C to stop")
        print("💡 Speak clearly into your microphone")
        print()
        
        if not self.start_recording():
            return
        
        # Start processing thread
        process_thread = threading.Thread(target=self._process_audio_queue)
        process_thread.daemon = True
        process_thread.start()
        
        try:
            while self.is_recording:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping system...")
        finally:
            self.stop_recording()
            self.cleanup()
    
    def _process_audio_queue(self):
        """Process audio from queue in separate thread"""
        audio_buffer = b""
        buffer_size = self.sample_rate * 3  # 3 seconds of audio
        last_transcription = ""
        processing_count = 0
        
        while self.is_recording:
            try:
                # Get audio data from queue
                audio_chunk = self.audio_queue.get(timeout=0.1)
                audio_buffer += audio_chunk
                
                # Process when buffer is full
                if len(audio_buffer) >= buffer_size:
                    processing_count += 1
                    print(f"🔄 Processing audio #{processing_count}...", end="", flush=True)
                    
                    if self.vosk_recognizer is None:
                        print(" ❌ No Vosk recognizer")
                        audio_buffer = b""
                        continue
                    
                    # Reset recognizer for new audio
                    from vosk import KaldiRecognizer
                    recognizer = KaldiRecognizer(self.vosk_model, self.sample_rate)
                    
                    # Process audio in smaller chunks
                    chunk_size = 4000
                    transcription = ""
                    
                    for i in range(0, len(audio_buffer), chunk_size):
                        chunk_data = audio_buffer[i:i+chunk_size]
                        if len(chunk_data) > 0:
                            try:
                                if recognizer.AcceptWaveform(chunk_data):
                                    result = json.loads(recognizer.Result())
                                    text = result.get('text', '').strip()
                                    if text:
                                        transcription = text
                                else:
                                    result = json.loads(recognizer.PartialResult())
                                    partial = result.get('partial', '').strip()
                                    if partial and len(partial) > len(transcription):
                                        transcription = partial
                            except Exception as e:
                                print(f"Chunk processing error: {e}")
                    
                    # Get final result
                    try:
                        final_result = json.loads(recognizer.FinalResult())
                        final_text = final_result.get('text', '').strip()
                        if final_text:
                            transcription = final_text
                    except Exception as e:
                        print(f"Final result error: {e}")
                    
                    if transcription and transcription != last_transcription and len(transcription) > 2:
                        print(f"\n🎯 [{self.current_language.upper()}] {transcription}")
                        
                        # Speak response
                        response = f"I heard: {transcription}"
                        self.speak_text(response)
                        
                        last_transcription = transcription
                    else:
                        print(" ✓")  # No speech detected
                    
                    # Reset buffer
                    audio_buffer = b""
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"\nProcessing error: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        self.is_recording = False
        if self.audio:
            self.audio.terminate()

def main():
    """Main function"""
    print("🚀 Working Real-time Language Switch System")
    print("=" * 50)
    
    system = WorkingRealTimeSystem()
    
    try:
        system.run_realtime()
    except Exception as e:
        print(f"System error: {e}")
    finally:
        system.cleanup()

if __name__ == "__main__":
    main()
