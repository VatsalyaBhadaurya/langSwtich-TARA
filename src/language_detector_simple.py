"""
Simple Language Detection Module - Lightweight alternative
"""
import os
import json
from typing import Tuple, Optional

class SimpleLanguageDetector:
    def __init__(self, confidence_threshold=0.8):
        self.confidence_threshold = confidence_threshold
        self.supported_languages = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
            'ko': 'Korean', 'zh': 'Chinese', 'hi': 'Hindi', 'ar': 'Arabic'
        }
        self.current_language = 'en'
        self.detection_count = 0
        self.language_counts = {}
    
    def detect_language_simple(self, audio_tensor=None, text_hint: str = None) -> Tuple[str, float]:
        """
        Simple language detection based on text patterns or user input
        Args:
            audio_tensor: torch.Tensor (not used in simple version)
            text_hint: str - optional text hint for language detection
        Returns:
            tuple: (language_code, confidence_score)
        """
        # If we have text, try to detect language from it
        if text_hint:
            return self._detect_from_text(text_hint)
        
        # For now, return a default language with medium confidence
        # In a real implementation, you could use audio features
        return self.current_language, 0.7
    
    def _detect_from_text(self, text: str) -> Tuple[str, float]:
        """Detect language from text patterns"""
        text_lower = text.lower()
        
        # Simple pattern matching for common languages
        patterns = {
            'en': ['the', 'and', 'is', 'are', 'was', 'were', 'have', 'has', 'had'],
            'es': ['el', 'la', 'de', 'que', 'y', 'en', 'un', 'es', 'se', 'no'],
            'fr': ['le', 'la', 'de', 'et', 'à', 'un', 'il', 'que', 'ne', 'se'],
            'de': ['der', 'die', 'das', 'und', 'ist', 'sind', 'haben', 'mit', 'von'],
            'hi': ['है', 'हैं', 'का', 'की', 'के', 'में', 'से', 'को', 'पर', 'तो'],
            'zh': ['的', '了', '在', '是', '我', '你', '他', '她', '它', '们'],
            'ja': ['です', 'ます', 'の', 'を', 'に', 'は', 'が', 'と', 'で', 'から'],
            'ko': ['입니다', '습니다', '의', '을', '를', '에', '에서', '와', '과', '로']
        }
        
        scores = {}
        for lang, patterns_list in patterns.items():
            score = sum(1 for pattern in patterns_list if pattern in text_lower)
            if score > 0:
                scores[lang] = score / len(patterns_list)
        
        if scores:
            best_lang = max(scores, key=scores.get)
            confidence = min(scores[best_lang] * 2, 1.0)  # Scale confidence
            return best_lang, confidence
        
        return 'en', 0.5  # Default fallback
    
    def set_language(self, language: str):
        """Manually set the current language"""
        if language in self.supported_languages:
            self.current_language = language
            print(f"Language set to: {self.supported_languages[language]}")
        else:
            print(f"Unsupported language: {language}")
    
    def is_confidence_high(self, confidence: float) -> bool:
        """Check if confidence is above threshold"""
        return confidence >= self.confidence_threshold
    
    def get_supported_languages(self) -> dict:
        """Get list of supported languages"""
        return self.supported_languages
