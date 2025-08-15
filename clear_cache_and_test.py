#!/usr/bin/env python3
"""
Clear Streamlit cache and test app functionality
"""

import os
import shutil
from pathlib import Path

def clear_streamlit_cache():
    """Clear Streamlit cache directories."""
    print("🧹 Clearing Streamlit Cache...")
    
    # Common Streamlit cache locations
    cache_dirs = [
        Path.home() / ".streamlit",
        Path(".streamlit"),
        Path("__pycache__"),
        Path("services/__pycache__"),
        Path("utils/__pycache__")
    ]
    
    for cache_dir in cache_dirs:
        if cache_dir.exists():
            try:
                if cache_dir.name == "__pycache__":
                    shutil.rmtree(cache_dir)
                    print(f"✅ Cleared {cache_dir}")
                elif cache_dir.name == ".streamlit" and (cache_dir / "cache").exists():
                    shutil.rmtree(cache_dir / "cache")
                    print(f"✅ Cleared {cache_dir}/cache")
            except Exception as e:
                print(f"⚠️ Could not clear {cache_dir}: {e}")

def test_app_imports():
    """Test app imports and service initialization."""
    print("\n🧪 Testing App Imports...")
    
    try:
        # Test direct service imports
        from services import ServiceFactory
        print("✅ ServiceFactory import successful")
        
        # Test service creation
        gemini = ServiceFactory.get_gemini_service()
        chatbot = ServiceFactory.get_chatbot_service()
        audio = ServiceFactory.get_audio_service()
        print("✅ All services created successfully")
        
        # Test method availability
        if hasattr(gemini, 'identify_location'):
            print("✅ GeminiService.identify_location available")
        else:
            print("❌ GeminiService.identify_location NOT available")
            return False
        
        if hasattr(chatbot, 'analyze_location_context'):
            print("✅ ChatbotService.analyze_location_context available")
        else:
            print("❌ ChatbotService.analyze_location_context NOT available")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ App import test failed: {e}")
        return False

def main():
    """Main function."""
    print("🔧 Cache Clear and App Test Utility")
    print("=" * 50)
    
    # Clear cache
    clear_streamlit_cache()
    
    # Test imports
    if test_app_imports():
        print("\n🎉 All tests passed! App should work correctly.")
        print("\n🚀 To run the app:")
        print("   streamlit run app.py")
        print("\n💡 If you still see errors:")
        print("   1. Restart your terminal/IDE")
        print("   2. Clear browser cache")
        print("   3. Use incognito/private browsing mode")
    else:
        print("\n❌ Tests failed! Check the errors above.")

if __name__ == "__main__":
    main()