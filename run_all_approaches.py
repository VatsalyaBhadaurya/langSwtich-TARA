"""
Comprehensive Launcher for All Language Switch Approaches
"""
import sys
import os
import subprocess
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("🌍 Language Switch TARA - Multiple Approaches")
    print("=" * 60)
    print("Choose your preferred approach:")
    print()

def show_approaches():
    """Show available approaches"""
    approaches = [
        {
            "id": "1",
            "name": "Whisper Approach",
            "description": "Uses OpenAI Whisper for both language detection and speech recognition",
            "pros": "High accuracy, built-in language detection, works offline",
            "cons": "Larger model size, slower processing",
            "file": "src/approach_1_whisper.py"
        },
        {
            "id": "2", 
            "name": "Multi-TTS Approach",
            "description": "Multiple TTS engines with fallback options",
            "pros": "Better TTS compatibility, multiple voice options",
            "cons": "Requires multiple TTS engines installed",
            "file": "src/approach_2_simple_tts.py"
        },
        {
            "id": "3",
            "name": "Hybrid Approach", 
            "description": "Combines best available components automatically",
            "pros": "Automatic fallbacks, uses best available tools",
            "cons": "More complex, larger dependencies",
            "file": "src/approach_3_hybrid.py"
        },
        {
            "id": "4",
            "name": "Fixed Real-time Approach",
            "description": "Fixed real-time audio processing with threading",
            "pros": "True real-time processing, better audio handling",
            "cons": "More complex audio management",
            "file": "src/approach_4_realtime_fixed.py"
        },
        {
            "id": "5",
            "name": "Simple Approach (Original)",
            "description": "Original simple version with Vosk + pyttsx3",
            "pros": "Lightweight, easy to understand",
            "cons": "Limited functionality, basic TTS",
            "file": "src/main_simple.py"
        }
    ]
    
    for approach in approaches:
        print(f"{approach['id']}. {approach['name']}")
        print(f"   {approach['description']}")
        print(f"   ✅ Pros: {approach['pros']}")
        print(f"   ⚠️  Cons: {approach['cons']}")
        print()

def check_dependencies():
    """Check which dependencies are available"""
    print("🔍 Checking available dependencies...")
    
    deps = {
        "torch": "PyTorch",
        "whisper": "OpenAI Whisper", 
        "vosk": "Vosk",
        "TTS": "Coqui TTS",
        "pyttsx3": "pyttsx3 TTS",
        "speechbrain": "SpeechBrain"
    }
    
    available = []
    missing = []
    
    for dep, name in deps.items():
        try:
            __import__(dep)
            available.append(name)
            print(f"   ✅ {name}")
        except ImportError:
            missing.append(name)
            print(f"   ❌ {name}")
    
    print(f"\n📊 Summary: {len(available)}/{len(deps)} dependencies available")
    
    if missing:
        print(f"💡 Missing: {', '.join(missing)}")
        print("   Some approaches may not work fully")
    
    return available, missing

def install_whisper():
    """Install Whisper if not available"""
    try:
        import whisper
        print("✅ Whisper already installed")
        return True
    except ImportError:
        print("📦 Installing Whisper...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "openai-whisper"], check=True)
            print("✅ Whisper installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Whisper")
            return False

def run_approach(approach_id: str):
    """Run the selected approach"""
    approaches = {
        "1": ("src/approach_1_whisper.py", "Whisper"),
        "2": ("src/approach_2_simple_tts.py", "Multi-TTS"),
        "3": ("src/approach_3_hybrid.py", "Hybrid"),
        "4": ("src/approach_4_realtime_fixed.py", "Fixed Real-time"),
        "5": ("src/main_simple.py", "Simple")
    }
    
    if approach_id not in approaches:
        print("❌ Invalid approach selected")
        return False
    
    file_path, name = approaches[approach_id]
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    print(f"🚀 Starting {name} approach...")
    print("=" * 40)
    
    try:
        # Special handling for different approaches
        if approach_id == "1":  # Whisper
            if not install_whisper():
                return False
            subprocess.run([sys.executable, file_path, "--help"])
        elif approach_id == "2":  # Multi-TTS
            subprocess.run([sys.executable, file_path])
        elif approach_id == "3":  # Hybrid
            subprocess.run([sys.executable, file_path, "--help"])
        elif approach_id == "4":  # Fixed Real-time
            subprocess.run([sys.executable, file_path])
        elif approach_id == "5":  # Simple
            subprocess.run([sys.executable, file_path, "--help"])
        
        return True
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error running approach: {e}")
        return False

def main():
    """Main launcher"""
    print_banner()
    
    # Check dependencies
    available, missing = check_dependencies()
    print()
    
    # Show approaches
    show_approaches()
    
    # Get user choice
    while True:
        try:
            choice = input("Enter your choice (1-5) or 'q' to quit: ").strip()
            
            if choice.lower() == 'q':
                print("👋 Goodbye!")
                break
            
            if choice in ['1', '2', '3', '4', '5']:
                print(f"\n🎯 You selected approach {choice}")
                run_approach(choice)
                break
            else:
                print("❌ Invalid choice. Please enter 1-5 or 'q'")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
