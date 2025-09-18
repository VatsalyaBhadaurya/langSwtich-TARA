"""
Minimalistic Language Detection Module using SpeechBrain
"""
import torch
import speechbrain as sb
from speechbrain.pretrained import EncoderClassifier


class LanguageDetector:
    def __init__(self, confidence_threshold=0.8):
        self.confidence_threshold = confidence_threshold
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the language identification model"""
        try:
            self.model = EncoderClassifier.from_hparams(
                source="speechbrain/lang-id-voxlingua107-ecapa",
                savedir="models/lang-id",
                run_opts={"device": "cpu"}
            )
            print("✓ Language detection model loaded")
        except Exception as e:
            print(f"✗ Failed to load language model: {e}")
            self.model = None
    
    def detect_language(self, audio_tensor):
        """
        Detect language from audio tensor
        Args:
            audio_tensor: torch.Tensor of shape (samples,) or (1, samples)
        Returns:
            tuple: (language_code, confidence_score)
        """
        if self.model is None:
            return "en", 0.0
        
        try:
            # Ensure audio is in correct format
            if audio_tensor.dim() == 1:
                audio_tensor = audio_tensor.unsqueeze(0)
            
            # Get prediction
            prediction = self.model.classify_batch(audio_tensor)
            language = prediction[3][0]  # Language code
            confidence = float(prediction[1][0])  # Confidence score
            
            return language, confidence
        except Exception as e:
            print(f"Language detection error: {e}")
            return "en", 0.0
    
    def is_confidence_high(self, confidence):
        """Check if confidence is above threshold"""
        return confidence >= self.confidence_threshold
