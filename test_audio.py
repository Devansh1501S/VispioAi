#!/usr/bin/env python3
"""
Simple test script for audio service
"""

import os
from dotenv import load_dotenv
load_dotenv()

def test_audio_service():
    """Test the audio service functionality."""
    try:
        from services.audio_service import AudioService
        
        print("🔊 Testing Audio Service...")
        
        # Initialize service
        audio_service = AudioService()
        print("✅ Audio service initialized")
        
        # Test text-to-speech
        test_text = "Hello, this is a test of the audio service."
        print(f"🎵 Converting text to speech: '{test_text}'")
        
        audio_file = audio_service.text_to_speech(test_text)
        print(f"✅ Audio file created: {audio_file}")
        
        # Check if file exists
        if os.path.exists(audio_file):
            file_size = os.path.getsize(audio_file)
            print(f"✅ Audio file verified - Size: {file_size} bytes")
            
            # Get file extension
            _, ext = os.path.splitext(audio_file)
            print(f"✅ Audio format: {ext}")
            
            return True
        else:
            print("❌ Audio file was not created")
            return False
            
    except Exception as e:
        print(f"❌ Audio service test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_audio_service()
    if success:
        print("\n🎉 Audio service test passed!")
    else:
        print("\n❌ Audio service test failed!")