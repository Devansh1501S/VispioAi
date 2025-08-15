#!/usr/bin/env python3
"""
Simple deployment test for Streamlit Cloud
Run this to verify all dependencies work correctly
"""

import sys
import os

def test_imports():
    """Test all required imports."""
    print("🧪 Testing imports for Streamlit Cloud deployment...")
    
    # Test basic imports
    try:
        import streamlit as st
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        import google.generativeai as genai
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
        from PIL import Image
        print("✅ Pillow imported successfully")
    except ImportError as e:
        print(f"❌ Pillow import failed: {e}")
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
        import numpy as np
        print("✅ numpy imported successfully")
    except ImportError as e:
        print(f"❌ numpy import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        return False
    
    return True

def test_services():
    """Test service imports."""
    print("\n🔧 Testing service imports...")
    
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
    
    return True

def main():
    """Main test function."""
    print("🚀 Streamlit Cloud Deployment Test")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Working directory: {os.getcwd()}")
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        return False
    
    # Test services
    if not test_services():
        print("\n❌ Service tests failed!")
        return False
    
    print("\n🎉 All tests passed!")
    print("✅ Your app should deploy successfully on Streamlit Cloud")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
