"""
Quick launcher for the simple version
"""
import sys
import subprocess
import os

def check_dependencies():
    """Check if basic dependencies are available"""
    try:
        import numpy
        import soundfile
        import yaml
        print("✓ Basic dependencies available")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        return False

def install_lightweight():
    """Install lightweight dependencies"""
    print("📦 Installing lightweight dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-light.txt"], check=True)
        print("✓ Lightweight dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Installation failed: {e}")
        return False

def main():
    """Main launcher"""
    print("🚀 Language Switch TARA - Simple Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("src/main_simple.py"):
        print("✗ Please run this script from the project root directory")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("\n📦 Installing missing dependencies...")
        if not install_lightweight():
            print("✗ Failed to install dependencies")
            return
    
    # Launch the simple version
    print("\n🎯 Starting simple language switch system...")
    print("Choose mode:")
    print("1. Text input mode (recommended for testing)")
    print("2. Real-time audio mode (requires microphone)")
    print("3. File processing mode")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        subprocess.run([sys.executable, "src/main_simple.py", "--mode", "text"])
    elif choice == "2":
        subprocess.run([sys.executable, "src/main_simple.py", "--mode", "realtime"])
    elif choice == "3":
        input_file = input("Enter input audio file path: ").strip()
        output_file = input("Enter output file path (optional): ").strip()
        cmd = [sys.executable, "src/main_simple.py", "--mode", "file", "--input", input_file]
        if output_file:
            cmd.extend(["--output", output_file])
        subprocess.run(cmd)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
