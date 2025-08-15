#!/usr/bin/env python3
"""
Test script to verify all imports work correctly.
Run this before deploying to Streamlit Cloud.
"""

import sys
import os

def test_imports():
    """Test all required imports."""
    
    print("🧪 Testing imports...")
    
    # Test core imports
    try:
        import streamlit
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        import google.generativeai
        print("✅ google.generativeai imported successfully")
    except ImportError as e:
        print(f"❌ google.generativeai import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    try:
        import gtts
        print("✅ gtts imported successfully")
    except ImportError as e:
        print(f"❌ gtts import failed: {e}")
        return False
    
    try:
        import pygame
        print("✅ pygame imported successfully")
    except ImportError as e:
        print(f"❌ pygame import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow imported successfully")
    except ImportError as e:
        print(f"❌ Pillow import failed: {e}")
        return False
    
    # Test service imports
    try:
        from services.gemini_service import GeminiService
        print("✅ GeminiService imported successfully")
    except ImportError as e:
        print(f"❌ GeminiService import failed: {e}")
        return False
    
    try:
        from services.audio_service import AudioService
        print("✅ AudioService imported successfully")
    except ImportError as e:
        print(f"❌ AudioService import failed: {e}")
        return False
    
    try:
        from services.chatbot_service import ChatbotService
        print("✅ ChatbotService imported successfully")
    except ImportError as e:
        print(f"❌ ChatbotService import failed: {e}")
        return False
    
    # Test utility imports
    try:
        from utils.image_utils import resize_image, optimize_image_for_api
        print("✅ image_utils imported successfully")
    except ImportError as e:
        print(f"❌ image_utils import failed: {e}")
        return False
    
    print("🎉 All imports successful!")
    return True

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("✅ Ready for deployment!")
        sys.exit(0)
    else:
        print("❌ Import test failed!")
        sys.exit(1) 