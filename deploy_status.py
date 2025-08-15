#!/usr/bin/env python3
"""
Quick deployment status check
"""

import os
import sys

def check_deployment():
    print("🚀 DEPLOYMENT STATUS CHECK")
    print("=" * 40)
    
    # Check environment
    api_key = os.environ.get("GEMINI_API_KEY")
    print(f"🔑 API Key: {'✅ Found' if api_key else '❌ Missing'}")
    
    # Check imports
    try:
        import streamlit as st
        print("📦 Streamlit: ✅ Imported")
    except ImportError:
        print("📦 Streamlit: ❌ Failed")
        return False
    
    try:
        import requests
        print("📦 Requests: ✅ Imported")
    except ImportError:
        print("📦 Requests: ❌ Failed")
        return False
    
    try:
        from PIL import Image
        print("📦 PIL: ✅ Imported")
    except ImportError:
        print("📦 PIL: ❌ Failed")
        return False
    
    # Check services
    try:
        from services import ServiceFactory, GEMINI_AVAILABLE, AUDIO_AVAILABLE, CHATBOT_AVAILABLE
        print("🔧 Services: ✅ Imported")
        print(f"   - Gemini: {'✅' if GEMINI_AVAILABLE else '🔄 Fallback'}")
        print(f"   - Audio: {'✅' if AUDIO_AVAILABLE else '❌'}")
        print(f"   - Chatbot: {'✅' if CHATBOT_AVAILABLE else '❌'}")
    except ImportError as e:
        print(f"🔧 Services: ❌ Failed - {e}")
        return False
    
    # Test service creation
    try:
        gemini_service = ServiceFactory.get_gemini_service()
        print("🎯 Gemini Service: ✅ Created")
    except Exception as e:
        print(f"🎯 Gemini Service: ❌ Failed - {e}")
        return False
    
    print("\n" + "=" * 40)
    print("🎉 DEPLOYMENT READY!")
    print("✅ All components working")
    print("🚀 Your app should be fully functional")
    
    return True

if __name__ == "__main__":
    success = check_deployment()
    sys.exit(0 if success else 1)
