"""
Simple test script for Language Switch TARA
"""
import sys
import os

# Add src to path
sys.path.append('src')

def test_imports():
    """Test if all modules can be imported"""
    try:
        from language_detector import LanguageDetector
        print("✓ LanguageDetector imported successfully")
    except Exception as e:
        print(f"✗ LanguageDetector import failed: {e}")
    
    try:
        from speech_recognizer import SpeechRecognizer
        print("✓ SpeechRecognizer imported successfully")
    except Exception as e:
        print(f"✗ SpeechRecognizer import failed: {e}")
    
    try:
        from text_to_speech import TextToSpeech
        print("✓ TextToSpeech imported successfully")
    except Exception as e:
        print(f"✗ TextToSpeech import failed: {e}")
    
    try:
        from audio_handler import AudioHandler
        print("✓ AudioHandler imported successfully")
    except Exception as e:
        print(f"✗ AudioHandler import failed: {e}")

def test_basic_functionality():
    """Test basic functionality without models"""
    print("\n--- Testing Basic Functionality ---")
    
    # Test language detector initialization
    try:
        from language_detector import LanguageDetector
        detector = LanguageDetector()
        print("✓ LanguageDetector initialized")
    except Exception as e:
        print(f"✗ LanguageDetector initialization failed: {e}")
    
    # Test speech recognizer initialization
    try:
        from speech_recognizer import SpeechRecognizer
        recognizer = SpeechRecognizer()
        print("✓ SpeechRecognizer initialized")
    except Exception as e:
        print(f"✗ SpeechRecognizer initialization failed: {e}")
    
    # Test TTS initialization
    try:
        from text_to_speech import TextToSpeech
        tts = TextToSpeech()
        print("✓ TextToSpeech initialized")
    except Exception as e:
        print(f"✗ TextToSpeech initialization failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing Language Switch TARA System")
    print("=" * 40)
    
    test_imports()
    test_basic_functionality()
    
    print("\n" + "=" * 40)
    print("Test completed!")
    print("\nTo run the full system:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Download models (see README.md)")
    print("3. Run: python src/main.py --mode realtime")
