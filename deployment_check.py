#!/usr/bin/env python3
"""
Deployment check script for Streamlit Cloud
This script verifies that all required dependencies are properly installed
"""

import sys
import subprocess
import importlib

def check_package(package_name, import_name=None):
    """Check if a package is installed and can be imported."""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name} is installed and importable")
        return True
    except ImportError as e:
        print(f"❌ {package_name} is not properly installed: {e}")
        return False

def install_package(package_name):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ Successfully installed {package_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package_name}: {e}")
        return False

def main():
    print("🔍 Checking Streamlit Cloud deployment dependencies...")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    # List of required packages
    required_packages = [
        ("streamlit", "streamlit"),
        ("google-generativeai", "google.generativeai"),
        ("python-dotenv", "dotenv"),
        ("Pillow", "PIL"),
        ("gtts", "gtts"),
        ("pygame", "pygame"),
        ("numpy", "numpy"),
        ("requests", "requests"),
    ]
    
    all_good = True
    
    for package_name, import_name in required_packages:
        if not check_package(package_name, import_name):
            print(f"🔄 Attempting to install {package_name}...")
            if install_package(package_name):
                # Try checking again after installation
                if not check_package(package_name, import_name):
                    all_good = False
            else:
                all_good = False
    
    if all_good:
        print("\n🎉 All dependencies are properly installed!")
        print("✅ Your Streamlit app should work correctly now.")
    else:
        print("\n⚠️  Some dependencies failed to install.")
        print("Please check the Streamlit Cloud logs for more details.")
    
    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)