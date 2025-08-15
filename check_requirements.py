#!/usr/bin/env python3
"""
Requirements checker and installer for Streamlit Cloud deployment.
"""

import subprocess
import sys
import importlib

def check_and_install_package(package_name, install_name=None):
    """Check if a package is installed, install if missing."""
    if install_name is None:
        install_name = package_name
    
    try:
        importlib.import_module(package_name)
        print(f"✅ {package_name} is already installed")
        return True
    except ImportError:
        print(f"❌ {package_name} is missing, installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", install_name])
            print(f"✅ {package_name} installed successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to install {package_name}: {e}")
            return False

def main():
    """Check and install all required packages."""
    print("🔍 Checking required packages...")
    
    required_packages = [
        ("streamlit", "streamlit==1.45.1"),
        ("google.generativeai", "google-generativeai==0.8.5"),
        ("dotenv", "python-dotenv==1.0.1"),
        ("gtts", "gtts==2.5.4"),
        ("pygame", "pygame==2.6.0"),
        ("PIL", "Pillow==10.3.0"),
        ("numpy", "numpy==1.26.4"),
        ("requests", "requests==2.31.0"),
    ]
    
    all_installed = True
    for package, install_name in required_packages:
        if not check_and_install_package(package, install_name):
            all_installed = False
    
    if all_installed:
        print("🎉 All packages are installed and ready!")
        return True
    else:
        print("❌ Some packages failed to install")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 