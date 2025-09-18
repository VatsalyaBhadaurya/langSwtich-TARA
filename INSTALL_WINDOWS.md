# Windows Installation Guide

## Option 1: Lightweight Installation (Recommended)

This version works without heavy dependencies and is perfect for testing:

```bash
# Install lightweight dependencies
pip install -r requirements-light.txt

# Run the simple version
python src/main_simple.py --mode text
```

## Option 2: Full Installation (Advanced)

### Step 1: Install Microsoft Visual C++ Build Tools

1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install "C++ build tools" workload
3. Restart your computer

### Step 2: Install Dependencies

```bash
# Install core dependencies first
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install other dependencies
pip install -r requirements.txt
```

### Step 3: Download Models

```bash
# Create models directory
mkdir models

# Download Vosk model (small English model ~50MB)
# Option 1: Using PowerShell
Invoke-WebRequest -Uri "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip" -OutFile "vosk-model.zip"
Expand-Archive -Path "vosk-model.zip" -DestinationPath "models"
Rename-Item "models/vosk-model-small-en-us-0.15" "models/vosk"
Remove-Item "vosk-model.zip"

# Option 2: Manual download
# 1. Go to https://alphacephei.com/vosk/models
# 2. Download "vosk-model-small-en-us-0.15.zip"
# 3. Extract to models/vosk/
```

### Step 4: Test Installation

```bash
# Test simple version
python src/main_simple.py --mode text

# Test full version (if all dependencies installed)
python src/main.py --mode realtime
```

## Troubleshooting

### TTS Installation Issues
If TTS fails to install:
```bash
# Use lightweight TTS instead
pip install pyttsx3
```

### SpeechBrain Issues
If SpeechBrain fails:
```bash
# Use simple language detection
# The simple version will work without SpeechBrain
```

### Audio Issues
If microphone doesn't work:
1. Check Windows microphone permissions
2. Try running as administrator
3. Check if other applications are using the microphone

## Quick Start

1. **Install lightweight version:**
   ```bash
   pip install -r requirements-light.txt
   python src/main_simple.py --mode text
   ```

2. **Test with text input:**
   - Type text in different languages
   - Use `set <lang>` to change language
   - Type `quit` to exit

3. **Test with audio file:**
   ```bash
   python src/main_simple.py --mode file --input audio.wav --output response.wav
   ```
