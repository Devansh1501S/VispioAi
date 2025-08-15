#!/usr/bin/env python3
"""
Check Python version compatibility for the application.
"""

import sys
import platform

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    print(f"Platform: {platform.platform()}")
    
    # Check if Python 3.12 is compatible
    if version.major == 3 and version.minor >= 12:
        print("✅ Python 3.12+ is compatible")
        return True
    elif version.major == 3 and version.minor >= 8:
        print("✅ Python 3.8+ is compatible")
        return True
    else:
        print("❌ Python version too old. Need Python 3.8+")
        return False

def check_packages():
    """Check if required packages can be imported."""
    packages = [
        "streamlit",
        "google.generativeai",
        "PIL",
        "numpy",
        "requests"
    ]
    
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} imported successfully")
        except ImportError as e:
            print(f"❌ {package} import failed: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("🔍 Checking Python compatibility...")
    version_ok = check_python_version()
    
    if version_ok:
        print("\n🔍 Checking package compatibility...")
        packages_ok = check_packages()
        
        if packages_ok:
            print("\n🎉 All compatibility checks passed!")
            sys.exit(0)
        else:
            print("\n❌ Package compatibility issues found")
            sys.exit(1)
    else:
        print("\n❌ Python version compatibility issues found")
        sys.exit(1) 