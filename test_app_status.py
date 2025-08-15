#!/usr/bin/env python3
"""
Test script to verify app status
"""

import os
import sys

def test_environment():
    """Test environment variables."""
    print("🔍 Testing environment...")
    
    # Check if GEMINI_API_KEY is set
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        print("   ✅ GEMINI_API_KEY is set")
        print(f"   📝 Key length: {len(api_key)} characters")
    else:
        print("   ❌ GEMINI_API_KEY is not set")
        print("   💡 Add it to Streamlit Cloud Secrets")
    
    return api_key is not None

def test_imports():
    """Test critical imports."""
    print("\n📦 Testing imports...")
    
    try:
        import streamlit as st
        print("   ✅ streamlit imported")
    except ImportError as e:
        print(f"   ❌ streamlit import failed: {e}")
        return False
    
    try:
        import requests
        print("   ✅ requests imported")
    except ImportError as e:
        print(f"   ❌ requests import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("   ✅ PIL imported")
    except ImportError as e:
        print(f"   ❌ PIL import failed: {e}")
        return False
    
    return True

def test_services():
    """Test service imports."""
    print("\n🔧 Testing services...")
    
    try:
        from services import ServiceFactory, GEMINI_AVAILABLE, AUDIO_AVAILABLE, CHATBOT_AVAILABLE
        print("   ✅ ServiceFactory imported")
        print(f"   📊 GEMINI_AVAILABLE: {GEMINI_AVAILABLE}")
        print(f"   📊 AUDIO_AVAILABLE: {AUDIO_AVAILABLE}")
        print(f"   📊 CHATBOT_AVAILABLE: {CHATBOT_AVAILABLE}")
        
        # Test service creation
        try:
            gemini_service = ServiceFactory.get_gemini_service()
            print("   ✅ Gemini service created")
        except Exception as e:
            print(f"   ⚠️ Gemini service creation failed: {e}")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ ServiceFactory import failed: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 APP STATUS CHECK")
    print("=" * 40)
    
    all_tests_passed = True
    
    # Test environment
    if not test_environment():
        all_tests_passed = False
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test services
    if not test_services():
        all_tests_passed = False
    
    print("\n" + "=" * 40)
    if all_tests_passed:
        print("🎉 APP IS READY!")
        print("✅ All tests passed")
        print("🚀 Your app should work correctly")
    else:
        print("⚠️ Some issues detected")
        print("🔧 Please check the errors above")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
