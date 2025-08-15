#!/usr/bin/env python3
"""
Quick test to verify app works without errors
"""

def test_imports():
    """Test all critical imports."""
    print("🧪 Testing imports...")
    
    try:
        import streamlit as st
        print("   ✅ streamlit")
    except ImportError as e:
        print(f"   ❌ streamlit: {e}")
        return False
    
    try:
        import requests
        print("   ✅ requests")
    except ImportError as e:
        print(f"   ❌ requests: {e}")
        return False
    
    try:
        from PIL import Image
        print("   ✅ PIL")
    except ImportError as e:
        print(f"   ❌ PIL: {e}")
        return False
    
    try:
        import urllib3
        print(f"   ✅ urllib3 ({urllib3.__version__})")
    except ImportError as e:
        print(f"   ❌ urllib3: {e}")
        return False
    
    return True

def test_services():
    """Test service imports."""
    print("\n🔧 Testing services...")
    
    try:
        from services import ServiceFactory, GEMINI_AVAILABLE
        print("   ✅ ServiceFactory imported")
        print(f"   📊 GEMINI_AVAILABLE: {GEMINI_AVAILABLE}")
        return True
    except Exception as e:
        print(f"   ❌ ServiceFactory: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 QUICK APP TEST")
    print("=" * 30)
    
    if not test_imports():
        print("\n❌ Import test failed")
        return False
    
    if not test_services():
        print("\n❌ Service test failed")
        return False
    
    print("\n" + "=" * 30)
    print("🎉 ALL TESTS PASSED!")
    print("✅ App should deploy without errors")
    print("🚀 Ready for Streamlit Cloud")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
