#!/usr/bin/env python3
"""
Simple test to verify google-generativeai import works.
"""

def test_import():
    try:
        import google.generativeai as genai
        print("✅ google.generativeai imported successfully!")
        print(f"Version: {genai.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

if __name__ == "__main__":
    test_import() 