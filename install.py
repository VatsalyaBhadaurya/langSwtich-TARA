"""
Installation script for Language Switch TARA
"""
import os
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def download_file(url, filename, description):
    """Download a file from URL"""
    print(f"⬇️ {description}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"✓ {description} downloaded")
        return True
    except Exception as e:
        print(f"✗ {description} failed: {e}")
        return False

def extract_zip(zip_path, extract_to, description):
    """Extract zip file"""
    print(f"📂 {description}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"✓ {description} extracted")
        return True
    except Exception as e:
        print(f"✗ {description} failed: {e}")
        return False

def main():
    """Main installation process"""
    print("🚀 Installing Language Switch TARA")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8+ is required")
        return False
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    # Create models directory
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    print("✓ Models directory created")
    
    # Download Vosk model (small English model)
    vosk_url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
    vosk_zip = "models/vosk-model-small-en-us-0.15.zip"
    vosk_dir = "models/vosk"
    
    if not os.path.exists(vosk_dir):
        if download_file(vosk_url, vosk_zip, "Downloading Vosk model"):
            if extract_zip(vosk_zip, "models", "Extracting Vosk model"):
                # Rename extracted folder to 'vosk'
                extracted_folder = "models/vosk-model-small-en-us-0.15"
                if os.path.exists(extracted_folder):
                    os.rename(extracted_folder, vosk_dir)
                os.remove(vosk_zip)  # Clean up zip file
                print("✓ Vosk model installed")
            else:
                return False
        else:
            print("⚠️ Vosk model download failed - you can download it manually later")
    else:
        print("✓ Vosk model already exists")
    
    # Test installation
    print("\n🧪 Testing installation...")
    if run_command("python test_system.py", "Running system test"):
        print("\n🎉 Installation completed successfully!")
        print("\nTo start the system:")
        print("  python src/main.py --mode realtime")
        print("\nFor file processing:")
        print("  python src/main.py --mode file --input audio.wav")
        return True
    else:
        print("\n⚠️ Installation completed with warnings")
        print("Some components may not work properly")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
