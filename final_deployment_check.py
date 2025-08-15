#!/usr/bin/env python3
"""
Final deployment check for Streamlit Cloud
"""

import sys
import os

def check_critical_files():
    """Check that all critical files exist."""
    print("📁 Checking critical files...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'packages.txt',
        'runtime.txt',
        'services/__init__.py',
        'services/gemini_fallback.py',
        'services/audio_fallback.py',
        'services/chatbot_fallback.py',
        'utils/image_utils.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"   ✅ {file_path}")
    
    if missing_files:
        print(f"   ❌ Missing files: {missing_files}")
        return False
    
    return True

def check_requirements():
    """Check requirements.txt content."""
    print("\n📦 Checking requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        required_packages = [
            'streamlit',
            'google-generativeai',
            'python-dotenv',
            'Pillow',
            'gtts',
            'requests'
        ]
        
        missing_packages = []
        for package in required_packages:
            if package not in content:
                missing_packages.append(package)
            else:
                print(f"   ✅ {package}")
        
        if missing_packages:
            print(f"   ❌ Missing packages: {missing_packages}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error reading requirements.txt: {e}")
        return False

def check_packages():
    """Check packages.txt content."""
    print("\n🔧 Checking packages.txt...")
    
    try:
        with open('packages.txt', 'r') as f:
            content = f.read()
        
        required_packages = [
            'python3-dev',
            'build-essential',
            'ffmpeg'
        ]
        
        missing_packages = []
        for package in required_packages:
            if package not in content:
                missing_packages.append(package)
            else:
                print(f"   ✅ {package}")
        
        if missing_packages:
            print(f"   ❌ Missing packages: {missing_packages}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error reading packages.txt: {e}")
        return False

def check_runtime():
    """Check runtime.txt content."""
    print("\n🐍 Checking runtime.txt...")
    
    try:
        with open('runtime.txt', 'r') as f:
            content = f.read().strip()
        
        if 'python-3.12' in content:
            print("   ✅ Python 3.12 specified")
            return True
        else:
            print(f"   ⚠️ Unexpected runtime: {content}")
            return True  # Not critical
        
    except Exception as e:
        print(f"   ❌ Error reading runtime.txt: {e}")
        return False

def check_app_structure():
    """Check app.py has required imports."""
    print("\n🔍 Checking app.py structure...")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_elements = [
            'import streamlit',
            'ServiceFactory',
            'GEMINI_API_KEY',
            'st.set_page_config'
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in content:
                missing_elements.append(element)
            else:
                print(f"   ✅ {element}")
        
        if missing_elements:
            print(f"   ❌ Missing elements: {missing_elements}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error reading app.py: {e}")
        return False

def main():
    """Main deployment check."""
    print("🚀 FINAL DEPLOYMENT CHECK")
    print("=" * 50)
    
    all_checks_passed = True
    
    # Check critical files
    if not check_critical_files():
        all_checks_passed = False
    
    # Check requirements
    if not check_requirements():
        all_checks_passed = False
    
    # Check packages
    if not check_packages():
        all_checks_passed = False
    
    # Check runtime
    if not check_runtime():
        all_checks_passed = False
    
    # Check app structure
    if not check_app_structure():
        all_checks_passed = False
    
    print("\n" + "=" * 50)
    if all_checks_passed:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Your app is ready for Streamlit Cloud deployment!")
        print("\n📋 Deployment Steps:")
        print("1. Push code to GitHub")
        print("2. Connect repository to Streamlit Cloud")
        print("3. Add GEMINI_API_KEY to Streamlit Cloud Secrets")
        print("4. Deploy!")
        print("\n🔑 Secrets format:")
        print("GEMINI_API_KEY = 'your_actual_api_key_here'")
    else:
        print("❌ Some checks failed!")
        print("Please fix the issues before deploying.")
    
    return all_checks_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
