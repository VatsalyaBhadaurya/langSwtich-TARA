"""
Minimalistic Audio Handling Module
"""
import pyaudio
import wave
import numpy as np
import torch
import soundfile as sf
from typing import Optional, Tuple


class AudioHandler:
    def __init__(self, sample_rate=16000, chunk_size=4000):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.audio = pyaudio.PyAudio()
        self.stream = None
    
    def start_recording(self):
        """Start audio recording stream"""
        try:
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            return True
        except Exception as e:
            print(f"Failed to start recording: {e}")
            return False
    
    def stop_recording(self):
        """Stop audio recording stream"""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
    
    def read_audio_chunk(self) -> Optional[bytes]:
        """Read a chunk of audio data"""
        if self.stream:
            try:
                return self.stream.read(self.chunk_size, exception_on_overflow=False)
            except Exception as e:
                print(f"Audio read error: {e}")
                return None
        return None
    
    def bytes_to_tensor(self, audio_bytes: bytes) -> torch.Tensor:
        """Convert audio bytes to PyTorch tensor"""
        try:
            # Convert bytes to numpy array
            audio_array = np.frombuffer(audio_bytes, dtype=np.int16)
            # Normalize to [-1, 1] range
            audio_array = audio_array.astype(np.float32) / 32768.0
            # Convert to tensor
            return torch.tensor(audio_array, dtype=torch.float32)
        except Exception as e:
            print(f"Audio conversion error: {e}")
            return torch.tensor([])
    
    def save_audio(self, audio_tensor: torch.Tensor, filepath: str):
        """Save audio tensor to file"""
        try:
            # Convert tensor to numpy and denormalize
            audio_array = audio_tensor.numpy()
            audio_array = (audio_array * 32768.0).astype(np.int16)
            # Save as WAV file
            sf.write(filepath, audio_array, self.sample_rate)
            return True
        except Exception as e:
            print(f"Audio save error: {e}")
            return False
    
    def cleanup(self):
        """Clean up audio resources"""
        self.stop_recording()
        self.audio.terminate()
