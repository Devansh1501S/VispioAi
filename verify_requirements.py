#!/usr/bin/env python3
"""
Verify all requirements are properly installed and working
"""

import sys
import importlib
from packaging import version

def check_requirements():
    """Check all required packages are installed with correct versions."""
    
    requirements = {
        'streamlit': '1.45.1',
        'google.generativeai': '0.8.5',
        'gtts': '2.5.4',
        'pydub': '0.25.1',
        'pygame': '2.6.0',
        'PIL': '10.3.0',  # Pillow
        'dotenv': '1.0.1',  # python-dotenv
        'requests': '2.31.0',
        'numpy': '1.26.4',
        'typing_extensions': '4.13.0',
        'packaging': '24.0'
    }
    
    print("🔍 Verifying Requirements...")
    print("=" * 50)
    
    all_good = True
    
    for package, min_version in requirements.items():
        try:
            # Special handling for some packages
            if package == 'PIL':
                import PIL
                pkg_version = PIL.__version__
                package_name = 'Pillow'
            elif package == 'dotenv':
                import dotenv
                try:
                    pkg_version = dotenv.__version__
                except AttributeError:
                    pkg_version = 'installed'
                package_name = 'python-dotenv'
            elif package == 'google.generativeai':
                import google.generativeai as genai
                pkg_version = genai.__version__
                package_name = 'google-generativeai'
            else:
                module = importlib.import_module(package)
                pkg_version = getattr(module, '__version__', 'unknown')
                package_name = package
            
            # Version comparison
            if pkg_version != 'unknown':
                try:
                    if version.parse(pkg_version) >= version.parse(min_version):
                        status = "✅"
                        version_info = f"{pkg_version} (>= {min_version})"
                    else:
                        status = "⚠️"
                        version_info = f"{pkg_version} (< {min_version}) - UPDATE NEEDED"
                        all_good = False
                except:
                    status = "✅"
                    version_info = f"{pkg_version} (version check skipped)"
            else:
                status = "✅"
                version_info = "installed (version unknown)"
            
            print(f"{status} {package_name:<20} {version_info}")
            
        except ImportError:
            print(f"❌ {package_name:<20} NOT INSTALLED")
            all_good = False
        except Exception as e:
            print(f"⚠️ {package_name:<20} Error: {e}")
            all_good = False
    
    print("=" * 50)
    
    if all_good:
        print("🎉 All requirements verified successfully!")
        print("📦 Your environment is ready for Vispio!")
        return True
    else:
        print("❌ Some requirements need attention.")
        print("💡 Run: pip install -r requirements.txt")
        return False

def check_optional_dependencies():
    """Check optional system dependencies."""
    print("\n🔧 Checking Optional Dependencies...")
    print("=" * 50)
    
    # Check ffmpeg
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ ffmpeg                Available (audio conversion enabled)")
        else:
            print("⚠️ ffmpeg                Not working properly")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("⚠️ ffmpeg                Not found (audio limited to MP3)")
        print("   Install: winget install ffmpeg (Windows)")
    except Exception as e:
        print(f"⚠️ ffmpeg                Error checking: {e}")

def main():
    """Main verification function."""
    print("🔍 Vispio Requirements Verification")
    print("=" * 50)
    
    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"🐍 Python Version: {python_version}")
    
    if sys.version_info >= (3, 8):
        print("✅ Python version compatible")
    else:
        print("❌ Python 3.8+ required")
        return False
    
    print()
    
    # Check requirements
    requirements_ok = check_requirements()
    
    # Check optional dependencies
    check_optional_dependencies()
    
    print("\n" + "=" * 50)
    
    if requirements_ok:
        print("🚀 Ready to run: streamlit run app.py")
        return True
    else:
        print("🔧 Fix requirements first, then try again")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)