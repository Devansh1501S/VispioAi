#!/usr/bin/env python3
"""
Health check script for Vispio deployment
Run this to verify all dependencies and services are working
"""

import sys
import os
from dotenv import load_dotenv

def check_dependencies():
    """Check if all required packages are installed."""
    required_packages = [
        'streamlit',
        'google.generativeai',
        'gtts',
        'pydub',
        'pygame',
        'PIL',
        'dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            elif package == 'google.genai':
                import google.generativeai as genai
            else:
                __import__(package)
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def check_environment_variables():
    """Check if required environment variables are set."""
    load_dotenv()
    
    required_vars = ['GEMINI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var} - SET")
        else:
            print(f"❌ {var} - MISSING")
            missing_vars.append(var)
    
    return len(missing_vars) == 0

def check_services():
    """Check if services can be initialized."""
    try:
        from services.gemini_service import GeminiService
        from services.audio_service import AudioService
        from services.chatbot_service import ChatbotService
        
        # Test service initialization
        try:
            gemini_service = GeminiService()
            print("✅ Gemini Service - OK")
        except Exception as e:
            print(f"❌ Gemini Service - ERROR: {e}")
            return False
        
        try:
            audio_service = AudioService()
            print("✅ Audio Service - OK")
        except Exception as e:
            print(f"❌ Audio Service - ERROR: {e}")
            return False
        
        try:
            chatbot_service = ChatbotService()
            print("✅ Chatbot Service - OK")
        except Exception as e:
            print(f"❌ Chatbot Service - ERROR: {e}")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Service Import Error: {e}")
        return False

def main():
    """Run all health checks."""
    print("🔍 Vispio Health Check")
    print("=" * 50)
    
    print("\n📦 Checking Dependencies...")
    deps_ok = check_dependencies()
    
    print("\n🔑 Checking Environment Variables...")
    env_ok = check_environment_variables()
    
    print("\n⚙️ Checking Services...")
    services_ok = check_services()
    
    print("\n" + "=" * 50)
    
    if deps_ok and env_ok and services_ok:
        print("🎉 All checks passed! Vispio is ready to deploy.")
        sys.exit(0)
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()