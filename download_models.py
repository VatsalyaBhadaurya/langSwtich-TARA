"""
Model downloader for Language Switch TARA
"""
import os
import urllib.request
import zipfile
import shutil
from pathlib import Path

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

def download_vosk_model():
    """Download Vosk model"""
    print("🎯 Downloading Vosk Speech Recognition Model")
    print("=" * 50)
    
    # Create models directory
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Vosk model URLs (small English model)
    vosk_url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
    vosk_zip = "vosk-model.zip"
    vosk_dir = "models/vosk"
    
    if os.path.exists(vosk_dir):
        print("✓ Vosk model already exists")
        return True
    
    # Download model
    if download_file(vosk_url, vosk_zip, "Downloading Vosk model"):
        if extract_zip(vosk_zip, "models", "Extracting Vosk model"):
            # Rename extracted folder to 'vosk'
            extracted_folder = "models/vosk-model-small-en-us-0.15"
            if os.path.exists(extracted_folder):
                if os.path.exists(vosk_dir):
                    shutil.rmtree(vosk_dir)
                os.rename(extracted_folder, vosk_dir)
                print("✓ Vosk model installed successfully")
            
            # Clean up zip file
            if os.path.exists(vosk_zip):
                os.remove(vosk_zip)
            
            return True
    
    return False

def main():
    """Main downloader"""
    print("🚀 Language Switch TARA - Model Downloader")
    print("=" * 50)
    
    success = download_vosk_model()
    
    if success:
        print("\n🎉 Models downloaded successfully!")
        print("\nYou can now run:")
        print("  python src/main_simple.py --mode realtime")
    else:
        print("\n⚠️ Model download failed")
        print("You can still use text mode:")
        print("  python src/main_simple.py --mode text")

if __name__ == "__main__":
    main()
