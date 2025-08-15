#!/usr/bin/env python3
"""
Test script for the fallback Gemini service
"""

import sys
import os

def test_fallback_import():
    """Test if the fallback service can be imported."""
    print("🧪 Testing fallback service import...")
    
    try:
        from services.gemini_fallback import GeminiFallbackService
        print("✅ Fallback service imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Fallback service import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error importing fallback service: {e}")
        return False

def test_fallback_creation():
    """Test if the fallback service can be created."""
    print("\n🔧 Testing fallback service creation...")
    
    try:
        from services.gemini_fallback import GeminiFallbackService
        
        # Test with a dummy API key
        service = GeminiFallbackService("dummy_key")
        print("✅ Fallback service created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating fallback service: {e}")
        return False

def test_required_packages():
    """Test if all required packages for fallback are available."""
    print("\n📦 Testing required packages...")
    
    required_packages = [
        ("requests", "requests"),
        ("PIL", "PIL"),
        ("json", "json"),
        ("base64", "base64"),
        ("io", "io"),
    ]
    
    all_good = True
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name} available")
        except ImportError as e:
            print(f"❌ {package_name} not available: {e}")
            all_good = False
    
    return all_good

def main():
    """Main test function."""
    print("🚀 Testing Fallback Service")
    print("=" * 40)
    
    # Test package availability
    if not test_required_packages():
        print("\n❌ Required packages missing!")
        return False
    
    # Test import
    if not test_fallback_import():
        print("\n❌ Import failed!")
        return False
    
    # Test creation
    if not test_fallback_creation():
        print("\n❌ Service creation failed!")
        return False
    
    print("\n🎉 All fallback service tests passed!")
    print("✅ The fallback service should work correctly")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
