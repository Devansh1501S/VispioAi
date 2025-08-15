#!/usr/bin/env python3
"""
Complete test script for all services
"""

import sys
import os

def test_imports():
    """Test all imports."""
    print("🧪 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ PIL imported successfully")
    except ImportError as e:
        print(f"❌ PIL import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        return False
    
    try:
        from gtts import gTTS
        print("✅ gtts imported successfully")
    except ImportError as e:
        print(f"❌ gtts import failed: {e}")
        return False
    
    return True

def test_services():
    """Test service imports."""
    print("\n🔧 Testing services...")
    
    try:
        from services import ServiceFactory, GEMINI_AVAILABLE, AUDIO_AVAILABLE, CHATBOT_AVAILABLE
        print("✅ ServiceFactory imported successfully")
        print(f"   - GEMINI_AVAILABLE: {GEMINI_AVAILABLE}")
        print(f"   - AUDIO_AVAILABLE: {AUDIO_AVAILABLE}")
        print(f"   - CHATBOT_AVAILABLE: {CHATBOT_AVAILABLE}")
    except ImportError as e:
        print(f"❌ ServiceFactory import failed: {e}")
        return False
    
    return True

def test_gemini_service():
    """Test Gemini service creation."""
    print("\n🤖 Testing Gemini service...")
    
    try:
        from services import ServiceFactory
        
        # Test with dummy API key
        os.environ["GEMINI_API_KEY"] = "dummy_key_for_testing"
        
        gemini_service = ServiceFactory.get_gemini_service()
        print("✅ Gemini service created successfully")
        
        # Check if it has required methods
        required_methods = [
            'generate_caption', 'identify_location', 'identify_product',
            'comprehensive_analysis', 'extract_text_and_details'
        ]
        
        for method in required_methods:
            if hasattr(gemini_service, method):
                print(f"   ✅ Method {method} available")
            else:
                print(f"   ❌ Method {method} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Gemini service test failed: {e}")
        return False

def test_audio_service():
    """Test audio service creation."""
    print("\n🔊 Testing audio service...")
    
    try:
        from services import ServiceFactory, AUDIO_AVAILABLE
        
        if not AUDIO_AVAILABLE:
            print("⚠️ Audio service not available")
            return True  # Not critical for core functionality
        
        audio_service = ServiceFactory.get_audio_service()
        print("✅ Audio service created successfully")
        
        # Check if it has required methods
        if hasattr(audio_service, 'text_to_speech'):
            print("   ✅ Method text_to_speech available")
        else:
            print("   ❌ Method text_to_speech missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Audio service test failed: {e}")
        return False

def test_chatbot_service():
    """Test chatbot service creation."""
    print("\n💬 Testing chatbot service...")
    
    try:
        from services import ServiceFactory, CHATBOT_AVAILABLE
        
        if not CHATBOT_AVAILABLE:
            print("⚠️ Chatbot service not available")
            return True  # Not critical for core functionality
        
        chatbot_service = ServiceFactory.get_chatbot_service()
        print("✅ Chatbot service created successfully")
        
        # Check if it has required methods
        required_methods = [
            'chat_with_image', 'analyze_location_context', 
            'analyze_product_context', 'get_suggested_questions'
        ]
        
        for method in required_methods:
            if hasattr(chatbot_service, method):
                print(f"   ✅ Method {method} available")
            else:
                print(f"   ❌ Method {method} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Chatbot service test failed: {e}")
        return False

def test_utils():
    """Test utility functions."""
    print("\n🛠️ Testing utilities...")
    
    try:
        from utils.image_utils import resize_image, optimize_image_for_api
        print("✅ Image utilities imported successfully")
        
        # Test with a dummy image
        from PIL import Image
        import io
        
        # Create a simple test image
        test_image = Image.new('RGB', (100, 100), color='red')
        
        # Test resize function
        resized = resize_image(test_image, max_size=(50, 50))
        print("   ✅ resize_image function works")
        
        # Test optimize function
        optimized = optimize_image_for_api(test_image, max_file_size_mb=1.0)
        print("   ✅ optimize_image_for_api function works")
        
        return True
        
    except Exception as e:
        print(f"❌ Utilities test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Complete Service Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test services
    if not test_services():
        all_tests_passed = False
    
    # Test individual services
    if not test_gemini_service():
        all_tests_passed = False
    
    if not test_audio_service():
        all_tests_passed = False
    
    if not test_chatbot_service():
        all_tests_passed = False
    
    # Test utilities
    if not test_utils():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Your app is ready for deployment!")
        print("\n📋 Next steps:")
        print("1. Add your GEMINI_API_KEY to Streamlit Cloud Secrets")
        print("2. Deploy to Streamlit Cloud")
        print("3. Test the deployed app")
    else:
        print("❌ Some tests failed!")
        print("Please fix the issues before deploying.")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
