"""
Speech Recognition Test Launcher
Choose which approach to test
"""
import sys
import os
import subprocess

def print_banner():
    """Print welcome banner"""
    print("🎤 Speech Recognition Test Launcher")
    print("=" * 50)
    print("Choose which approach to test:")
    print()

def show_options():
    """Show available test options"""
    options = [
        {
            "id": "1",
            "name": "Vosk Test (Detailed Feedback)",
            "description": "Uses Vosk with detailed processing feedback",
            "file": "src/test_speech.py",
            "pros": "Real-time, shows partial results, detailed feedback"
        },
        {
            "id": "2", 
            "name": "Whisper Test (High Accuracy)",
            "description": "Uses OpenAI Whisper for better accuracy",
            "file": "src/whisper_simple.py",
            "pros": "High accuracy, language detection, works offline"
        },
        {
            "id": "3",
            "name": "Simple Vosk (Basic)",
            "description": "Basic Vosk implementation",
            "file": "src/simple_working.py",
            "pros": "Simple, lightweight, fast"
        },
        {
            "id": "4",
            "name": "Text Mode Test",
            "description": "Test TTS without microphone",
            "file": "src/main_simple.py",
            "args": ["--mode", "text"],
            "pros": "No microphone needed, test TTS only"
        }
    ]
    
    for option in options:
        print(f"{option['id']}. {option['name']}")
        print(f"   {option['description']}")
        print(f"   ✅ {option['pros']}")
        print()

def check_dependencies():
    """Check which dependencies are available"""
    print("🔍 Checking dependencies...")
    
    deps = {
        "vosk": "Vosk",
        "whisper": "Whisper", 
        "pyttsx3": "TTS",
        "pyaudio": "Audio"
    }
    
    available = []
    for dep, name in deps.items():
        try:
            __import__(dep)
            print(f"   ✅ {name}")
            available.append(name)
        except ImportError:
            print(f"   ❌ {name}")
    
    print(f"\n📊 {len(available)}/{len(deps)} dependencies available")
    return available

def run_test(choice):
    """Run the selected test"""
    options = {
        "1": ("src/test_speech.py", "Vosk Test with Detailed Feedback"),
        "2": ("src/whisper_simple.py", "Whisper Test"),
        "3": ("src/simple_working.py", "Simple Vosk Test"),
        "4": ("src/main_simple.py", "Text Mode Test", ["--mode", "text"])
    }
    
    if choice not in options:
        print("❌ Invalid choice")
        return False
    
    option = options[choice]
    file_path = option[0]
    name = option[1]
    args = option[2] if len(option) > 2 else []
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    print(f"🚀 Starting {name}...")
    print("=" * 40)
    
    try:
        cmd = [sys.executable, file_path] + args
        subprocess.run(cmd, check=True)
        return True
    except KeyboardInterrupt:
        print("\n🛑 Test stopped by user")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main launcher"""
    print_banner()
    
    # Check dependencies
    available = check_dependencies()
    print()
    
    # Show options
    show_options()
    
    # Get user choice
    while True:
        try:
            choice = input("Enter your choice (1-4) or 'q' to quit: ").strip()
            
            if choice.lower() == 'q':
                print("👋 Goodbye!")
                break
            
            if choice in ['1', '2', '3', '4']:
                print(f"\n🎯 You selected option {choice}")
                run_test(choice)
                break
            else:
                print("❌ Invalid choice. Please enter 1-4 or 'q'")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()