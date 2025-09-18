"""
Quick test script to verify everything is working
"""
import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    modules = [
        ("numpy", "NumPy"),
        ("pyaudio", "PyAudio"),
        ("pyttsx3", "pyttsx3 TTS"),
        ("vosk", "Vosk"),
        ("json", "JSON"),
        ("threading", "Threading"),
        ("queue", "Queue")
    ]
    
    success = 0
    for module, name in modules:
        try:
            __import__(module)
            print(f"   ✅ {name}")
            success += 1
        except ImportError:
            print(f"   ❌ {name}")
    
    print(f"\n📊 {success}/{len(modules)} modules available")
    return success == len(modules)

def test_vosk_model():
    """Test if Vosk model is available"""
    print("\n🔍 Testing Vosk model...")
    
    if os.path.exists("models/vosk"):
        print("   ✅ Vosk model directory exists")
        
        # Check for key files
        key_files = ["am/final.mdl", "graph/HCLr.fst", "graph/Gr.fst"]
        missing_files = []
        
        for file in key_files:
            if not os.path.exists(f"models/vosk/{file}"):
                missing_files.append(file)
        
        if missing_files:
            print(f"   ⚠️ Missing files: {missing_files}")
            return False
        else:
            print("   ✅ Vosk model files complete")
            return True
    else:
        print("   ❌ Vosk model not found")
        return False

def test_audio():
    """Test audio system"""
    print("\n🎤 Testing audio system...")
    
    try:
        import pyaudio
        audio = pyaudio.PyAudio()
        
        # Check for input devices
        device_count = audio.get_device_count()
        input_devices = []
        
        for i in range(device_count):
            info = audio.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                input_devices.append(info['name'])
        
        if input_devices:
            print(f"   ✅ Found {len(input_devices)} input devices")
            print(f"   📱 Devices: {', '.join(input_devices[:3])}...")
            audio.terminate()
            return True
        else:
            print("   ❌ No input devices found")
            audio.terminate()
            return False
    
    except Exception as e:
        print(f"   ❌ Audio test failed: {e}")
        return False

def test_tts():
    """Test text-to-speech"""
    print("\n🔊 Testing TTS...")
    
    try:
        import pyttsx3
        engine = pyttsx3.init()
        
        # Get available voices
        voices = engine.getProperty('voices')
        if voices:
            print(f"   ✅ TTS engine loaded with {len(voices)} voices")
            return True
        else:
            print("   ⚠️ TTS engine loaded but no voices found")
            return False
    
    except Exception as e:
        print(f"   ❌ TTS test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Language Switch TARA - Quick Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Vosk Model", test_vosk_model),
        ("Audio System", test_audio),
        ("Text-to-Speech", test_tts)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name} Test:")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! System is ready to use.")
        print("\nTo run the system:")
        print("   python src/realtime_working.py")
    else:
        print("\n⚠️ Some tests failed. Check the issues above.")
        print("\nTo fix issues:")
        print("   1. Install missing dependencies: pip install -r requirements-light.txt")
        print("   2. Download Vosk model: python download_models.py")
        print("   3. Check microphone permissions")

if __name__ == "__main__":
    main()
