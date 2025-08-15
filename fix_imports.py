#!/usr/bin/env python3
"""
Import fix for Streamlit Cloud deployment issues
"""

import sys
import subprocess
import importlib

def install_package(package):
    """Install a package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_fix_imports():
    """Check and fix import issues for Streamlit Cloud."""
    
    print("🔧 Checking and fixing imports for Streamlit Cloud...")
    
    # Critical packages that must be available
    critical_packages = [
        ("google.generativeai", "google-generativeai==0.8.5"),
        ("streamlit", "streamlit==1.45.1"),
        ("gtts", "gtts==2.5.4"),
        ("PIL", "Pillow==10.3.0"),
        ("dotenv", "python-dotenv==1.0.1"),
    ]
    
    missing_packages = []
    
    for module_name, package_name in critical_packages:
        try:
            importlib.import_module(module_name)
            print(f"✅ {module_name} - OK")
        except ImportError:
            print(f"❌ {module_name} - MISSING")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {missing_packages}")
        for package in missing_packages:
            try:
                install_package(package)
                print(f"✅ Installed {package}")
            except Exception as e:
                print(f"❌ Failed to install {package}: {e}")
        
        # Verify installation
        print("\n🔍 Verifying installation...")
        for module_name, _ in critical_packages:
            try:
                importlib.import_module(module_name)
                print(f"✅ {module_name} - NOW OK")
            except ImportError:
                print(f"❌ {module_name} - STILL MISSING")
    
    print("\n🎉 Import check complete!")

if __name__ == "__main__":
    check_and_fix_imports()