#!/bin/bash
# Setup script for Streamlit Cloud deployment

echo "🚀 Setting up ImageNarratorAI..."

# Update pip to latest version
python -m pip install --upgrade pip

# Install Python packages with specific flags to avoid conflicts
pip install --no-cache-dir --upgrade --force-reinstall -r requirements.txt

# Create necessary directories
mkdir -p /tmp/audio_cache
mkdir -p /tmp/image_cache

echo "✅ Setup completed successfully!"
