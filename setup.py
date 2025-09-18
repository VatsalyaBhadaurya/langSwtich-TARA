"""
Setup script for Language Switch TARA
"""
from setuptools import setup, find_packages

setup(
    name="langswitch-tara",
    version="1.0.0",
    description="Real-time language switching system using open-source tools",
    packages=find_packages(),
    install_requires=[
        "speechbrain>=0.5.16",
        "vosk>=0.3.45",
        "TTS>=0.22.0",
        "torch>=1.13.0",
        "torchaudio>=0.13.0",
        "numpy>=1.21.0",
        "soundfile>=0.12.1",
        "pyaudio>=0.2.11",
        "pyyaml>=6.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "langswitch=src.main:main",
        ],
    },
)
